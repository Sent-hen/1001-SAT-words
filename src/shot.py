import sys, asyncio, re, os, tempfile, pathlib
from playwright.async_api import async_playwright

async def launch(p):
    # bundled Chromium if installed, else the system Chrome / Edge
    for kw in ({}, {"channel": "chrome"}, {"channel": "msedge"}):
        try: return await p.chromium.launch(**kw)
        except Exception: pass
    raise SystemExit("no Chromium/Chrome/Edge found for Playwright")

async def main(src, out, w, h):
    txt=open(src, encoding="utf-8").read()
    txt=re.sub(r"<style>@import[^<]*</style>","",txt)
    txt=re.sub(r"@import url\([^)]*\);","",txt)
    tmp=os.path.join(tempfile.gettempdir(), "_shot"+os.path.splitext(src)[1])
    open(tmp,"w", encoding="utf-8").write(txt)
    async with async_playwright() as p:
        b = await launch(p)
        pg = await b.new_page(viewport={"width": w, "height": h})
        await pg.goto(pathlib.Path(tmp).as_uri()); await pg.wait_for_timeout(500)
        await pg.screenshot(path=out, full_page=src.endswith('.html'), timeout=60000); await b.close()
if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])))
