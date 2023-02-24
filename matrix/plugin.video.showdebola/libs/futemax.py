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
    from urllib.parse import urlparse, parse_qs, quote, quote_plus #python 3
except ImportError:    
    from urlparse import urlparse, parse_qs #python 2
    from urllib import quote, quote_plus
import random
try:
    from kodi_six import xbmcaddon
    proxy = xbmcaddon.Addon().getSetting("proxy")
except:
    proxy = 'false'

homepage = 'https://futemax.app'
search_page = 'https://futemax.app/buscar/'


def aovivo_agora():
    if proxy == 'true':
        fute_page = quote(homepage + '/')
        page = 'https://statistic.joelsilva3.repl.co/resolver?url=' + fute_page
    else:
        page = homepage + '/'
    html = request.get_url(page)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        home = soup.find("div", {"class": "widget-home"})
        itens_home = home.find_all("div", {"class": "item-wd"})
        status = True
    else:
        itens_home = []
        status = False
    jogos = []
    if itens_home:
        for i in itens_home:
            try:
                name = i.find("span", {"class": "title-item"}).text
                if not 'bbb' in name and not 'BBB' in name and not 'Fazenda' in name and not 'FAZENDA' in name and not 'Power Couple' in name:
                    try:
                        name = name.split("Assistir ")[1]
                    except:
                        pass
                    try:
                        name = name.split(" ao vivo")[0]
                    except:
                        pass
                    date = (i.find("div", {"class": "date"}).text).replace(" ", "").replace("\r", "").replace("\n", "")
                    name = name + " (" + date + ")"
                    href = i.find("a", {"rel": "bookmark"}).get("href")
                    jogos.append((name,href))
            except:
                pass
    return jogos, status


class Resolver:
    def resolve(self,url):
        url_parsed = urlparse(url)
        origin = '%s://%s'%(url_parsed.scheme,url_parsed.netloc)
        referer = url
        headers = {'User-Agent': UA,
        'Referer': origin + '/'}
        if proxy == 'true':
            fute_page = quote(url)
            url = 'https://statistic.joelsilva3.repl.co/resolver?url=' + fute_page      
        html = request.get_url(url, headers=headers)
        if html:      
            try:
                html = html.decode('utf-8')
            except:
                pass
            soup = BeautifulSoup(html, 'html.parser')
            div = soup.find("div", {"class": "options_iframe"})
            a = div.find_all("a")
            page = []
            for i in a:
                if 'thanksgod' in i.get("data-url"):
                    page.append(i.get("data-url"))
            if page:
                url_parsed2 = urlparse(page[0])
                origin2 = '%s://%s'%(url_parsed2.scheme,url_parsed2.netloc)
                referer2 = page[0]
                headers = {'User-Agent': UA,
                'Referer': referer}
                if proxy == 'true':
                    fute_page = quote(page[0])
                    url = 'https://statistic.joelsilva3.repl.co/resolver?url=' + fute_page
                else:
                    url = page[0]               
                html2 = request.get_url(url,headers=headers)
                if html2:
                    try:
                        html2 = html2.decode('utf-8')
                    except:
                        pass            
                    stream = re.findall(r'source:.+?"(.*?)",', html2)
                    if stream:
                        stream = random.choice(stream) + "|User-Agent=" + UA + "&Origin=" + origin2 + "&Referer=" + referer2
                    else:
                        stream = False
                else:
                    stream = False
            else:
                stream = False
        else:
            stream = False
        return stream

ResolverFute = Resolver()