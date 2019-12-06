import xbmc
import xbmcgui
import urllib
import time
COLOR1         = 'blue'
COLOR2         = 'yellow'

urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'


def download(url, dest, dp = None):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("Elmore...Maintenance","Downloading & Copying File",' ', ' ')
    dp.update(0)
    start_time=time.time()
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url, dp):
    try: 
		percent = min(numblocks * blocksize * 100 / filesize, 100) 
		currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
		kbps_speed = numblocks * blocksize / (time.time() - start_time) 
		if kbps_speed > 0 and not percent == 100: 
			eta = (filesize - numblocks * blocksize) / kbps_speed 
		else: 
			eta = 0
		kbps_speed = kbps_speed / 1024 
		type_speed = 'KB'
		if kbps_speed >= 1024:
			kbps_speed = kbps_speed / 1024 
			type_speed = 'MB'
		total = float(filesize) / (1024 * 1024) 
		mbs = '[COLOR %s][B]Tamanho:[/B] [COLOR %s]%.02f[/COLOR] MB de [COLOR %s]%.02f[/COLOR] MB[/COLOR]' % (COLOR2, COLOR1, currently_downloaded, COLOR1, total) 
		e   = '[COLOR %s][B]Velocidade:[/B] [COLOR %s]%.02f [/COLOR]%s/s ' % (COLOR2, COLOR1, kbps_speed, type_speed)
		e  += '[B]Tempo Restante:[/B] [COLOR '+COLOR1+']%02d:%02d[/COLOR][/COLOR]' % divmod(eta, 60)
		dp.update(percent, '', mbs, e)
    except Exception, e:
        xbmc.log("Erro ao Fazer Download: %s" % str(e), xbmc.LOGERROR)
        pass
    if dp.iscanceled(): 
        raise Exception("Canceled")
        dp.close()
