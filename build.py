#!/usr/bin/env python3
"""Build the one-page public website. Private archive content is never read."""
from pathlib import Path
import os,re,shutil,html,hashlib
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist'
BASE=os.environ.get('BASE_PATH','/the-operators').rstrip('/')
ORIGIN=os.environ.get('SITE_ORIGIN','https://massaicoalition.com').rstrip('/')
PUBLIC_ASSETS=('site.css','favicon.svg','operators-logo.png','durkin.png','graffiti.jpg','marker.ttf','condensed.ttf','FONT-LICENSE-Barlow.txt','FONT-LICENSE-Marker.txt')
if OUT.exists():shutil.rmtree(OUT)
(OUT/'assets').mkdir(parents=True)
for filename in PUBLIC_ASSETS:shutil.copy2(ROOT/'assets'/filename,OUT/'assets'/filename)
css=(OUT/'assets/site.css').read_text().replace("url('/assets/graffiti.jpg')","url(graffiti.jpg)")
(OUT/'assets/site.css').write_text(css)
page=(ROOT/'home.html').read_text()
page=re.sub(r'<script\b[^>]*>.*?</script>','',page,flags=re.S)
page=page.replace('viewbox=','viewBox=')
# Replacing hidden line breaks with spaces keeps the exact headline readable.
page=page.replace('The sports<br/>agency for<br/>','The sports agency for ')
page=page.replace('The sports<br>agency for<br>','The sports agency for ')
page=re.sub(r'<link\s+[^>]*rel="canonical"[^>]*/?>','<link rel="canonical" href="'+html.escape(ORIGIN+BASE+'/')+'">',page)
page=re.sub(r'(["\'])/assets/',lambda m:m[1]+BASE+'/assets/',page)
version=hashlib.sha256(css.encode()).hexdigest()[:10]
page=re.sub(r'site\.css\?[^"\']+', 'site.css?v='+version,page)
(OUT/'index.html').write_text(page)
(OUT/'.nojekyll').touch()
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+html.escape(ORIGIN+BASE+'/')+'</loc></url></urlset>')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+BASE+'/sitemap.xml\n')
# Do not block archived routes in robots: crawlers must be able to observe their 404 status.
(OUT/'404.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | The Operators</title><link rel="stylesheet" href="'''+BASE+'''/assets/site.css"></head><body><main class="page-hero" id="main"><p class="small">404 / Page not found</p><h1>This page is no longer available.</h1><a class="button" href="'''+BASE+'''/">The Operators ↗</a></main></body></html>''')
print('Built one public homepage, one 404 response page, and '+str(len(PUBLIC_ASSETS))+' allowed assets. No archive content is included.')
