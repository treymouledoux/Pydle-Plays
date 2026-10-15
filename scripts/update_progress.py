"""Read Pydle's rendered archive and update the README progress block."""

import asyncio
import math
import os
from pathlib import Path
import re
from urllib.parse import quote

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


async def fetch_archive():
    from playwright.async_api import async_playwright

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()
        try:
            archive_url = os.getenv("PYDLE_ARCHIVE_URL") or "https://pydle.net"
            await page.goto(archive_url, wait_until="networkidle")
            # The archive may be a dialog in the game rather than a separate URL.
            control = page.get_by_role("link", name=re.compile("archive", re.I))
            if not await control.count():
                control = page.get_by_role("button", name=re.compile("archive", re.I))
            if not await control.count():
                control = page.get_by_text(re.compile(r"^\s*archive\s*$", re.I))
            if await control.count():
                await control.first.click()
            elif archive_url.rstrip("/") == "https://pydle.net":
                raise ValueError("Archive control not found; set PYDLE_ARCHIVE_URL to the archive URL.")
            await page.wait_for_function("() => /#\\s*\\d+/.test(document.body.innerText)")
            # Some archives load more entries as their container scrolls.
            previous = None
            stable = 0
            for _ in range(100):
                text = await page.locator("body").inner_text()
                current = archive_ids(text)
                stable = stable + 1 if current == previous else 0
                if stable >= 3:
                    return current
                previous = current
                await page.evaluate("""() => {
                    for (const element of [document.scrollingElement, ...document.querySelectorAll('*')]) {
                        if (element && element.scrollHeight > element.clientHeight)
                            element.scrollTop = element.scrollHeight;
                    }
                }""")
                await page.wait_for_timeout(750)
            raise ValueError("Archive did not finish loading; README left unchanged.")
        finally:
            await browser.close()


def progress_block(completed, available, broken=frozenset()):
    count = len(completed & available)
    broken_count = len((broken - completed) & available)
    total = len(available)
    unattempted = total - count - broken_count
    percent = count / total * 100
    filled = round(percent / 5)
    badge = quote(f"{count}/{total} ({percent:.1f}%)", safe="")
    return f"""{START}
![Pydle progress](https://img.shields.io/badge/Pydle-{badge}-8b5cf6?style=for-the-badge)

`{'█' * filled}{'░' * (20 - filled)}` **{percent:.1f}%**

**{count} / {total} games completed** · **{count + broken_count} attempted** · **{broken_count} broken**

![Pydle pie chart](assets/pydle-progress.svg)
{END}"""


def chart_svg(completed, broken, unattempted, pending=False):
    slices = [("Completed", completed, "#8b5cf6"),
              ("Broken attempts", broken, "#f59e0b")]
    if not pending:
        slices.append(("Unattempted", unattempted, "#475569"))
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
        y = 110 + index * 34
        parts.append(f'<circle cx="290" cy="{y-5}" r="6" fill="{color}"/><text x="308" y="{y}" font-family="sans-serif" font-size="16" fill="white">{name}: {value}</text>')
    note = 'Archive sync pending' if pending else f'{completed / total * 100:.1f}% completed' if total else 'No games yet'
    parts.append(f'<text x="280" y="240" font-family="sans-serif" font-size="16" fill="#cbd5e1">{note}</text></svg>')
    return '\n'.join(parts) + '\n'


def update_readme(available):
    path = ROOT / "README.md"
    text = path.read_text()
    if text.count(START) != 1 or text.count(END) != 1 or text.index(START) >= text.index(END):
        raise ValueError("README needs one ordered pair of progress markers.")
    completed, broken = attempt_ids(ROOT / "games")
    block = progress_block(completed, available, broken)
    count = len(completed & available)
    broken_count = len(broken & available)
    chart = ROOT / "assets" / "pydle-progress.svg"
    chart.parent.mkdir(exist_ok=True)
    chart.write_text(chart_svg(count, broken_count, len(available) - count - broken_count))
    before, rest = text.split(START)
    _, after = rest.split(END)
    path.write_text(before + block + after)
    print(block)


if __name__ == "__main__":
    update_readme(asyncio.run(fetch_archive()))
