import six
try:
    from urllib.parse import urlparse, parse_qs, quote, unquote, quote_plus, unquote_plus, urlencode #python 3
except ImportError:    
    from urlparse import urlparse, parse_qs #python 2
    from urllib import quote, unquote, quote_plus, unquote_plus, urlencode
if six.PY3:
    from http.server import HTTPServer
    from http.server import BaseHTTPRequestHandler
    from http.server import SimpleHTTPRequestHandler
else:
    from BaseHTTPServer import BaseHTTPRequestHandler
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from BaseHTTPServer import HTTPServer
import threading
import socket
import requests
import time

HOST_NAME = '127.0.0.1'
PORT_NUMBER = 55333

global GLOBAL_HEADERS
global GLOBAL_URL
GLOBAL_HEADERS = {}
GLOBAL_URL = ''

class handler(SimpleHTTPRequestHandler):
    def basename(self,p):
        """Returns the final component of a pathname"""
        i = p.rfind('/') + 1
        return p[i:] 
    
    def get_headers(self,url):
        global GLOBAL_HEADERS
        try:
            url = url.split('url=')[1]
        except:
            pass
        data = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36', 'Connection': 'keep-alive'}
        if '|' in url or '&' in url or 'h123' in url:
            try:
                referer = url.split('Referer=')[1]
                try:
                    referer = referer.split('&')[0]
                except:
                    pass
            except:
                referer = None
            try:
                origin = url.split('Origin=')[1]
                try:
                    origin = origin.split('&')[0]
                except:
                    pass
            except:
                origin = None
            try:
                cookie = url.split('Cookie=')[1]
                try:
                    cookie = cookie.split('&')[0]
                except:
                    pass
            except:
                cookie = None                            
            try:
                referer = unquote_plus(referer)
            except:
                pass
            try:
                origin = unquote_plus(origin)
            except:
                pass
            try:
                cookie = unquote_plus(cookie)
            except:
                pass            
            if referer:
                data.update({'Referer': referer})
            if origin:
                data.update({'Origin': origin})
            if cookie:
                data.update({'Cookie': cookie})
            if referer or origin or cookie:
                GLOBAL_HEADERS = data
        if not GLOBAL_HEADERS:
            GLOBAL_HEADERS = data
    
    def append_headers(self,headers):
        return '|%s' % '&'.join(['%s=%s' % (key, headers[key]) for key in headers])    
    
    def convert_to_m3u8(self,url):
        if '|' in url:
            url = url.split('|')[0]
        elif '&h123' in url:
            url = url.split('&h123')[0]
        # if '&' in url:
        #     url = url.split('&')[0]
        if not '.m3u8' in url and not '/hl' in url and int(url.count(":")) == 2 and int(url.count("/")) > 4:
            parsed_url = urlparse(url)
            try:
                host_part1 = '%s://%s'%(parsed_url.scheme,parsed_url.netloc)
                host_part2 = url.split(host_part1)[1]
                url = host_part1 + '/live' + host_part2
                file = self.basename(url)
                if '.ts' in file:
                    file_new = file.replace('.ts', '.m3u8')
                    url = url.replace(file, file_new)
                else:
                    file_new = file + '.m3u8'
                    url = url.replace(file, file_new)
            except:
                pass
        return url
    
    def ts(self,url,headers,head=False):
        global GLOBAL_URL
        global GLOBAL_HEADERS
        if not headers:
            headers = GLOBAL_HEADERS
        if GLOBAL_URL and not 'http' in url:
            url = GLOBAL_URL + url    
        if head:
            try:
                r = requests.head(url, headers=headers)
            except:
                pass
            return
        for i in range(30):
            i = i + 1
            try:
                r = requests.get(url, headers=headers, stream=True)
                if r.status_code == 200:
                    self.send_response(200)
                    self.send_header('Content-type','video/mp2t')
                    self.end_headers()
                    for chunk in r.iter_content(1024):
                        try:
                            self.wfile.write(chunk)
                        except:
                            pass
                r.close()
                break
            except:
                pass
            if i == 20:
                self.send_response(404)
                self.end_headers()
                def shutdown(server):
                    server.shutdown()
                t = threading.Thread(target=shutdown, args=(self.server, ))
                t.start()                
                break
    
    def m3u8(self,url,headers,head=False):
        global GLOBAL_URL
        if head:
            try:
                r = requests.head(url,headers=headers)
            except:
                pass
            return
        
        for i in range(20):
            i = i + 1          
            try:
                r = requests.get(url, headers=headers,timeout=2)
                r_parse = urlparse(r.url)
                base_url = "http://" + r_parse.netloc
                if r.status_code == 200:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/vnd.apple.mpegurl')
                    self.end_headers()
                    text_ = r.text
                    if '.html' in text_ and 'http' in text_:
                        text_ = text_.replace('http', 'http://'+HOST_NAME+':'+str(PORT_NUMBER)+'/?url=http')
                    elif 'chunklist_' in text_ and not 'http' in text_:
                        file = self.basename(url)
                        base_url = url.replace(file, '')
                        if base_url.endswith('/'):
                            base_url = base_url[:-1]
                        text_ = text_.replace('chunklist_', 'http://'+HOST_NAME+':'+str(PORT_NUMBER)+'/?url='+base_url+'/chunklist_')
                    elif 'media_' in text_ and '.ts' in text_ and not 'http' in text_:
                        file = self.basename(url)
                        base_url = url.replace(file, '')
                        if base_url.endswith('/'):
                            base_url = base_url[:-1]
                        text_ = text_.replace('media_', 'http://'+HOST_NAME+':'+str(PORT_NUMBER)+'/?url='+base_url+'/media_')
                    elif not '/hl' in text_ and not 'http' in text_:
                        file = self.basename(r.url)
                        base_url = r.url.replace(file, '')
                        GLOBAL_URL = base_url
                    elif '/hl' in text_ and not 'http' in text_:
                        text_ = text_.replace('/hl', 'http://'+HOST_NAME+':'+str(PORT_NUMBER)+'/?url='+base_url+'/hl')
                    else:
                        text_ = text_.replace('http', 'http://'+HOST_NAME+':'+str(PORT_NUMBER)+'/?url=http')
                    self.wfile.write(text_.encode("utf-8"))
                    r.close()
                    break
            except:
                pass
            try:
                r = requests.head(url,headers=headers,timeout=2)
            except:
                pass
            time.sleep(3)             
            if i == 8: # 24 segundos
                self.send_response(404)
                self.end_headers()
                def shutdown(server):
                    server.shutdown()
                t = threading.Thread(target=shutdown, args=(self.server, ))
                t.start()      
                break

    def do_HEAD(self):
        global GLOBAL_HEADERS
        global GLOBAL_URL
        try:
            url = self.path.split('url=')[1]
        except:
            url = ''
        try:
            url = unquote_plus(url)
        except:
            pass
        try:
            url = unquote(url)
        except:
            pass
        if url:
            self.get_headers(url)       
            url = self.convert_to_m3u8(url)
        if self.path == '/check':
            self.send_response(200)
            self.end_headers()
        elif self.path == '/stop':
            self.send_response(200)
            self.end_headers()

            def shutdown(server):
                server.shutdown()
            t = threading.Thread(target=shutdown, args=(self.server, ))
            t.start()                
        elif url.startswith('http') and '/hl' in url and '.m3u8' in url:
            self.m3u8(url,GLOBAL_HEADERS,head=True)
        elif not url.startswith('http') and '.m3u8' in self.path:
            if self.path.startswith('/'):
                path_url = self.path[1:]
            else:
                path_url = self.path
            url = GLOBAL_URL + path_url
            self.m3u8(url,GLOBAL_HEADERS,head=True)
        elif not 'http' in url and not '/hl' in url and '.ts' in self.path:
            self.ts(self.path,GLOBAL_HEADERS,head=True)
        elif url.endswith(".ts") or ('/hl' in url and not url.endswith(".ts") and not url.endswith(".m3u8")):
            self.ts(url,GLOBAL_HEADERS,head=True)
        elif url.endswith(".html"):
            self.ts(url,GLOBAL_HEADERS,head=True)
        elif '.m3u8' in url:
            self.m3u8(url,GLOBAL_HEADERS,head=True)    

    
    def do_GET(self):
        global GLOBAL_HEADERS
        global GLOBAL_URL
        try:
            url = self.path.split('url=')[1]
        except:
            url = ''
        try:
            url = unquote_plus(url)
        except:
            pass
        try:
            url = unquote(url)
        except:
            pass
        if url:
            self.get_headers(url)      
            url = self.convert_to_m3u8(url)
        if self.path == '/check':
            self.send_response(200)
            self.end_headers()            
        elif self.path == '/stop':
            self.send_response(200)
            self.end_headers()
            def shutdown(server):
                server.shutdown()
            t = threading.Thread(target=shutdown, args=(self.server, ))
            t.start()                
        elif url.startswith('http') and '/hl' in url and '.m3u8' in url:
            self.m3u8(url,GLOBAL_HEADERS)
        elif not url.startswith('http') and '.m3u8' in self.path:
            if self.path.startswith('/'):
                path_url = self.path[1:]
            else:
                path_url = self.path
            url = GLOBAL_URL + path_url
            self.m3u8(url,GLOBAL_HEADERS)
        elif not 'http' in url and not '/hl' in url and '.ts' in self.path:
            self.ts(self.path,GLOBAL_HEADERS)
        elif url.endswith(".ts") or ('/hl' in url and not url.endswith(".ts") and not url.endswith(".m3u8")):
            self.ts(url,GLOBAL_HEADERS)
        elif url.endswith(".html"):
            self.ts(url,GLOBAL_HEADERS)
        elif '.m3u8' in url:
            self.m3u8(url,GLOBAL_HEADERS)

httpd = HTTPServer(('', PORT_NUMBER), handler)
def serve_forever(httpd):
    with httpd:  # to make sure httpd.server_close is called
        httpd.serve_forever()#


class mediaserver:
    def __init__(self):
        self.server = threading.Thread(target=serve_forever, args=(httpd, ))
    
    def in_use(self):
        url = 'http://'+HOST_NAME+':'+str(PORT_NUMBER)+'/check'
        use = False
        try:
            r = requests.head(url,timeout=1)
            if r.status_code == 200:
                use = True
        except:
            pass
        return use 

    def start(self):
        if not self.in_use():
            self.server.start()
        time.sleep(3)

    def stop(self):
        httpd.shutdown()

def prepare_url(url):
    try:
        url = unquote_plus(url)
    except:
        pass
    try:
        url = unquote(url)
    except:
        pass
    url = url.replace('|', '&h123=true&')
    url = quote_plus(url)
    url = 'http://'+HOST_NAME+':'+str(PORT_NUMBER)+'/?url=' + url
    return url

def req_shutdown():
    url = 'http://'+HOST_NAME+':'+str(PORT_NUMBER)+'/stop'
    try:
        r = requests.get(url,timeout=2)
        r.close()
    except:
        pass

# try:
#     mediaserver().start()
# except KeyboardInterrupt:
#     mediaserver().stop()







    

