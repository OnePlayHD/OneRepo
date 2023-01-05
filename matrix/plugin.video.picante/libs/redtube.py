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

homepage = 'https://www.redtube.com.br'
search_page = homepage + '/?search='

def index():
    lista_menu = [('Recomendados', homepage + '/recommended'), ('Mais Vistos', homepage + '/mostviewed'), ('Populares', homepage + '/hot?cc=br'), ('Mais Novos', homepage + '/newest')]
    return lista_menu

def index_page(url):
    html = request.get_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all("a", class_=re.compile("^video_link"))
    lista_pagina = []
    if a:
        for i in a:
            href = homepage + i.get("href") if i.get("href") else ''
            img = i.find("img").get("data-o_thumb") if i.find("img").get("data-o_thumb") else i.find("img").get("data-src")
            name = i.find("img").get("alt") if i.find("img").get("alt") else 'Nome desconhecido!'
            lista_pagina.append((name,img,href))
    try:
        next = soup.find("link", {"rel": "next"}).get('href')
        if next:
            next_url = next
        else:
            next_url = False
    except:
        next_url = False
    return lista_pagina, next_url

def categorias():
    url = homepage +'/categories'
    html = request.get_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.find("ul", {"id": "categories_list_block"})
    div_list = ul.find_all("div", class_=re.compile("^category_item_wrapper"))
    lista_categorias = []
    if div_list:
        for i in div_list:
            href = homepage + i.find("a").get("href") if i.find("a").get("href") else ''
            name = i.find("img").get("alt") if i.find("img").get("alt") else 'Nome desconhecido!'
            img = i.find("img").get("data-src") if i.find("img").get("data-src") else ''
            lista_categorias.append((name,href,img))
    return lista_categorias

class RedResolver:
    def resolve(self, url):
        html = request.get_url(url)
        referer = url
        url_parsed = urlparse(url)
        origin = '%s://%s'%(url_parsed.scheme,url_parsed.netloc)
        try:
            html = html.decode('utf-8')
        except:
            pass
        json_url = ''
        mediaurl = re.findall('mediaDefinition.+?"videoUrl":"(.*?)"', html)
        if mediaurl:
            json_url += '{"url": "%s"}'%mediaurl[0]
        if json_url:
            stream_ = json.loads(json_url)
            if stream_:
                url_json = stream_.get('url')
                m3u8_json = request.get_url(url_json)
                m3u8 = json.loads(m3u8_json)
                if m3u8:
                    q_1080p = []
                    q_720p = []
                    q_480p = []
                    q_360p = []
                    for i in m3u8:
                        link = i.get('videoUrl')
                        quality = i.get('quality')
                        if quality == '1080':
                            q_1080p.append(link)
                        elif quality == '720':
                            q_720p.append(link)
                        elif quality == '480':
                            q_480p.append(link)
                        elif quality == '240':
                            q_360p.append(link)
                    if q_1080p:
                        stream = q_1080p[0] + '|User-Agent=' + quote_plus(UA) + '&Origin=' + quote_plus(origin) + '&Referer=' + quote_plus(referer) 
                    elif q_720p:
                        stream = q_720p[0] + '|User-Agent=' + quote_plus(UA) + '&Origin=' + quote_plus(origin) + '&Referer=' + quote_plus(referer) 
                    elif q_480p:
                        stream = q_480p[0] + '|User-Agent=' + quote_plus(UA) + '&Origin=' + quote_plus(origin) + '&Referer=' + quote_plus(referer) 
                    elif q_360p:
                        stream = q_360p[0] + '|User-Agent=' + quote_plus(UA) + '&Origin=' + quote_plus(origin) + '&Referer=' + quote_plus(referer)
                    else:
                        stream = False
                else:
                    stream = False
            else:
                stream = False
        else:
            stream = False
        return stream
RedtubeResolver = RedResolver()