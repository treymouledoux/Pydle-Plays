"""Read Pydle's rendered archive and update the README progress block."""

import asyncio
import math
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- pydle-progress:start -->"
END = "<!-- pydle-progress:end -->"


def archive_ids(text):
    """Count actual numbered entries, never assume the highest ID is the total."""
    ids = {int(number) for number in re.findall(r"#\s*(\d+)\b", text)}
    ids.discard(0)
    if not ids:
        raise ValueError("No numbered games found in the archive; README left unchanged.")
    return ids


def completed_ids(directory):
    return attempt_ids(directory)[0]


def attempt_ids(directory):
    """A completed solution takes precedence over a broken attempt for the same ID."""
    ids = set()
    broken = set()
    for path in directory.glob("*.py"):
        match = re.match(r"#(\d+)\b", path.name)
        if match:
            target = broken if "(broken)" in path.stem.casefold() else ids
            target.add(int(match[1]))
    return ids, broken - ids


def game_results(directory):
    """Use recorded Pydle scores only when the attempt includes saved code."""
    results = {}
    header = re.compile(r"^\s*#.*?(\d+)\s*/\s*(?:250|125)\b.*$", re.M)
    for path in sorted(directory.glob("*.py")):
        match = re.match(r"#(\d+)\b", path.name)
        if not match:
            continue
        game = results.setdefault(int(match[1]), {"best": None, "broken": False})
        text = path.read_text()
        headers = list(header.finditer(text))
        file_broken = "(broken)" in path.stem.casefold()
        game["broken"] |= file_broken
        for index, section in enumerate(headers):
            end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
            code = text[section.end():end]
            if not any(line.strip() and not line.lstrip().startswith('#') for line in code.splitlines()):
                continue
            if file_broken or "broken" in section[0].casefold():
                game["broken"] = True
                continue
            score = int(section[1])
            if game["best"] is None or score < game["best"]:
                game["best"] = score
    for game in results.values():
        score = game["best"]
        game["status"] = "Hard" if score is not None and score < 125 else "Easy only" if score is not None and score < 250 else "Broken" if game["broken"] else "Incomplete"
    return results


def result_counts(results, total):
    if total < len(results):
        raise ValueError("Archive total is smaller than the number of repo games; check scraper diagnostics.")
    counts = {name: 0 for name in ("Hard", "Easy only", "Broken", "Incomplete")}
    for result in results.values():
        counts[result["status"]] += 1
    counts["Incomplete"] += total - len(results)
    return counts


async def dialog_surface(dialog):
    # Headless UI's role=dialog wrapper can have zero height; its fixed panel is visible.
    panel = dialog.locator('[id^="headlessui-dialog-panel-"]')
    return panel.first if await panel.count() else dialog


async def dismiss_startup_dialogs(page):
    """Headless UI dialogs cover the menu on a browser's first visit."""
    dialogs = page.locator('[role="dialog"]')
    for _ in range(5):
        visible = [dialogs.nth(i) for i in range(await dialogs.count())
                   if await (await dialog_surface(dialogs.nth(i))).is_visible()]
        if not visible:
            return
        dialog = visible[-1]
        surface = await dialog_surface(dialog)
        if await dialog.get_by_role("heading", name=re.compile("Puzzle Archive", re.I)).count():
            return
        print("Dismissing startup dialog:", (await dialog.inner_text())[:500])
        if await dialog.get_by_role("heading", name="How to play Pydle", exact=True).count():
            # The captured page has one unlabeled button inside this dialog: X.
            close = dialog.locator('button:not([data-headlessui-focus-guard])')
            # Its absolutely positioned SVG is visible even when the button has no box.
            icon = close.locator('svg')
            if await icon.count() and await icon.first.is_visible():
                await icon.first.click(timeout=5000)
            else:
                await close.click(timeout=5000)
            await surface.wait_for(state="hidden", timeout=5000)
            continue
        await page.keyboard.press("Escape")
        try:
            await surface.wait_for(state="hidden", timeout=2000)
            continue
        except Exception:
            close = dialog.get_by_role("button", name=re.compile(r"close|dismiss|got it|start|okay|^ok$", re.I))
            if not await close.count():
                close = dialog.locator('button[title*="close" i]')
            if not await close.count():
                raise ValueError("Startup dialog could not be dismissed; see scraper diagnostics.")
            await close.first.click(timeout=5000)
            await surface.wait_for(state="hidden", timeout=5000)
    raise ValueError("Too many startup dialogs; see scraper diagnostics.")


async def click_control(page, control):
    from playwright.async_api import TimeoutError as PlaywrightTimeoutError

    for attempt in range(3):
        await dismiss_startup_dialogs(page)
        try:
            await control.click(timeout=2000)
            return
        except PlaywrightTimeoutError:
            # A first-visit popup may mount between the check and the click.
            if attempt == 2:
                raise


async def fetch_archive():
    from playwright.async_api import async_playwright

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()
        try:
            archive_url = os.getenv("PYDLE_ARCHIVE_URL") or "https://pydle.net"
            await page.goto(archive_url, wait_until="networkidle")
            # Archive controls can be icon buttons with only a tooltip or SVG title.
            candidates = [
                page.get_by_role("link", name=re.compile("archive", re.I)),
                page.get_by_role("button", name=re.compile("archive", re.I)),
                page.locator('[title*="archive" i], [aria-label*="archive" i], a[href*="archive" i]'),
                page.get_by_text(re.compile(r"^\s*(?:puzzle\s+)?archive\s*$", re.I)),
                page.locator('button, a, [role="button"]').filter(
                    has=page.locator('svg title').filter(has_text=re.compile("archive", re.I))),
            ]
            dialog = page.locator('[role="dialog"]').filter(
                has=page.get_by_role("heading", name=re.compile("Puzzle Archive", re.I)))
            menu_candidates = [
                page.get_by_role("button", name=re.compile("menu|navigation", re.I)),
                page.locator('button[title*="menu" i], button[aria-haspopup="menu"], button[aria-controls*="menu" i]'),
                page.locator('button').filter(has=page.locator('svg.lucide-menu, svg[data-lucide="menu"]')),
            ]
            menu_opened = False
            for _ in range(30):
                await dismiss_startup_dialogs(page)
                if await dialog.count() and await (await dialog_surface(dialog.first)).is_visible():
                    break
                clicked = False
                for candidate in candidates:
                    for index in range(await candidate.count()):
                        control = candidate.nth(index)
                        if await control.is_visible():
                            await click_control(page, control)
                            clicked = True
                            break
                    if clicked:
                        break
                if clicked:
                    await dialog.first.get_by_role("heading", name=re.compile("Puzzle Archive", re.I)).wait_for(state="visible")
                    break
                if not menu_opened:
                    for candidate in menu_candidates:
                        for index in range(await candidate.count()):
                            control = candidate.nth(index)
                            if await control.is_visible():
                                await click_control(page, control)
                                menu_opened = True
                                break
                        if menu_opened:
                            break
                await page.wait_for_timeout(500)
            await dialog.first.get_by_role("heading", name=re.compile("Puzzle Archive", re.I)).wait_for(state="visible", timeout=10000)
            archive = dialog.first
            return len(await read_archive(archive))
        except Exception:
            diagnostics = ROOT / "artifacts" / "pydle-scraper"
            diagnostics.mkdir(parents=True, exist_ok=True)
            try:
                (diagnostics / "page.html").write_text(await page.content())
                (diagnostics / "page.txt").write_text(await page.locator("body").inner_text())
                await page.screenshot(path=str(diagnostics / "page.png"), full_page=True)
                print(f"Scraper failed at {page.url}; page title: {await page.title()}")
                print("Visible controls:", await page.locator('button, a, [role="button"]').evaluate_all(
                    "elements => elements.map(e => ({text: e.innerText, title: e.title, label: e.getAttribute('aria-label'), href: e.getAttribute('href')}))"))
            except Exception as diagnostic_error:
                print(f"Could not save all diagnostics: {diagnostic_error}")
            raise
        finally:
            await browser.close()



async def read_archive(archive, poll_interval=0.75):
    entries = archive.get_by_role("button").filter(has_text=re.compile(r"Pydle\s*#\s*\d+", re.I))
    await entries.first.wait_for(state="visible")
    labels = entries.get_by_text(re.compile(r"^\s*Pydle\s*#\s*\d+\s*$", re.I))
    # Read only archive entries, excluding the current game's header.
    # Accumulate IDs to support lists that discard offscreen rows.
    seen = set()
    previous = None
    stable = 0
    for _ in range(100):
        seen.update(archive_ids("\n".join(await labels.all_text_contents())))
        metrics = await archive.evaluate("""element => {
            const scrollable = [...element.querySelectorAll('*')].filter(e =>
                e.scrollHeight > e.clientHeight &&
                /auto|scroll/.test(getComputedStyle(e).overflowY));
            for (const e of scrollable) e.scrollTop += Math.max(1, e.clientHeight * .8);
            return scrollable.map(e => [e.scrollTop, e.scrollHeight, e.clientHeight]);
        }""")
        at_bottom = all(top + height >= full - 2 for top, full, height in metrics)
        current = (frozenset(seen), str(metrics))
        stable = stable + 1 if current == previous and at_bottom else 0
        if stable >= 3:
            return seen
        previous = current
        await asyncio.sleep(poll_interval)
    raise ValueError("Archive did not finish loading; README left unchanged.")

def progress_block(results, total, pending=False):
    counts = result_counts(results, total)
    completed = counts["Hard"] + counts["Easy only"]
    attempted = len(results)
    summary = f"**{completed} games completed**" if pending else f"**{completed} / {total} games completed** · **{completed / total * 100:.1f}%**"
    chart = "![Pydle pie chart](assets/pydle-progress.svg)"
    rows = ["| Game | Best saved score | Result |", "| --- | ---: | --- |"]
    for number, result in sorted(results.items()):
        score = result["best"] if result["best"] is not None else "—"
        status = result["status"]
        rows.append(f"| #{number} | {score} | {status} |")
    note = "\n\nArchive percentage and remaining incomplete games will appear after the first successful update." if pending else ""
    return (f"{START}\n{summary} · **{attempted} attempted**\n\n"
            f"**{counts['Hard']} hard** · **{counts['Easy only']} easy only** · "
            f"**{counts['Broken']} broken** · **{counts['Incomplete']} incomplete**\n\n{chart}{note}\n\n"
            + "\n".join(rows) + f"\n{END}")


def chart_svg(counts, pending=False):
    colors = {"Hard": "#3b82f6", "Easy only": "#22c55e", "Broken": "#eab308", "Incomplete": "#ef4444"}
    slices = [(name, value, colors[name]) for name, value in counts.items()]
    completed = counts["Hard"] + counts["Easy only"]
    total = sum(value for _, value, _ in slices)
    description = ', '.join(f'{name}: {value}' for name, value, _ in slices)
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="640" height="280" viewBox="0 0 640 280" role="img" aria-labelledby="title desc">',
             '<title id="title">My Pydle Plays</title>',
             f'<desc id="desc">{description}</desc>',
             '<rect width="640" height="280" rx="18" fill="#0f172a"/>',
             '<text x="280" y="60" font-family="sans-serif" font-size="24" fill="white">My Pydle Plays</text>']
    angle = -math.pi / 2
    for index, (name, value, color) in enumerate(slices):
        if value and total:
            end = angle + 2 * math.pi * value / total
            if value == total:
                parts.append(f'<circle cx="140" cy="140" r="100" fill="{color}"/>')
            else:
                x1, y1 = 140 + 100 * math.cos(angle), 140 + 100 * math.sin(angle)
                x2, y2 = 140 + 100 * math.cos(end), 140 + 100 * math.sin(end)
                parts.append(f'<path d="M 140 140 L {x1:.4f} {y1:.4f} A 100 100 0 {int(value / total > .5)} 1 {x2:.4f} {y2:.4f} Z" fill="{color}"/>')
            angle = end
        y = 100 + index * 30
        parts.append(f'<circle cx="290" cy="{y-5}" r="6" fill="{color}"/><text x="308" y="{y}" font-family="sans-serif" font-size="16" fill="white">{name}: {value}</text>')
    note = 'Archive sync pending' if pending else f'{completed / total * 100:.1f}% completed' if total else 'No games yet'
    parts.append(f'<text x="280" y="240" font-family="sans-serif" font-size="16" fill="#cbd5e1">{note}</text></svg>')
    return '\n'.join(parts) + '\n'


def update_readme(total):
    path = ROOT / "README.md"
    text = path.read_text()
    if text.count(START) != 1 or text.count(END) != 1 or text.index(START) >= text.index(END):
        raise ValueError("README needs one ordered pair of progress markers.")
    results = game_results(ROOT / "games")
    block = progress_block(results, total)
    chart = ROOT / "assets" / "pydle-progress.svg"
    chart.parent.mkdir(exist_ok=True)
    chart.write_text(chart_svg(result_counts(results, total)))
    before, rest = text.split(START)
    _, after = rest.split(END)
    path.write_text(before + block + after)
    print(block)


if __name__ == "__main__":
    update_readme(asyncio.run(fetch_archive()))
