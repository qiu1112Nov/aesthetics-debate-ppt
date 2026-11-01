from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
from fontTools.ttLib import TTFont
from lxml import html
import json,math
r=Path(__file__).resolve().parent
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
srv=ThreadingHTTPServer(('127.0.0.1',8765),partial(Quiet,directory=str(r)));Thread(target=srv.serve_forever,daemon=True).start()
checks=[];errors=[];requests_failed=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);pg=b.new_page(viewport={'width':1920,'height':1184})
 pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('response',lambda e:requests_failed.append([e.status,e.url]) if e.status>=400 else None)
 pg.goto('http://127.0.0.1:8765');pg.evaluate('document.fonts.ready')
 assert pg.locator('.slide').count()==22
 for i in range(22):
  pg.evaluate('(i)=>window.preview.show(i)',i)
  a=pg.locator('.slide.active').evaluate('''s=>{const b=s.getBoundingClientRect();let text=[...s.querySelectorAll('*')].filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())&&e.getClientRects().length);return {id:s.id,minPx:Math.min(...text.map(e=>{let f=parseFloat(getComputedStyle(e).fontSize);if(e instanceof SVGGraphicsElement){let m=e.getScreenCTM();return f*Math.sqrt(m.a*m.a+m.b*m.b)}return f})),horizontal:text.filter(e=>!(e instanceof SVGElement)&&e.scrollWidth>e.clientWidth+3).map(e=>e.textContent),outside:text.filter(e=>{let r=e.getBoundingClientRect();return r.left<b.left-1||r.right>b.right+1||r.top<b.top-1||r.bottom>b.bottom+1}).map(e=>e.textContent),conclusionOverlaps:[...s.querySelectorAll('.content p,.content h2,.content figcaption,.content cite')].filter(e=>{let r=e.getBoundingClientRect(),t=s.querySelector('.takeaway').getBoundingClientRect();return r.bottom>t.top-3}).map(e=>e.textContent),images:[...s.querySelectorAll('img')].every(e=>e.complete&&e.naturalWidth>0)}}''')
  assert a['minPx']>=47.99,a
  assert not a['horizontal'] and not a['outside'] and not a['conclusionOverlaps'] and a['images'],a
  checks.append(a)
 pg.locator('#overview').click();assert pg.locator('#thumbs').evaluate('e=>e.open');pg.locator('.thumb-grid button').nth(13).click();assert pg.locator('#P14').is_visible()
 pg.locator('#jump').fill('22');pg.locator('#jump').press('Tab');assert pg.locator('#P22').is_visible();pg.keyboard.press('ArrowLeft');assert pg.locator('#P21').is_visible()
 # Every separate page must load with its ID and all resources.
 for i in range(1,23):
  pg.goto(f'http://127.0.0.1:8765/pages/P{i:02d}.html');pg.evaluate('document.fonts.ready');assert pg.locator('.slide').count()==1;assert pg.locator(f'#P{i:02d}').is_visible();assert pg.locator('img').evaluate_all('es=>es.every(e=>e.complete&&e.naturalWidth>0)')
 pg.goto('http://127.0.0.1:8765');pg.evaluate('document.fonts.ready');font_loaded=pg.evaluate("document.fonts.check('48px \"Preview Sans SC\"') && document.fonts.check('48px \"Preview Serif SC\"')");assert font_loaded
 pg.set_viewport_size({'width':390,'height':844});pg.evaluate('window.preview.show(0)');pg.wait_for_timeout(100);pg.screenshot(path=str(r/'mobile-preview-P01.png'))
 pg.set_viewport_size({'width':844,'height':390});pg.evaluate('window.preview.show(4)');pg.wait_for_timeout(100);pg.screenshot(path=str(r/'mobile-preview-P05-landscape.png'))
 # Offline local file entry without HTTP.
 local_file='Not tested: managed Chromium policy blocks file:// with net::ERR_BLOCKED_BY_ADMINISTRATOR. HTTP preview passed.'
 b.close()
srv.shutdown()
assert not errors and not requests_failed,(errors,requests_failed)
# Check bundled font subsets cover visible Chinese and punctuation.
tree=html.fromstring((r/'index.html').read_text());txt=''.join(tree.xpath('//section//text()'))
missing={}
for f in ['PreviewSansSC.woff','PreviewSerifSC.woff']:
 font=TTFont(r/'assets/fonts'/f);c=font.getBestCmap();missing[f]=sorted({ord(a) for a in txt if not a.isspace() and ord(a) not in c});assert not missing[f],missing
(r/'validation-final.json').write_text(json.dumps({'result':'PASS','pages':checks,'page_count':22,'single_page_entries':22,'minimum_projected_text_px':48,'planned_ppt_mapping':'13 1/3 × 7.5 inches; 48px = 24pt; PPTX object sizes not tested','fonts_loaded':font_loaded,'font_subset_missing_codepoints':missing,'desktop_navigation':'PASS: previous, jump, keyboard, thumbnail selection','local_file_entry':local_file,'mobile_viewports':'44 page/view combinations recorded in validation.json','js_errors':errors,'failed_http_resources':requests_failed,'limitations':['实体手机和投影待测','PPTX未制作','纸本引文及馆方元数据仍有待核项目']},ensure_ascii=False,indent=2))
print('PASS: 22 pages, 22 single-page entries, effective SVG text sizes, glyph coverage, image loads, text boundaries, navigation. Local file:// is blocked by managed browser policy; HTTP preview passed.')
