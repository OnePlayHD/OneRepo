try:
    from urllib.request import Request, urlopen, URLError  # Python 3
except ImportError:
    from urllib2 import Request, urlopen, URLError # Python 2

APKS_BASE = 'https://raw.githubusercontent.com/OnePlayHD/OneRepo/master/matrix/apks_oneplay.txt'

def open_url(url):
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
    req.add_header('Accept-Language', 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7')
    try:
        response = urlopen(req,timeout=12)
        content = response.read()
    except:
        content = ''
    try:
        content = content.decode('utf-8')
    except:
        pass
    return content

def listar_apks():
    import ntpath
    temp = []
    apks = open_url(APKS_BASE)
    if apks:
        mylist = apks.split("\n")
        if len(mylist) > 0:
            for url in mylist:
                if '.apk' in url:
                    name = ntpath.basename(url)
                    temp.append((name,url))
            return temp
    return False