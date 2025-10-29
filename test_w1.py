
import pytest
from playwright.async_api import expect
from demoqa import (
    LoginPage,
    TextBoxPage,
    DragPage,
    SelectPage,
    AlertPage,
    FramePage,
    CheckBoxPage,
    RadioButtonPage,
    MultiPage,
    CalendarPage,
)

class TestDemoQA:
    @pytest.mark.asyncio
    async def test_login_success(self):
        async with LoginPage() as lp:
            await lp.login(lp.username, lp.password)
            await lp.expect_text_visible("oabgnol63")

    @pytest.mark.asyncio
    async def test_input(self):
        async with TextBoxPage() as tb:
            if not tb.page:
                raise RuntimeError("Page not initialized")
            await tb.expect_title()
            await tb.text_box_interact("Full Name", "fill", "Aa")
            await tb.text_box_interact(name="name@example.com", action="fill" , value="Bb1@test.com")
            await tb.text_box_interact("Current Address", "fill", "Cc2#")
            await tb.page.locator("#permanentAddress").fill("Dd3$")
            await tb.button_interact(name="Submit", action="click")
            await tb.expect_text_visible("Name:Aa")
            await tb.expect_text_visible("Email:Bb1@test.com")
            await tb.expect_text_visible("Current Address :Cc2#")
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

    @pytest.mark.asyncio
    async def test_drag_drop(self):
        async with DragPage() as dp:
            if not dp.page:
                raise RuntimeError("Page not initialized")
            await dp.expect_title()
            await dp.page.locator(dp.drag_id).drag_to(
                dp.page.get_by_role("tabpanel", name=dp.simple_drop_name)
                .locator(dp.drop_id))
            await dp.expect_text_visible("Dropped!")

    @pytest.mark.asyncio
    async def test_select(self):
        async with SelectPage() as sp:
            if not sp.page:
                raise RuntimeError("Page not initialized")
            await sp.expect_title()
            await sp.page.locator(sp.group_menu["id"]).click()
            await sp.page.get_by_text(sp.group_menu["sel"][0], exact=True).click()
            await sp.page.locator(sp.select_one["id"]).click()
            await sp.page.get_by_text(sp.select_one["sel"][0], exact=True).click()
            await sp.page.locator(sp.select_menu_container["id"]).nth(2).click()
            await sp.page.locator("#react-select-4-option-0").click()
            await sp.page.locator("#react-select-4-option-1").click()
            await sp.page.locator("#react-select-4-option-2").click()
            await sp.page.locator("#react-select-4-option-3").click()
            await sp.page.locator(sp.inplace_select["id"]).select_option("volvo")
            # await sp.page.pause()
            await sp.expect_text_visible(sp.group_menu["sel"][0])
            await sp.expect_text_visible(sp.select_one["sel"][0])
            for value in sp.select_menu_container["values"]:
                await expect(sp.page.get_by_text(value, exact=True).nth(1)).to_be_visible()

    @pytest.mark.asyncio
    async def test_alert(self):
        async with AlertPage() as ap:
            if not ap.page:
                raise RuntimeError("Page not initialized")
            await ap.expect_title()
            ap.page.on("dialog", lambda dialog: dialog.accept("Hello!"))
            await ap.page.locator('#promtButton').click()
            await expect(ap.page.get_by_text("You entered Hello!")).to_be_visible()

    @pytest.mark.asyncio
    async def test_frame(self):
        async with FramePage() as fp:
            if not fp.page:
                raise RuntimeError("Page not initialized")
            await fp.expect_title()
            frame = fp.page.frame("#frame1")
            if frame:
                await expect(frame.locator("#sampleHeading")).to_have_text("This is a sample page")
            else:
                raise ValueError("Frame not found")

    @pytest.mark.asyncio
    async def test_checkbox(self):
        async with CheckBoxPage() as cb:
            if not cb.page:
                raise RuntimeError("Page not initialized")
            await cb.expect_title()
            await cb.page.get_by_role('button', name='Toggle').click()
            await cb.page.locator("label").filter(has_text="Downloads").get_by_role("img").first.click()
            await expect(cb.page.get_by_text("downloads", exact=True)).to_be_visible()
            await expect(cb.page.get_by_text("wordFile", exact=True)).to_be_visible()
            await expect(cb.page.get_by_text("excelFile", exact=True)).to_be_visible()

    @pytest.mark.asyncio
    async def test_radiobutton(self):
        async with RadioButtonPage() as rp:
            if not rp.page:
                raise RuntimeError("Page not initialized")
            await rp.expect_title()
            await rp.page.get_by_text("Yes").click()
            await expect(rp.page.get_by_text("You have selected Yes", exact=True)).to_be_visible()

    @pytest.mark.asyncio
    async def test_multipage(self):
        async with MultiPage() as mp:
            if not mp.page:
                raise RuntimeError("Page not initialized")
            await mp.expect_title()
            async with mp.page.expect_popup() as page1_info:
                await mp.page.get_by_role("button", name="New Tab").click()
            page1 = await page1_info.value
            if page1:
                await expect(page1.get_by_role("heading", name="This is a sample page")).to_be_visible()
            else:
                raise ValueError("Popup page not found")

    @pytest.mark.asyncio
    async def test_calendar(self):
        from enum import Enum
        from datetime import date
        async with CalendarPage() as page:
            class Weekday(Enum):
                MONDAY = 0
                TUESDAY = 1
                WEDNESDAY = 2
                THURSDAY = 3
                FRIDAY = 4
                SATURDAY = 5
                SUNDAY = 6
        
            class Month(Enum):
                JANUARY = 1
                FEBRUARY = 2
                MARCH = 3
                APRIL = 4
                MAY = 5
                JUNE = 6
                JULY = 7
                AUGUST = 8
                SEPTEMBER = 9
                OCTOBER = 10
                NOVEMBER = 11
                DECEMBER = 12
        
            
            today = date.today()
            formatted_date = today.strftime("%m/%d/%Y")
            weekday_num = today.weekday()
            month_num = today.month
            day = today.day
        
            weekday_enum = Weekday(weekday_num)
            month_enum = Month(month_num)
        
            weekday_name = weekday_enum.name.capitalize()
            month_name = month_enum.name.capitalize()
        
            if day == 1 or (day > 20 and day % 10 == 1):
                dday = f"{day}st"
            elif day == 2 or (day > 20 and day % 10 == 2):
                dday = f"{day}nd"
            elif day == 3 or (day > 20 and day % 10 == 3):
                dday = f"{day}rd"
            else:
                dday = f"{day}th"
        
            if not page.page:
                raise RuntimeError("Page not initialized")
            await page.expect_title()
            await page.page.locator("#datePickerMonthYearInput").click()
            await page.page.get_by_role("option", name=f"Choose {weekday_name}, {month_name} {dday},").click()
            await expect(page.page.locator("#datePickerMonthYearInput")).to_have_value(formatted_date)
