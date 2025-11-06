
import pytest
from playwright.async_api import expect
from demoqa import (
    get_browser,
    LoginPage,
    TextBoxPage
)

@pytest.mark.asyncio
@pytest.mark.smoke
async def test_login_success():
    async with LoginPage() as lp:
        await lp.login(lp.username, lp.password)
        await lp.expect_text_visible("oabgnol63")

@pytest.mark.asyncio
@pytest.mark.regression
@pytest.mark.skip_browser("firefox")
@pytest.mark.skip_browser("msedge")
async def test_input():
    async with TextBoxPage() as tb:
        if not tb.page:
            raise RuntimeError("Page not initialized")
        await tb.expect_title()
        await tb.fill_name("Aa")
        await tb.fill_email("Bb1@test.com")
        await tb.fill_address("Cc2#")
        await tb.page.locator("#permanentAddress").fill("Dd3$")
        await tb.button_interact(name="Submit", action="click")
        await tb.expect_text_visible("Name:Aa")
        await tb.expect_text_visible("Email:Bb1@test.com")
        await tb.expect_text_visible("Current Addres :Cc2#")

@pytest.mark.asyncio
@pytest.mark.skip_browser("firefox")
@pytest.mark.skip_browser("msedge")
async def test_http_auth():
    browser = get_browser()
    context = await browser.new_context(http_credentials={"username": "admin", "password": "admin"})
    page = await context.new_page()
    await page.goto("https://the-internet.herokuapp.com/basic_auth")
    await expect(page.get_by_text("Congratulations! You must")).to_be_visible()
    await context.close()

@pytest.mark.asyncio
@pytest.mark.skip_browser("firefox")
@pytest.mark.skip_browser("msedge")
async def test_multi_login(test_data):
    async with LoginPage() as lp:
        await lp.login(test_data['username'], test_data['password'])
        await lp.expect_text_visible(test_data['username'])