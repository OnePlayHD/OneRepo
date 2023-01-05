import sys
from kodi_six import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
PY3 = sys.version_info[0] == 3
if PY3:
    from urllib.parse import unquote, quote_plus, unquote_plus, urlencode #python 3
else:    
    from urllib import unquote, quote_plus, unquote_plus, urlencode
import os
from threading import Thread
import time
import requests
plugin = sys.argv[0]
handle = int(sys.argv[1])
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
addonid = addon.getAddonInfo('id')
icon = addon.getAddonInfo('icon')
translate = xbmcvfs.translatePath if PY3 else xbmc.translatePath
profile = translate(addon.getAddonInfo('profile')) if PY3 else translate(addon.getAddonInfo('profile')).decode('utf-8')
home = translate(addon.getAddonInfo('path')) if PY3 else translate(addon.getAddonInfo('path')).decode('utf-8')
fanart_default = os.path.join(home, 'fanart.jpg')
dialog = xbmcgui.Dialog()

radios = {'sertanejo': 'https://hls.hunter.fm/sertanejo/192.m3u8', 
    'pop': 'https://hls.hunter.fm/pop/192.m3u8', 
    'pagode': 'https://hls.hunter.fm/pagode/192.m3u8',
    'hitsbrasil': 'https://hls.hunter.fm/hitsbrasil/192.m3u8',
    'gospel': 'https://hls.hunter.fm/gospel/192.m3u8',
    'rock': 'https://hls.hunter.fm/rock/192.m3u8',
    'modasertaneja': 'https://hls.hunter.fm/modasertaneja/192.m3u8',
    'pisadinha': 'https://hls.hunter.fm/pisadinha/192.m3u8',
    'pop2k': 'https://hls.hunter.fm/pop2k/192.m3u8',
    'tropical': 'https://hls.hunter.fm/tropical/192.m3u8',
    'lofi': 'https://hls.hunter.fm/lofi/192.m3u8',
    '80s': 'https://hls.hunter.fm/80s/192.m3u8'}

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
    if action is None and action_f == 'radios_menu':
        f(params_dict)
    elif action == action_f:
        f(params_dict)


def image_radio(radio):
    icon = os.path.join(home, 'images','%s.jpg'%radio)
    return icon


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
        iconimage = icon
    fanart = params.get("fanart")
    if not fanart:
        fanart = fanart_default
    description = params.get("description")
    if not description:
        description = ''
    liz = xbmcgui.ListItem(name)
    liz.setArt({'fanart': fanart, 'thumb': iconimage, 'icon': "DefaultFolder.png"})
    liz.setInfo(type="music", infoLabels={"Title": name, "Plot": description})
    ok = xbmcplugin.addDirectoryItem(handle=handle, url=u, listitem=liz, isFolder=folder)
    return ok


def get_info(radio):
    radios = {'sertanejo': 'jld3aw2-d1a2s1d-sdwadsfawd', 'pop': 'jl2vwy6i-apswl5mr-onw1zw43kc', 'pagode': '3522-b9236sd665-94768sdh36', 'rock': 'jic321Sd-dawd1S27s-Se24s1daw2', 'gospel': '8763gs4-2312312-q421st52a', 'modasertaneja': '67sd22-fghd234-456ifgsa1hj', 'pisadinha': '21412q-634fsdda-56756dfsa', 'pop2k': 'jl339l70-23gg7tj7-hf6w8d3hg2', 'tropical': 'jld3aw2-2312312-qwfast85d', 'lofi': 'jic321Sd-de2s3d7s-S12e24s1daw2', '80s': 'ji%C3%A732234-22d21sd23-4sqq312dsas', 'hitsbrasil': 'ji%C3%A751234-22d21sd23-4121111dsas'}
    url = 'https://api.hunter.fm/station/%s/live'%(radios[radio])
    count = 0
    j = {}
    while True:
        count += 1
        try:
            j = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}).json()
            break
        except:
            pass
        if count > 7:
            break
    now = j.get('now')
    icon = ''
    title = ''
    artist = ''
    new_info = {}    
    if now:
        hashThumb = now.get('hashThumb')
        name = now.get('name')
        singers = now.get('singers')
        if name:
            title = name
        if singers:
            artist = ' feat. '.join(singers)
        if hashThumb:     
            icon = 'https://apihunter.zoreu.repl.co/img?url=https://cdn.hunter.fm/image/thumb/music/%s/300x300ht.jpg'%hashThumb
    new_info['title'] = title
    new_info['artist'] = artist
    new_info['icon'] = icon
    return new_info

def updateinfo():
    sleep = 5 * 1000
    while True:
        xbmc.sleep(sleep)
        if xbmc.Player().isPlaying():
            file = xbmc.Player().getPlayingFile()
            try:
                radio = file.split('/')[3]
                i = get_info(radio)
                info = {'artist': i['artist'],'title': i['title'],'genre': radio, 'userrating': 10}
                liz = xbmcgui.ListItem()
                liz.setPath(file)
                liz.setArt({'thumb': i['icon']})
                liz.setArt({'fanart': i['icon']})
                liz.setInfo('music', info)
                xbmc.Player().updateInfoTag(liz)                
            except:
                pass
        elif not xbmc.Player().isPlaying():          
            break

  
@route
def radios_menu(params):
    item(params={'name': 'Sertanejo', 'iconimage': image_radio('sertanejo'), 'action': 'play_radio', 'radio': 'sertanejo'},folder=False)
    item(params={'name': 'Pagode', 'iconimage': image_radio('pagode'), 'action': 'play_radio', 'radio': 'pagode'},folder=False)
    item(params={'name': 'Pop', 'iconimage': image_radio('pop'), 'action': 'play_radio', 'radio': 'pop'},folder=False)
    item(params={'name': 'Hits Brasil', 'iconimage': image_radio('hitsbrasil'), 'action': 'play_radio', 'radio': 'hitsbrasil'},folder=False)
    item(params={'name': 'Gospel', 'iconimage': image_radio('gospel'), 'action': 'play_radio', 'radio': 'gospel'},folder=False)
    item(params={'name': 'Rock', 'iconimage': image_radio('rock'), 'action': 'play_radio', 'radio': 'rock'},folder=False)
    item(params={'name': 'Moda Sertaneja', 'iconimage': image_radio('modasertaneja'), 'action': 'play_radio', 'radio': 'modasertaneja'},folder=False)
    item(params={'name': 'Pisadinha', 'iconimage': image_radio('pisadinha'), 'action': 'play_radio', 'radio': 'pisadinha'},folder=False)
    item(params={'name': 'Pop2k', 'iconimage': image_radio('pop2k'), 'action': 'play_radio', 'radio': 'pop2k'},folder=False)
    item(params={'name': 'Tropical', 'iconimage': image_radio('tropical'), 'action': 'play_radio', 'radio': 'tropical'},folder=False)
    item(params={'name': 'Lofi', 'iconimage': image_radio('lofi'), 'action': 'play_radio', 'radio': 'lofi'},folder=False)
    item(params={'name': '80s', 'iconimage': image_radio('80s'), 'action': 'play_radio', 'radio': '80s'},folder=False)
    xbmcplugin.endOfDirectory(handle)

@route
def play_radio(params):
    radio = params.get('radio')
    url = radios[radio]
    liz = xbmcgui.ListItem(radio)
    xbmc.Player().play(item=url, listitem=liz)
    t = Thread(target=updateinfo)
    t.start()