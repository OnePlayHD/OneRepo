# -*- coding: utf-8 -*-
import six
import re
try:
    from urllib.request import Request, urlopen # Python 3
except ImportError:
    from urllib2 import Request, urlopen # Python 2
from datetime import datetime
from bs4 import BeautifulSoup

def open_url(url,headers=False):
    try:
        req = Request(url)
        if headers:
            for key, value in headers.items():
                req.add_header(key, value)
        else:
            req.add_header('User-Agent', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36')
        count = 0 
        while True:
            count = count + 1
            try:
                response = urlopen(req, timeout=5)
                code = response.getcode()
            except:
                code = 500
            if code == 200 or count == 3:
                if code == 200:
                    data = response.read()
                    try:
                        data = data.decode('utf-8')
                    except:
                        pass
                elif not code == 200:
                    data = ''
                return data                
    except:
        data = ''
        return data


def getID_EPG(channel):
    if re.search("A&E",channel,re.IGNORECASE):
        channel_id = 'AE'
    elif re.search("AMC",channel,re.IGNORECASE):
        channel_id = 'AMC'
    elif re.search("Animal Planet",channel,re.IGNORECASE):
        channel_id = 'Animal-Planet'
    elif re.search("Arte 1",channel,re.IGNORECASE):
        channel_id = 'Arte-1'
    elif re.search("AXN",channel,re.IGNORECASE):
        channel_id = 'AXN'
    elif re.search("Baby TV",channel,re.IGNORECASE) or re.search("BabyTV",channel,re.IGNORECASE):
        channel_id = 'Baby-TV'
    elif re.search("Band",channel,re.IGNORECASE) and not re.search("Band News",channel,re.IGNORECASE) and not re.search("Band Sports",channel,re.IGNORECASE) and not re.search("BandNews",channel,re.IGNORECASE) and not re.search("Band Sports",channel,re.IGNORECASE):
        channel_id = 'Band'
    elif re.search("Band News",channel,re.IGNORECASE) or re.search("BandNews",channel,re.IGNORECASE) :
        channel_id = 'Band-News'
    elif re.search("Band Sports",channel,re.IGNORECASE) or re.search("BandSports",channel,re.IGNORECASE):
        channel_id = 'Band-Sports'
    elif re.search("BIS",channel,re.IGNORECASE):
        channel_id = 'Bis'
    elif re.search("Boomerang",channel,re.IGNORECASE):
        channel_id = 'Boomerang'
    elif re.search("Canal Brasil",channel,re.IGNORECASE):
        channel_id = 'Canal-Brasil'
    elif re.search("Cancao Nova",channel,re.IGNORECASE) or re.search("Canção Nova",channel,re.IGNORECASE):
        channel_id = 'TV-Cancao-Nova'
    elif re.search("Cartoon Network",channel,re.IGNORECASE):
        channel_id = 'Cartoon-Network'
    elif re.search("Cinemax",channel,re.IGNORECASE):
        channel_id = 'Cinemax'
    elif re.search("Combate",channel,re.IGNORECASE):
        channel_id = 'Combate'
    elif re.search("Comedy Central",channel,re.IGNORECASE):
        channel_id = 'Comedy-Central'
    elif re.search("Cultura",channel,re.IGNORECASE):
        channel_id = 'Cultura'
    elif re.search("Curta!",channel,re.IGNORECASE) or re.search("Curta",channel,re.IGNORECASE):
        channel_id = 'Curta'
    elif re.search("Discovery Channel",channel,re.IGNORECASE):
        channel_id = 'Discovery-Channel'
    elif re.search("Discovery Civilization",channel,re.IGNORECASE):
        channel_id = 'Discovery-Civilization'
    elif re.search("Discovery Home Health",channel,re.IGNORECASE) or re.search("Discovery H&H",channel,re.IGNORECASE) or re.search("Discovery Home & Health",channel,re.IGNORECASE):
        channel_id = 'Discovery-Home-and-Health'
    elif re.search("Discovery Kids",channel,re.IGNORECASE):
        channel_id = 'Discovery-Kids'
    elif re.search("Discovery Science",channel,re.IGNORECASE):
        channel_id = 'Discovery-Science'
    elif re.search("Discovery Theater",channel,re.IGNORECASE):
        channel_id = 'Discovery-Theater'
    elif re.search("Discovery Turbo",channel,re.IGNORECASE):
        channel_id = 'Discovery-Turbo'
    elif re.search("Discovery World",channel,re.IGNORECASE):
        channel_id = 'Discovery-World'
    elif re.search("Disney Channel",channel,re.IGNORECASE):
        channel_id = 'Disney-Channel'
    elif re.search("Disney Junior",channel,re.IGNORECASE) or re.search("Disney Jr",channel,re.IGNORECASE):
        channel_id = 'Disney-Junior'
    elif re.search("Disney XD",channel,re.IGNORECASE):
        channel_id = 'Disney-XD'
    elif re.search("Disney",channel,re.IGNORECASE):
        channel_id = 'Disney-Channel'
    elif re.search("E!",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("ESPN",channel,re.IGNORECASE) and not re.search("ESPN Brasil",channel,re.IGNORECASE) and not re.search("ESPN Extra",channel,re.IGNORECASE) and not re.search("ESPN 2",channel,re.IGNORECASE) and not re.search("ESPN 3",channel,re.IGNORECASE) and not re.search("ESPN 4",channel,re.IGNORECASE) and not re.search("ESPN2",channel,re.IGNORECASE) and not re.search("ESPN3",channel,re.IGNORECASE) and not re.search("ESPN4",channel,re.IGNORECASE):
        channel_id = 'ESPN'
    elif re.search("ESPN Brasil",channel,re.IGNORECASE):
        channel_id = 'ESPN-Brasil'
    elif re.search("ESPN 3",channel,re.IGNORECASE):
        channel_id = 'ESPN-mais'        
    elif re.search("ESPN Extra",channel,re.IGNORECASE) or re.search("ESPN+",channel,re.IGNORECASE) or re.search("ESPN Mais",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("FishTV",channel,re.IGNORECASE) or re.search("Fish TV",channel,re.IGNORECASE):
        channel_id = 'FishTV'
    elif re.search("Food Network",channel,re.IGNORECASE):
        channel_id = 'Food-Network'
    elif re.search("Fox News",channel,re.IGNORECASE):
        channel_id = 'Fox-News'        
    elif re.search("Fox Sports 2",channel,re.IGNORECASE):
        channel_id = 'Fox-Sports-2'
    elif re.search("Fox Sports",channel,re.IGNORECASE) or re.search("Fox Sports 1",channel,re.IGNORECASE):
        channel_id = 'Fox-Sports'        
    elif re.search("Futura",channel,re.IGNORECASE):
        channel_id = 'Futura'
    elif re.search("FX",channel,re.IGNORECASE) and not re.search("US",channel,re.IGNORECASE):
        channel_id = 'FX'
    elif re.search("Film & Arts",channel,re.IGNORECASE) or re.search("Film&Arts",channel,re.IGNORECASE):
        channel_id = 'Film-and-Arts'
    elif re.search("Globo Brasilia",channel,re.IGNORECASE) or re.search("Globo Brasília",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Globo Campinas",channel,re.IGNORECASE) or re.search("Globo EPTV Campinas",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Globo Minas",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Globo News",channel,re.IGNORECASE) or re.search("GloboNews",channel,re.IGNORECASE):
        channel_id = 'Globo-News'
    elif re.search("Globo RBS TV Poa",channel,re.IGNORECASE) or re.search("RBS TV",channel,re.IGNORECASE) or re.search("RBS Porto Alegre",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Globo RJ",channel,re.IGNORECASE):
        channel_id = 'Globo'
    elif re.search("Globo SP",channel,re.IGNORECASE):
        channel_id = 'Globo'
    elif re.search("Globo TV Anhanguera",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Globo TV Bahia",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Globo TV Tem Bauru",channel,re.IGNORECASE) or re.search("TV Tem Bauru",channel,re.IGNORECASE) or re.search("TVTem Bauru",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Globo TV Tribuna",channel,re.IGNORECASE) or re.search("TV Tribuna",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Globo TV Vanguarda",channel,re.IGNORECASE) or re.search("TV Vanguarda",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Globo Inter TV Alto Litoral",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Globo Inter TV Grande Minas",channel,re.IGNORECASE) or re.search("Globo Inter TV Minas",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Globo NSC Florianopolis",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Globo Nordeste",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Globo RPC Parana",channel,re.IGNORECASE) or re.search("Globo RPC Curitiba",channel,re.IGNORECASE) or re.search("RPC",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Gloob",channel,re.IGNORECASE):
        channel_id = 'Gloob'
    elif re.search("GNT",channel,re.IGNORECASE):
        channel_id = 'GNT'
    elif re.search("HBO 2",channel,re.IGNORECASE):
        channel_id = 'HBO2'
    elif re.search("HBO Family",channel,re.IGNORECASE):
        channel_id = 'HBO-Family'
    elif re.search("HBO Plus",channel,re.IGNORECASE):
        channel_id = 'HBO-Plus'
    elif re.search("HBO Signature",channel,re.IGNORECASE):
        channel_id = 'HBO-Signature'
    elif re.search("HBO Mundi",channel,re.IGNORECASE) or re.search("Max HD",channel,re.IGNORECASE):
        channel_id = 'Max-HD'
    elif re.search("HBO Extreme",channel,re.IGNORECASE) or re.search("Max Prime",channel,re.IGNORECASE):
        channel_id = 'Max-Prime'
    elif re.search("HBO Pop",channel,re.IGNORECASE) or re.search("Max UP",channel,re.IGNORECASE):
        channel_id = 'Max-Up'
    elif re.search("HBO",channel,re.IGNORECASE):
        channel_id = 'HBO'        
    elif re.search("History 2",channel,re.IGNORECASE) and not re.search("H26",channel,re.IGNORECASE) or re.search("H2",channel,re.IGNORECASE) and not re.search("H26",channel,re.IGNORECASE):
        channel_id = 'H2'        
    elif re.search("History Channel",channel,re.IGNORECASE) or re.search("History",channel,re.IGNORECASE):
        channel_id = 'The-History-Channel'
    elif re.search("Ideal TV",channel,re.IGNORECASE):
        channel_id = 'Ideal-TV'
    elif re.search("Investigação Discovery",channel,re.IGNORECASE) or re.search("Investigacao Discovery",channel,re.IGNORECASE):
        channel_id = 'Investigacao-Discovery-ID'
    elif re.search("i.Sat",channel,re.IGNORECASE):
        channel_id = 'i-Sat'
    elif re.search("Lifetime",channel,re.IGNORECASE):
        channel_id = 'Lifetime'
    elif re.search("Mais GloboSat",channel,re.IGNORECASE) or re.search("Mais na Tela",channel,re.IGNORECASE):
        channel_id = 'Globosat'
    elif re.search("Megapix",channel,re.IGNORECASE):
        channel_id = 'Megapix'
    elif re.search("MTV",channel,re.IGNORECASE) and not re.search("US",channel,re.IGNORECASE):
        channel_id = 'MTV'
    elif re.search("Multishow",channel,re.IGNORECASE):
        channel_id = 'Multishow'
    elif re.search("NatGeo Kids",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Nat Geo Kids",channel,re.IGNORECASE) and not re.search("Nat Geo Wild",channel,re.IGNORECASE) and not re.search("National Geographic",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Nat Geo Wild",channel,re.IGNORECASE) or re.search("National Geographic Wild",channel,re.IGNORECASE):
        channel_id = 'NatGeo-Wild-HD'
    elif re.search("National Geographic",channel,re.IGNORECASE):
        channel_id = 'National-Geographic'
    elif re.search("NBR",channel,re.IGNORECASE):
        channel_id = 'NBR'
    elif re.search("Nickelodeon",channel,re.IGNORECASE) and not re.search("Nick Jr",channel,re.IGNORECASE) and not re.search("Nick Junior",channel,re.IGNORECASE):
        channel_id = 'Nickelodeon'
    elif re.search("Nick Jr",channel,re.IGNORECASE):
        channel_id = 'Nick-Jr'
    elif re.search("Novo Tempo",channel,re.IGNORECASE):
        channel_id = 'TV-Novo-Tempo'
    elif re.search("Off",channel,re.IGNORECASE) and not re.search("CNN",channel,re.IGNORECASE):
        channel_id = 'Off'
    elif re.search("PlayBoy",channel,re.IGNORECASE):
        channel_id = 'Playboy-TV'
    elif re.search("Paramount",channel,re.IGNORECASE):
        channel_id = 'Paramount'
    elif re.search("Premiere 2",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Premiere 3",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Premiere 4",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Premiere 5",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Premiere 6",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Premiere 7",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Premiere 8",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Premiere 9",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Premiere Clubes",channel,re.IGNORECASE):
        channel_id = 'Premiere-Futebol-Clube'
    elif re.search("Prime Box",channel,re.IGNORECASE):
        channel_id = 'Prime-Box-Brazil'
    elif re.search("Ra Tim Bum",channel,re.IGNORECASE):
        channel_id = 'TV-Ra-Tim-Bum'
    elif re.search("Record News",channel,re.IGNORECASE):
        channel_id = 'Record-News'
    elif re.search("RecordTV",channel,re.IGNORECASE) or re.search("Record TV",channel,re.IGNORECASE) or re.search("Record SP",channel,re.IGNORECASE):
        channel_id = 'Record'
    elif re.search("Rede Brasil",channel,re.IGNORECASE):
        channel_id = 'Rede-Brasil'
    elif re.search("Rede TV",channel,re.IGNORECASE) or re.search("RedeTV",channel,re.IGNORECASE):
        channel_id = 'RedeTV'
    elif re.search("Rede Vida",channel,re.IGNORECASE):
        channel_id = 'Rede-Vida'
    elif re.search("Rede Amazonica",channel,re.IGNORECASE) or re.search("Rede Amazonas",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("RIT",channel,re.IGNORECASE):
        channel_id = 'RIT-TV'
    elif re.search("SBT",channel,re.IGNORECASE):
        channel_id = 'SBT'
    elif re.search("Sexy Hot",channel,re.IGNORECASE) or re.search("SexyHot",channel,re.IGNORECASE):
        channel_id = 'Sexy-Hot'
    elif re.search("Sony",channel,re.IGNORECASE):
        channel_id = 'Sony'
    elif re.search("Space",channel,re.IGNORECASE):
        channel_id = 'Space'
    elif re.search("Sportv",channel,re.IGNORECASE) and not re.search("Sportv 2",channel,re.IGNORECASE) and not re.search("Sportv 3",channel,re.IGNORECASE):
        channel_id = 'SporTV'
    elif re.search("Sportv 2",channel,re.IGNORECASE):
        channel_id = 'SporTV2'
    elif re.search("Sportv 3",channel,re.IGNORECASE):
        channel_id = 'SporTV3'
    elif re.search("Studio Universal",channel,re.IGNORECASE):
        channel_id = 'Studio-Universal'
    elif re.search("Syfy",channel,re.IGNORECASE):
        channel_id = 'Syfy'
    elif re.search("TBS",channel,re.IGNORECASE):
        channel_id = 'TBS'
    elif re.search("TCM",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Telecine Action",channel,re.IGNORECASE):
        channel_id = 'Telecine-Action'
    elif re.search("Telecine Cult",channel,re.IGNORECASE):
        channel_id = 'Telecine-Cult'
    elif re.search("Telecine Fun",channel,re.IGNORECASE):
        channel_id = 'Telecine-Fun'
    elif re.search("Telecine Pipoca",channel,re.IGNORECASE):
        channel_id = 'Telecine-Pipoca'
    elif re.search("Telecine Premium",channel,re.IGNORECASE):
        channel_id = 'Telecine-Premium'
    elif re.search("Telecine Touch",channel,re.IGNORECASE):
        channel_id = 'Telecine-Touch'
    elif re.search("Terra Viva",channel,re.IGNORECASE):
        channel_id = 'Terra-Viva'
    elif re.search("TLC",channel,re.IGNORECASE):
        channel_id = 'TLC'
    elif re.search("TNT",channel,re.IGNORECASE) and not re.search("TNT Series",channel,re.IGNORECASE) and not re.search("TNT Séries",channel,re.IGNORECASE) and not re.search("TNT Sports",channel,re.IGNORECASE) and not re.search("TNTSports",channel,re.IGNORECASE):
        channel_id = 'TNT'
    elif re.search("TNT Series",channel,re.IGNORECASE) or re.search("TNT Séries",channel,re.IGNORECASE):
        channel_id = 'TNT-Series'
    elif re.search("Tooncast",channel,re.IGNORECASE):
        channel_id = 'Tooncast'
    elif re.search("truTV",channel,re.IGNORECASE):
        channel_id = 'truTV'
    elif re.search("TV Aparecida",channel,re.IGNORECASE):
        channel_id = 'TV-Aparecida'
    elif re.search("HGTV Brasil",channel,re.IGNORECASE):
        channel_id = ''       
    elif re.search("Tv Brasil",channel,re.IGNORECASE):
        channel_id = 'TV-Brasil'
    elif re.search("Tv Camara",channel,re.IGNORECASE) or re.search("Tv Câmara",channel,re.IGNORECASE):
        channel_id = 'TV-Camara'
    elif re.search("Tv Diario Fortaleza",channel,re.IGNORECASE) or re.search("Tv Diário",channel,re.IGNORECASE) or re.search("Tv Diario",channel,re.IGNORECASE) :
        channel_id = ''
    elif re.search("Tv Escola",channel,re.IGNORECASE):
        channel_id = 'TV-Escola'
    elif re.search("TV Gazeta Alagoas",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("TV Gazeta",channel,re.IGNORECASE) and not re.search("TV Gazeta Sul",channel,re.IGNORECASE) and not re.search("TV Gazeta Vitoria",channel,re.IGNORECASE):
        channel_id = 'Gazeta'
    elif re.search("Tv Justica",channel,re.IGNORECASE) or re.search("Tv Justiça",channel,re.IGNORECASE):
        channel_id = 'TV-Justica'
    elif re.search("TV Liberal Belem",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Tv Senado",channel,re.IGNORECASE):
        channel_id = 'TV-Senado'
    elif re.search("Tv Verdes Mares",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("VH1",channel,re.IGNORECASE) and not re.search("VH1 Megahits",channel,re.IGNORECASE):
        channel_id = 'Vh1'
    elif re.search("VH1 Megahits",channel,re.IGNORECASE):
        channel_id = 'Vh1-Mega-Hits'
    elif re.search("Viva",channel,re.IGNORECASE):
        channel_id = 'Viva'
    elif re.search("Warner Channel",channel,re.IGNORECASE) or re.search("Warner",channel,re.IGNORECASE):
        channel_id = 'Warner-Channel'
    elif re.search("WooHoo",channel,re.IGNORECASE):
        channel_id = 'Woohoo'
    elif re.search("Zoomoo",channel,re.IGNORECASE):
        channel_id = 'Zoomoo'
    elif re.search("CNN Brasil",channel,re.IGNORECASE) and not re.search("CNN INTERNACIONAL",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("CNN INTERNACIONAL",channel,re.IGNORECASE):
        channel_id = 'CNN-International'        
    elif re.search("Jovem Pan News",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Star Channel",channel,re.IGNORECASE) or re.search("Fox Channel",channel,re.IGNORECASE):
        channel_id = 'Fox'
    elif re.search("Star Hits 2",channel,re.IGNORECASE) or re.search("Fox Premium 2",channel,re.IGNORECASE):
        channel_id = ''    
    elif re.search("Star Hits",channel,re.IGNORECASE) or re.search("Fox Premium 1",channel,re.IGNORECASE):
        channel_id = 'Fox1'
    elif re.search("Star Life",channel,re.IGNORECASE) or re.search("Fox Life",channel,re.IGNORECASE):
        channel_id = 'Fox-Life'
    elif re.search("Conmebol TV 1",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Conmebol TV 2",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Conmebol TV 3",channel,re.IGNORECASE):
        channel_id = ''
    elif re.search("Conmebol TV 4",channel,re.IGNORECASE):
        channel_id = ''                                                           
    elif re.search("Universal Channel",channel,re.IGNORECASE) or re.search("Universal TV",channel,re.IGNORECASE):
        channel_id = 'Universal-Channel'
    elif re.search("Sex Prive",channel,re.IGNORECASE) or re.search("Sex Privé",channel,re.IGNORECASE):
        channel_id = 'Sex-Prive-Brasileirinhas'              
    else:
        channel_id = ''
    return channel_id


def get_channel_epg(chanid):
    mytime = datetime.now()
    url = 'https://www.tvmap.com.br/' + chanid
    mytime = mytime.strftime('%d%H%M')
    if chanid:
        r = open_url(url)
    else:
        r = False
    epg_final = []
    if r:
        try:
            soup = BeautifulSoup(r, 'html.parser')
            ul = soup.find("ul", {"id": "timelineul"})
            li = ul.find_all("li")
            time1 = [] #pegar ultimo
            time2 = [] #pegar primeiro        
            if li:
                #ocorrencia 1
                for i in li:
                    day = i.find("div", {"class": "datebox"}).find("p").get("title")
                    try:
                        day = day.split(", ")[1]
                        day = day.split(" de")[0]
                        day = day.replace(" ","")
                    except:
                        day = False
                    t = i.find("div", {"class": "hourbox"}).find("span").text #time
                    t = t.replace(" h", "")
                    if day:
                        time_compare = t.replace(":", "")
                        time_compare = day + time_compare
                        if int(time_compare) <= int(mytime):
                            time1.append(time_compare)
                #ocorrencia 2
                for i in li:
                    day = i.find("div", {"class": "datebox"}).find("p").get("title")
                    try:
                        day = day.split(", ")[1]
                        day = day.split(" de")[0]
                        day = day.replace(" ","")
                    except:
                        day = False
                    t = i.find("div", {"class": "hourbox"}).find("span").text #time
                    t = t.replace(" h", "")
                    if day:
                        time_compare = t.replace(":", "")
                        time_compare = day + time_compare
                        if int(mytime) < int(time_compare):
                            time2.append(time_compare)
                #comparar
                if time1 and time2:
                    for i in li:
                        title = i.find("div", {"class": "timelineheader"}).find("a").text
                        try:
                            desc = i.find("div", {"class": "text_exposed_root"}).text
                        except:
                            desc = ''
                        day = i.find("div", {"class": "datebox"}).find("p").get("title")
                        try:
                            day = day.split(", ")[1]
                            day = day.split(" de")[0]
                            day = day.replace(" ","")
                        except:
                            day = False
                        t = i.find("div", {"class": "hourbox"}).find("span").text #time
                        t = t.replace(" h", "")
                        if day:
                            time_compare = t.replace(":", "")
                            time_compare = day + time_compare
                            if int(time1[-1]) <= int(time_compare) < int(time2[0]):
                                t_hour = time2[0][2:-2]
                                t_minute = time2[0][4:]
                                epg = '\n[COLOR aquamarine][B]' + str(t) + '[/B] ' + title + '[/COLOR]'
                                encerra = '\n\n[COLOR orange][B]TERMINA ÀS:[/B][/COLOR] ' + str(t_hour) + ':' + str(t_minute)
                                if desc:
                                    sinopse = '\n\n[COLOR lime][B]SINOPSE:[/B][/COLOR] '+ desc
                                else:
                                    sinopse = '\n\n[COLOR lime][B]SINOPSE:[/B][/COLOR] Indisponivel'
                                try:
                                    epg = epg.decode('utf-8')
                                except:
                                    pass
                                try:
                                    encerra = encerra.decode('utf-8')
                                except:
                                    pass
                                try:
                                    sinopse = sinopse.decode('utf-8')
                                except:
                                    pass                       
                                desc_epg = encerra+sinopse
                                epg_final.append((epg,desc_epg))
                                break
        except:
            pass
    if epg_final:
        epg = epg_final[0][0]
        desc_epg = epg_final[0][1]
    else:
        epg = '\n[COLOR orange][B]Epg indisponivel[/B][/COLOR]'
        desc_epg = ''
    if six.PY2:
        try:
            epg = epg.encode('utf-8', 'ignore')
        except:
            pass
        try:
            desc_epg = desc_epg.encode('utf-8', 'ignore')
        except:
            pass
    return epg,desc_epg