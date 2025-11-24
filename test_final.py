#####################
#
# pytest -sv test_final.py --log-cli-level=INFO -n 4
#
#####################

import pytest
import logging
import json
import random
import pytest_asyncio

from demoqa import (
    LoginPage,
    BooksPage,
    RegisterPage,
    init_browser,
    close_browser,
)

logging.basicConfig(level=logging.INFO, format="%(funcName)s: %(message)s", force=True)
logger = logging.getLogger(__name__)


class TestDemoQA:

    @pytest_asyncio.fixture(scope="class", autouse=True)
    async def _setup(self):

        ## Cannot do reCAPTCHA automation in setup

        # await init_browser(browser_type="chrome")
        # async with RegisterPage() as rp:
        #     user = {
        #         "userName": "testuser666",
        #         "password": "Exploit99*",
        #         "firstName": "Test",
        #         "lastName": "User"
        #     }
        #     self.exist_user = await rp.reg_new_user(user)
        #     logger.info(f"Registered user: {self.exist_user}")
        # await close_browser()
        logger.info("Setting up TestDemoQA class")
        yield
        
    new_user = {
        "userName": f"testuser{random.randint(6000, 6999)}",
        "password": "Exploit99*"
    }

    exist_user = {
        "userName": "testuser666",
        "password": "Exploit99*"
    }

    api_endpoint = "/Account/v1/User"

    # Test 1
    @pytest.mark.asyncio
    @pytest.mark.skip_browser("firefox")
    @pytest.mark.skip_browser("msedge")
    async def test_login_success(self):
        async with LoginPage() as lp:
            await lp.login(lp.username, lp.password)
            await lp.expect_text_visible(lp.username)

    # Test 2
    @pytest.mark.asyncio
    @pytest.mark.skip_browser("firefox")
    @pytest.mark.skip_browser("msedge")
    async def test_sort_ascending_verify(self):
        async with BooksPage() as bp:
            await bp.sort_by_title("ascending")
            assert await bp.verify_sort("Title", "ascending"), "Sort ascending verification failed"

    @pytest.mark.asyncio
    @pytest.mark.skip_browser("firefox")
    @pytest.mark.skip_browser("msedge")
    async def test_sort_descending_verify(self):
        async with BooksPage() as bp:
            await bp.sort_by_title("descending")
            assert await bp.verify_sort("Title", "descending"), "Sort descending verification failed"

    # Test 3
    @pytest.mark.asyncio
    @pytest.mark.skip_browser("firefox")
    @pytest.mark.skip_browser("msedge")
    async def test_set_rows_per_page(self):
        async with BooksPage() as bp:
            await bp.set_row_per_page(5)
            assert await bp.verify_num_pages(2), "Number of rows per page verification failed"
            assert await bp.verify_num_rows(5), "Number of rows verification failed"

    @pytest.mark.asyncio
    @pytest.mark.skip_browser("firefox")
    @pytest.mark.skip_browser("msedge")
    async def test_page_jump(self):
        async with BooksPage() as bp:
            await bp.set_row_per_page(5)
            await bp.click_next_page_button()
            await bp.verify_current_page(2)

    # Test 4
    @pytest.mark.asyncio
    @pytest.mark.skip_browser("firefox")
    @pytest.mark.skip_browser("msedge")
    async def test_book_search(self):
        book = "Speaking JavaScript"
        async with BooksPage() as bp:
            await bp.text_box_interact(name="Type to search", action="fill", value=book)
            await bp.verify_filter_by_title(book)

    # Test 5
    @pytest.mark.asyncio
    @pytest.mark.skip_browser("firefox")
    @pytest.mark.skip_browser("msedge")
    async def test_create_user_api(self, api_request_context_final):
        res = await api_request_context_final.post(
            self.api_endpoint, data=self.new_user
        )
        logger.info("RESPONSE STATUS: %s", res.status)
        assert res.status == 201, f"Unexpected status: {res.status}"
        try:
            body = await res.json()
        except Exception:
            body = await res.text()
        logger.info("RESPONSE BODY: %s", body)
        if isinstance(body, dict):
            assert body['userID'] is not None
            assert body['username'] == self.new_user['userName']
            assert body['books'] is not None
        else:
            raise AssertionError("Expect json response")

    @pytest.mark.asyncio
    @pytest.mark.skip_browser("firefox")
    @pytest.mark.skip_browser("msedge")
    async def test_create_exist_user_api(self, api_request_context_final):
        res = await api_request_context_final.post(
            self.api_endpoint, data=self.exist_user
        )

        logger.info("RESPONSE STATUS: %s", res.status)
        logger.info("RESPONSE BODY: %s", await res.text())
        assert res.status == 406, f"Unexpected status: {res.status}"
        try:
            body = await res.json()
        except Exception:
            body = await res.text()
        logger.info("RESPONSE BODY: %s", body)
        if isinstance(body, dict):
            assert body['code'] == "1204"
            assert body['message'] == "User exists!"
        else:
            raise AssertionError("Expect json response")