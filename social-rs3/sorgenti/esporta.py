from playwright.sync_api import sync_playwright
import os
out="../grafiche"; os.makedirs(out,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    pg=b.new_page(viewport={"width":1200,"height":2000})
    pg.goto("file://"+os.path.abspath("creatives.html")); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(800)
    print("fonts:",pg.evaluate("document.fonts.check('40px Anton')"))
    for el in pg.query_selector_all(".c"):
        i=el.get_attribute("id"); el.screenshot(path=f"{out}/{i}.png"); print(i)
    b.close()
