
import pytest
import pytest_asyncio
from playwright.async_api import expect
from w1 import (
    init_browser,
    close_browser,
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

@pytest_asyncio.fixture(scope="function", autouse=True)
async def browser():
    await init_browser()
    yield
    await close_browser()

@pytest.mark.asyncio
async def test_login_success():
    async with LoginPage() as lp:
        await lp.login(lp.username, lp.password)
        if not lp.page:
            raise RuntimeError("Page not initialized")
        await lp.expect_text_visible("oabgnol63")

@pytest.mark.asyncio
async def test_input():
    async with TextBoxPage() as page:
        if not page.page:
            raise RuntimeError("Page not initialized")
        await page.expect_title()
        await page.page.get_by_role("textbox", name="Full Name").fill("Aa")
        await page.page.get_by_role("textbox", name="name@example.com").fill("Bb1@test.com")
        await page.page.get_by_role("textbox", name="Current Address").fill("Cc2#")
        await page.page.locator("#permanentAddress").fill("Dd3$")
        await page.page.get_by_role("button", name="Submit").click()
        await expect(page.page.get_by_text("Name:Aa")).to_be_visible()
        await expect(page.page.get_by_text("Email:Bb1@test.com")).to_be_visible()
        await expect(page.page.get_by_text("Current Address :Cc2#")).to_be_visible()
        # await expect(page.page.get_by_text("Permanent Address :Dd3$")).to_be_visible()

@pytest.mark.asyncio
async def test_keyboard_input():
    async with TextBoxPage() as page:
        if not page.page:
            raise RuntimeError("Page not initialized")
        await page.expect_title()
        await page.page.get_by_role("textbox", name="Full Name").click()
        await page.page.keyboard.type("Hello World")
        await page.page.keyboard.press("Control+KeyA")
        await page.page.keyboard.press("Backspace")
        await expect(page.page.get_by_role("textbox", name="Full Name")).to_have_text("")

@pytest.mark.asyncio
async def test_drag_drop():
    async with DragPage() as page:
        if not page.page:
            raise RuntimeError("Page not initialized")
        await page.expect_title()
        await page.page.locator(page.drag_id).drag_to(
            page.page.get_by_role("tabpanel", name=page.simple_drop_name)
            .locator(page.drop_id))
        await expect(page.page.get_by_text("Dropped!")).to_be_visible()

@pytest.mark.asyncio
async def test_select():
    async with SelectPage() as page:
        if not page.page:
            raise RuntimeError("Page not initialized")
        await page.expect_title()
        await page.page.locator(page.group_menu["id"]).click()
        await page.page.get_by_text(page.group_menu["sel"][0], exact=True).click()
        await page.page.locator(page.select_one["id"]).click()
        await page.page.get_by_text(page.select_one["sel"][0], exact=True).click()
        await page.page.locator(page.select_menu_container["id"]).nth(2).click()
        await page.page.locator("#react-select-4-option-0").click()
        await page.page.locator("#react-select-4-option-1").click()
        await page.page.locator("#react-select-4-option-2").click()
        await page.page.locator("#react-select-4-option-3").click()
        await page.page.locator(page.inplace_select["id"]).select_option("volvo")
        # await page.page.pause()
        await expect(page.page.get_by_text(page.group_menu["sel"][0])).to_be_visible()
        await expect(page.page.get_by_text(page.select_one["sel"][0])).to_be_visible()
        for value in page.select_menu_container["values"]:
            await expect(page.page.get_by_text(value, exact=True).nth(1)).to_be_visible()

@pytest.mark.asyncio
async def test_alert():
    async with AlertPage() as page:
        if not page.page:
            raise RuntimeError("Page not initialized")
        await page.expect_title()
        page.page.on("dialog", lambda dialog: dialog.accept("Hello!"))
        await page.page.locator('#promtButton').click()
        await expect(page.page.get_by_text("You entered Hello!")).to_be_visible()

@pytest.mark.asyncio
async def test_frame():
    async with FramePage() as page:
        if not page.page:
            raise RuntimeError("Page not initialized")
        await page.expect_title()
        frame = page.page.frame("#frame1")
        if frame:
            await expect(frame.locator("#sampleHeading")).to_have_text("This is a sample page")
        else:
            raise ValueError("Frame not found")

@pytest.mark.asyncio
async def test_checkbox():
    async with CheckBoxPage() as page:
        if not page.page:
            raise RuntimeError("Page not initialized")
        await page.expect_title()
        await page.page.get_by_role('button', name='Toggle').click()
        await page.page.locator("label").filter(has_text="Downloads").get_by_role("img").first.click()
        await expect(page.page.get_by_text("downloads", exact=True)).to_be_visible()
        await expect(page.page.get_by_text("wordFile", exact=True)).to_be_visible()
        await expect(page.page.get_by_text("excelFile", exact=True)).to_be_visible()

@pytest.mark.asyncio
async def test_radiobutton():
    async with RadioButtonPage() as page:
        if not page.page:
            raise RuntimeError("Page not initialized")
        await page.expect_title()
        await page.page.get_by_text("Yes").click()
        await expect(page.page.get_by_text("You have selected Yes", exact=True)).to_be_visible()

@pytest.mark.asyncio
async def test_multipage():
    async with MultiPage() as page:
        if not page.page:
            raise RuntimeError("Page not initialized")
        await page.expect_title()
        async with page.page.expect_popup() as page1_info:
            await page.page.get_by_role("button", name="New Tab").click()
        page1 = await page1_info.value
        if page1:
            await expect(page1.get_by_role("heading", name="This is a sample page")).to_be_visible()
        else:
            raise

@pytest.mark.asyncio
async def test_calendar():
    async with CalendarPage() as page:
        from enum import Enum
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
       
        from datetime import date
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
