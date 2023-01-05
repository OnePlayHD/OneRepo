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

homepage = 'https://www.mydoramas.com'
search_page = homepage + '/?s='

def index_page(url=None):
    if not url:
        url = homepage + '/'
    html = request.get_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    div_videos = soup.find("div", {"id": "videos"})
    divs_box_videos = soup.find_all("div", {"class": "boxvideo"})
    lista_videos = []
    if divs_box_videos:
        for i in divs_box_videos:
            img = i.find("img").get("src") if i.find("img").get("src") else ''
            name = i.find("a", {"class": "titulo"}).text if i.find("a", {"class": "titulo"}) else i.find("a", {"class": "thumb"}).get("title")
            href = i.find("a", {"class": "titulo"}).get("href") if i.find("a", {"class": "titulo"}).get("href") else i.find("a", {"class": "thumb"}).get("href")
            category = i.find("span", {"class": "qualidade"}).text
            lista_videos.append((name,category,img,href))
    try:
        next = soup.find("a", {"rel": "next"}).get("href")
        if next:
            next_url = next
        else:
            next_url = False
    except:
        next_url = False
    return lista_videos, next_url

def seasons(url):
    html = request.get_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    sinopse = soup.find("div", {"class": "sinopsee"})
    if sinopse:
        desc = sinopse.text
    else:
        desc = ''
    temps = soup.find_all("div", class_=lambda x: x and x.endswith('view'))
    if not temps:
        movie_link = False
        #movie_link = re.findall('<a data-href="(.*?)">',html,re.IGNORECASE|re.MULTILINE|re.DOTALL)
        try:
            movie_link = re.findall('<a data-href="(.*?)">',html.decode('utf-8'))[0]
        except:
            pass

        # li = soup.find_all("li")
        # for i in li:
        #     print(i)
        #     break
        # eps = soup.find("div", {"class": "eps"})
        # if eps:
        #     movie = eps.find("a").get("data-href")
        #     if movie:
        #         movie_link = movie
        #     else:
        #         movie_link = False
        # else:
        #     movie_link = False
    else:
        movie_link = False
    seasons = []
    if temps:
        count_season = 0
        for temp in temps:
            count_season += 1
            seasons.append(count_season)
    return seasons, desc, movie_link


def episodes(url,season):
    html = request.get_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    temps = soup.find_all("div", class_=lambda x: x and x.endswith('view'))
    episodes = []
    if temps:
        count_season = 0
        for temp in temps:
            count_season += 1
            if int(season) == count_season:
                eps = temp.find_all("a")
                count_ep = 0
                for ep in eps:
                    count_ep += 1
                    href = ep.get("data-href")
                    #name = ep.text
                    episodes.append((count_ep,href))
    return episodes


def decode_url(url):
    if '.php' in url:
        try:
            video_id = parse_qs(urlparse(url).query)['id'][0]
        except:
            video_id = ''           
        if 'fembed' in url and video_id:
            url = 'https://fembed.com/v/' + video_id
        elif 'upstream' in url and video_id:
            url = 'https://upstream.to/' + video_id
        elif 'streamtape' in url and video_id:
            url = 'https://streamtape.com/e/' + video_id
    else:
        try:
            upstream = parse_qs(urlparse(url).query)['upstream'][0]
        except:
            upstream = ''
        try:
            fembed = parse_qs(urlparse(url).query)['fembed'][0]
        except:
            fembed = ''
        if fembed:
            url = 'https://fembed.com/v/' + fembed
        elif upstream:
            url = 'https://upstream.to/' + upstream
    return url

def resolve_filmes(url):
    #https://warezstream.net/movie/tt0395140
    api = 'https://warezstream.net/api'
    if 'warezstream.net/movie/' in url:
        html = request.get_url(url)
        soup = BeautifulSoup(html, 'html.parser')
        try:
            video_id = soup.find("div", {"class": "player_select_item"}).get("data-id")
        except:
            video_id = ''
        if video_id:
            json_ = request.get_url(api,post={'action': 'getPlayer', 'video_id': video_id})
            try:
                url = json.loads(json_)['data']['video_url']
                url = url + '|Referer=' + quote_plus(url) + '&User-Agent=' + quote_plus(UA)
            except:
                pass
    return url

def find_link(url):
    if '/player/' in url:
        url = decode_url(url)
    elif 'mydoramas' in url:
        html = request.get_url(url)
        soup = BeautifulSoup(html, 'html.parser')
        url = soup.find("iframe").get("src") if soup.find("iframe").get("src") else False
        if url:
            if 'nyiabak.com' in url:
                url = url.replace("nyiabak.com", "fembed.com")
    return url

def links(url):
    if not 'http' in url:
        url = homepage + url
    if not 'warezstream' in url and not 'youtube' and not '/player/' in url:
        html = request.get_url(url)
        soup = BeautifulSoup(html, 'html.parser')
        itens = soup.find("div", {"class": "itens"})
        a = itens.find_all("a")
    else:
        a = []
    options = []
    if a:
        count = 0
        for i in a:
            count += 1
            number = '0%s'%str(count) if count < 10 else str(count)
            href = 'https:' + i.get("data-href") if not 'http' in i.get("data-href") else i.get("data-href")
            if 'upstream' in href:
                name = 'SERVIDOR UPSTREAM'
            elif 'fembed' in href:
                name = 'SERVIDOR FEMBED (MAIS ESTABILIDADE)'
            elif 'vidlox' in href:
                name = 'SERVIDOR VIDLOX'
            elif 'streamtape' in href:
                name = 'SERVIDOR STREAMTAPE'
            else:
                name = 'SERVIDOR %s'%number
            href = decode_url(href)
            options.append((name,href))
    else:
        if 'warezstream' in url:
            name = 'SERVIDOR ALTERNATIVO'
            href = resolve_filmes(url)
            options.append((name,href))
        elif 'www.youtube-nocookie.com/embed/' in url:
            name = 'VIDEO NO YOUTUBE'
            try:
                video_id = url.split('/embed/')[1]
                try:
                    video_id = video_id.split("&")[0]
                except:
                    pass
            except:
                video_id = ''
            if video_id:                
                href = 'plugin://plugin.video.tubemusic/?video_id=' + video_id
                options.append((name,href))
        elif 'youtube.com' in url:
            name = 'VIDEO NO YOUTUBE'
            try:
                video_id = parse_qs(urlparse(url).query)['v'][0]
            except:
                video_id = ''
            if video_id:
                href = 'plugin://plugin.video.tubemusic/?video_id=' + video_id
                options.append((name,href))
        elif '/player/' in url:
            href = find_link(url)
            if 'fembed' in href:
                name = 'SERVIDOR FEMBED (MAIS ESTABILIDADE)'
            elif 'upstream' in href:
                name = 'SERVIDOR UPSTREAM'
            else:
                name = 'SERVIDOR ALTERNATIVO'
            options.append((name,href))
    return options



#seasons('https://www.mydoramas.com/assistir-my-little-bride-online-gratis/')
#print(resolve_filmes(url='https://warezstream.net/movie/tt0395140'))
# url = find_link(url='https://www.mydoramas.com/player/?&upstream=921kw8jr8ahu&fembed=11kkwuj1zyp8egm')
# print(url)
#print(links(url))