
import pytest
from demoqa import (
    LoginPage,
)

@pytest.mark.asyncio
@pytest.mark.skip_browser("firefox")
@pytest.mark.skip_browser("msedge")
async def test_login(session_data):
    async with LoginPage() as lp:
        await lp.login(lp.username, lp.password)
        await lp.expect_text_visible(lp.username)

@pytest.mark.asyncio
@pytest.mark.skip_browser("firefox")
@pytest.mark.skip_browser("msedge")
async def test_login_storage_state(authenticated_state):
    async with LoginPage() as lp:
        await lp.expect_text_visible("oabgnol63", timeout=10000)
        await lp.page.pause()