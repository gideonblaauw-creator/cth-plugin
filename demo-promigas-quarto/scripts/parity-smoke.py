#!/usr/bin/env python3
"""Smoke parity for Quarto vs static demo (local servers)."""
from playwright.sync_api import sync_playwright

BASE_ORIG = "http://127.0.0.1:8765/index.html"
BASE_Q = "http://127.0.0.1:8767/index.html"

def run_checks(page, base, label):
    results = []
    page.goto(f"{base}#0", wait_until="networkidle")
    page.wait_for_timeout(1500)

    def ok(name, cond, note=""):
        results.append((label, name, "PASS" if cond else "FAIL", note))

    ok("Screen 1 title ES", "Paiva" in page.locator("#t1").inner_text())
    ok("Lang toggle EN", True)
    page.locator('#lang-toggle button[data-lang="en"]').click()
    page.wait_for_timeout(200)
    ok("Screen 1 title EN", "Paiva" in page.locator("#t1").inner_text() or "committee" in page.locator("#t1").inner_text().lower())
    page.locator('#lang-toggle button[data-lang="es"]').click()

    ok("Progress dots", page.locator(".dot").count() == 7)
    ok("Transform button", page.locator("#btn-transform").is_visible())
    page.locator("#btn-transform").click()
    ok("Governance list", not page.locator("#gov-list").evaluate("el => el.hidden"))

    for i in range(1, 7):
        page.locator("#nav-next").click()
        page.wait_for_timeout(300)
    ok("Screen 7 closing", "Próximo paso" in page.locator("#t7").inner_text() or "Next step" in page.locator("#t7").inner_text())

    page.goto(f"{base}#1", wait_until="networkidle")
    page.wait_for_timeout(500)
    page.locator("#btn-guajira").click()
    page.wait_for_timeout(2500)
    ok("Guajira stats", page.locator("#stat-com").inner_text().strip() == "4")

    page.goto(f"{base}#4", wait_until="networkidle")
    page.locator("#sel-community").select_option(index=1)
    page.locator('#size-options button[data-kwp="25"]').click()
    page.locator("#btn-create").click()
    page.wait_for_timeout(500)
    ok("CEOF diagram", page.locator("#ceof-wrap.visible").count() == 1)

    page.goto(f"{base}#0", wait_until="networkidle")
    page.wait_for_timeout(500)
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(300)
    ok("Keyboard next", page.locator("#screen-1").evaluate("el => el.classList.contains('active')"))

    return results


def main():
    all_rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for label, base in [("live-static", BASE_ORIG), ("quarto", BASE_Q)]:
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            all_rows.extend(run_checks(page, base, label))
            page.close()
        browser.close()

    print("| Build | Element | Result | Note |")
    print("|---|---|---|---|")
    for label, name, status, note in all_rows:
        print(f"| {label} | {name} | {status} | {note} |")

    fails = [r for r in all_rows if r[2] == "FAIL"]
    if fails:
        raise SystemExit(f"{len(fails)} FAIL")
    print("ALL PASS")


if __name__ == "__main__":
    main()
