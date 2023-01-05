import requests

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'

class browser:
    def get_url(self,url,headers=False,post=False):
        self.url = url
        self.headers = headers
        self.post = post
        if not self.headers:
            self.headers = {'User-Agent': UA, 'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'}
        if self.post:
            try:
                req = requests.post(url=self.url,headers=self.headers,data=self.post,verify=False)
                status = True
            except:
                status = False
        else:
            try:
                req = requests.get(url=self.url,headers=self.headers,verify=False)
                status = True
            except:
                status = False
        if status:
            return req.content
        else:
            return False

request = browser()