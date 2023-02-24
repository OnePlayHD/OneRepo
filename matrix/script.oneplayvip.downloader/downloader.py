# -*- coding: utf-8 -*-
import six
from kodi_six import xbmc, xbmcgui
import time
import os
try:
    from urllib.request import build_opener, install_opener, Request, urlopen, URLError, urlretrieve  # Python 3
except ImportError:
    from urllib2 import build_opener, install_opener, Request, urlopen, URLError # Python 2
    from urllib import urlretrieve
from default import icon

def infoDialog(message, heading='ONEPLAY VIP DOWNLOADER', iconimage='', time=3000, sound=False):
    if iconimage == '':
        iconimage = icon
    elif iconimage == 'INFO':
        iconimage = xbmcgui.NOTIFICATION_INFO
    elif iconimage == 'WARNING':
        iconimage = xbmcgui.NOTIFICATION_WARNING
    elif iconimage == 'ERROR':
        iconimage = xbmcgui.NOTIFICATION_ERROR
    xbmcgui.Dialog().notification(heading, message, iconimage, time, sound=sound)


def notify(msg):
    infoDialog(msg, iconimage='INFO')


def download_py2(url, dest, dp):
    from contextlib import closing
    req = Request(url)  
    req.add_header('User-Agent', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Mobile Safari/537.36')   
    msg = 'Baixando, Aguarde....'
    dp.update(0, msg, '')
    with closing(urlopen(req)) as dl_file:
        with open(dest, 'wb') as out_file:
            out_file.write(dl_file.read())
    notify('Download completo.')

def download_py3(url, dest, dp):
    opener = build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Mobile Safari/537.36')]
    install_opener(opener)        
    urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp)) 


def download(url, name, dest, dp = None):
    global start_time
    start_time=time.time()
    if not dp:
        dp = xbmcgui.DialogProgress() 
        if six.PY3:
            dp.create('Baixando '+name+'...','Por favor espere...')
        else:
            dp.create('Baixando '+name+'...','Por favor espere...', '', '')
            
    dp.update(0)
    try:
        if six.PY3:
            download_py3(url, dest, dp)
        else:
            download_py2(url, dest, dp)
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
        notify('Download completo.')
    elif dp.iscanceled(): 
        dp.close()
        raise notify('Download parado.')