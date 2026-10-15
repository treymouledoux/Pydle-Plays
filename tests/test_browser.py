"""Browser regressions based on the captured Pydle help dialog markup."""

import os
import unittest

from scripts.update_progress import click_control, dismiss_startup_dialogs, read_archive


@unittest.skipUnless(os.getenv("RUN_BROWSER_TESTS"), "Browser tests run after Chromium is installed")
class PopupTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        from playwright.async_api import async_playwright
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch()
        self.page = await self.browser.new_page()
        await self.page.set_content('''
            <button aria-haspopup="menu" onclick="this.dataset.clicked='true'">Menu</button>
            <template id="help">
              <div role="dialog" aria-modal="true" aria-labelledby="help-title"
                   style="position:fixed;inset:0;z-index:100;background:white">
                <h3 id="help-title">How to play Pydle</h3>
                <button onclick="this.closest('[role=dialog]').remove()">
                  <svg aria-hidden="true"><path d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/></svg>
                </button>
              </div>
            </template>''')

    async def asyncTearDown(self):
        await self.browser.close()
        await self.playwright.stop()

    async def show_help(self):
        await self.page.evaluate("document.body.append(document.querySelector('#help').content.cloneNode(true))")

    async def test_unlabeled_close_button(self):
        await self.show_help()
        await click_control(self.page, self.page.locator('[aria-haspopup="menu"]'))
        self.assertEqual(await self.page.locator('[aria-haspopup="menu"]').get_attribute('data-clicked'), 'true')

    async def test_popup_mounts_between_check_and_click(self):
        test = self
        control = self.page.locator('[aria-haspopup="menu"]')

        class LatePopup:
            first = True

            async def click(self, **kwargs):
                if self.first:
                    self.first = False
                    await test.show_help()
                await control.click(**kwargs)

        await click_control(self.page, LatePopup())
        self.assertEqual(await control.get_attribute('data-clicked'), 'true')

    async def test_archive_stays_open(self):
        await self.page.set_content('<div role="dialog"><h3>Puzzle Archive</h3><button>Pydle #1</button></div>')
        await dismiss_startup_dialogs(self.page)
        self.assertTrue(await self.page.get_by_role('dialog').is_visible())

    async def test_zero_height_headless_ui_wrapper(self):
        await self.show_help()
        await self.page.evaluate('''() => {
            const dialog = document.querySelector('[role=dialog]');
            dialog.removeAttribute('style');
            dialog.style.cssText = 'position:relative;height:0';
            const panel = document.createElement('div');
            panel.id = 'headlessui-dialog-panel-regression';
            panel.style.cssText = 'position:fixed;inset:0;z-index:100;background:white';
            while (dialog.firstChild) panel.append(dialog.firstChild);
            dialog.append(panel);
        }''')
        self.assertFalse(await self.page.get_by_role('dialog').is_visible())
        self.assertTrue(await self.page.locator('#headlessui-dialog-panel-regression').is_visible())
        await click_control(self.page, self.page.locator('[aria-haspopup="menu"]'))
        self.assertEqual(await self.page.locator('[aria-haspopup="menu"]').get_attribute('data-clicked'), 'true')

    async def test_archive_scrolls_to_end_and_excludes_page_header(self):
        await self.page.set_content('''
            <h1>Pydle #999</h1>
            <div role="dialog" style="height:0;position:relative">
              <div id="headlessui-dialog-panel-archive" style="position:fixed;inset:20px">
                <h3>Puzzle Archive</h3>
                <div style="height:200px;overflow-y:auto" id="entries"></div>
              </div>
            </div>''')
        await self.page.evaluate('''() => {
            const entries = document.querySelector('#entries');
            for (let i=1; i<=234; i++) {
                const button = document.createElement('button');
                // No text-node spacing: whole-button textContent would turn #1 + 0 into #10.
                button.innerHTML = `<span>Pydle #${i}</span><span>0 chars</span><span>Unplayed</span>`;
                button.style.cssText = 'display:block;height:40px';
                entries.append(button);
            }
        }''')
        ids = await read_archive(self.page.locator('[role="dialog"]'), poll_interval=0.01)
        self.assertEqual(ids, set(range(1, 235)))
        self.assertTrue(await self.page.locator('#entries').evaluate('e => e.scrollTop + e.clientHeight >= e.scrollHeight - 2'))

    async def test_zero_size_button_with_visible_absolute_svg(self):
        await self.show_help()
        await self.page.evaluate('''() => {
            const button = document.querySelector('[role=dialog] button');
            button.style.cssText = 'display:inline-block;width:0;height:0;padding:0;border:0';
            button.querySelector('svg').style.cssText = 'position:absolute;top:8px;right:8px;width:24px;height:24px';
        }''')
        self.assertFalse(await self.page.locator('[role=dialog] button').is_visible())
        self.assertTrue(await self.page.locator('[role=dialog] button svg').is_visible())
        await click_control(self.page, self.page.locator('[aria-haspopup="menu"]'))
        self.assertEqual(await self.page.locator('[aria-haspopup="menu"]').get_attribute('data-clicked'), 'true')
