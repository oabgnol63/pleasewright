import os
import json
import asyncio
import subprocess
from dotenv import load_dotenv
load_dotenv()

from playwright._impl._page import Page
from playwright.async_api import async_playwright, expect
from playwright.async_api._generated import Playwright


capabilities = {
    "browserName": "Chrome",  # Browsers allowed: `Chrome`, `MicrosoftEdge`, `pw-chromium`, `pw-firefox` and `pw-webkit`
    "browserVersion": "141",
    "LT:Options": {
        "platform": "Windows 10",
        "build": "Playwright Python Build",
        "name": "Playwright Test",
        "user": os.getenv("LT_USERNAME"),
        "accessKey": os.getenv("LT_ACCESS_KEY"),
        "network": True,
        "video": True,
        "console": True,
        "tunnel": False,  # Add tunnel configuration if testing locally hosted webpage
        "tunnelName": "",  # Optional
        "geoLocation": "",  # country code can be fetched from https://www.lambdatest.com/capabilities-generator/
    },
}


async def run(playwright: Playwright):
    playwrightVersion = (
        str(subprocess.getoutput("playwright --version")).strip().split(" ")[1]
    )
    capabilities["LT:Options"]["playwrightClientVersion"] = playwrightVersion  # type: ignore

    lt_cdp_url = f"wss://cdp.lambdatest.com/playwright?capabilities={json.dumps(capabilities)}"
    browser = await playwright.chromium.connect(lt_cdp_url, timeout=120000)
    page: Page = await browser.new_page()  # type: ignore
    try:
        await page.goto("https://demoqa.com/login")
        await page.get_by_role("textbox", name="UserName").fill("oabgnol63")
        await page.get_by_role("textbox", name="Password").fill("Exploit99*")
        await page.click("button#login")
        await expect(page.get_by_text("oabgnol63")).to_be_visible(timeout=10000)

        title = await page.title()
        print("Title:: ", title)

        if "LambdaTest" in title:
            await set_test_status(page, "passed", "Title matched")
        else:
            await set_test_status(page, "failed", "Title did not match")
    except Exception as err:
        print("Error:: ", err)
        await set_test_status(page, "failed", str(err))

    await browser.close()


async def set_test_status(page: Page, status: str, remark: str):
    action_dict = {
        "action": "setTestStatus",
        "arguments": {"status": status, "remark": remark},
    }
    await page.evaluate(
        "_ => {}",
        json.dumps({"lambdatest_action": action_dict})
    )


async def run_playwright():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == "__main__":
    asyncio.run(run_playwright())