# -*- coding: utf-8 -*-

'''
    Genesis XBMC Addon
    Copyright (C) 2014 lambda

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
'''

import urllib,urllib2,re,os,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
try:
    import json
except:
    import simplejson as json
try:
    import CommonFunctions as common
except:
    import commonfunctionsdummy as common


def get(url):
    debrid = realdebrid(url)
    if not debrid == None: return debrid

    if '/vk.com' in url:                url = vk(url)
    elif 'docs.google.com' in url:      url = googledocs(url)
    elif 'picasaweb.google.com' in url: url = picasaweb(url)
    elif 'youtube.com' in url:          url = youtube(url)
    elif 'odnoklassniki.ru' in url:     url = odnoklassniki(url)
    elif 'videomega.tv' in url:         url = videomega(url)
    elif 'movreel.com' in url:          url = movreel(url)
    elif 'v-vids.com' in url:           url = v_vids(url)
    elif 'vidbull.com' in url:          url = vidbull(url)
    elif '180upload.com' in url:        url = _180upload(url)
    elif 'hugefiles.net' in url:        url = hugefiles(url)
    elif 'filecloud.io' in url:         url = filecloud(url)
    elif 'uploadrocket.net' in url:     url = uploadrocket(url)
    elif 'kingfiles.net' in url:        url = kingfiles(url)
    elif 'streamin.to' in url:          url = streamin(url)
    elif 'grifthost.com' in url:        url = grifthost(url)
    elif 'ishared.eu' in url:           url = ishared(url)
    elif 'cloudyvideos.com' in url:     url = cloudyvideos(url)
    elif 'mrfile.me' in url:            url = mrfile(url)
    elif 'mail.ru' in url:              url = mailru(url)

    else:
        import urlresolver
        host = urlresolver.HostedMediaFile(url)
        if host: resolver = urlresolver.resolve(url)
        else: return url
        if not resolver.startswith('http://'): return
        if not resolver == url: return resolver

    return url


def realdebrid(url):
    try:
        user = xbmcaddon.Addon().getSetting("realdedrid_user")
        password = xbmcaddon.Addon().getSetting("realdedrid_password")

        if (user == '' or password == ''): raise Exception()

        login_data = urllib.urlencode({'user' : user, 'pass' : password})
        login_link = 'https://real-debrid.com/ajax/login.php?%s' % login_data
        result = getUrl(login_link, close=False).result
        result = json.loads(result)
        error = result['error']
        if not error == 0: raise Exception()

        url = 'https://real-debrid.com/ajax/unrestrict.php?link=%s' % url
        url = url.replace('filefactory.com/stream/', 'filefactory.com/file/')
        result = getUrl(url).result
        result = json.loads(result)
        url = result['generated_links'][0][-1]
        return url
    except:
        return

def vk(url):
    try:
        url = url.replace('http://', 'https://')
        result = getUrl(url).result

        u = re.compile('url(720|540|480)=(.+?)&').findall(result)

        url = []
        try: url += [[{'quality': 'HD', 'url': i[1]} for i in u if i[0] == '720'][0]]
        except: pass
        try: url += [[{'quality': 'SD', 'url': i[1]} for i in u if i[0] == '540'][0]]
        except: pass
        try: url += [[{'quality': 'SD', 'url': i[1]} for i in u if i[0] == '480'][0]]
        except: pass

        if url == []: return
        return url
    except:
        return

def googledocs(url):
    try:
        url = url.split('/preview', 1)[0]

        result = getUrl(url).result
        result = re.compile('"fmt_stream_map",(".+?")').findall(result)[0]
        result = json.loads(result)

        url = [i.split('|')[-1] for i in result.split(',')]
        if url == []: return
        try: url = [i for i in url if not any(x in i for x in ['&itag=43&', '&itag=35&', '&itag=34&', '&itag=5&'])][0]
        except: url = url[0]
        return url
    except:
        return

def picasaweb(url):
    try:
        result = getUrl(url).result
        result = re.compile('{"content":(\[.+?\])').findall(result)[0]
        result = json.loads(result)

        url = [i for i in result if i['type'] == 'application/x-shockwave-flash']
        url += [i for i in result if i['type'] == 'video/mpeg4']
        url = url[-1]['url']
        url = getUrl(url, output='geturl').result
        return url
    except:
        return

def youtube(url):
    try:
        id = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
        result = getUrl('http://gdata.youtube.com/feeds/api/videos/%s?v=2' % id).result

        state, reason = None, None
        try: state = common.parseDOM(result, "yt:state", ret="name")[0]
        except: pass
        try: reason = common.parseDOM(result, "yt:state", ret="reasonCode")[0]
        except: pass
        if state == 'deleted' or state == 'rejected' or state == 'failed' or reason == 'requesterRegion' : return

        url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
        return url
    except:
        return

def odnoklassniki(url):
    try:
        url = [i for i in url.split('/') if i.isdigit()][-1]
        url = 'http://www.odnoklassniki.ru/dk?cmd=videoPlayerMetadata&mid=%s' % url

        result = getUrl(url).result
        result = json.loads(result)

        a = "&start=0|User-Agent=%s" % urllib.quote_plus('Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')
        u = result['videos']

        url = []
        try: url += [[{'quality': 'HD', 'url': i['url'] + a} for i in u if i['name'] == 'hd'][0]]
        except: pass
        try: url += [[{'quality': 'SD', 'url': i['url'] + a} for i in u if i['name'] == 'sd'][0]]
        except: pass

        if url == []: return
        return url
    except:
        return

def videomega(url):
    try:
        url = url.replace('/?ref=', '/iframe.php?ref=')
        result = getUrl(url).result
        url = re.compile('document.write.unescape."(.+?)"').findall(result)[0]
        url = urllib.unquote_plus(url)
        url = re.compile('file: "(.+?)"').findall(url)[0]
        return url
    except:
        return

def movreel(url):
    try:
        user = xbmcaddon.Addon().getSetting("movreel_user")
        password = xbmcaddon.Addon().getSetting("movreel_password")

        login = 'http://movreel.com/login.html'
        post = {'op': 'login', 'login': user, 'password': password, 'redirect': url}
        post = urllib.urlencode(post)
        result = getUrl(url, close=False).result
        result += getUrl(login, post=post, close=False).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "name": "F1" })[-1]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': '', 'method_premium': ''})
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        url = re.compile('(<a .+?</a>)').findall(result)
        url = [i for i in url if 'Download Link' in i][-1]
        url = common.parseDOM(url, "a", ret="href")[0]
        return url
    except:
        return

def v_vids(url):
    try:
        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "name": "F1" })[0]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': '', 'method_premium': ''})
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        url = common.parseDOM(result, "a", ret="href", attrs = { "id": "downloadbutton" })[0]
        return url
    except:
        return

def vidbull(url):
    try:
        result = getUrl(url, mobile=True).result
        url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video.+?" })[0]
        return url
    except:
        return

def _180upload(url):
    try:
        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "name": "F1" })[0]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update(captcha().get(result))
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        url = common.parseDOM(result, "a", ret="href", attrs = { "id": "lnk_download" })[0]
        return url
    except:
        return

def hugefiles(url):
    try:
        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "action": "" })
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': 'Free Download'})
        post.update(captcha().get(result))
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "action": "" })
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': 'Free Download'})
        post = urllib.urlencode(post)

        u = getUrl(url, output='geturl', post=post).result
        if not url == u: return u
    except:
        return

def filecloud(url):
    try:
        result = getUrl(url, close=False).result
        result = getUrl('http://filecloud.io/download.html').result

        url = re.compile("__requestUrl\s+=\s+'(.+?)'").findall(result)[0]

        ukey = re.compile("'ukey'\s+:\s+'(.+?)'").findall(result)[0]
        __ab1 = re.compile("__ab1\s+=\s+(\d+);").findall(result)[0]
        ctype = re.compile("'ctype'\s+:\s+'(.+?)'").findall(result)[0]

        challenge = re.compile("__recaptcha_public\s+=\s+'(.+?)'").findall(result)[0]
        challenge = 'http://www.google.com/recaptcha/api/challenge?k=' + challenge

        post = {'ukey': ukey, '__ab1': str(__ab1), 'ctype': ctype}
        post.update(captcha().get(challenge))
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result
        result = getUrl('http://filecloud.io/download.html').result

        url = common.parseDOM(result, "a", ret="href", attrs = { "id": "downloadBtn" })[0]
        return url
    except:
        return

def uploadrocket(url):
    try:
        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "name": "freeorpremium" })[0]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': 'Free Download'})
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "name": "F1" })[0]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update(captcha().get(result))
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        url = common.parseDOM(result, "a", ret="href", attrs = { "onclick": "window[.]open.+?" })[0]
        return url
    except:
        return

def kingfiles(url):
    try:
        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "action": "" })[0]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': ' '})
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "action": "" })[0]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': ' '})
        post.update(captcha().get(result))
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        url = re.compile("var download_url = '(.+?)'").findall(result)[0]
        return url
    except:
        return

def streamin(url):
    try:
        url = url.replace('streamin.to/', 'streamin.to/embed-')
        if not url.endswith('.html'): url = url + '.html'
        result = getUrl(url, mobile=True).result
        url = re.compile("file:'(.+?)'").findall(result)[0]
        return url
    except:
        return

def grifthost(url):
    try:
        url = url.replace('/embed-', '/').split('-')[0]

        result = getUrl(url, close=False).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "name": "F1" })[-1]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': '', 'method_premium': ''})
        post = urllib.urlencode(post)

        import time
        request = urllib2.Request(url, post)

        for i in range(0, 4):
            try:
                response = urllib2.urlopen(request, timeout=5)
                result = response.read()
                response.close()
                url = re.compile('(<a .+?</a>)').findall(result)
                url = [i for i in url if '/download.png' in i][-1]
                url = common.parseDOM(url, "a", ret="href")[0]
                return url
            except:
                time.sleep(1)
    except:
        return

def ishared(url):
    try:
        result = getUrl(url).result
        url = re.compile('path:"(.+?)"').findall(result)[0]
        return url
    except:
        return

def cloudyvideos(url):
    try:
        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "name": "F1" })[-1]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': '', 'method_premium': ''})
        post = urllib.urlencode(post)

        import time
        request = urllib2.Request(url, post)

        for i in range(0, 4):
            try:
                response = urllib2.urlopen(request, timeout=5)
                result = response.read()
                response.close()
                btn = common.parseDOM(result, "input", ret="value", attrs = { "class": "graybtn" })[0]
                url = re.compile('href=[\'|\"](.+?)[\'|\"]><input.+?class=[\'|\"]graybtn[\'|\"]').findall(result)[0]
                return url
            except:
                time.sleep(1)
    except:
        return

def mrfile(url):
    try:
        result = getUrl(url).result

        post = {}
        f = common.parseDOM(result, "Form", attrs = { "name": "F1" })[-1]
        k = common.parseDOM(f, "input", ret="name", attrs = { "type": "hidden" })
        for i in k: post.update({i: common.parseDOM(f, "input", ret="value", attrs = { "name": i })[0]})
        post.update({'method_free': '', 'method_premium': ''})
        post = urllib.urlencode(post)

        result = getUrl(url, post=post).result

        url = re.compile("file:\s+'(.+?)'").findall(result)[0]
        return url
    except:
        return

def mailru(url):
    try:
        url = url.replace('/my.mail.ru/video/', '/api.video.mail.ru/videos/embed/')
        result = getUrl(url).result
        url = re.compile('videoSrc\s+=\s+"(.+?)"').findall(result)[0]
        url = getUrl(url, output='geturl').result
        return url
    except:
        return



class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='10'):
        if not proxy == None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post == None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')
        if not referer == None:
            request.add_header('Referer', referer)
        if not cookie == None:
            request.add_header('cookie', cookie)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

class captcha:
    def get(self, data):
        try:
            captcha = {}

            solvemedia = common.parseDOM(data, "iframe", ret="src")
            solvemedia = [i for i in solvemedia if 'api.solvemedia.com' in i]

            if len(solvemedia) > 0:
                url = solvemedia[0]
                result = getUrl(url).result
                challenge = common.parseDOM(result, "input", ret="value", attrs = { "id": "adcopy_challenge" })[0]
                response = common.parseDOM(result, "iframe", ret="src")
                response += common.parseDOM(result, "img", ret="src")
                response = [i for i in response if '/papi/media' in i][0]
                response = 'http://api.solvemedia.com' + response
                response = self.get_response(response)
                captcha.update({'adcopy_challenge': challenge, 'adcopy_response': response})
                return captcha

            recaptcha = []
            if data.startswith('http://www.google.com'): recaptcha += [data]
            recaptcha += common.parseDOM(data, "script", ret="src", attrs = { "type": "text/javascript" })
            recaptcha = [i for i in recaptcha if 'http://www.google.com' in i]

            if len(recaptcha) > 0:
                url = recaptcha[0]
                result = getUrl(url).result
                challenge = re.compile("challenge\s+:\s+'(.+?)'").findall(result)[0]
                response = 'http://www.google.com/recaptcha/api/image?c=' + challenge
                response = self.get_response(response)
                captcha.update({'recaptcha_challenge_field': challenge, 'recaptcha_challenge': challenge, 'recaptcha_response_field': response, 'recaptcha_response': response})
                return captcha

            numeric = re.compile("left:(\d+)px;padding-top:\d+px;'>&#(.+?);<").findall(data)

            if len(numeric) > 0:
                result = sorted(numeric, key=lambda ltr: int(ltr[0]))
                response = ''.join(str(int(num[1])-48) for num in result)
                captcha.update({'code': response})
                return captcha

        except:
            return captcha

    def get_response(self, response):
        try:
            dataPath = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile"))
            i = os.path.join(dataPath.decode("utf-8"),'img')
            f = xbmcvfs.File(i, 'w')
            f.write(getUrl(response).result)
            f.close()
            f = xbmcgui.ControlImage(450,15,400,130, i)
            d = xbmcgui.WindowDialog()
            d.addControl(f)
            xbmcvfs.delete(i)
            d.show()
            xbmc.sleep(3000)
            t = 'Type the letters in the image'
            c = common.getUserInput(t, '')
            d.close()
            return c
        except:
            return