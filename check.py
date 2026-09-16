"""Prevent private archive pages and assets from entering the public website."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import os,re,sys,json
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'dist';BASE=os.environ.get('BASE_PATH','/the-operators').rstrip('/')
class Page(HTMLParser):
 def __init__(self,s):super().__init__();self.refs=[];self.ids=set();self.text=[];self.headings=[];self.inh3=False;self.feed(s)
 def handle_starttag(self,t,a):
  d=dict(a)
  if 'id' in d:self.ids.add(d['id'])
  if t=='h3':self.inh3=True
  for k in ['href','src']:
   if k in d:self.refs.append(d[k])
 def handle_endtag(self,t):
  if t=='h3':self.inh3=False
 def handle_data(self,d):
  self.text.append(d)
  if self.inh3:self.headings.append(d)
p=Page((OUT/'index.html').read_text());errors=[]
expected=['Career','Health','Finances','EA responsibilities','Your network','Travel']
if p.headings!=expected:errors.append('Service headings differ from the requested six')
for u in p.refs:
 x=urlsplit(u)
 if x.scheme=='mailto':continue
 if x.scheme or x.netloc:continue
 if not x.path:
  if x.fragment not in p.ids:errors.append('Broken anchor '+u)
 elif not x.path.startswith(BASE+'/assets/'):errors.append('Unexpected public subpage link '+u)
 elif not (OUT/unquote(x.path[len(BASE)+1:])).is_file():errors.append('Missing asset '+u)
words=' '.join(p.text)
for forbidden in ['Your life.','Your rules.','Let\'s make good things happen.','Family & home','Travel & experiences']:
 if forbidden in words:errors.append('Retired homepage copy '+forbidden)
if re.search(r'\bRyan\b',words):errors.append('Old visible name')
files=[str(f.relative_to(OUT)) for f in OUT.rglob('*') if f.is_file()]
allowed={'index.html','404.html','sitemap.xml','robots.txt','.nojekyll'}|{'assets/'+s for s in ['site.css','favicon.svg','operators-logo.png','durkin.png','graffiti.jpg','marker.ttf','FONT-LICENSE-Marker.txt']}
if set(files)!=allowed:errors.append('Public files differ from explicit allowlist: '+str(set(files)^allowed))
if (OUT/'sitemap.xml').read_text().count('<loc>')!=1:errors.append('Sitemap must contain only homepage')
print(json.dumps({'public_pages':1,'service_headings':p.headings,'public_files':len(files),'errors':errors},indent=2));sys.exit(bool(errors))
