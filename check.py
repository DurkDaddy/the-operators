"""Validate public routes, contact removal, and archive exclusion."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import os,re,sys,json
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'dist';BASE=os.environ.get('BASE_PATH','').rstrip('/')
class Page(HTMLParser):
 def __init__(self,s):super().__init__();self.refs=[];self.ids=set();self.text=[];self.headings=[];self.inh3=False;self.inmain=False;self.main=[];self.meta={};self.meta_keys=[];self.canonical='';self.feed(s)
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='meta':
   key=d.get('property') or d.get('name','')
   if key.startswith(('og:','twitter:')):self.meta[key]=d.get('content','');self.meta_keys.append(key)
  if t=='link' and d.get('rel')=='canonical':self.canonical=d.get('href','')
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
if ' '.join(pages['learn-more/index.html'].main).strip()!='Durkin is currently building the Mass AI Coalition right now and is putting 100% of his focus into that.':errors.append('Learn More main text differs from requested exact text')
for name,p in pages.items():
 required={'og:type':'website','og:site_name':'The Operators','og:locale':'en_US',
           'og:url':p.canonical,'og:image:type':'image/jpeg','og:image:width':'1200',
           'og:image:height':'630','twitter:card':'summary_large_image'}
 for key,value in required.items():
  if p.meta.get(key)!=value:errors.append('Incorrect sharing metadata '+key+' on '+name)
 for key in ['og:title','og:description','og:image','og:image:secure_url','og:image:alt','twitter:title','twitter:description','twitter:image','twitter:image:alt']:
  if not p.meta.get(key):errors.append('Missing sharing metadata '+key+' on '+name)
 if len(p.meta_keys)!=len(set(p.meta_keys)):errors.append('Duplicate sharing metadata on '+name)
 for og,twitter in [('title','title'),('description','description'),('image','image'),('image:alt','image:alt')]:
  if p.meta.get('og:'+og)!=p.meta.get('twitter:'+twitter):errors.append('Social previews disagree on '+og+' on '+name)
 image=urlsplit(p.meta.get('og:image',''))
 if image.scheme!='https' or image.netloc!=urlsplit(p.canonical).netloc:errors.append('Share image must use canonical HTTPS host on '+name)
 if p.meta.get('og:image:secure_url')!=p.meta.get('og:image'):errors.append('Share image secure URL differs on '+name)
 if image.path!=BASE+'/assets/operators-social-20260925.jpg':errors.append('Incorrect share image path on '+name)
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
allowed={'index.html','learn-more/index.html','404.html','sitemap.xml','robots.txt','.nojekyll'}|{'assets/'+s for s in ['site.css','favicon.svg','operators-logo.png','durkin.png','graffiti.jpg','atlas-nyc-graffiti.png','operators-social-20260925.jpg','marker.ttf','FONT-LICENSE-Marker.txt','knewave.ttf','FONT-LICENSE-Knewave.txt']}
if set(files)!=allowed:errors.append('Public files differ from allowlist: '+str(set(files)^allowed))
if (OUT/'sitemap.xml').read_text().count('<loc>')!=2:errors.append('Sitemap must contain only homepage and Learn More')
if 'atlas-nyc-graffiti.png' not in (OUT/'index.html').read_text():errors.append('Agent and talent mural is missing')
if not BASE:
 for name in ['index.html','learn-more/index.html','sitemap.xml','robots.txt']:
  if re.search(r'https?://(?:www\.)?(?:massaicoalition|massaialliance)\.com', (OUT/name).read_text()):errors.append('Standalone site links to Coalition hosting in '+name)
print(json.dumps({'public_pages':2,'service_headings':pages['index.html'].headings,'public_files':len(files),'errors':errors},indent=2));sys.exit(bool(errors))
