# -*- coding: utf-8 -*-
import six
from kodi_six import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
from libs import pornhub, redtube
from libs.redtube import RedtubeResolver
from libs.pornhub import PornhubResolver
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
search_icon = os.path.join(home, 'resources', 'images', 'search.png')
next_icon = os.path.join(home, 'resources', 'images', 'next.png')
donate_icon = os.path.join(home, 'resources', 'images', 'donate.png')
password = addon.getSetting("parental_pass")
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
    ok = xbmcplugin.addDirectoryItem(handle=handle, url=u, listitem=liz, isFolder=True)
    return ok

def menu():
    xbmcplugin.setContent(handle, 'videos')
    if not password:
        dialog.ok('Informação', 'ESSE ADDON É PROIBIDO PARA MENORES DE 18 ANOS!\nUSE SEM A PRESENÇA DE CRIANÇAS OU MENORES DE 18 ANOS')
        item({'name': 'INSIRA NOVA SENHA DE CONTROLE PARENTAL', 'action': 'settings', 'iconimage': icon},folder=True)
    else:
        item({'name': 'ENTRAR', 'action': 'server', 'iconimage': icon},folder=True)
    item({'name': 'DOAÇÃO VIA PIX QR CODE', 'action': 'donate', 'iconimage': donate_icon},folder=True)
    xbmcplugin.endOfDirectory(handle,cacheToDisc=False)

def servidores():
    xbmcplugin.setContent(handle, 'videos')
    p = dialog.input('Insira a senha:', option=xbmcgui.ALPHANUM_HIDE_INPUT)
    if p == password:
        item({'name': 'PORNHUB', 'action': 'pornhub', 'iconimage': icon},folder=True)
        item({'name': 'REDTUBE', 'action': 'redtube', 'iconimage': icon},folder=True)
        item({'name': 'TROCAR SENHA', 'action': 'settings', 'iconimage': icon},folder=True)
        xbmcplugin.endOfDirectory(handle)
    else:
        infoDialog('Senha invalida...', heading=addonname, iconimage='INFO')

def pornhub_menu():
    xbmcplugin.setContent(handle, 'videos')
    menu = pornhub.index()
    item({'name': 'Pesquisar', 'action': 'sch_pornhub', 'iconimage': search_icon},folder=True)
    if menu:        
        for name, url in menu:
            try:
                name = name.encode('utf-8', 'ignore')
            except:
                pass
            try:
                url = url.encode('utf-8', 'ignore')
            except:
                pass            
            item({'name': name, 'url': url, 'action': 'pag_pornhub', 'iconimage': icon},folder=True)
        item({'name': 'Categorias', 'action': 'cat_pornhub', 'iconimage': icon},folder=True)
        xbmcplugin.endOfDirectory(handle)

def redtube_menu():
    xbmcplugin.setContent(handle, 'videos')
    menu = redtube.index()
    item({'name': 'Pesquisar', 'action': 'sch_redtube', 'iconimage': search_icon},folder=True)
    if menu:        
        for name, url in menu:
            try:
                name = name.encode('utf-8', 'ignore')
            except:
                pass
            try:
                url = url.encode('utf-8', 'ignore')
            except:
                pass            
            item({'name': name, 'url': url, 'action': 'pag_redtube', 'iconimage': icon},folder=True)
        item({'name': 'Categorias', 'action': 'cat_redtube', 'iconimage': icon},folder=True)
        xbmcplugin.endOfDirectory(handle)
        

def pagination_pornhub(url):
    xbmcplugin.setContent(handle, 'videos')
    lista_menu, next = pornhub.index_page(url)
    if lista_menu:
        for name,img,href in lista_menu:
            try:
                name = name.encode('utf-8', 'ignore')
            except:
                pass
            try:
                href = href.encode('utf-8', 'ignore')
            except:
                pass
            try:
                img = img.encode('utf-8', 'ignore')
            except:
                pass          
            item({'name': name, 'url': href, 'action': 'play', 'iconimage': img},folder=False)
    if next:
        page = parse_qs(urlparse(next).query).get('page')[0]
        item({'name': 'PAGINA '+ str(page), 'url': next, 'action': 'pag_pornhub', 'iconimage': next_icon},folder=True)
    xbmcplugin.endOfDirectory(handle)

def pagination_redtube(url):
    xbmcplugin.setContent(handle, 'videos')
    lista_menu, next = redtube.index_page(url)
    if lista_menu:
        for name,img,href in lista_menu:
            try:
                name = name.encode('utf-8', 'ignore')
            except:
                pass
            try:
                href = href.encode('utf-8', 'ignore')
            except:
                pass
            try:
                img = img.encode('utf-8', 'ignore')
            except:
                pass          
            item({'name': name, 'url': href, 'action': 'play', 'iconimage': img},folder=False)
    if next:
        page = parse_qs(urlparse(next).query).get('page')[0]
        item({'name': 'PAGINA '+ str(page), 'url': next, 'action': 'pag_redtube', 'iconimage': next_icon},folder=True)
    xbmcplugin.endOfDirectory(handle)

def search_pornhub(sch):
    url = pornhub.search_page + sch
    return url

def search_redtube(sch):
    url = redtube.search_page + sch
    return url

def categorias_pornhub():
    lista_categorias = pornhub.categorias()
    if lista_categorias:
        for name, href, img in lista_categorias:
            try:
                name = name.encode('utf-8', 'ignore')
            except:
                pass
            try:
                href = href.encode('utf-8', 'ignore')
            except:
                pass
            try:
                img = img.encode('utf-8', 'ignore')
            except:
                pass
            item({'name': name, 'url': href, 'action': 'pag_pornhub', 'iconimage': img},folder=True)
        xbmcplugin.endOfDirectory(handle)

def categorias_redtube():
    lista_categorias = redtube.categorias()
    if lista_categorias:
        for name, href, img in lista_categorias:
            try:
                name = name.encode('utf-8', 'ignore')
            except:
                pass
            try:
                href = href.encode('utf-8', 'ignore')
            except:
                pass
            try:
                img = img.encode('utf-8', 'ignore')
            except:
                pass
            item({'name': name, 'url': href, 'action': 'pag_redtube', 'iconimage': img},folder=True)
        xbmcplugin.endOfDirectory(handle)        



def play_video(name,url,iconimage):
    if 'redtube' in url:
        resolved = RedtubeResolver.resolve(url)
    elif 'pornhub' in url:
        resolved = PornhubResolver.resolve(url)
    else:
        resolved = False   
    if resolved:
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
    elif 'settings' in action:
        addon.openSettings()
        if password and 'TROCAR' in name:
            infoDialog('Entre com a senha nova..', heading=addonname, iconimage='INFO')
    elif 'server' in action:
        servidores()
    elif 'pornhub' in action:
        pornhub_menu()
    elif 'redtube' in action:
        redtube_menu()        
    elif 'pag_pornhub' in action:
        pagination_pornhub(url)
    elif 'pag_redtube' in action:
        pagination_redtube(url)        
    elif 'sch_pornhub' in action:
        sch = search()
        if not sch == False and not sch == 'false':
            url = search_pornhub(sch)
            pagination_pornhub(url)
    elif 'sch_redtube' in action:
        sch = search()
        if not sch == False and not sch == 'false':
            url = search_redtube(sch)
            pagination_redtube(url)            
    elif 'cat_pornhub' in action:
        categorias_pornhub()
    elif 'cat_redtube' in action:
        categorias_redtube()       
    elif 'play' in action:
        play_video(name,url,iconimage)
    elif 'donate' in action:
        dialog_donate = Donate()
        dialog_donate.doModal()