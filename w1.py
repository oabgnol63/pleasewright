import asyncio
from typing import Literal
from datetime import date
from playwright.async_api import async_playwright, expect
 
# global browser instance
_playwright = None
_browser = None
 
async def init_browser():
    global _playwright, _browser
    if _browser is None:
        _playwright = await async_playwright().start()
        _browser = await _playwright.chromium.launch(
            headless=False,
            executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
            slow_mo=500,
        )
    return _browser
 
async def close_browser():
    global _playwright, _browser
    if _browser:
        await _browser.close()
    if _playwright:
        await _playwright.stop()
    _browser = None
    _playwright = None
 
def get_browser():
    if _browser is None:
        raise RuntimeError("Browser not initialized")
    return _browser
 
 
class BasePage:    
    def __init__(self, url: str = ""):
        self.url = url
        self.page_title = "DEMOQA"
        self.page = None
 
    async def __aenter__(self):
        await self.navigate()
        return self
 
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_page()
 
    async def navigate(self, url: str | None = None,
                       timeout: int = 60000,
                       wait_until: Literal["load", "domcontentloaded", "networkidle", "commit"] = "commit"):
        browser = get_browser()
        self.page = await browser.new_page()
        target_url = url or self.url
        if target_url:
            await self.page.goto(target_url, timeout=timeout, wait_until=wait_until)
        return self.page
   
    async def close_page(self):
        if self.page:
            await self.page.close()
            self.page = None
 
    async def expect_title(self, title: str | None = None, timeout: int = 30000):
        if self.page:
            if title is None:
                title = self.page_title
            await expect(self.page).to_have_title(title, timeout=timeout)
 
class LoginPage(BasePage):
    url = "https://demoqa.com/login"
    ph_username = 'UserName'
    ph_password = 'Password'
    username = "oabgnol63"
    password = "Exploit99*"
    login_button_id = "button#login"
 
    def __init__(self):
        super().__init__(url=self.url)
 
    async def login(self, username, password):
        if self.page:
            await self.page.get_by_role("textbox", name=self.ph_username).fill(username)
            await self.page.get_by_role("textbox", name=self.ph_password).fill(password)
            await self.page.click(f'{self.login_button_id}')
   
    async def test_login_success(self):
        await self.login(self.username, self.password)
        if not self.page:
            raise RuntimeError("Page not initialized")
        await expect(self.page.get_by_text("oabgnol63")).to_be_visible()
        print("Login test passed")
 
class TextBoxPage(BasePage):
    url = "https://demoqa.com/text-box"
 
    def __init__(self):
        super().__init__(url=self.url)
 
    async def test_input(self):
        if not self.page:
            raise RuntimeError("Page not initialized")
        await self.expect_title()
        await self.page.get_by_role("textbox", name="Full Name").fill("Aa")
        await self.page.get_by_role("textbox", name="name@example.com").fill("Bb1@test.com")
        await self.page.get_by_role("textbox", name="Current Address").fill("Cc2#")
        await self.page.locator("#permanentAddress").fill("Dd3$")
        await self.page.get_by_role("button", name="Submit").click()
        await expect(self.page.get_by_text("Name:Aa")).to_be_visible()
        await expect(self.page.get_by_text("Email:Bb1@test.com")).to_be_visible()
        await expect(self.page.get_by_text("Current Address :Cc2#")).to_be_visible()
        # await expect(self.page.get_by_text("Permanent Address :Dd3$")).to_be_visible()
        print("Text box input test passed")
 
    async def test_keyboard_input(self):
        if not self.page:
            raise RuntimeError("Page not initialized")
        await self.expect_title()
        await self.page.get_by_role("textbox", name="Full Name").click()
        await self.page.keyboard.type("Hello World")
        await self.page.keyboard.press("Control+KeyA")
        await self.page.keyboard.press("Backspace")
        await expect(self.page.get_by_role("textbox", name="Full Name")).to_have_text("")
        print("Keyboard input test passed")
 
class DragPage(BasePage):
    url = "https://demoqa.com/droppable"
    drag_id = "#draggable"
    drop_id = "#droppable"
    simple_drop_name = "Simple"
 
    def __init__(self):
        super().__init__(url=self.url)
 
    async def test_drag_drop(self):
        if not self.page:
            raise RuntimeError("Page not initialized")
        await self.expect_title()
        await self.page.locator(self.drag_id).drag_to(
            self.page.get_by_role("tabpanel", name=self.simple_drop_name)
            .locator(self.drop_id))
        await expect(self.page.get_by_text("Dropped!")).to_be_visible()
        print("Drag and drop test passed")
 
class SelectPage(BasePage):
    url = "https://demoqa.com/select-menu"
 
    group_menu = {
        "id": "#withOptGroup svg",
        "sel": ["Group 1, option 1"]
    }
 
    select_one = {
        "id": "#selectOne svg",
        "sel": ["Dr."]
    }
 
    select_menu_container = {
        "id": "#selectMenuContainer svg",
        "sel": ["react-select-4-option-0", "react-select-4-option-1", "react-select-4-option-2", "react-select-4-option-3"],
        "values": ["Green", "Blue", "Black", "Red"]
    }
 
    inplace_select = {
        "id": "#cars",
        "sel": ["volvo"]
    }
 
    def __init__(self):
        super().__init__(url=self.url)
 
    async def test_select(self):
        if not self.page:
            raise RuntimeError("Page not initialized")
        await self.expect_title()
        await self.page.locator(self.group_menu["id"]).click()
        await self.page.get_by_text(self.group_menu["sel"][0], exact=True).click()
        await self.page.locator(self.select_one["id"]).click()
        await self.page.get_by_text(self.select_one["sel"][0], exact=True).click()
        await self.page.locator(self.select_menu_container["id"]).nth(2).click()
        await self.page.locator("#react-select-4-option-0").click()
        await self.page.locator("#react-select-4-option-1").click()
        await self.page.locator("#react-select-4-option-2").click()
        await self.page.locator("#react-select-4-option-3").click()
        await self.page.locator(self.inplace_select["id"]).select_option("volvo")
        # await self.page.pause()
        await expect(self.page.get_by_text(self.group_menu["sel"][0])).to_be_visible()
        await expect(self.page.get_by_text(self.select_one["sel"][0])).to_be_visible()
        for value in self.select_menu_container["values"]:
            await expect(self.page.get_by_text(value, exact=True).nth(1)).to_be_visible()
        print("Select menu test passed")
       
class AlertPage(BasePage):
    url = "https://demoqa.com/alerts"
 
    def __init__(self):
        super().__init__(url=self.url)
 
    async def test_alert(self):
        if not self.page:
            raise RuntimeError("Page not initialized")
        await self.expect_title()
        self.page.on("dialog", lambda dialog: dialog.accept("Hello!"))
        await self.page.locator('#promtButton').click()
        await expect(self.page.get_by_text("You entered Hello!")).to_be_visible()
        print("Alert test passed")
 
class FramePage(BasePage):
    url = "https://demoqa.com/frames"
 
    def __init__(self):
        super().__init__(url=self.url)
 
    async def test_frame(self):
        if not self.page:
            raise RuntimeError("Page not initialized")
        await self.expect_title()
        frame = self.page.frame("#frame1")
        if frame:
            await expect(frame.locator("#sampleHeading")).to_have_text("This is a sample page")
        print("Frame test passed")
 
class CheckBoxPage(BasePage):
    url = "https://demoqa.com/checkbox"
 
    def __init__(self):
        super().__init__(url=self.url)
 
    async def test_checkbox(self):
        if not self.page:
            raise RuntimeError("Page not initialized")
        await self.expect_title()
        await self.page.get_by_role('button', name='Toggle').click()
        await self.page.locator("label").filter(has_text="Downloads").get_by_role("img").first.click()
        await expect(self.page.get_by_text("downloads", exact=True)).to_be_visible()
        await expect(self.page.get_by_text("wordFile", exact=True)).to_be_visible()
        await expect(self.page.get_by_text("excelFile", exact=True)).to_be_visible()
        print("Checkbox test passed")
 
class RadioButtonPage(BasePage):
    url = "https://demoqa.com/radio-button"
 
    def __init__(self):
        super().__init__(url=self.url)
 
    async def test_radiobutton(self):
        if not self.page:
            raise RuntimeError("Page not initialized")
        await self.expect_title()
        await self.page.get_by_text("Yes").click()
        await expect(self.page.get_by_text("You have selected Yes", exact=True)).to_be_visible()
        print("Radio button test passed")
 
class MultiPage(BasePage):
    url = "https://demoqa.com/browser-windows"
 
    def __init__(self):
        super().__init__(url=self.url)
 
    async def test_multipage(self):
        if not self.page:
            raise RuntimeError("Page not initialized")
        await self.expect_title()
        async with self.page.expect_popup() as page1_info:
            await self.page.get_by_role("button", name="New Tab").click()
        page1 = await page1_info.value
        if page1:
            await expect(page1.get_by_role("heading", name="This is a sample page")).to_be_visible()
            print("Multi-page test passed")
        print("Multi-page test passed")
 
class CalendarPage(BasePage):
    url = "https://demoqa.com/date-picker"
 
    def __init__(self):
        super().__init__(url=self.url)
 
    async def test_calendar(self):
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
       
        if not self.page:
            raise RuntimeError("Page not initialized")
        await self.expect_title()
        await self.page.locator("#datePickerMonthYearInput").click()
        await self.page.get_by_role("option", name=f"Choose {weekday_name}, {month_name} {dday},").click()
        await expect(self.page.locator("#datePickerMonthYearInput")).to_have_value(formatted_date)
        print("Calendar test passed")
 
 
DEMOQA
 