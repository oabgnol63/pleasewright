from typing import Literal, Any
from typing import Optional
from playwright.async_api import async_playwright, expect, Page, Browser
 
# global browser instance
_playwright = None
_browser = None
 
async def init_browser() -> Optional[Browser]:
    try:
        global _playwright, _browser
        if _browser is None:
            _playwright = await async_playwright().start()
            _browser = await _playwright.chromium.launch(
                headless=False,
                executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
                slow_mo=500,
            )
        return _browser
    except Exception as e:
        raise e
 
async def close_browser() -> None:
    try:
        global _playwright, _browser
        if _browser:
            await _browser.close()
        if _playwright:
            await _playwright.stop()
        _browser = None
        _playwright = None
    except Exception as e:
        raise e
 
def get_browser() -> Browser:
    if _browser is None:
        raise RuntimeError("Browser not initialized")
    return _browser
 
 
class BasePage:    
    def __init__(self, url: str = "") -> None:
        self.url = url
        self.page_title = "DEMOQA"
        self.page: Optional[Page] = None
 
    async def __aenter__(self) -> Any:
        await self.navigate()
        return self
 
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close_page()
 
    async def navigate(self, url: str | None = None,
                       timeout: int = 60000,
                       wait_until: Literal["load", "domcontentloaded", "networkidle", "commit"] = "commit") -> Page | None:
        try:
            browser = get_browser()
            self.page = await browser.new_page()
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

    async def text_box_interact(self, name: str, action: str, value: str = "", **kwargs: Any) -> None:
        if self.page:
            textbox = self.page.get_by_role("textbox", name=name, **kwargs)
            if not textbox:
                raise ValueError(f"Textbox with name '{name}' not found")
            match action:
                case "fill":
                    await textbox.fill(value, **kwargs)
                case "click":
                    await textbox.click(**kwargs)
                case "expect_value":
                    await expect(textbox).to_have_value(value, **kwargs)
                case _:
                    raise ValueError(f"Unsupported action '{action}' for textbox")
        else:
            raise RuntimeError("Page not initialized")
                
    async def button_interact(self, name: str, action: str, value: str = "", **kwargs: Any) -> None:
        if self.page:
            button = self.page.get_by_role("button", name=name, **kwargs)
            if not button:
                raise ValueError(f"Textbox with name '{name}' not found")
            match action:
                case "click":
                    await button.click(**kwargs)
                case _:
                    raise ValueError("Invalid button action")
        else:
            raise RuntimeError("Page not initialized")

    async def expect_text_visible(self, text: str, **kwargs: Any) -> None:
        if self.page:
            await expect(self.page.get_by_text(text, **kwargs)).to_be_visible(**kwargs)
        else:
            raise RuntimeError("Page not initialized")

    async def type_text(self, text: str, **kwargs) -> None:
        if self.page:
            await self.page.keyboard.type(text, **kwargs)
        else:
            raise RuntimeError("Page not initialized")

    async def press_key(self, keys: str, **kwargs) -> None:
        if self.page:
            await self.page.keyboard.press(keys)
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
 
    def __init__(self):
        super().__init__(url=self.url)
   
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
 
