from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import json
r=Path(__file__).resolve().parent
if (r/'review-status.json').exists() and any(x.get('confirmed') for x in json.loads((r/'review-status.json').read_text())):
 raise SystemExit('存在已确认页：禁止批量覆盖截图；仅渲染用户授权页面，冻结目录不得写入。')
(r/'screenshots').mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
srv=ThreadingHTTPServer(('127.0.0.1',8765),partial(Quiet,directory=str(r)));Thread(target=srv.serve_forever,daemon=True).start()
results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1920,'height':1184},device_scale_factor=1);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8765/');page.evaluate('document.fonts.ready');page.wait_for_timeout(250)
 for n in range(1,23):
  id=f'P{n:02d}';page.evaluate('(n)=>window.preview.show(n)',n-1);page.wait_for_timeout(100)
  sl=page.locator('#'+id)
  checks=sl.evaluate('''s=>{const bounds=s.getBoundingClientRect();const els=[...s.querySelectorAll('*')].filter(e=>e.getClientRects().length&&e.textContent.trim()&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));return {text:els.map(e=>{const r=e.getBoundingClientRect();const f=parseFloat(getComputedStyle(e).fontSize);return {tag:e.tagName,text:e.textContent.trim(),size:f,x:r.left-bounds.left,y:r.top-bounds.top,w:r.width,h:r.height,overflow:e.scrollWidth>e.clientWidth+3||e.scrollHeight>e.clientHeight+3}}),images:[...s.querySelectorAll('img')].map(e=>({src:e.getAttribute('src'),loaded:e.complete&&e.naturalWidth>0,width:e.naturalWidth,height:e.naturalHeight})),outside:[...s.querySelectorAll('p,h1,h2,figcaption,blockquote')].filter(e=>{let a=e.getBoundingClientRect();return a.left<bounds.left-1||a.right>bounds.right+1||a.bottom>bounds.bottom+1}).map(e=>e.textContent)}}''')
  checks.update(page=id,min_text_px=min(x['size'] for x in checks['text']));results.append(checks);sl.screenshot(path=str(r/'screenshots'/f'{id}.png'))
  print(id,'min',checks['min_text_px'],'overflow',[(x['text'][:26],round(x['y']),round(x['h'])) for x in checks['text'] if x['overflow']],'outside',checks['outside'],flush=True)
 # Desktop navigation and mobile browser checks.
 page.locator('#jump').fill('22');page.locator('#jump').press('Tab');assert page.locator('#P22').is_visible();page.locator('#prev').click();assert page.locator('#P21').is_visible()
 mobile=[]
 for w,h in [(390,844),(844,390)]:
  page.set_viewport_size({'width':w,'height':h});page.wait_for_timeout(100)
  for n in range(22):
   page.evaluate('(n)=>window.preview.show(n)',n)
   a=page.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth,stage:document.querySelector(".slide.active").getBoundingClientRect().toJSON()})')
   mobile.append({'page':n+1,'viewport':[w,h],**a});assert a['scroll']<=w and a['stage']['width']<=w+1
 b.close()
srv.shutdown();(r/'validation.json').write_text(json.dumps({'canvas':[1920,1080],'planned_slide_inches':[13.3333333333,7.5],'px_to_pt':.5,'pages':results,'mobile':mobile,'js_errors':errors,'status':'technical checks only; all pages pending user review','font_metric_note':'text[].overflow includes scrollHeight font metrics; it is a diagnostic, not proof of visible clipping. Final geometry checks are in validation-final.json.'},ensure_ascii=False,indent=2))
for start,end in [(1,6),(7,12),(13,18),(19,22)]:
 sheet=Image.new('RGB',(960,540*(end-start+1)),'#F3F0E8')
 for j,n in enumerate(range(start,end+1)):
  im=Image.open(r/'screenshots'/f'P{n:02d}.png');im.thumbnail((960,540));sheet.paste(im,(0,j*540))
 sheet.save(r/f'overview-P{start:02d}-P{end:02d}.jpg',quality=92)
# Compact inspection sheets, not replacements for full-resolution review files.
for start,end in [(1,6),(7,12),(13,18),(19,22)]:
 sheet=Image.new('RGB',(1536,432*((end-start)//2+1)),'#F3F0E8')
 for j,n in enumerate(range(start,end+1)):
  im=Image.open(r/'screenshots'/f'P{n:02d}.png');im.thumbnail((768,432));sheet.paste(im,((j%2)*768,(j//2)*432))
 sheet.save(f'/tmp/inspect-{start}.jpg',quality=85)
