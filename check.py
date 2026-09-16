"""Validate public routes, contact removal, and archive exclusion."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import os,re,sys,json
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'dist';BASE=os.environ.get('BASE_PATH','/the-operators').rstrip('/')
class Page(HTMLParser):
 def __init__(self,s):super().__init__();self.refs=[];self.ids=set();self.text=[];self.headings=[];self.inh3=False;self.inmain=False;self.main=[];self.feed(s)
 def handle_starttag(self,t,a):
  d=dict(a)
  if 'id' in d:self.ids.add(d['id'])
  if t=='h3':self.inh3=True
  if t=='main':self.inmain=True
  for k in ['href','src']:
   if k in d:self.refs.append(d[k])
 def handle_endtag(self,t):
  if t=='h3':self.inh3=False
  if t=='main':self.inmain=False
 def handle_data(self,d):
  self.text.append(d)
  if self.inh3:self.headings.append(d)
  if self.inmain:self.main.append(d)
pages={p:Page((OUT/p).read_text()) for p in ['index.html','learn-more/index.html']};errors=[]
expected=['Career','Network','EA','Health','Finances','Travel']
if pages['index.html'].headings!=expected:errors.append('Service order incorrect')
if ' '.join(pages['learn-more/index.html'].main).strip()!='Durkin is currently building other companies right now':errors.append('Learn More main text differs from requested exact text')
for name,p in pages.items():
 for u in p.refs:
  x=urlsplit(u)
  if x.scheme=='mailto':errors.append('Public email link remains')
  if x.scheme or x.netloc:continue
  if not x.path:
   if x.fragment not in p.ids:errors.append('Broken anchor '+u)
  elif x.path in [BASE+'/',BASE+'/learn-more/']:continue
  elif not x.path.startswith(BASE+'/assets/'):errors.append('Unexpected public link '+u)
  elif not (OUT/unquote(x.path[len(BASE)+1:])).is_file():errors.append('Missing asset '+u)
 words=' '.join(p.text)
 if re.search(r'\bRyan\b|Talk to Durkin|contact@|Your life\.|Your rules\.',words):errors.append('Retired name or contact text '+name)
files=[str(f.relative_to(OUT)) for f in OUT.rglob('*') if f.is_file()]
allowed={'index.html','learn-more/index.html','404.html','sitemap.xml','robots.txt','.nojekyll'}|{'assets/'+s for s in ['site.css','favicon.svg','operators-logo.png','durkin.png','graffiti.jpg','boston-graffiti-v2.png','marker.ttf','FONT-LICENSE-Marker.txt']}
if set(files)!=allowed:errors.append('Public files differ from allowlist: '+str(set(files)^allowed))
if (OUT/'sitemap.xml').read_text().count('<loc>')!=2:errors.append('Sitemap must contain only homepage and Learn More')
if 'boston-graffiti-v2.png' not in (OUT/'index.html').read_text():errors.append('Corrected mural is missing')
print(json.dumps({'public_pages':2,'service_headings':pages['index.html'].headings,'public_files':len(files),'errors':errors},indent=2));sys.exit(bool(errors))
