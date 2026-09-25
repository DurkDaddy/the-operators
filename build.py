#!/usr/bin/env python3
"""Build the public homepage and Learn More page. Private archive content is never read."""
from pathlib import Path
from html.parser import HTMLParser
import os,re,shutil,html,hashlib
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist'
BASE=os.environ.get('BASE_PATH','').rstrip('/')
ORIGIN=os.environ.get('SITE_ORIGIN','https://www.theoperators.co').rstrip('/')
SOCIAL_IMAGE='operators-social-20260925.jpg'
SOCIAL_ALT='The Operators: Agent and manager to 100x AI talent, beside a vibrant Atlas graffiti mural.'
PUBLIC_ASSETS=('site.css','favicon.svg','operators-logo.png','durkin.png','graffiti.jpg','atlas-nyc-graffiti.png',SOCIAL_IMAGE,'marker.ttf','FONT-LICENSE-Marker.txt','knewave.ttf','FONT-LICENSE-Knewave.txt')

class PageMetadata(HTMLParser):
    def __init__(self, page):
        super().__init__()
        self.title='';self.description='';self.in_title=False
        self.feed(page)
    def handle_starttag(self, tag, attrs):
        values=dict(attrs)
        if tag=='title':self.in_title=True
        if tag=='meta' and values.get('name')=='description':self.description=values.get('content','')
    def handle_endtag(self, tag):
        if tag=='title':self.in_title=False
    def handle_data(self, data):
        if self.in_title:self.title+=data

def social_metadata(page, url):
    metadata=PageMetadata(page)
    image=ORIGIN+BASE+'/assets/'+SOCIAL_IMAGE
    og={'type':'website','site_name':'The Operators','locale':'en_US',
        'title':metadata.title,'description':metadata.description,'url':url,
        'image':image,'image:secure_url':image,'image:type':'image/jpeg',
        'image:width':'1200','image:height':'630','image:alt':SOCIAL_ALT}
    twitter={'card':'summary_large_image','title':metadata.title,
             'description':metadata.description,'image':image,'image:alt':SOCIAL_ALT}
    tags=[f'<meta property="og:{key}" content="{html.escape(value,quote=True)}">' for key,value in og.items()]
    tags += [f'<meta name="twitter:{key}" content="{html.escape(value,quote=True)}">' for key,value in twitter.items()]
    return '\n'.join(tags)

if OUT.exists():shutil.rmtree(OUT)
(OUT/'assets').mkdir(parents=True)
for filename in PUBLIC_ASSETS:shutil.copy2(ROOT/'assets'/filename,OUT/'assets'/filename)
css=(OUT/'assets/site.css').read_text().replace("url('/assets/graffiti.jpg')","url(graffiti.jpg)").replace("url('/assets/boston-graffiti-v2.png')","url(boston-graffiti-v2.png)")
css=re.sub(r"url\((['\"]?)/assets/",r"url(\1",css)
(OUT/'assets/site.css').write_text(css)
version=hashlib.sha256(css.encode()).hexdigest()[:10]
for source,path in [('home.html','/'),('learn-more.html','/learn-more/')]:
    page=(ROOT/source).read_text()
    page=re.sub(r'<script\b[^>]*>.*?</script>','',page,flags=re.S)
    page=page.replace('viewbox=','viewBox=')
    page=re.sub(r'<link\s+[^>]*rel="canonical"[^>]*/?>','<link rel="canonical" href="'+html.escape(ORIGIN+BASE+path)+'">',page)
    page=page.replace('href="/"','href="'+BASE+'/"').replace('href="/learn-more/"','href="'+BASE+'/learn-more/"')
    page=re.sub(r'(["\'])/assets/',lambda m:m[1]+BASE+'/assets/',page)
    page=re.sub(r'site\.css\?[^"\']+', 'site.css?v='+version,page)
    page=page.replace('</head>','\n'+social_metadata(page,ORIGIN+BASE+path)+'\n</head>')
    dest=OUT/path.lstrip('/')/'index.html'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(page)
(OUT/'.nojekyll').touch()
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+html.escape(ORIGIN+BASE+'/')+'</loc></url><url><loc>'+html.escape(ORIGIN+BASE+'/learn-more/')+'</loc></url></urlset>')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+BASE+'/sitemap.xml\n')
# Do not block archived routes in robots: crawlers must be able to observe their 404 status.
(OUT/'404.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | The Operators</title><link rel="stylesheet" href="'''+BASE+'''/assets/site.css"></head><body><main class="page-hero" id="main"><p class="small">404 / Page not found</p><h1>This page is no longer available.</h1><a class="button" href="'''+BASE+'''/">The Operators ↗</a></main></body></html>''')
print('Built homepage, Learn More, one 404 response page, and '+str(len(PUBLIC_ASSETS))+' allowed assets. No archive content is included.')
