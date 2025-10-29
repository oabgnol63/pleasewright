import pytest
import logging

logging.basicConfig(level=logging.INFO, format="%(funcName)s: %(message)s", force=True)
logger = logging.getLogger(__name__)

from playwright.async_api import APIRequestContext

class TestAPIRequests:
    @pytest.mark.asyncio
    async def test_get(self, api_request_context: APIRequestContext) -> None:
        res = await api_request_context.get(
            f"/api/users/2", data={}
        )
        logger.info("RESPONSE STATUS: %s", res.status)
        assert res.status == 200, f"Unexpected status: {res.status}"
        try:
            body = await res.json()
        except Exception:
            body = await res.text()
        logger.info("RESPONSE BODY: %s", body)
        if isinstance(body, dict):
            first_name = body['data']['first_name']
            assert first_name == "Janet"
        else:
            raise AssertionError("Expect json response")

    @pytest.mark.asyncio
    async def test_post(self, api_request_context: APIRequestContext) -> None:
        res = await api_request_context.post(
            f"/api/users", data={"name": "Raghav", "job": "Teacher"}
        )
        logger.info("RESPONSE STATUS: %s", res.status)
        assert res.status == 201, f"Unexpected status: {res.status}"
        try:
            body = await res.json()
        except Exception:
            body = await res.text()
        logger.info("RESPONSE BODY: %s", body)
        if isinstance(body, dict):
            assert body['name'] == "Raghav"
            assert body['job'] == "Teacher"
        else:
            raise AssertionError("Expect json response")
        
    @pytest.mark.asyncio
    async def test_put(self, api_request_context: APIRequestContext) -> None:
        res = await api_request_context.put(
            f"/api/users/2", data={"name": "Raghav", "job": "Instructor"}
        )
        logger.info("RESPONSE STATUS: %s", res.status)
        assert res.status == 200, f"Unexpected status: {res.status}"
        try:
            body = await res.json()
        except Exception:
            body = await res.text()
        logger.info("RESPONSE BODY: %s", body)
        if isinstance(body, dict):
            assert body['name'] == "Raghav"
            assert body['job'] == "Instructor"
        else:
            raise AssertionError("Expect json response")
        
    @pytest.mark.asyncio
    async def test_delete(self, api_request_context: APIRequestContext) -> None:
        res = await api_request_context.delete(
            f"/api/users/2"
        )
        logger.info("RESPONSE STATUS: %s", res.status)
        assert res.status == 204, f"Unexpected status: {res.status}"