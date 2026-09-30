import sys, asyncio, re, os
from playwright.async_api import async_playwright
async def main(src, out, w, h):
    txt=open(src).read()
    txt=re.sub(r"<style>@import[^<]*</style>","",txt)
    tmp="/tmp/_shot"+os.path.splitext(src)[1]
    open(tmp,"w").write(txt)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": w, "height": h})
        await pg.goto("file://" + tmp); await pg.wait_for_timeout(500)
        await pg.screenshot(path=out, full_page=src.endswith('.html'), timeout=60000); await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])))
