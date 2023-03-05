import sys
import six
import os
from kodi_six import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
if six.PY3:
    from urllib.parse import unquote, quote_plus, unquote_plus, urlencode #python 3
    from urllib.request import Request, urlopen, URLError  # Python 3
else:    
    from urllib import unquote, quote_plus, unquote_plus, urlencode
    from urllib2 import Request, urlopen, URLError # Python 2
import re
import time
import server
import threading
import requests

plugin = sys.argv[0]
handle = int(sys.argv[1])
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
addonid = addon.getAddonInfo('id')
icon = addon.getAddonInfo('icon')
translate = xbmcvfs.translatePath if six.PY3 else xbmc.translatePath
profile = translate(addon.getAddonInfo('profile')) if six.PY3 else translate(addon.getAddonInfo('profile')).decode('utf-8')
home = translate(addon.getAddonInfo('path')) if six.PY3 else translate(addon.getAddonInfo('path')).decode('utf-8')
fanart_default = os.path.join(home, 'fanart.png')
dialog = xbmcgui.Dialog()



def route(f):
    action_f = f.__name__
    params_dict = {}
    param_string = sys.argv[2]
    if param_string:
        split_commands = param_string[param_string.find('?') + 1:].split('&')
        for command in split_commands:
            if len(command) > 0:
                if "=" in command:
                    split_command = command.split('=')
                    key = split_command[0]
                    value = split_command[1]
                    try:
                        key = unquote_plus(key)
                    except:
                        pass
                    try:
                        value = unquote_plus(value)
                    except:
                        pass
                    params_dict[key] = value
                else:
                    params_dict[command] = ""
    action = params_dict.get('action')
    url = params_dict.get('url')
    if action is None and action_f == 'main':
        f()
    elif url and action is None and action_f == 'playitem':
        f(params_dict)
    elif action == action_f:
        f(params_dict)

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



def SetView(name):
    if name == 'Wall':
        try:
            xbmc.executebuiltin('Container.SetViewMode(500)')
        except:
            pass
    if name == 'List':
        try:
            xbmc.executebuiltin('Container.SetViewMode(50)')
        except:
            pass
    if name == 'Poster':
        try:
            xbmc.executebuiltin('Container.SetViewMode(51)')
        except:
            pass
    if name == 'Shift':
        try:
            xbmc.executebuiltin('Container.SetViewMode(53)')
        except:
            pass
    if name == 'InfoWall':
        try:
            xbmc.executebuiltin('Container.SetViewMode(54)')
        except:
            pass
    if name == 'WideList':
        try:
            xbmc.executebuiltin('Container.SetViewMode(55)')
        except:
            pass
    if name == 'Fanart':
        try:
            xbmc.executebuiltin('Container.SetViewMode(502)')
        except:
            pass

def get_kversion():
	full_version_info = xbmc.getInfoLabel('System.BuildVersion')
	baseversion = full_version_info.split(".")
	intbase = int(baseversion[0])
	# if intbase > 16.5:
	# 	log('HIGHER THAN 16.5')
	# if intbase < 16.5:
	# 	log('LOWER THAN 16.5')
	return intbase

def get_url(params):
    if params:
        url = '%s?%s'%(plugin, urlencode(params))
    else:
        url = ''
    return url


def item(params,folder=True):
    u = get_url(params)
    if not u:
        u = ''
    name = params.get("name")
    if name:
        name = name
    else:
        name = 'Unknow'
    iconimage = params.get("iconimage")
    if not iconimage:
        iconimage = params.get("iconImage", icon)
    fanart = params.get("fanart")
    if not fanart:
        fanart = fanart_default
    description = params.get("description")
    if not description:
        description = ''           
    playable = params.get("playable")
    liz = xbmcgui.ListItem(name)
    liz.setArt({'fanart': fanart, 'thumb': iconimage, 'icon': "DefaultFolder.png"})
    # if params.get("media"):
    if get_kversion() > 19:
        info = liz.getVideoInfoTag()
        info.setTitle(name)
        info.setMediaType('video')
        info.setPlot(description)
    else:    
        liz.setInfo(type="Video", infoLabels={"Title": name, 'mediatype': 'video', "Plot": description})
    # else:
    #     liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})                                                  
    if playable:
        if playable == 'true':
            liz.setProperty('IsPlayable', 'true')
    ok = xbmcplugin.addDirectoryItem(handle=handle, url=u, listitem=liz, isFolder=folder)
    return ok


class MyPlayer(xbmc.Player):
    def __init__ (self):
        xbmc.Player.__init__(self)
    def play(self, url, listitem):
        #print 'Now im playing... %s' % url
        xbmc.Player().play(url, listitem)        
    # def onPlayBackEnded(self):
    #     #Will be called when xbmc stops playing a file
    #     server.req_shutdown()
    # def onPlayBackStopped(self):
    #     # Will be called when user stops xbmc playing a file
    #     server.req_shutdown()

def monitor():
    while True:
        #if not xbmc.Player().isPlaying():
        #if xbmc.getCondVisibility("Player.HasMedia") == False:
            #server.mediaserver().stop()
        if not xbmc.Player().isPlaying():
            server.req_shutdown()
            break

def req(url):
    try:
        r = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'},timeout=10)
        return r.text
    except:
        src = ''
        return src
    
def re_me(data, re_patten):
    match = ''
    m = re.search(re_patten, data)
    if m != None:
        match = m.group(1)
    else:
        match = ''
    return     

@route
def playlist(param):
    url = param.get('url', '')
    infoDialog('CARREGANDO AGUARDE...', iconimage='INFO')
    data = req(url)
    if re.search("#EXTM3U",data) or re.search("#EXTINF",data):
        xbmcplugin.setContent(handle, 'videos')
        content = data.rstrip()
        match1 = re.compile(r'#EXTINF:.+?tvg-logo="(.*?)".+?group-title="(.*?)",(.*?)[\n\r]+([^\r\n]+)').findall(content)
        if match1:
            group_list = []
            for thumbnail,cat,channel_name,stream_url in match1:
                if not '.mp4' in stream_url and not '.mkv' in stream_url and not '.avi' in stream_url and not '.wmv' in stream_url and not '.mp3' in stream_url:
                    if not cat in group_list:
                        group_list.append(cat)
                        try:
                            cat = cat.encode('utf-8', 'ignore')
                        except:
                            pass
                        item({'name': cat, 'action': 'playlist2', 'url': url, 'iconimage': ''})
        elif not match1:
            match2 = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\r\n]+)').findall(content)
            group_list = []
            if match2:
                for other,channel_name,stream_url in match2:
                    if not '.mp4' in stream_url and not '.mkv' in stream_url and not '.avi' in stream_url and not '.wmv' in stream_url and not '.mp3' in stream_url:
                        if 'tvg-logo' in other:
                            thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
                            if thumbnail:
                                if not thumbnail.startswith('http'):
                                    thumbnail = ''
                            else:
                                thumbnail = ''
                        if 'group-title' in other:
                            cat = re_me(other,'group-title=[\'"](.*?)[\'"]')
                        else:
                            cat = ''
                        if cat:
                            if not cat in group_list:
                                group_list.append(cat)
                                try:
                                    cat = cat.encode('utf-8', 'ignore')
                                except:
                                    pass
                                item({'name': cat, 'action': 'playlist2', 'url': url, 'iconimage': ''})
                        else:
                            stream_url = stream_url.replace(' ', '').replace('\r', '').replace('\n', '')
                            item({'name': channel_name, 'action': 'playitem', 'url': stream_url, 'iconimage': thumbnail},folder=False)
            else:
                infoDialog('Playlist indisponivel', iconimage='INFO')
        xbmcplugin.endOfDirectory(handle)
                                      
@route
def playlist2(param):
    name = param.get('name', '')
    url = param.get('url', '')
    try:
        name = name.decode('utf-8')
    except:
        pass
    infoDialog('CARREGANDO AGUARDE...', iconimage='INFO')    
    data = req(url)
    if re.search("#EXTM3U",data) or re.search("#EXTINF",data):
        xbmcplugin.setContent(handle, 'videos')
        content = data.rstrip()
        match1 = re.compile(r'#EXTINF:.+?tvg-logo="(.*?)".+?group-title="(.*?)",(.*?)[\n\r]+([^\r\n]+)').findall(content)
        if match1:
            group_list = []
            for thumbnail,cat,channel_name,stream_url in match1:
                if not '.mp4' in stream_url and not '.mkv' in stream_url and not '.avi' in stream_url and not '.wmv' in stream_url and not '.mp3' in stream_url: 
                    if cat == name:
                        stream_url = stream_url.replace(' ', '').replace('\r', '').replace('\n', '')
                        item({'name': channel_name, 'action': 'playitem', 'url': stream_url, 'iconImage': thumbnail},folder=False)
        elif not match1:
            match2 = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\r\n]+)').findall(content)
            group_list = []
            if match2:
                for other,channel_name,stream_url in match2:
                    if not '.mp4' in stream_url and not '.mkv' in stream_url and not '.avi' in stream_url and not '.wmv' in stream_url and not '.mp3' in stream_url:
                        if 'tvg-logo' in other:
                            thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
                            if thumbnail:
                                if not thumbnail.startswith('http'):
                                    thumbnail = ''
                            else:
                                thumbnail = ''
                        if 'group-title' in other:
                            cat = re_me(other,'group-title=[\'"](.*?)[\'"]')
                        else:
                            cat = ''
                        if cat:
                            if cat == name:
                                stream_url = stream_url.replace(' ', '').replace('\r', '').replace('\n', '')
                                item({'name':channel_name,'mode': 'playitem', 'url': stream_url, 'iconImage': thumbnail},folder=False)                          
            else:
                infoDialog('Playlist indisponivel', iconimage='INFO')
        xbmcplugin.endOfDirectory(handle)                       

                            
@route
def main():    
    xbmcplugin.setContent(handle, 'movies')
    item({'name': 'MINHAS PLAYLISTS', 'action': 'myplaylists'})
    item({'name': 'ADICIONAR PLAYLIST', 'action': 'settings'})
    xbmcplugin.endOfDirectory(handle)
    SetView('WideList') 

@route
def myplaylists(param):
    listas_disponiveis = []
    for i in range(10):
        i = i + 1
        tag = 'lista' + str(i)
        if 'http' in addon.getSetting(tag):
            listas_disponiveis.append(addon.getSetting(tag))
    if listas_disponiveis:
        for n, i in enumerate(listas_disponiveis):
            n = n + 1
            name = 'LISTA ' + str(n)
            item({'name': name, 'action': 'playlist', 'url': i})
        xbmcplugin.endOfDirectory(handle)
        SetView('WideList')
    else:
        infoDialog('SEM PLAYLIST ADICIONADA', iconimage='INFO')  

@route
def settings(param):
    addon.openSettings()


@route
def playitem(param):
    xbmcplugin.endOfDirectory(handle, cacheToDisc=False)
    name = param.get('name', '')
    url = param.get('url','')
    iconimage = param.get('iconImage', '')
    if url:
        if 'plugin://' in url:
            xbmc.executebuiltin('RunPlugin(%s)'%url)
        else:
            url_to_play = server.prepare_url(url)
            infoDialog('ABRINDO PROXY...',iconimage='INFO')
            server.mediaserver().start()
            if not name:
                name = 'F4mTester'
            liz = xbmcgui.ListItem(name)
            liz.setPath(url_to_play)
            if iconimage:
                liz.setArt({"icon": iconimage, "thumb": iconimage})
            else:
                liz.setArt({"icon": icon, "thumb": icon})
            if get_kversion() > 19:
                info = liz.getVideoInfoTag()
                info.setTitle(name)
            else:                  
                liz.setInfo(type='video', infoLabels={'Title': name})
            liz.setMimeType("application/vnd.apple.mpegurl")
            liz.setContentLookup(False) 
            mplayer = MyPlayer()
            mplayer.play(url_to_play,liz)
            time.sleep(3)
            t2 = threading.Thread(target=monitor)
            t2.start()


