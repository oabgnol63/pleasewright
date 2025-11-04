import pytest
import pytest_asyncio
from typing import AsyncGenerator
from playwright.async_api import async_playwright, APIRequestContext

from demoqa import (
    init_browser,
    close_browser
)

# def pytest_addoption(parser):
#     parser.addoption(
#         "--browser",
#         action="store",
#         default=None,
#         help="Browser to run tests on: chrome, edge, or firefox"
#     )

@pytest_asyncio.fixture(scope="function", params=['chrome', 'msedge', 'firefox'], autouse=True)
async def browser(request):
    browser_channel = request.config.getoption("browser_channel")
    if browser_channel is not None and browser_channel != request.param:
        pytest.skip()
    await init_browser(request.param)
    yield
    await close_browser()

@pytest_asyncio.fixture(scope="function")
async def api_request_context() -> AsyncGenerator[APIRequestContext, None]:
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': 'reqres-free-v1'
    }
    async with async_playwright() as pw:
        request_context = await pw.request.new_context(
            base_url="https://reqres.in/", extra_http_headers=headers
        )
        yield request_context
        await request_context.dispose()