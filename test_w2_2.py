
import pytest
from demoqa import (
    LoginPage,
    TextBoxPage
)

class TestDemoQA:
    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_login_success(self):
        async with LoginPage() as lp:
            await lp.login(lp.username, lp.password)
            await lp.expect_text_visible("oabgnol63")

    @pytest.mark.asyncio
    @pytest.mark.regression
    @pytest.mark.skip_browser("firefox")
    @pytest.mark.skip_browser("msedge")
    async def test_input(self):
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
            # await tb.expect_text_visible("Permanent Address :Dd3$")

    @pytest.mark.asyncio
    async def test_keyboard_input(self):
        async with TextBoxPage() as tb:
            if not tb.page:
                raise RuntimeError("Page not initialized")
            await tb.expect_title()
            await tb.text_box_interact("Full Name", "click")
            await tb.type_text("Hello World")
            await tb.press_key("Control+KeyA")
            await tb.press_key("Backspace")
            await tb.text_box_interact("Full Name", "expect_value", "")
