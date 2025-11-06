import pytest
import json
import pytest_asyncio
from typing import AsyncGenerator
from playwright.async_api import async_playwright, APIRequestContext

from demoqa import (
    init_browser,
    close_browser
)

def pytest_addoption(parser):

    parser.addoption("--record-video", action="store", choices=["on", "failure"], default=None)
    parser.addoption("--slow", action="store", default=None, help="for slow_mo")

def pytest_generate_tests(metafunc):
    if 'test_data' in metafunc.fixturenames:
        data_file = metafunc.module.__file__[:-2] + 'json'
        try:
            with open(data_file) as f:
                data = json.load(f)
            if isinstance(data, list):
                metafunc.parametrize('test_data', data, indirect=True)
        except FileNotFoundError:
            pass

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest_asyncio.fixture(scope="function", params=['chrome', 'msedge', 'firefox'], autouse=True)
async def browser(request):
    markers = request.node.own_markers
    skip_browser = [m.args[0] for m in markers if m.name == "skip_browser"]
    browser_channel = request.config.getoption("browser_channel")
    if browser_channel is not None and browser_channel != request.param:
        pytest.skip()
    elif request.param in skip_browser:
        pytest.skip()
    else:
        config = {
            "browser_type": request.param,
            "video": request.config.getoption("--record-video"),
            "slow": request.config.getoption("--slow"),
        }
        await init_browser(**config)
        yield
        
        # Determine if we should keep the video
        video_option = request.config.getoption("--record-video")
        keep_video = False
        if video_option == "on":
            keep_video = True
        elif video_option == "failure" and request.node.rep_call.failed:
            keep_video = True
        
        await close_browser(keep_video)

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

@pytest.fixture(scope="function")
def test_data(request):
    if hasattr(request, 'param'):
        yield request.param
    else:
        data_file = request.module.__file__[:-2] + 'json'
        with open(data_file) as f:
            data = json.load(f)
        yield data

