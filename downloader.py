# -*- coding: utf-8 -*-
import six
from kodi_six import xbmcgui, xbmcaddon
import time
import os
try:
    import urllib.request as urllib2
except ImportError:
    import urllib as urllib2

addon = xbmcaddon.Addon()
addonid = addon.getAddonInfo('id')
addonname = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')
dialog = xbmcgui.Dialog()

def download(url, dest, dp = None):
    global start_time
    start_time=time.time()
    if not dp:
        dp = xbmcgui.DialogProgress() 
        if six.PY3:
            dp.create('Baixando...','Por favor aguarde...')
        else:
            dp.create('Baixando...','Por favor aguarde...', '', '')
    dp.update(0)
    try:
        urllib2.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
    except:
        try:
            os.remove(dest)
        except:
            pass
        raise Exception
 
def _pbhook(numblocks, blocksize, filesize, url, dp):
    try:
        percent = int(min((numblocks*blocksize*100)/filesize, 100))
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        dp.close()
        raise Exception("Canceled")
#checkintegrity23022021
#checkintegrity08072020