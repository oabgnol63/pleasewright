
import pytest
from demoqa import (
    LoginPage,
)

## Login POM page: defined in demoqa.py

## Test login using data from beforeAll
# pytest -sv test_w3.py -k "test_login_session_data"
@pytest.mark.asyncio
@pytest.mark.skip_browser("firefox")
@pytest.mark.skip_browser("msedge")
async def test_login_session_data(session_data):
    async with LoginPage() as lp:
        await lp.login(lp.username, lp.password)
        await lp.expect_text_visible(lp.username)

## Test using state storage
#  pytest -sv test_w3.py -k "test_login_storage_state"
@pytest.mark.asyncio
@pytest.mark.skip_browser("firefox")
@pytest.mark.skip_browser("msedge")
async def test_login_storage_state(authenticated_state):
    async with LoginPage() as lp:
        await lp.expect_text_visible("oabgnol63", timeout=30000)

## Using cloud
# write these to env file or set env (lambda test)
# LT_USERNAME = 
# LT_ACCESS_KEY =
# python test_cloud.py

## Parallel run
# pytest -sv test_w1.py -n auto