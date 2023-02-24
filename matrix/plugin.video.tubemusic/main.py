# -*- coding: utf-8 -*-
import os
import re
import sys
import six
import random 
from kodi_six import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
try:
    from urllib.parse import urlparse, parse_qs, quote, unquote, quote_plus, unquote_plus, urlencode #python 3
except ImportError:    
    from urlparse import urlparse, parse_qs #python 2
    from urllib import quote, unquote, quote_plus, unquote_plus, urlencode
from bs4 import BeautifulSoup
try:
    from urllib.request import Request, urlopen, URLError  # Python 3
except ImportError:
    from urllib2 import Request, urlopen, URLError # Python 2
try:
    import json
except:
    import simplejson as json
import math
import time
import requests


plugin = sys.argv[0]
handle = int(sys.argv[1])
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')
translate = xbmcvfs.translatePath if six.PY3 else xbmc.translatePath
home = translate(addon.getAddonInfo('path')) if six.PY3 else translate(addon.getAddonInfo('path')).decode('utf-8')
dialog = xbmcgui.Dialog()
fanart_default = os.path.join(home, 'fanart.jpg')
temp_folder = os.path.join(home, 'temp_srt')
temp_srt = os.path.join(home, 'temp_srt', 'srt_temp.srt')
subtitle = addon.getSetting("subtitle")
lang_subtitle = addon.getSetting("lang_subtitle")
player_repeat = addon.getSetting("repeat")
playlisturl = addon.getSetting("playlisturl")


def infoDialog(message, heading=addonname, iconimage='', time=3000, sound=False):
    if iconimage == '':
        iconimage = icon
    elif iconimage == 'INFO':
        iconimage = xbmcgui.NOTIFICATION_INFO
    elif iconimage == 'WARNING':
        iconimage = xbmcgui.NOTIFICATION_WARNING
    elif iconimage == 'ERROR':
        iconimage = xbmcgui.NOTIFICATION_ERROR
    dialog.notification(heading, message, iconimage, time, sound=sound)

def browser(url):
    try:
        req = Request(url)
        if not 'youtube' in url:
            req.add_header('User-Agent', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36')
            req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
            req.add_header('Accept-Languaget', 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6')
        else:
            req.add_header('User-Agent', 'Mozilla/5.0')
            req.add_header('accept-language', 'en-US,en')
        response = urlopen(req)
        html = response.read()
        try:
            html = html.decode('utf-8')
        except:
            pass
    except:
        html = ''
    return html

def lasturl(url):
    try:
        req = Request(url)
        if not 'youtube' in url:
            req.add_header('User-Agent', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36')
            req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
            req.add_header('Accept-Languaget', 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6')
        else:
            req.add_header('User-Agent', 'Mozilla/5.0')
            req.add_header('accept-language', 'en-US,en')
        response = urlopen(req)
        final = response.geturl()
    except:
        final = url
    return final

def float_to_srt_time_format(d):
    """Convert decimal durations into proper srt format.

    :rtype: str
    :returns:
    SubRip Subtitle (str) formatted time duration.

    float_to_srt_time_format(3.89) -> '00:00:03,890'
    """
    fraction, whole = math.modf(d)
    time_fmt = time.strftime("%H:%M:%S,", time.gmtime(whole))
    ms = "%.3f"%fraction
    ms = ms.replace("0.", "")
    return str(time_fmt + ms)

def xmltosrt(url):
    data = browser(url)
    soup = BeautifulSoup(data, "html.parser")
    ps = soup.findAll('p')
    segments = []
    for i, p in enumerate(ps):
        text = p.text or ""
        caption = text
        start = float(p['t'])
        try:
            duration = float(p['d'])
        except KeyError:
            duration = 0.0
        end = start + duration
        start = start / 1000
        end = end / 1000        
        sequence_number = i + 1  # convert from 0-indexed to 1.
        line = "%s\n%s --> %s\n%s\n"%(sequence_number,float_to_srt_time_format(start),float_to_srt_time_format(end),caption)
        # line = "{seq}\n{start} --> {end}\n{text}\n".format(
        #     seq=sequence_number,
        #     start=float_to_srt_time_format(start),
        #     end=float_to_srt_time_format(end),
        #     text=caption,
        #     )
        segments.append(line)
    return "\n".join(segments).strip()

def get_icon(video_id):
    iconimage = "https://img.youtube.com/vi/%s/0.jpg"%video_id
    return iconimage

def get_fanart(video_id):
    fanart = "https://i.ytimg.com/vi/%s/hqdefault.jpg"%video_id
    return fanart

def get_info(video_id):
    iconimage = get_icon(video_id)
    try:
        url = '\x68\x74\x74\x70\x73\x3a\x2f\x2f\x77\x77\x77\x2e\x79\x6f\x75\x74\x75\x62\x65\x2e\x63\x6f\x6d\x2f\x79\x6f\x75\x74\x75\x62\x65\x69\x2f\x76\x31\x2f\x70\x6c\x61\x79\x65\x72\x3f\x76\x69\x64\x65\x6f\x49\x64\x3d\x25\x73\x26\x6b\x65\x79\x3d\x41\x49\x7a\x61\x53\x79\x41\x4f\x5f\x46\x4a\x32\x53\x6c\x71\x55\x38\x51\x34\x53\x54\x45\x48\x4c\x47\x43\x69\x6c\x77\x5f\x59\x39\x5f\x31\x31\x71\x63\x57\x38\x26\x63\x6f\x6e\x74\x65\x6e\x74\x43\x68\x65\x63\x6b\x4f\x6b\x3d\x54\x72\x75\x65\x26\x72\x61\x63\x79\x43\x68\x65\x63\x6b\x4f\x6b\x3d\x54\x72\x75\x65'%video_id
        body = {'context': {'client': {'clientName': 'ANDROID', 'clientVersion': '16.20'}}}
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        req.add_header('Content-Type', 'application/json')
        req.add_header('accept-language', 'en-US,en')
        jsondata = json.dumps(body)
        jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
        #req.add_header('Content-Length', len(jsondataasbytes))
        response = urlopen(req, jsondataasbytes)
        json_html = response.read()
        json_data = json.loads(json_html)
        video_720p = []
        video_480p = []
        video_360p = []
        video_240p = []
        video_144p = []
        videos = json_data.get("streamingData").get("formats")
        title = json_data.get("videoDetails").get("title")
        srt_data = []
        try:
            if int(lang_subtitle) == 1:
                lang = "pt-BR"
            else:
                lang = "en"
            caption = json_data.get("captions").get("playerCaptionsTracklistRenderer").get("captionTracks")
            for c in caption:
                if c.get("languageCode") == lang:
                    xml = c.get("baseUrl")
                    srt_data.append(xmltosrt(xml))
        except:
            pass
        try:
            try:
                if not xbmcvfs.exists(temp_folder):
                    os.mkdir(temp_folder)
            except:
                pass
            if srt_data:
                if subtitle == "true":
                    if six.PY2:
                        with open(temp_srt, 'w') as f:
                            try:
                                utf8 = srt_data[0].encode('utf-8')
                            except:
                                utf8 = srt_data[0]                         
                            f.write(utf8)
                    else:
                        with open(temp_srt, 'w', encoding='utf-8') as f:
                            f.write(srt_data[0])
                    srt_file = temp_srt
                else:
                    srt_file = ''
            else:
                srt_file = ''
        except:
            srt_file = ''
        
        for v in videos:
            if v.get('qualityLabel') == '720p':
                video_720p.append(v.get("url"))
            if v.get('qualityLabel') == '480p':
                video_480p.append(v.get("url"))                            
            if v.get('qualityLabel') == '360p':
                video_360p.append(v.get("url"))
            if v.get('qualityLabel') == '240p':
                video_240p.append(v.get("url"))
            if v.get('qualityLabel') == '144p':
                video_144p.append(v.get("url"))                                 
        if video_720p:
            stream = video_720p[0] + '|User-Agent=Mozilla/5.0'
        elif video_480p:
            stream = video_480p[0] + '|User-Agent=Mozilla/5.0'
        elif video_360p:
            stream = video_360p[0] + '|User-Agent=Mozilla/5.0'
        elif video_240p:
            stream = video_240p[0] + '|User-Agent=Mozilla/5.0'
        elif video_144p:
            stream = video_144p[0] + '|User-Agent=Mozilla/5.0'                                  
    except:
        stream = False
        title = 'unknow'
        srt_file = ''
    return stream,title,iconimage,srt_file


def get_url(params):
    url = '%s?%s'%(plugin, urlencode(params))
    return url

def item(name,url,iconimage,fanart):
    li=xbmcgui.ListItem(name)
    if not 'plugin://' in url:
        if 'AJUSTES' in name:
            url = get_url({"name": name, "action": "ajustes", "url": "", "iconimage": iconimage, "fanart": fanart})
        elif 'MINHA' in name:
            url = get_url({"name": name, "action": "openyoutube", "url": "", "iconimage": iconimage, "fanart": fanart})            
        else:
            url = get_url({"name": name, "action": "playlist", "url": url, "iconimage": iconimage, "fanart": fanart})
        folder = True
    else:
        li.setProperty('IsPlayable', 'true')
        folder = False
    if iconimage:
        li.setArt({"icon": "DefaultVideo.png", "thumb": iconimage})
    li.setInfo('video', { 'mediatype': 'video' })
    li.setInfo(type="Video", infoLabels={"Title": name, "Plot": ''})
    if fanart:
        li.setProperty('fanart_image', fanart)
    else:
        li.setProperty('fanart_image', fanart_default)
    xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=li, isFolder=folder)


def playvideo(video_id):
    try:
        os.remove(srt)
    except:
        pass    
    link,title,iconimage,srt = get_info(video_id)
    if link:
        li=xbmcgui.ListItem(title, path=link)
        li.setInfo(type="Video", infoLabels={"Title": title, "Plot": ''})
        li.setArt({"icon": "DefaultVideo.png", "thumb": iconimage})
        #xbmc.Player().play(item=link, listitem=listitem)
        if srt:
            if subtitle == "true":
                li.setSubtitles([srt])
        xbmcplugin.setResolvedUrl(handle=handle, succeeded=True, listitem=li)
    else:
        infoDialog("VIDEO NOT FOUND", iconimage="INFO")

def req_youtube(url):
    try:
        src = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}).json()
    except:
        src = {}
    return src 

def playlist_resolver(playlist_id):
    import scrapetube
    items = []
    try:
        videos = scrapetube.get_playlist(playlist_id)
        for v in videos:
            video_id = v.get('videoId')
            title = v.get('title')['runs'][0]['text']
            try:
                title = title.encode('utf-8', 'ignore')
            except:
                pass
            items.append((title,video_id))
    except:
        pass
    #return items
    # page = 0
    # videos_playlist = []
    # try:
    #     while True:
    #         page += 1
    #         if six.PY3:
    #             url = 'https://invidious.nerdvpn.de/api/v1/playlists/%s?page=%s'%(playlist_id,str(page))
    #         else:
    #             url = 'https://apiyt.joelsilva3.repl.co/api?url=https://invidious.nerdvpn.de/api/v1/playlists/%s?page=%s'%(playlist_id,str(page))
    #         req = req_youtube(url)
    #         total_videos = req['videoCount']
    #         videos = req['videos']
    #         for i in videos:
    #             title = i['title']
    #             video_id = i['videoId']
    #             if not video_id in str(videos_playlist):
    #                 videos_playlist.append((title,video_id))
    #         # print('pagina: ', page)
    #         # print('total atual: ', len(videos_playlist))
    #         if len(videos_playlist) == int(total_videos) - 1:
    #             break
    #         #limit while 15
    #         if page == 8:
    #             break
    # except:
    #     pass
    # return videos_playlist
    return items   


def genre_playlist():
    url = 'https://github.com/zoreu/plugin.video.tubemusic/raw/main/playlist'
    html = browser(url).replace('\n', '').replace('\r', '')
    source = re.findall(r'nam.+?=.+?"(.*?)".+?laylis.+?=.+?"(.*?)"', html)
    if source:
        for name, playlist in source:
            if six.PY2:
                try:
                    name = name.encode('utf-8', 'ignore')
                except:
                    pass            
            item(name,playlist,icon,"")
    else:
        infoDialog("GENRES NOT FOUND", iconimage="INFO")

def play_playlist(items):
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    for name,iconimage,url in items:
        li = xbmcgui.ListItem(name)
        li.setInfo('video', {'Title': name})
        li.setArt({"icon": "DefaultVideo.png", "thumb": iconimage})       
        playlist.add(url=url, listitem=li)
    xbmc.Player().play(playlist, windowed=False, startpos=-1)
    if player_repeat == 'true':
        xbmc.executebuiltin("PlayerControl(RepeatAll)")
    else:
        xbmc.executebuiltin("PlayerControl(RepeatOff)")


def open_playlist(url):
    if six.PY2:
        q = dialog.yesno(heading="Tube Music", line1='Mostrar playlist ou Tocar playlist?', nolabel='Tocar playlist', yeslabel='Mostrar playlist')
    else:
        q = dialog.yesno(heading="Tube Music", message='Mostrar playlist ou Tocar playlist?', nolabel='Tocar playlist', yeslabel='Mostrar playlist')    
    if q:
        open = True
    else:
        open = False         

    html = browser(url).replace('\n', '').replace('\r', '')
    source = re.findall(r'nam.+?=.+?"(.*?)".+?ideo_i.+?=.+?"(.*?)"', html)
    if source:
        playlist = []
        random.shuffle(source)
        total = len(source)
        if not open:
            dp = xbmcgui.DialogProgress()
            if six.PY3:
                dp.create('Abrindo playlist','Adicionando clipe...')
            else:
                dp.create('Abrindo playlist','Adicionando clipe...', '','')        
        for count, (name, video_id) in enumerate(source):
            percent = int(count/total * 100)
            try:
                name = name.encode('utf-8', 'ignore')
            except:
                pass            
            iconimage = get_icon(video_id)
            fanart = get_fanart(video_id)
            link = 'plugin://plugin.video.tubemusic/?video_id=%s'%video_id
            if open:
                item(name,link,iconimage,fanart)
            else:
                playlist.append((name,iconimage,link))
                # if six.PY3:
                #     dp.update(percent, name)
                # else:
                #     dp.update(percent, name,'', '')
                dp.update(percent)
        if open:
            xbmcplugin.endOfDirectory(handle)
        else:
            play_playlist(playlist)
    else:
        infoDialog("NO PLAYLIST", iconimage="INFO")

def open_playlist_youtube(playlist_id):
    if six.PY2:
        q = dialog.yesno(heading="Tube Music", line1='Mostrar playlist ou Tocar playlist?', nolabel='Tocar playlist', yeslabel='Mostrar playlist')
    else:
        q = dialog.yesno(heading="Tube Music", message='Mostrar playlist ou Tocar playlist?', nolabel='Tocar playlist', yeslabel='Mostrar playlist')    
    if q:
        open = True
    else:
        open = False         

    source = playlist_resolver(playlist_id)
    if source:
        playlist = []
        #random.shuffle(source)
        total = len(source)
        if not open:
            dp = xbmcgui.DialogProgress()
            if six.PY3:
                dp.create('Abrindo playlist','Adicionando clipe...')
            else:
                dp.create('Abrindo playlist','Adicionando clipe...', '','')        
        for count, (name, video_id) in enumerate(source):
            percent = int(count/total * 100)
            try:
                name = name.encode('utf-8', 'ignore')
            except:
                pass            
            iconimage = get_icon(video_id)
            fanart = get_fanart(video_id)
            link = 'plugin://plugin.video.tubemusic/?video_id=%s'%video_id
            if open:
                item(name,link,iconimage,fanart)
            else:
                playlist.append((name,iconimage,link))
                # if six.PY3:
                #     dp.update(percent, name)
                # else:
                #     dp.update(percent, name,'', '')
                dp.update(percent)
        if open:
            xbmcplugin.endOfDirectory(handle)
        else:
            play_playlist(playlist)
    else:
        infoDialog("NO PLAYLIST", iconimage="INFO")

def open_playlist_youtube2(playlist_id):
    dp = xbmcgui.DialogProgress()  
    if six.PY3:
        dp.create('Abrindo playlist','Resolvendo...')
    else:
        dp.create('Abrindo playlist','Resolvendo...', '','')      
    source = playlist_resolver(playlist_id)
    if source:
        playlist = []
        #random.shuffle(source)
        if six.PY3:
            dp.update(0, 'Adicionando clipe...')
        else:
            dp.update(0, 'Adicionando clipe...','', '')        
        total = len(source)     
        for count, (name, video_id) in enumerate(source):
            percent = int(count/total * 100)
            try:
                name = name.encode('utf-8', 'ignore')
            except:
                pass            
            iconimage = get_icon(video_id)
            fanart = get_fanart(video_id)
            link = 'plugin://plugin.video.tubemusic/?video_id=%s'%video_id
            playlist.append((name,iconimage,link))
            # if six.PY3:
            #     dp.update(percent, name)
            # else:
            #     dp.update(percent, name,'', '')
            dp.update(percent)
        play_playlist(playlist)
    else:
        infoDialog("NO PLAYLIST", iconimage="INFO")                  


def menu():
    item('MINHA PLAYLIST','',icon,'')
    genre_playlist()
    item('AJUSTES','',icon,'')
    xbmcplugin.endOfDirectory(handle)


def run():
    xbmcplugin.setContent(handle, 'videos')
    args = parse_qs(sys.argv[2][1:])
    action = args.get("action")
    name = args.get("name")
    url = args.get("url")
    iconimage = args.get("iconimage")
    fanart = args.get("fanart")
    description = args.get("description")
    video_id = args.get("video_id")
    playlist_id = args.get("playlist_id")
    if name:
        name = name[0]
    else:
        name = 'Unknow'
    if url:
        url = url[0]
    else:
        url = ''
    if iconimage:
        iconimage = iconimage[0]
    else:
        iconimage = ''
    if fanart:
        fanart = fanart[0]
    else:
        fanart = ''
    if description:
        description = description[0]
    else:
        description = ''

    if video_id:
        video_id = video_id[0]                        
        playvideo(video_id)
    elif playlist_id:
        playlist_id = playlist_id[0] 
        open_playlist_youtube2(playlist_id)
    elif action == None:
        menu()
    elif 'playlist' in action:
        open_playlist(url)
    elif 'openyoutube' in action:
        if playlisturl:
            if 'http' in playlisturl:
                last = lasturl(playlisturl)
                last = last.replace('m.youtube.com', 'youtube.com')
                try:
                    parsed = urlparse(last)
                    query = parsed.query
                    playlist_id = parse_qs(query)['list'][0]
                except:
                    playlist_id = ''
                if playlist_id:
                    open_playlist_youtube(playlist_id)
                else:
                    dialog.ok('Tube Music', 'Playlist invalida!')
            else:
                dialog.ok('Tube Music', 'Playlist invalida!')
        else:
            dialog.ok('Tube Music', 'Sem playlist nos ajustes!')
    elif 'ajustes':
        addon.openSettings()
if __name__ == "__main__":
    run()