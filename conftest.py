import pytest
import json
import pytest_asyncio
from typing import AsyncGenerator
from playwright.async_api import async_playwright, APIRequestContext

from demoqa import (
    init_browser,
    close_browser
)

SESSION_DATA = [
    {
        "username": "test",
        "password": "Exploit99*"
    },
    {
        "username": "test2",
        "password": "Exploit99*"
    }
]

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
    if 'session_data' in metafunc.fixturenames:
        metafunc.parametrize('session_data', SESSION_DATA, indirect=True)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture(scope="session")
def session_data():
    yield SESSION_DATA

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
        storage_state = None
        if 'authenticated_state' in request.fixturenames:
            storage_state = request.getfixturevalue('authenticated_state')
        
        config = {
            "browser_type": request.param,
            "video": request.config.getoption("--record-video"),
            "slow": request.config.getoption("--slow"),
            "storage_state": storage_state
        }
        await init_browser(**config)
        
        yield
        
        # keep video or not
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
    yield request.param

@pytest_asyncio.fixture(scope="session")
async def authenticated_state():
    # temp browser to get auth state
    temp_playwright = await async_playwright().start()
    temp_browser = await temp_playwright.chromium.launch(
        headless=False,
        executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe"
    )
    temp_context = await temp_browser.new_context()
    temp_page = await temp_context.new_page()
    
    await temp_page.goto("https://demoqa.com/login")
    await temp_page.get_by_role("textbox", name="UserName").fill("oabgnol63")
    await temp_page.get_by_role("textbox", name="Password").fill("Exploit99*")
    await temp_page.click("button#login")
    await temp_page.wait_for_selector(f"text=oabgnol63", timeout=10000)
    
    auth_file = "state.json"
    await temp_context.storage_state(path=auth_file)
    await temp_context.close()
    await temp_browser.close()
    await temp_playwright.stop()
    
    yield auth_file
