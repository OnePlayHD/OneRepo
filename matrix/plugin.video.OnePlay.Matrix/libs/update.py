# -*- coding: utf-8 -*-
import six
from kodi_six import xbmc, xbmcvfs, xbmcgui, xbmcplugin, xbmcaddon
from libs.control import oneplay
import re
import sys
import os
addon = xbmcaddon.Addon()
addonid = addon.getAddonInfo('id')
addonname = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')
translate = xbmcvfs.translatePath if six.PY3 else xbmc.translatePath
dialog = xbmcgui.Dialog()
handle = int(sys.argv[1])
update_version = '23.02.2023'

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
        
def auto_update():
    try:
        url_version = 'https://onepod.inrupt.net/public/updateoneplay/version.txt'
        ver = oneplay().navegador_update(url=url_version)
        try:
            ver = ver.replace('\n', '').replace('\r', '').replace(' ', '')
        except:
            pass
        if ver != update_version and ver !='' and ver !=None and ver !='none':
            url_update = 'https://onepod.inrupt.net/public/updateoneplay/update.txt'
            data = oneplay().navegador_update(url=url_update)
            match = re.findall('rl="(.*?)"', data, flags=re.MULTILINE|re.DOTALL|re.IGNORECASE)
            if match:
                for url in match:
                    install(url)
                if six.PY2:
                    xbmc.executebuiltin("XBMC.Container.Refresh")
                else:
                    xbmc.executebuiltin("Container.Refresh")

    except:
        pass                   
        
def install(url):
    special_dir = 'special://home/addons/'+addonid
    special_packages = 'special://home/addons/packages'
    directory = translate(special_dir)
    packages = translate(special_packages)       
    if os.path.exists(directory):
        try:
            from libs import downloader, extract
            import ntpath
            filename = ntpath.basename(url)
            dest=os.path.join(packages, filename)
            dp = xbmcgui.DialogProgress()
            if six.PY3:
                dp.create('Baixando '+addonid+'...','Aguarde...')
            else:
                dp.create('Baixando '+addonid+'...','Aguarde...', '', '')
            downloader.download(url,addonid,dest,dp=dp)
            zip_file = dest
            extract_folder = directory
            if six.PY3:
                dp.create('Extraindo '+addonid+'...','Aguarde...')
            else:
                dp.create('Extraindo '+addonid+'...','Aguarde...', '', '')
            dp.update(0)
            extract.all(zip_file,extract_folder, dp=dp)
            try:
                os.remove(zip_file)
            except:
                pass
            infoDialog('Atualizacao concluida', iconimage='INFO')
        except:
            infoDialog('Error', iconimage='WARNING')