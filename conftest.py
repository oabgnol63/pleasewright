import pytest_asyncio
from typing import AsyncGenerator
from playwright.async_api import async_playwright, APIRequestContext

from demoqa import (
    init_browser,
    close_browser
)

@pytest_asyncio.fixture(scope="function", autouse=True)
async def browser():
    await init_browser()
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