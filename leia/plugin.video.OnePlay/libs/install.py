# -*- coding: utf-8 -*-
import six
from kodi_six import xbmc, xbmcvfs, xbmcgui, xbmcplugin, xbmcaddon
from libs.control import oneplay
import re
import sys
import os
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
import datetime
try:
    import json
except:
    import simplejson as json
addon = xbmcaddon.Addon()
addonid = addon.getAddonInfo('id')
addonname = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')
translate = xbmcvfs.translatePath if six.PY3 else xbmc.translatePath
dialog = xbmcgui.Dialog()

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

def get_kversion():
	full_version_info = xbmc.getInfoLabel('System.BuildVersion')
	baseversion = full_version_info.split(".")
	intbase = int(baseversion[0])
	# if intbase > 16.5:
	# 	log('HIGHER THAN 16.5')
	# if intbase < 16.5:
	# 	log('LOWER THAN 16.5')
	return  intbase

def db_kodi():
    special_dir = 'special://profile/Database'
    directory = translate(special_dir)
    if six.PY3:
        db = os.path.join(directory, 'Addons33.db')
    else:
        db = os.path.join(directory, 'Addons27.db')
    return db

def delete_id(addon_id):
    db = db_kodi()
    try:
        conn = database.connect(db)
        cursor = conn.cursor()
        sql = 'DELETE FROM installed WHERE addonID=?'
        cursor.execute(sql, (addon_id,))
        conn.commit()
        conn.close()
    except:
        pass


def enable_addon(addon_id):
    if get_kversion() >16.5:
        try:
            delete_id(addon_id)
            db = db_kodi()
            now = datetime.datetime.now()
            installDate = now.strftime("%Y-%m-%d %H:%M:%S")
            conn = database.connect(db)
            cursor = conn.cursor()
            sql = 'INSERT INTO installed (addonID,enabled,installDate) VALUES(?,?,?)'
            cursor.execute(sql, (addon_id,1,installDate,))
            conn.commit()
            conn.close()
        except:
            pass


def check_addons():
    try:
        check_url = 'https://onepod.inrupt.net/public/updateoneplay/check_addons.txt'
        data = oneplay().navegador_update(url=check_url)
        match = re.findall('id="(.*?)".+?rl="(.*?)"', data, flags=re.MULTILINE|re.DOTALL|re.IGNORECASE)
        if match:
            for id_addon, url in match:
                special_dir = 'special://home/addons/'+id_addon
                directory = translate(special_dir)
                if not os.path.exists(directory):
                    install(id_addon,url)
                    xbmc.sleep(5)
                    if six.PY2:
                        xbmc.executebuiltin("XBMC.UpdateLocalAddons")
                    else:
                        xbmc.executebuiltin("UpdateLocalAddons")                
                    enable_addon(id_addon)
                    xbmc.sleep(3)
                    if six.PY2:
                        xbmc.executebuiltin("XBMC.UpdateAddonRepos")
                    else:
                        xbmc.executebuiltin("UpdateAddonRepos")                    
    except:
        pass

        
def install(myid,url):
    special_dir = 'special://home/addons/'+myid
    special_packages = 'special://home/addons/packages'
    addons_dir = 'special://home/addons/'
    dest_dir = translate(addons_dir)
    directory = translate(special_dir)
    packages = translate(special_packages)       
    if not os.path.exists(directory):
        try:
            from libs import downloader, extract
            import ntpath
            filename = ntpath.basename(url)
            dest=os.path.join(packages, filename)
            dp = xbmcgui.DialogProgress()
            if six.PY3:
                dp.create('Baixando '+myid+'...','Aguarde...')
            else:
                dp.create('Baixando '+myid+'...','Aguarde...', '', '')
            downloader.download(url,myid,dest,dp=dp)
            zip_file = dest
            extract_folder = dest_dir
            if six.PY3:
                dp.create('Extraindo '+myid+'...','Aguarde...')
            else:
                dp.create('Extraindo '+myid+'...','Aguarde...', '', '')
            dp.update(0)
            extract.all(zip_file,extract_folder, dp=dp)
            try:
                os.remove(zip_file)
            except:
                pass
            infoDialog('Download concluido', iconimage='INFO')
        except:
            infoDialog('Error', iconimage='WARNING')