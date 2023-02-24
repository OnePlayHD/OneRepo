# -*- coding: utf-8 -*-
import six
import os
from kodi_six import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
from scrapy import listar_apks
import ntpath
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')
translate = xbmcvfs.translatePath if six.PY3 else xbmc.translatePath
folder_downloads = '/storage/emulated/0/download'

def platform():
    from kodi_six import xbmc

    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux') or xbmc.getCondVisibility('system.platform.linux.Raspberrypi'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios') or xbmc.getCondVisibility('system.platform.darwin'):
        return 'ios'


def infoDialog(message, heading=addonname, iconimage='', time=3000, sound=False):
    if iconimage == '':
        iconimage = icon
    elif iconimage == 'INFO':
        iconimage = xbmcgui.NOTIFICATION_INFO
    elif iconimage == 'WARNING':
        iconimage = xbmcgui.NOTIFICATION_WARNING
    elif iconimage == 'ERROR':
        iconimage = xbmcgui.NOTIFICATION_ERROR
    xbmcgui.Dialog().notification(heading, message, iconimage, time, sound=sound)


def download_apk(url,dest):       
    try:
        import downloader
        filename = ntpath.basename(url)
        dp = xbmcgui.DialogProgress()
        if six.PY3:
            dp.create('Baixando '+filename+'...','Por favor espere...')
        else:
            dp.create('Baixando '+filename+'...','Por favor espere...', '', '')
        downloader.download(url,filename,dest,dp=dp)
        infoDialog('Download completo', iconimage='INFO')
    except:
        infoDialog('Erro ao baixar apk', iconimage='WARNING')

def installAPK(FMANAGER,apkfile):
    xbmc.executebuiltin('StartAndroidActivity(%s,,,"content://%s")'%(FMANAGER,apkfile))


def selectapks(items):
    op = xbmcgui.Dialog().select('SELECIONE UM APK ABAIXO', items)
    return op

def build_itens():
    from scrapy import listar_apks
    itens = listar_apks()
    namelist = []
    urllist = []
    if itens:
        for name, url in itens:
            namelist.append(name)
            urllist.append(url)
        select = selectapks(namelist)
        try:
            if select >=0:
                return urllist[select]
        except:
            pass
    return False

def baixar_apk():
    if platform() == 'android':
        url = build_itens()
        if url:
            if url.endswith('.apk'):
                name = ntpath.basename(url)
                if not xbmcvfs.exists(folder_downloads): xbmcvfs.mkdir(folder_downloads)
                dest = translate(os.path.join(folder_downloads,name))
                try:
                    os.remove(dest)
                except:
                    pass
                #if xbmcvfs.exists(folder_downloads):
                download_apk(url,dest)
                if os.path.isfile(dest):
                    #installAPK('com.android.documentsui',dest)
                    xbmcgui.Dialog().ok(addonname, 'Verifique a pasta download e instale o apk!')
    else:
        xbmcgui.Dialog().ok(addonname, 'Seu dispositivo não é android!')

if __name__ == '__main__': baixar_apk()