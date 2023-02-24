# -*- coding: utf-8 -*-
import six
from kodi_six import xbmc, xbmcvfs, xbmcgui, xbmcplugin, xbmcaddon
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

def notify(msg):
    infoDialog(msg, iconimage='INFO')
    

def download(url, name, dest, dp = None):
    global start_time
    start_time=time.time()
    if not dp:
        dp = xbmcgui.DialogProgress() 
        if six.PY3:
            dp.create('Downloading '+name+'...','Please wait...')
        else:
            dp.create('Downloading '+name+'...','Please wait...', '', '')
            
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
        currently_downloaded = float(numblocks) * blocksize / (1024 * 1024)
        kbps_speed = numblocks * blocksize / (time.time() - start_time)
        if kbps_speed > 0:
            eta = (filesize - numblocks * blocksize) / kbps_speed
        else:
            eta = 0
        kbps_speed = kbps_speed / 1024
        total = float(filesize) / (1024 * 1024)
        if six.PY3:
            msg = '%.02f MB de %.02f MB\n' % (currently_downloaded, total)
            msg += '[COLOR yellow]Speed:[/COLOR] %.02d Kb/s ' % kbps_speed
            msg += '[COLOR yellow]Time left:[/COLOR] %02d:%02d' % divmod(eta, 60)   
            dp.update(percent, msg)
        else:
            mbs = '%.02f MB de %.02f MB' % (currently_downloaded, total)
            e = '[COLOR yellow]Speed:[/COLOR] %.02d Kb/s ' % kbps_speed
            e += '[COLOR yellow]Time left:[/COLOR] %02d:%02d' % divmod(eta, 60)
            dp.update(percent, mbs, e)
    except:
        percent = 100
        dp.update(percent)
    if percent == 100:
        notify('Download completed.')
    elif dp.iscanceled(): 
        dp.close()
        raise notify('Download stopped.')
