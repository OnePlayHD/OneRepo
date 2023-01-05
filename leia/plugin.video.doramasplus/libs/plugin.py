# -*- coding: utf-8 -*-
"""
    Doramas
    Copyright (C) 2022 zoreu
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import routing
import six
from kodi_six import xbmc, xbmcaddon, xbmcvfs
from kodi_six.xbmcplugin import addDirectoryItem, endOfDirectory, setContent
from kodi_six.xbmcgui import Dialog, ListItem, WindowDialog, ControlImage, ControlLabel, NOTIFICATION_INFO, NOTIFICATION_WARNING, NOTIFICATION_ERROR
from libs import mydoramas

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
import base64


#https://www.mydoramas.com/

plugin = routing.Plugin()
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')
translate = xbmcvfs.translatePath if six.PY3 else xbmc.translatePath
profile = translate(addon.getAddonInfo('profile')) if six.PY3 else translate(addon.getAddonInfo('profile')).decode('utf-8')
home = translate(addon.getAddonInfo('path')) if six.PY3 else translate(addon.getAddonInfo('path')).decode('utf-8')
fanart_default = os.path.join(home, 'fanart.jpg')
dontate_qr = os.path.join(home, 'resources', 'pix', 'qrcode-pix.png')
search_icon = os.path.join(home, 'resources', 'images', 'search.png')
next_icon = os.path.join(home, 'resources', 'images', 'next.png')
donate_icon = os.path.join(home, 'resources', 'images', 'donate.png')

def detect_resolveurl():
    folder = 'special://home/addons/script.module.resolveurl'
    if not os.path.exists(translate(folder)):
        resolveurl = False
    else:
        resolveurl = True
    return resolveurl

           
def infoDialog(message, heading=addonname, iconimage='', time=3000, sound=False):
    if iconimage == '':
        iconimage = icon
    elif iconimage == 'INFO':
        iconimage = NOTIFICATION_INFO
    elif iconimage == 'WARNING':
        iconimage = NOTIFICATION_WARNING
    elif iconimage == 'ERROR':
        iconimage = NOTIFICATION_ERROR
    Dialog().notification(heading, message, iconimage, time, sound=sound)

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


def item(params,dest,folder=True):
    keys = quote(urlencode(params))
    name = params.get('name')
    iconimage = params.get('iconimage')
    fanart = params.get('fanart')
    description = params.get('description')
    if not name:
        name = 'Desconhecido'
    if not iconimage:
        iconimage = ''
    if not fanart:
        fanart = fanart_default
    if not description:
        description = ''
    try:
        name = name.encode("utf-8", "ignore")
    except:
        pass
    try:
        description = description.encode("utf-8", "ignore")
    except:
        pass    
    liz = ListItem(name)
    liz.setArt({'fanart': fanart, 'thumb': iconimage, 'icon': "DefaultFolder.png"})
    liz.setInfo(type="Video", infoLabels={"Title": name, 'mediatype': 'video', "Plot": description})
    if description:
        try:
            desc2 = base64.b32encode(description).decode('utf-8')
        except:
            desc2 = 'sem sinopse'
        context = "RunPlugin(%s)"%plugin.url_for(infomation, info=quote(desc2))
        liz.addContextMenuItems([("Sinopse", context)])
    addDirectoryItem(plugin.handle,plugin.url_for(dest, keys=keys),liz,folder)
    
@plugin.route('/')
def index():
    setContent(plugin.handle, 'videos')
    item(params={'name': 'Pesquisar Doramas', 'iconimage': search_icon},dest=pesquisar_doramas,folder=True)
    item(params={'name': 'Lista de Doramas', 'iconimage': icon},dest=pagination_doramas,folder=True)
    item(params={'name': 'Doação via PIX Qr Code', 'iconimage': donate_icon},dest=doacao,folder=True)
    #item(params={'name': 'Video teste'},dest=play,folder=True)
    endOfDirectory(plugin.handle)

@plugin.route('/doramas/<keys>')
def pagination_doramas(keys):
    setContent(plugin.handle, 'videos')
    decode = unquote(keys)
    url = parse_qs(decode).get('url')
    if url:
        url = url[0]
    lista_videos, next_url = mydoramas.index_page(url)
    if lista_videos:
        for name,category,img,href in lista_videos:
            original_name = name
            name_display = '%s (%s)'%(name,category)
            try:
                name_display = name_display.encode("utf-8", "ignore")
            except:
                pass
            try:
                original_name = original_name.encode("utf-8", "ignore")
            except:
                pass
            item(params={'name': name_display, 'original_name': original_name, 'iconimage': img, 'url': href},dest=show_seasons,folder=True)
    if next_url:
        page = next_url.split('page/')[1].split('/')[0]
        item(params={'name': 'Pagina '+str(page), 'iconimage': next_icon, 'url': next_url},dest=pagination_doramas,folder=True)
    endOfDirectory(plugin.handle)

@plugin.route('/seasons/<keys>')
def show_seasons(keys):
    setContent(plugin.handle, 'videos')
    decode = unquote(keys)
    url = parse_qs(decode).get('url')
    original_name = parse_qs(decode).get('original_name')
    iconimage = parse_qs(decode).get('iconimage')
    if url and original_name and iconimage:
        url = url[0]      
        original_name = original_name[0]
        try:
            original_name = original_name.encode("utf-8", "ignore")
        except:
            pass
        iconimage = iconimage[0]
        seasons, desc, movie_link = mydoramas.seasons(url)
        try:
            desc2 = base64.b32encode(desc.encode('utf-8')).decode('utf-8')
        except:
            desc2  = ''
        try:
            desc = desc.encode("utf-8", "ignore")
        except:
            pass
        if seasons:
            for season in seasons:
                name = 'Temporada 0%s'%str(season) if int(season) < 10 else 'Temporada %s'%str(season)
                try:
                    name = name.encode("utf-8", "ignore")
                except:
                    pass
                item(params={'name': name, 'original_name': original_name, 'iconimage': iconimage, 'url': url, 'description': desc, 'season': str(season), 'desc2': desc2},dest=show_episodes,folder=True)
            endOfDirectory(plugin.handle)
        elif movie_link and not seasons:
            params={'original_name': original_name, 'iconimage': iconimage, 'url': movie_link, 'description': desc}
            keys = quote(urlencode(params))
            show_options(keys)

@plugin.route('/episodes/<keys>')
def show_episodes(keys):
    setContent(plugin.handle, 'videos')
    decode = unquote(keys)
    url = parse_qs(decode).get('url')
    original_name = parse_qs(decode).get('original_name')
    iconimage = parse_qs(decode).get('iconimage')
    description = parse_qs(decode).get('desc2')
    s = parse_qs(decode).get('season')
    if url and original_name and iconimage and s:
        url = url[0]
        original_name = original_name[0]
        try:
            original_name = original_name.encode("utf-8", "ignore")
        except:
            pass
        iconimage = iconimage[0]
        description = description[0]
        try:
            description = base64.b32decode(description).decode('utf-8')
        except:
            description = ''
        try:
            desc2 = base64.b32encode(description.encode('utf-8')).decode('utf-8')
        except:
            desc2  = ''                  
        try:
            description = description.encode("utf-8", "ignore")
        except:
            pass
        s = s[0]
        episodes = mydoramas.episodes(url,s)
        if episodes:
            for episode, href in episodes:
                e = '0%s'%str(episode) if int(episode) < 10 else str(episode)
                name =  'Episódio %s'%str(e)
                try:
                    name = name.encode("utf-8", "ignore")
                except:
                    pass
                #original_name = f'{original_name} - {s}x{e}'
                item(params={'name': name, 'original_name': original_name, 'iconimage': iconimage, 'url': href, 'description': description, 'desc2': desc2},dest=show_options,folder=True)
            endOfDirectory(plugin.handle)

@plugin.route('/options/<keys>')
def show_options(keys):
    decode = unquote(keys)
    original_name = parse_qs(decode).get('original_name')[0]
    iconimage = parse_qs(decode).get('iconimage')[0]
    url = parse_qs(decode).get('url')[0]
    try:
        description = parse_qs(decode).get('desc2')[0]
    except:
        try:
            description = parse_qs(decode).get('description')[0]
        except:
            description = ''
    try:
        original_name = original_name.encode("utf-8", "ignore")
    except:
        pass
    try:
        description = base64.b32decode(description).decode('utf-8')
    except:
        description = ''    
    try:
        description = description.encode("utf-8", "ignore")
    except:
        pass
    options = mydoramas.links(url)
    if options:     
        for name, href in options:
            try:
                name = name.encode("utf-8", "ignore")
            except:
                pass
            try:
                href = href.encode("utf-8", "ignore")
            except:
                pass                       
            item(params={'name': name, 'original_name': original_name, 'iconimage': iconimage, 'url': href, 'description': description},dest=play,folder=False)
        endOfDirectory(plugin.handle)

@plugin.route('/play/<keys>')
def play(keys):
    decode = unquote(keys)
    original_name = parse_qs(decode).get('original_name')[0]
    iconimage = parse_qs(decode).get('iconimage')[0]
    url = mydoramas.find_link(parse_qs(decode).get('url')[0])
    try:
        description = parse_qs(decode).get('description')[0]
    except:
        decription = ''
    if detect_resolveurl() == False:
        try:
            import time
            xbmc.executebuiltin('InstallAddon(script.module.resolveurl)', wait=True)
            time.sleep(17)
        except:
            pass
    try:
        if url and not '.mp4' in url and not 'plugin://' in url:
            import resolveurl
            resolved = resolveurl.resolve(url)
        else:
            resolved = url
    except:
        resolved = False       
    if resolved:
        liz=ListItem(original_name, path=resolved)
        liz.setArt({'thumb': iconimage})
        liz.setInfo(type="Video", infoLabels={"Title": original_name, 'mediatype': 'video', "Plot": description})
        xbmc.Player().play(item=resolved, listitem=liz)
    else:
        infoDialog('Falha ao resolver url', iconimage='INFO')

@plugin.route('/sinopse/<info>')
def infomation(info):
    info = unquote(info)
    try:
        description = base64.b32decode(info).decode('utf-8')
    except:
        description = info     
    Dialog().textviewer('Sinopse', description)


@plugin.route('/search')
def pesquisar_doramas():
    pesquisa = search()
    if pesquisa:
        url = mydoramas.search_page + pesquisa
        keys = quote(urlencode({'url': url}))
        pagination_doramas(keys)


@plugin.route('/play/<keys>')
def play(keys):
    decode = unquote(keys)
    name = parse_qs(decode).get('name')[0]
    url = parse_qs(decode).get('url')[0]
    iconimage = parse_qs(decode).get('iconimage')[0]  
    liz=ListItem(name, path=url)
    liz.setArt({'thumb': iconimage})
    liz.setInfo(type="Video", infoLabels={"Title": name, 'mediatype': 'video', "Plot": ''})
    xbmc.Player().play(item=url, listitem=liz)

class Donate(WindowDialog):
    def __init__(self):
        self.image = ControlImage(440, 145, 400, 400, dontate_qr)
        self.text = ControlLabel(x=150,y=570,width=1100,height=25,label='[B]SE ESSE ADD-ON LHE AGRADA, FAÇA UMA DOAÇÃO VIA PIX ACIMA E MANTENHA ESSE SERVIÇO ATIVO[/B]',textColor='white')
        self.text2 = ControlLabel(x=495,y=600,width=1000,height=25,label='[B]PRESSIONE VOLTAR PARA SAIR[/B]',textColor='white')
        self.addControl(self.image)
        self.addControl(self.text)
        self.addControl(self.text2)

@plugin.route('/donate')
def doacao():
    Donate().doModal()
    
def run():
	plugin.run()