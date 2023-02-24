import xbmc, xbmcvfs, xbmcgui, xbmcaddon, xbmcplugin, re
import os
import urllib.parse as urlparse
import gzip
import sys     
import threading

try:
    from urllib.request import Request, urlopen, URLError  # Python 3
except ImportError:
    from urllib2 import Request, urlopen, URLError # Python 2
try:
    from StringIO import StringIO ## for Python 2
except ImportError:            
    from io import BytesIO as StringIO ## for Python 3

__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.f4mTester'
selfAddon = xbmcaddon.Addon(id=addon_id)
player_type = selfAddon.getSetting("player_type")
iptv = selfAddon.getSetting("iptv")
ask = selfAddon.getSetting("ask")
plugin = sys.argv[0]
handle = int(sys.argv[1])
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'


class MyPlayer (xbmc.Player):

    def __init__ (self):
        xbmc.Player.__init__(self)

    def play(self, url, li):
        #print 'Now im playing... %s' % url
        # self.stopPlaying.clear()
        # runningthread=thread.start_new_thread(xbmc.Player().play(item=url, listitem=li),(parar,))
        progress = xbmcgui.DialogProgress()
        # import checkbad
        # checkbad.do_block_check(False)

        #progress.create('Conectando...')
        progress.create('Estabilizador','Conectando...')
        # stream_delay = 1
        #progress.update( 20, "", 'Aguarde...', "" )
        # xbmc.sleep(stream_delay*100)
        #progress.update( 100, "", 'Carregando transmissão...', "" )
        prog=0
        xbmc.sleep(2000)


        
        xbmc.Player().play(item=url, listitem=li)

        while not xbmc.Player().isPlaying() and not xbmc.Monitor().abortRequested():
            xbmc.sleep(200)
            progress.update(prog+10,'Carregando transmissão...')
            prog=prog+10


        progress.close()


    def onPlayBackEnded( self ):
        # Will be called when xbmc stops playing a file
        print("seting event in onPlayBackEnded " )
        threading.Event()

        # self.stopPlaying.set()
        # thread.exit()
        # iniciavideo().stop()

        #print "stop Event is SET" 
    def onPlayBackStopped( self ):
        # Will be called when user stops xbmc playing a file
        print("seting event in onPlayBackStopped ") 
        threading.Event()
        # self.stopPlaying.set()
        # thread.exit()
        # iniciavideo().stop()

        #print "stop Event is SET"  

class iniciavideo():
    
    def tocar(url, li):

        
        # parar=threading.Event()
        # parar.clear()   
        mplayer = MyPlayer()    
        # iniciavideo().stop()
        # mplayer.stopPlaying = parar

        mplayer.play(url,li)


        # thread.start_new_thread(mplayer.play,(url,li))
        
        # mplayer.play(url,listitem)

        firstTime=True
        played=False

        
        while True:
            # if parar.isSet():            
                # break
            if xbmc.Player().isPlaying():
                played=True
            xbmc.log('Sleeping...')
            xbmc.sleep(1000)
            if firstTime:
                xbmc.executebuiltin('Dialog.Close(all,True)')
                firstTime=False
                # parar.isSet()
                # thread.exit()
                # iniciavideo().stop()


                    #print 'Job done'
        # return played
    
    def stop(self):
        threading.Event()

def get_kversion():
	full_version_info = xbmc.getInfoLabel('System.BuildVersion')
	baseversion = full_version_info.split(".")
	intbase = int(baseversion[0])
	# if intbase > 16.5:
	# 	log('HIGHER THAN 16.5')
	# if intbase < 16.5:
	# 	log('LOWER THAN 16.5')
	return intbase


def open_url(url,referer=False,post=False,timeout=12):
    req = Request(url)
    req.add_header('sec-ch-ua', '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"')
    req.add_header('sec-ch-ua-mobile', '?0')
    req.add_header('sec-ch-ua-platform', '"Windows"')
    req.add_header('Upgrade-Insecure-Requests', '1')    
    req.add_header('User-Agent', UA)
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
    req.add_header('Sec-Fetch-Site', 'none')
    req.add_header('Sec-Fetch-Mode', 'navigate')
    req.add_header('Sec-Fetch-User', '?1')
    req.add_header('Sec-Fetch-Dest', 'document')
    # req.add_header('Accept-Encoding', 'gzip')
    req.add_header('Accept-Language', 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7')
    if referer:    
        req.add_header('Referer', referer)
    try:
        if post:
            post = urlparse.urlencode(post)
            try:
                response = urlopen(req,data=post.encode('utf-8'),timeout=timeout)
                code = response.getcode()
                encoding = response.info().get('Content-Encoding')
            except:
                response = urlopen(req,data=post,timeout=timeout)
                code = response.getcode()
                encoding = response.info().get('Content-Encoding')
        else:
            try:
                response = urlopen(req,timeout=timeout)
                code = response.getcode()
                encoding = response.info().get('Content-Encoding')
            except:
                code = 401
                encoding = 'none'
    except:
        code = 401
        encoding = 'none'
    if code == 200:
        try:
            content = response.read()
        except:
            content = ''
    else:
        content = ''         
    try:
        content = content.decode('utf-8')
    except:
        pass
    return content
   

def get_url(params):
    url = '%s?%s'%(plugin, urlparse.urlencode(params))
    return url
    
def item(params,folder=True):
    url = get_url(params)
    name = params.get("name")
    if name:
        name = name
    else:
        name = 'Unknow'
    icon = params.get("iconImage")
    fanart = params.get("fanart")
    description = params.get("description")
    if description:
        description  = description
    else:
        description = ''
    
    li=xbmcgui.ListItem(name)
    if icon:
        li.setArt({"icon": "DefaultVideo.png", "thumb": icon})
    if fanart:
        li.setProperty('fanart_image', fanart)
    if get_kversion() > 19:
        info = li.getVideoInfoTag()
        info.setTitle(name)
        info.setPlot(description)
    else:
        li.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=li, isFolder=folder)    

def basename(p):
    """Returns the final component of a pathname"""
    i = p.rfind('/') + 1
    return p[i:]

def ts_to_m3u8(url):
    stream = False
    # xbmc.sleep(500)

    if not '.m3u8' in url and int(url.count(":")) == 2 and int(url.count("/")) > 4:
        url_parsed = urlparse.urlparse(url)
        try:
            host_part1 = '%s://%s'%(url_parsed.scheme,url_parsed.netloc)
            host_part2 = url.split(host_part1)[1]
            url = host_part1 + '/live' + host_part2
            url_no_param = url
            try:
                url_no_param = host_part2.split('&')[0]
            except:
                pass
            try:
                url_no_param = host_part2.split('|')[0]
            except:
                pass         
                
            file = basename(url_no_param)
            try:
                file = file.split('&')[0]
            except:
                pass
            try:
                file = file.split('|')[0]
            except:
                pass
            if '.ts' in file:
                file_new = file.replace('.ts', '.m3u8')
                url = url.replace(file, file_new)
            else:
                file_new = file + '.m3u8'
                url = url.replace(file, file_new)
            stream = 'HLSRETRY'
        except:
            pass
    return url,stream

def m3u8_to_ts(url):
    if '.m3u8' in url and '/live/' in url and int(url.count("/")) > 5:
        url = url.replace('/live', '').replace('.m3u8', '')
    return url
    
def playF4mLink(url,name,proxy=None,use_proxy_for_chunks=False,auth_string=None,streamtype='HDS',setResolved=False,swf="", callbackpath="", callbackparam="",referer="", origin="", cookie="", iconImage=""):
    from F4mProxy import f4mProxyHelper
    player=f4mProxyHelper()
    #progress = xbmcgui.DialogProgress()
    #progress.create('Starting local proxy')
    url,stream = ts_to_m3u8(url)   
    if stream:
        streamtype = stream        

    if setResolved:
        urltoplay,item=player.playF4mLink(url, name, proxy, use_proxy_for_chunks,maxbitrate,simpleDownloader,auth_string,streamtype,setResolved,swf,callbackpath, callbackparam,referer,origin,cookie,iconImage)
        item.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

    else:
        xbmcplugin.endOfDirectory(handle, cacheToDisc=False)        
        player.playF4mLink(url, name, proxy, use_proxy_for_chunks,maxbitrate,simpleDownloader,auth_string,streamtype,setResolved,swf,callbackpath, callbackparam,referer,origin,cookie,iconImage)


def ffmpeg_direct(url,name,iconImage):
    plugin = xbmcvfs.translatePath('special://home/addons/inputstream.ffmpegdirect')
    if os.path.exists(plugin)==False:
        try:
            xbmc.executebuiltin('InstallAddon(inputstream.ffmpegdirect)', wait=True)
        except:
            pass
    if name == "":
        name = "F4mTester"
    li=xbmcgui.ListItem(name, path=url)
    if iconImage:
        li.setArt({"icon": "DefaultVideo.png", "thumb": iconImage})
    if not '.mp4' in url and not '.mp3' in url and not '.mkv' in url and not '.avi' in url and not '.rmvb' in url:
        if os.path.exists(plugin)==True:
            url = m3u8_to_ts(url)
            #url,stream = ts_to_m3u8(url) 
            li.setProperty('inputstream', 'inputstream.ffmpegdirect')
            li.setProperty('IsPlayable', 'true')
            if '.m3u8' in url:
                li.setContentLookup(False)
                li.setMimeType('application/vnd.apple.mpegurl')
                li.setProperty('inputstream.ffmpegdirect.mime_type', 'application/vnd.apple.mpegurl')
                li.setProperty('ForceResolvePlugin','false')
                # li.setProperty('inputstream', 'inputstream.adaptive')
                # li.setProperty('inputstream.ffmpegdirect.manifest_type','hls')
            else:
                # li.setContentLookup(True)
                li.setMimeType('video/mp2t')
                li.setProperty('inputstream.ffmpegdirect.mime_type', 'video/mp2t')
                # li.setProperty('ForceResolvePlugin','true')
            # li.setProperty('http-reconnect', 'true')
            # li.setProperty('TotalTime', '3600')
            li.setProperty('inputstream.ffmpegdirect.stream_mode', 'catchup')
            # li.setProperty('inputstream.ffmpegdirect.timezone_shift', '20')
            li.setProperty('inputstream.ffmpegdirect.is_realtime_stream', 'true')
            li.setProperty('inputstream.ffmpegdirect.is_catchup_stream', 'catchup')
            li.setProperty('inputstream.ffmpegdirect.catchup_granularity', '60')
            li.setProperty('inputstream.ffmpegdirect.catchup_terminates', 'true')            
            li.setProperty('inputstream.ffmpegdirect.open_mode', 'curl')
            # li.setProperty('inputstream.ffmpegdirect.playback_as_live', 'true')
            # if '.m3u8' in url:             
                # li.setProperty('inputstream.ffmpegdirect.manifest_type','hls') 
            li.setProperty('inputstream.ffmpegdirect.manifest_type','ism')
            #print('aqui', url)                
            li.setProperty('inputstream.ffmpegdirect.default_url',url)
            li.setProperty('inputstream.ffmpegdirect.catchup_url_format_string',url)
            li.setProperty('inputstream.ffmpegdirect.programme_start_time','1')
            li.setProperty('inputstream.ffmpegdirect.programme_end_time','19')
            li.setProperty('inputstream.ffmpegdirect.catchup_buffer_start_time','1')
            li.setProperty('inputstream.ffmpegdirect.catchup_buffer_offset','1') 
            li.setProperty('inputstream.ffmpegdirect.default_programme_duration','19')
    # xbmc.Player().play(item=url, listitem=li)
    if get_kversion() > 19:
        info = li.getVideoInfoTag()
        info.setTitle(name)
    else:
        li.setInfo(type="Video", infoLabels={"Title": name, "Plot": ""})
    t1 = threading.Thread(target=iniciavideo.tocar,args=(url,li))
    t1.start()
    # t1.join()
    
def playiptv(url,name,iconImage):
    if '.m3u8' in url and not 'pluto.tv' in url and not 'plugin' in url:
        url = 'plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&amp;name='+urlparse.quote_plus(str(name))+'&amp;iconImage='+urlparse.quote_plus(iconImage)+'&amp;url='+urlparse.quote_plus(url)
    elif not '.mp4' in url and not '.mkv' in url and not '.avi' in url and not '.rmvb' in url and not 'pluto.tv' in url and not 'plugin' in url:
        url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name='+urlparse.quote_plus(str(name))+'&amp;iconImage='+urlparse.quote_plus(iconImage)+'&amp;url='+urlparse.quote_plus(url)                    
    if 'plugin' in url:
        xbmc.executebuiltin('RunPlugin(%s)'%url)
    elif not 'plugin' in url:
        li=xbmcgui.ListItem(name, path=url)
        if iconImage:
            li.setArt({"icon": "DefaultVideo.png", "thumb": iconImage})
        li.setProperty('IsPlayable', 'true')
        if get_kversion() > 19:
            info = li.getVideoInfoTag()
            info.setTitle(name)
        else:
            li.setInfo(type="Video", infoLabels={"Title": name, "Plot": ""})
        # xbmc.Player().play(item=url, listitem=li)
        t1 = threading.Thread(target=iniciavideo.tocar,args=(url,li))
        t1.start()
        t1.join()
        
def re_me(data, re_patten):
    match = ''
    m = re.search(re_patten, data)
    if m != None:
        match = m.group(1)
    else:
        match = ''
    return match
    
def playlist(url):
    xbmcplugin.setContent(handle, 'videos')
    data = open_url(url)    
    if re.search("#EXTM3U",data) or re.search("#EXTINF",data):
        content = data.rstrip()
        match1 = re.compile(r'#EXTINF:.+?tvg-logo="(.*?)".+?group-title="(.*?)",(.*?)[\n\r]+([^\r\n]+)').findall(content)
        if match1 !=[]:
            group_list = []
            for thumbnail,cat,channel_name,stream_url in match1:
                if not cat in group_list:
                    group_list.append(cat)
                    try:
                        cat = cat.encode('utf-8', 'ignore')
                    except:
                        pass
                    item({'name': cat,'mode': 'playlist2', 'url': url, 'iconImage': ''})
        elif match1 ==[]:
            match2 = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\r\n]+)').findall(content)
            #match2 = sorted(match2)
            group_list = []
            for other,channel_name,stream_url in match2:
                if 'tvg-logo' in other:
                    thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
                    if thumbnail:
                        if thumbnail.startswith('http'):
                            thumbnail = thumbnail
                        else:
                            thumbnail = ''
                    else:
                        thumbnail = ''
                else:
                    thumbnail = ''

                if 'group-title' in other:
                    cat = re_me(other,'group-title=[\'"](.*?)[\'"]')
                else:
                    cat = ''
                if cat > '':
                    if not cat in group_list:
                        group_list.append(cat)
                        try:
                            cat = cat.encode('utf-8', 'ignore')
                        except:
                            pass
                        item({'name': cat,'mode': 'playlist2', 'url': url, 'iconImage': ''})
                else:
                    item({'name':channel_name,'mode': 'playiptv', 'url': stream_url, 'iconImage': thumbnail},folder=False)
            if match2 ==[]:
                control.infoDialog(lang.id('no_playlist_available'), iconimage='INFO')
    xbmcplugin.endOfDirectory(handle)


def playlist2(name,url):       
    xbmcplugin.setContent(handle, 'videos')
    data = open_url(url)
    if re.search("#EXTM3U",data) or re.search("#EXTINF",data):
        content = data.rstrip()
        match1 = re.compile(r'#EXTINF:.+?tvg-logo="(.*?)".+?group-title="(.*?)",(.*?)[\n\r]+([^\r\n]+)').findall(content)
        if match1 !=[]:
            #match1 = sorted(match1)
            group_list = []
            for thumbnail,cat,channel_name,stream_url in match1:
                try:
                    name = name.decode('utf-8')
                except:
                    pass
                if cat == name:
                    item({'name':channel_name,'mode': 'playiptv', 'url': stream_url, 'iconImage': thumbnail},folder=False)
        elif match1 ==[]:
            match2 = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\r\n]+)').findall(content)
            #match2 = sorted(match2)
            for other,channel_name,stream_url in match2:
                if 'tvg-logo' in other:
                    thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
                    if thumbnail:
                        if thumbnail.startswith('http'):
                            thumbnail = thumbnail
                        else:
                            thumbnail = ''
                    else:
                        thumbnail = ''
                else:
                    thumbnail = ''

                if 'group-title' in other:
                    cat = re_me(other,'group-title=[\'"](.*?)[\'"]')
                else:
                    cat = ''
                if cat > '':
                    try:
                        name = name.decode('utf-8')
                    except:
                        pass
                    if cat == name:
                        item({'name':channel_name,'mode': 'playiptv', 'url': stream_url, 'iconImage': thumbnail},folder=False)
    xbmcplugin.endOfDirectory(handle)
        


paramstring=sys.argv[2]
args = urlparse.parse_qs(sys.argv[2][1:])
try:
    mode = args.get("mode")
    mode = mode[0]
except:
    if paramstring:
        mode='play'
    else:
        mode = None
try:
    url = args.get("url")
    url = url[0]
except:
    url = ''
try:
    name = args.get("name")
    name = name[0]
except:
    name = ''
try:
    proxy_string = args.get("proxy")
    proxy_string = proxy_string[0]
except:
    proxy_string=None
try:    
    auth_string = args.get("auth")
    auth_string = auth_string[0]
except:
    auth_string=''
try:    
    streamtype = args.get("streamtype")
    streamtype = streamtype[0]
except:
    streamtype='HDS'
try:    
    swf = args.get("swf")
    swf = swf[0]
except:
    swf=None
try:    
    callbackpath = args.get("callbackpath")
    callbackpath = callbackpath[0]
except:
    callbackpath=""
try:    
    iconImage = args.get("iconImage")
    iconImage = iconImage[0]
except:
    iconImage=""    
try:
    callbackparam = args.get("callbackparam")
    callbackparam = callbackparam[0]
except:
    callbackparam=""
try:
    referer=args.get("referer")
except:
    referer=""

try:
    origin=args.get("origin")
except:
    origin=""

try:
    cookie=args.get("cookie")
except:
    cookie=""
try:
    proxy_use_chunks_temp = args.get("proxy_for_chunks")
    import json
    proxy_use_chunks=json.loads(proxy_use_chunks_temp[0])
except:
    proxy_use_chunks=True
try:
    simpleDownloader_temp = args.get("simpledownloader")
    import json
    simpleDownloader=json.loads(simpleDownloader_temp[0])
except:
    simpleDownloader=False
try:
    maxbitrate = args.get("maxbitrate")
    maxbitrate = int(maxbitrate[0])
except:
    maxbitrate=0
try:
    setResolved = args.get("setresolved")
    setResolved = setResolved[0]
    import json
    setResolved=json.loads(setResolved)
except:
    setResolved=False
   
if mode == None:
    if 'http' in iptv:
        item({'name': 'IPTV', 'mode': 'playlist', 'url': iptv},folder=True)
    item({'name': 'Settings', 'mode': 'settings'},folder=True)        
    xbmcplugin.endOfDirectory(handle, cacheToDisc=False)
elif mode == 'settings':
    selfAddon.openSettings()
elif mode == "play":
    player_type = int(player_type)
    confirmation = True
    if ask == 'true':
        dialog = xbmcgui.Dialog()
        index = dialog.select('Select a player', ['inputstream.ffmpegdirect', 'F4mProxy'])
        if index >= 0:
            player_type = index
        else:
            confirmation = False           
    if player_type == 0 and confirmation == True:
        ffmpeg_direct(url,name,iconImage)
    elif confirmation == True:
        playF4mLink(url,name,proxy_string,proxy_use_chunks,auth_string,streamtype,setResolved,swf,callbackpath,callbackparam,referer,origin,cookie,iconImage)
elif mode == 'playlist':
    playlist(url)
elif mode == 'playlist2':
    playlist2(name,url)      
elif mode == 'playiptv':
    if 'plugin' in url:
        url = url.replace(';&amp;', '&').replace(';', '&').replace('&amp;', '&')
    playiptv(url,name,iconImage)