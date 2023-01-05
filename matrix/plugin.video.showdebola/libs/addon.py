# -*- coding: utf-8 -*-
import six
from kodi_six import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
from libs import api
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
dontate_qr = os.path.join(home, 'resources', 'pix', 'qrcode-pix.png')
search_icon = os.path.join(home, 'resources', 'images', 'search.jpg')
next_icon = os.path.join(home, 'resources', 'images', 'next.jpg')
donate_icon = os.path.join(home, 'resources', 'images', 'donate.jpg')
f4m = addon.getSetting("f4m")
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

def search():
    vq = get_search_string(heading='Digite a pesquisa', message="")        
    if ( not vq ): return False
    title = quote(vq).replace('%20', '+')
    return title

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
    item({'name': 'JOGOS RECENTES', 'action': 'aovivo', 'iconimage': icon},folder=True)
    item({'name': 'AJUSTES', 'action': 'ajustes', 'iconimage': icon},folder=True)
    item({'name': 'DOAÇÃO VIA PIX QR CODE', 'action': 'donate', 'iconimage': donate_icon},folder=True)
    #xbmcplugin.endOfDirectory(handle,cacheToDisc=False)
    xbmcplugin.endOfDirectory(handle)


def menu_aovivo():
    xbmcplugin.setContent(handle, 'videos')
    jogos = api.aovivo_agora()
    if jogos:
        for name, href in jogos:
            try:
                name = name.encode("utf-8", 'Ignore')
            except:
                pass
            try:
                href = href.encode('utf-8', 'ignore')
            except:
                pass            
            item({'name': name, 'url': href, 'action': 'play', 'iconimage': icon},folder=False)
        xbmcplugin.endOfDirectory(handle,cacheToDisc=False)
    else:
        infoDialog('Nenhum jogo disponivel...', heading=addonname, iconimage='INFO')
    

def play_video(name,url,iconimage):
    dp = xbmcgui.DialogProgress()
    if six.PY3:
        dp.create('Por favor aguarde','Resolvendo link')
    else:
        dp.create('Por favor aguarde','Resolvendo link' '','')     
    resolved = api.resolver(url)
    if resolved:
        f4mtester = translate('special://home/addons/plugin.video.f4mTester')     
        if f4m == 'true' and os.path.exists(f4mtester):
            plugin = 'plugin://plugin.video.f4mTester/?url='+quote(resolved)+'&streamtype=HLSRETRY&iconImage='+quote(iconimage)+'&name='+quote(name)
            xbmc.executebuiltin('RunPlugin(%s)'%plugin)
        else:
            liz=xbmcgui.ListItem(name, path=resolved)
            liz.setArt({'thumb': iconimage})
            liz.setInfo(type="Video", infoLabels={"Title": name, 'mediatype': 'video', "Plot": ''})           
            xbmc.Player().play(item=resolved, listitem=liz)
    else:
        infoDialog('Falha ao resolver url..', heading=addonname, iconimage='INFO')


class Donate(xbmcgui.WindowDialog):
    def __init__(self):
        self.image = xbmcgui.ControlImage(440, 145, 400, 400, dontate_qr)
        self.text = xbmcgui.ControlLabel(x=150,y=570,width=1100,height=25,label='[B]SE ESSE ADD-ON LHE AGRADA, FAÇA UMA DOAÇÃO VIA PIX ACIMA E MANTENHA ESSE SERVIÇO ATIVO[/B]',textColor='white')
        self.text2 = xbmcgui.ControlLabel(x=495,y=600,width=1000,height=25,label='[B]PRESSIONE VOLTAR PARA SAIR[/B]',textColor='white')
        self.addControl(self.image)
        self.addControl(self.text)
        self.addControl(self.text2)


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
    elif 'aovivo' in action:
        menu_aovivo()    
    elif 'play' in action:
        play_video(name,url,iconimage)
    elif 'ajustes' in action:
        addon.openSettings()
    elif 'donate' in action:
        dialog_donate = Donate()
        dialog_donate.doModal()