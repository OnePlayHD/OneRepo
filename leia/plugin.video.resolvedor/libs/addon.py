# -*- coding: utf-8 -*-
import six
from kodi_six import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
try:
    from urllib.parse import urlparse, parse_qs, quote, unquote, quote_plus, unquote_plus, urlencode #python 3
except ImportError:    
    from urlparse import urlparse, parse_qs #python 2
    from urllib import quote, unquote, quote_plus, unquote_plus, urlencode
import sys
import os
import re
try:
    import json
except:
    import simplejson as json

plugin = sys.argv[0]
handle = int(sys.argv[1])

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')
translate = xbmcvfs.translatePath if six.PY3 else xbmc.translatePath
profile = translate(addon.getAddonInfo('profile')) if six.PY3 else translate(addon.getAddonInfo('profile')).decode('utf-8')
home = translate(addon.getAddonInfo('path')) if six.PY3 else translate(addon.getAddonInfo('path')).decode('utf-8')
fanart_default = os.path.join(home, 'fanart.jpg')
dialog = xbmcgui.Dialog()

def get_url(params):
    if params:
        url = '%s?%s'%(plugin, urlencode(params))
    else:
        url = ''
    return url

           
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

def to_unicode(text, encoding='utf-8', errors='strict'):
    """Force text to unicode"""
    if isinstance(text, bytes):
        return text.decode(encoding, errors=errors)
    return text

def get_search_string(heading='', message=''):
    """Ask the user for a search string"""
    search_string = None
    keyboard = xbmc.Keyboard(message, heading)
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_string = to_unicode(keyboard.getText())
    return search_string

def enter_url():
    vq = get_search_string(heading='Digite a url', message="")        
    if ( not vq ): return False
    return vq

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
    fanart = params.get("fanart")
    if not fanart:
        fanart = fanart_default
    description = params.get("description")
    if not description:
        description = ''
    playable = params.get("playable")
    liz = xbmcgui.ListItem(name)
    liz.setArt({'fanart': fanart, 'thumb': iconimage, 'icon': "DefaultFolder.png"})
    liz.setInfo(type="Video", infoLabels={"Title": name, 'mediatype': 'video', "Plot": description})
    if playable:
        if playable == 'true':
            liz.setProperty('IsPlayable', 'true')
    ok = xbmcplugin.addDirectoryItem(handle=handle, url=u, listitem=liz, isFolder=folder)
    return ok

def menu():
    xbmcplugin.setContent(handle, 'videos')
    item({'name': 'INSIRA URL DE TESTE', 'action': 'openurl', 'iconimage': icon},folder=True)
    xbmcplugin.endOfDirectory(handle)
 

def play_video(name,url,iconimage,playable=True):
    try:
        import resolveurl
        resolved = resolveurl.resolve(url)
    except:
        resolved = False
    if resolved:
        if playable:
            liz=xbmcgui.ListItem(path=resolved)
            liz.setArt({'thumb': iconimage})            
            liz.setInfo(type="Video", infoLabels={"Title": name, 'mediatype': 'video', "Plot": ''})
            xbmc.Player().play(item=resolved, listitem=liz)
        else:
            liz=xbmcgui.ListItem(path=resolved)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    else:
        infoDialog('Falha ao resolver url..', heading=addonname, iconimage='INFO')


def run():
    args = parse_qs(sys.argv[2][1:])
    action = args.get("action")
    name = args.get("name")
    url = args.get("url")
    iconimage = args.get("iconimage")
    fanart = args.get("fanart")
    description = args.get("description")
    playable = args.get("playable")
    search_ = args.get("search")
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
    if search_:
        search_ = search_[0]
    else:
        search_ = 'false'
    if action == None:
        menu()
    elif 'openurl' in action:
        link = enter_url()
        if link:
            infoDialog('Resolvendo..', heading=addonname, iconimage='INFO')
            play_video('Resolvedor',link,iconimage)
    elif 'play' in action:
        if url:
            infoDialog('Resolvendo..', heading=addonname, iconimage='INFO')
            play_video('Resolvedor',url,iconimage,playable=False)


