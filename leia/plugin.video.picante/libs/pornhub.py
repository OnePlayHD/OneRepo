try:
    from libs.browser import request, UA #kodi
except:
    from browser import request, UA # vscode
from bs4 import BeautifulSoup
import re
try:
    import json
except:
    import simplejson as json
try:
    from urllib.parse import urlparse, parse_qs, quote_plus #python 3
except ImportError:    
    from urlparse import urlparse, parse_qs #python 2
    from urllib import quote_plus


homepage = 'https://pt.pornhub.com'
search_page = homepage + '/video/search?search='

def index():
    html = request.get_url(homepage + '/')
    soup = BeautifulSoup(html, 'html.parser')
    a1 = soup.find("a", {"data-mixpanel-listing": "Videos Menu Sidebar Hottest"})
    a2 = soup.find("a", {"data-mixpanel-listing": "Videos Menu Sidebar Most Viewed"})
    a3 = soup.find("a", {"data-mixpanel-listing": "Videos Menu Sidebar Recommended"})
    a4 = soup.find("a", {"data-mixpanel-listing": "Videos Menu Sidebar Top Rated"})
    a5 = soup.find("a", {"data-mixpanel-listing": "Videos Menu Sidebar Popular Homemade"})
    lista_index = []
    mais_excitantes = ('Mais Excitantes', homepage + a1.get('href') if a1.get('href') else '')
    mais_vistos = ('Mais Vistos', homepage + a2.get('href') if a2.get('href') else '')
    recomendados = ('Recomendados', homepage + a3.get('href') if a3.get('href') else '')
    mais_votados = ('Mais Votados', homepage + a4.get('href') if a4.get('href') else '')
    caseiros_populares = ('Caseiros Populares', homepage + a5.get('href') if a5.get('href') else '')
    lista_index.append(recomendados)
    lista_index.append(mais_excitantes)
    lista_index.append(mais_vistos)
    lista_index.append(mais_votados)
    lista_index.append(caseiros_populares)
    return lista_index

def index_page(url):
    html = request.get_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all("div", {"class": "phimage"})
    lista_pagina = []
    if divs:
        for i in divs:
            href = homepage + i.find("a", class_=re.compile("^fade")).get('href')
            name = i.find("a", class_=re.compile("^fade")).get('title')
            img = i.find("img").get('data-image') if i.find("img").get('data-image') else i.find("img").get('data-mediumthumb') 
            lista_pagina.append((name,img,href))
    try:
        next = soup.find("li", {"class": "page_next"}).find("a").get('href')
        if next:
            next_url = homepage + next
        else:
            next_url = False
    except:
        next_url = False
    return lista_pagina, next_url

def categorias():
    url = homepage +'/categories'
    html = request.get_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.find("ul", {"class": "catHeaderSubMenu"})    
    a_list = ul.find_all("a", {"class": "js-mixpanel"})
    lista_categorias = []
    if a_list:
        for i in a_list:
            name = i.find("strong").string
            href = homepage + i.get('href') if i.get('href') else ''
            img = i.find("img").get('data-image') if i.find("img").get('data-image') else ''
            lista_categorias.append((name,href,img))
    return lista_categorias

class PornResolver:
    def sort_sources_list(self,sources):
        if len(sources) > 1:
            try:
                sources.sort(key=lambda x: int(re.sub(r"\D", "", x[0])), reverse=True)
            except:
                try:
                    sources.sort(key=lambda x: re.sub("[^a-zA-Z]", "", x[0].lower()))
                except:
                    pass
        return sources     
    def pick_source(self,sources):
        if len(sources) == 1:
            return sources[0][1]
        elif len(sources) > 1:
            return sources[0][1]
        else:
            return ''    
    def resolve(self,url):
        html = request.get_url(url)
        referer = url
        url_parsed = urlparse(url)
        origin = '%s://%s'%(url_parsed.scheme,url_parsed.netloc)
        try:
            html = html.decode('utf-8')
        except:
            pass
        sources = []
        qvars = re.search(r'qualityItems_[^\[]+([^;]+)', html)
        if qvars:
            sources = json.loads(qvars.group(1))
            sources = [(src.get('text'), src.get('url')) for src in sources if src.get('url')]
        if not sources:
            sections = re.findall(r'(var\sra[a-z0-9]+=.+?);flash', html)
            for section in sections:
                pvars = re.findall(r'var\s(ra[a-z0-9]+)=([^;]+)', section)
                link = re.findall(r'var\smedia_\d+=([^;]+)', section)[0]
                link = re.sub(r"/\*.+?\*/", '', link)
                for key, value in pvars:
                    link = re.sub(key, value, link)
                link = link.replace('"', '').split('+')
                link = [i.strip() for i in link]
                link = ''.join(link)
                if 'urlset' not in link:
                    r = re.findall(r'(\d+p)', link, re.I)
                    if r:
                        sources.append((r[0], link))
        if not sources:
            fvars = re.search(r'flashvars_\d+\s*=\s*(.+?);\s', html)
            if fvars:
                sources = json.loads(fvars.group(1)).get('mediaDefinitions')
                sources = [(src.get('quality'), src.get('videoUrl')) for src in sources if
                           type(src.get('quality')) is not list and src.get('videoUrl')]
        if sources:
            sorted_sources = self.sort_sources_list(sources)
            picked_source = self.pick_source(sorted_sources)
            stream = picked_source + '|User-Agent=' + quote_plus(UA) + '&Origin=' + quote_plus(origin) + '&Referer=' + quote_plus(referer) 
        else:
            stream = False
        return stream

PornhubResolver = PornResolver()