import os
from typing import Literal, Any
from typing import Optional
from playwright.async_api import async_playwright, expect, Page, Browser
 
# global browser instance
_playwright = None
_browser = None
_context = None
 
async def init_browser(browser_type: str, slow: int | None = None, video: str | None = None) -> Optional[Browser]:
    try:
        global _playwright, _browser, _context
        if _browser is None:
            _playwright = await async_playwright().start()
            match browser_type:
                case 'chrome':
                    _browser = await _playwright.chromium.launch(
                        headless=False,
                        executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
                        slow_mo=slow,
                    )
                case 'msedge':
                    _browser = await _playwright.chromium.launch(
                        headless=False,
                        executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
                        slow_mo=slow,
                    )
                case 'firefox':
                    _browser = await _playwright.firefox.launch(
                        headless=False,
                        executable_path="C:/Program Files/Mozilla Firefox/firefox.exe",
                        slow_mo=slow,
                    )
                case _:
                    raise ValueError(f"Unsupported browser type: {browser_type}")
                
        _context = await _browser.new_context(
            record_video_dir="test-results/" if video else None,
            # record_video_size={"width": 1280, "height": 720} if video else None
        )
        await _context.tracing.start(screenshots=True, snapshots=True, sources=True)
        return _browser
    except Exception as e:
        raise e
 
async def close_browser(keep_video: bool = False) -> None:
    try:
        global _playwright, _browser, _context
        if _context:
            await _context.tracing.stop(path="trace.zip")
            video_paths = []
            if not keep_video:
                for page in _context.pages:
                    if page.video:
                        video_path = await page.video.path()
                        video_paths.append(video_path)
            await _context.close()
            if not keep_video and video_paths:
                for video_path in video_paths:
                    try:
                        if os.path.exists(video_path):
                            os.remove(video_path)
                    except Exception:
                        pass
        if _browser:
            await _browser.close()
        if _playwright:
            await _playwright.stop()
        _browser = None
        _playwright = None
        _context = None
    except Exception as e:
        raise e
 
def get_browser() -> Browser:
    if _browser is None:
        raise RuntimeError("Browser not initialized")
    return _browser

def get_context():
    if _context is None:
        raise RuntimeError("Context not initialized")
    return _context
 
 
class BasePage:    
    def __init__(self, url: str = "") -> None:
        self.url = url
        self.page_title = "DEMOQA"
        self.page: Optional[Page] = None
 
    async def __aenter__(self) -> Any:
        await self.navigate()
        return self
 
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> Any:
        return None
 
    async def navigate(self, url: str | None = None,
                       timeout: int = 60000,
                       wait_until: Literal["load", "domcontentloaded", "networkidle", "commit"] = "commit") -> Page | None:
        try:
            context = get_context()
            self.page = await context.new_page()
            target_url = url or self.url
            if target_url:
                await self.page.goto(target_url, timeout=timeout, wait_until=wait_until)
            return self.page
        except Exception as e:
            raise e
   
    async def close_page(self) -> None:
        if self.page:
            await self.page.close()
            self.page = None
 
    async def expect_title(self, title: str | None = None, timeout: int = 30000) -> None:
        if self.page:
            if title is None:
                title = self.page_title
            await expect(self.page).to_have_title(title, timeout=timeout)
        else:
            raise ValueError("Page not initialized")

    async def text_box_interact(
            self, 
            name: str, 
            action: str, 
            value: str = "", 
            locator_kwargs: dict = {}, 
            fill_kwargs: dict = {},
            click_kwargs: dict = {},
            expect_kwargs: dict = {}
    ) -> None:

        if self.page:
            textbox = self.page.get_by_role("textbox", name=name, **locator_kwargs)
            if not textbox:
                raise ValueError(f"Textbox with name '{name}' not found")
            match action:
                case "fill":
                    await textbox.fill(value, **fill_kwargs)
                case "click":
                    await textbox.click(**click_kwargs)
                case "expect_value":
                    await expect(textbox).to_have_value(value, **expect_kwargs)
                case _:
                    raise ValueError(f"Unsupported action '{action}' for textbox")
        else:
            raise RuntimeError("Page not initialized")
                
    async def button_interact(
            self, 
            name: str, 
            action: str, 
            value: str = "", 
            locator_kwargs: dict = {}, 
            click_kwargs: dict = {},
    ) -> None:

        if self.page:
            button = self.page.get_by_role("button", name=name, **locator_kwargs)
            if not button:
                raise ValueError(f"Textbox with name '{name}' not found")
            match action:
                case "click":
                    await button.click(**click_kwargs)
                case _:
                    raise ValueError("Invalid button action")
        else:
            raise RuntimeError("Page not initialized")

    async def expect_text_visible(
            self, text: str, 
            exact: bool | None = None, 
            visible: bool | None = None,
            timeout: float | None = None
    ) -> None:

        if self.page:
            await expect(self.page.get_by_text(text, exact=exact)).to_be_visible(visible=visible, timeout=timeout)
        else:
            raise RuntimeError("Page not initialized")

    async def type_text(self, text: str, **kwargs) -> None:
        if self.page:
            await self.page.keyboard.type(text, **kwargs)
        else:
            raise RuntimeError("Page not initialized")

    async def press_key(self, keys: str, **kwargs) -> None:
        if self.page:
            await self.page.keyboard.press(keys, **kwargs)
        else:
            raise RuntimeError("Page not initialized")
 
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
        else:
            raise RuntimeError("Page not initialized")
 
class TextBoxPage(BasePage):
    url = "https://demoqa.com/text-box"
    fullname_ph = "Full Name"
    email_ph = "name@example.com"
    current_address_ph = "Current Address"
    def __init__(self):
        super().__init__(url=self.url)
    
    async def fill_name(self, name: str) -> None:
        if self.page:
            await self.text_box_interact(self.fullname_ph, "fill", name)
        else:
            raise RuntimeError("Page not initialized")
        
    async def fill_email(self, email: str) -> None:
        if self.page:
            await self.text_box_interact(self.email_ph, "fill", email)
        else:
            raise RuntimeError("Page not initialized")
        
    async def fill_address(self, address: str) -> None:
        if self.page:
            await self.text_box_interact(self.current_address_ph, "fill", address)
        else:
            raise RuntimeError("Page not initialized")
   
class DragPage(BasePage):
    url = "https://demoqa.com/droppable"
    drag_id = "#draggable"
    drop_id = "#droppable"
    simple_drop_name = "Simple"
 
    def __init__(self):
        super().__init__(url=self.url)
  
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
        
class AlertPage(BasePage):
    url = "https://demoqa.com/alerts"
 
    def __init__(self):
        super().__init__(url=self.url)
  
class FramePage(BasePage):
    url = "https://demoqa.com/frames"
 
    def __init__(self):
        super().__init__(url=self.url)
  
class CheckBoxPage(BasePage):
    url = "https://demoqa.com/checkbox"
 
    def __init__(self):
        super().__init__(url=self.url)
  
class RadioButtonPage(BasePage):
    url = "https://demoqa.com/radio-button"
 
    def __init__(self):
        super().__init__(url=self.url)
  
class MultiPage(BasePage):
    url = "https://demoqa.com/browser-windows"
 
    def __init__(self):
        super().__init__(url=self.url)
  
class CalendarPage(BasePage):
    url = "https://demoqa.com/date-picker"
 
    def __init__(self):
        super().__init__(url=self.url)
 
