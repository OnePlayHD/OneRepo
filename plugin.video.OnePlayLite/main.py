# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf8')

import urllib
import urllib2
import datetime
from datetime import datetime
import xml.etree.ElementTree as ET
import re
import os
import base64
import codecs
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import traceback
import time
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP

Versao = "31.01.2020"

##CONFIGURAÇÕES
####  TITULO DO MENU  #################################################################
title_menu = '[B][COLOR aquamarine]:::[/COLOR][COLOR white]BEM-VINDOS AO ONEPLAY LITE[/COLOR][COLOR aquamarine]:::[/COLOR][/B]'
###  DESCRIÇÃO DO ADDON ###############################################################
url_title_descricao = 'https://pastebin.com/raw/gVEzmZwm'
####  LINK DO TITULO DE MENU  #########################################################
## OBS: POR PADRÃO JÁ TEM UM MENU EM BRANCO PARA NÃO TER ERRO AO CLICAR ###############
url_b64_title = '\x61\x48\x52\x30\x63\x44\x6f\x76\x4c\x32\x4a\x70\x64\x43\x35\x73\x65\x53\x39\x50\x62\x6d\x56\x51\x62\x47\x46\x35\x56\x6b\x6c\x51'
url_title = base64.b64decode(url_b64_title)

#### MENSAGEM BEM VINDOS  #############################################################
titulo_boas_vindas = 'BEM-VINDOS'
mensagem_bem_vindo = 'Que bom que você chegou!... Que sua jornada por aqui seja longa e repleta de alegria, Espero que possamos progredir juntos, evoluir lado a lado e crescer como iguais.\n\r[B]Seremos um time!  [COLOR aquamarine]#EQUIPE ONEPLAY[/COLOR][/B]'
####  MENSAGEM SECUNDARIA ######################################################
url_mensagem = 'https://pastebin.com/raw/gZHzn7v9'
####  TEMPO DA MENSAGEM EM MILISEGUNDOS ###############################################
time_msg = 15000

##### PESQUISA - get.php
url_b64_pesquisa = '\x61\x48\x52\x30\x63\x48\x4d\x36\x4c\x79\x39\x76\x62\x6d\x56\x77\x62\x47\x46\x35\x61\x47\x51\x75\x59\x32\x39\x74\x4c\x31\x42\x46\x55\x31\x46\x56\x53\x56\x4e\x42\x4c\x32\x64\x6c\x64\x43\x35\x77\x61\x48\x41\x3d'
url_pesquisa = base64.b64decode(url_b64_pesquisa)
menu_pesquisar = '[COLOR white][B]PESQUISAR...[/B][/COLOR]'
thumb_pesquisar = 'https://i.imgur.com/EinrK5v.png'
fanart_pesquisar = 'https://i.imgur.com/Cr8VMcr.jpg'
mensagem_busca_invalida = 'Digite Algo!'
#### Descrição Pesquisa
url_desc_pesquisa = 'https://pastebin.com/raw/jy1i34SJ'
## MENU ATUALIZAÇÃO
menu_atualizacao = '[B][COLOR aquamarine]ATUALIZAÇÃO[/COLOR][/B]'
thumb_update = 'https://i.imgur.com/flpknUR.png'
desc_atualizacao = 'Faça atualização automática no ONEPLAY usando esse recurso, só entrar que a atualização é verificada e atualizado.'
## MENU CONFIGURAÇÕES
menu_configuracoes = '[B][COLOR white]CONFIGURAÇÕES[/COLOR][/B]'
thumb_icon_config = 'https://i.imgur.com/PuULJQp.png'
desc_configuracoes = 'Desativar ou ativar as configurações de notificações e a área VIP do ONEPLAY'

#### MENU VIP ################################################################
titulo_vip = '[COLOR aquamarine][B]ÁREA DE ACESSO[/B][/COLOR] [COLOR gold][B](VIP)[/B][/COLOR]'
thumbnail_vip = 'https://i.imgur.com/5rgqF8K.png'
fanart_vip = 'https://i.imgur.com/nTIPRcu.png'
#### DESCRIÇÃO VIP ###########################################################
url_vip_descricao = 'https://pastebin.com/raw/0ZXHJ06u'
#### DIALOGO VIP - SERVIDOR DESATIVADO - CLICK ###################################
url_vip_dialogo = 'https://pastebin.com/raw/6wTe6Kgd'
##SERIVODR VIP
url_server_vip = 'http://psrv.io:80/get.php'


## MULTLINK
## nome para $nome, padrão: lsname para $lsname
playlist_command = 'nome'
dialog_playlist = 'Selecione um item'


# user - Padrão: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0
useragent = base64.b32decode('\x47\x41\x58\x44\x41\x4c\x52\x54\x46\x35\x34\x54\x49\x4d\x4b\x51\x4d\x56\x58\x44\x41\x3d\x3d\x3d')

#Base
url_b64_principal = '\x61\x48\x52\x30\x63\x48\x4d\x36\x4c\x79\x39\x33\x64\x33\x63\x75\x62\x32\x35\x6c\x63\x47\x78\x68\x65\x57\x68\x6b\x4c\x6d\x4e\x76\x62\x53\x39\x42\x59\x32\x56\x7a\x63\x32\x39\x51\x63\x6d\x39\x70\x59\x6d\x6c\x6b\x62\x79\x39\x42\x5a\x47\x52\x76\x62\x69\x39\x50\x62\x6d\x56\x51\x62\x47\x46\x35\x54\x47\x6c\x30\x5a\x53\x39\x51\x63\x6d\x6c\x75\x59\x32\x6c\x77\x59\x57\x77\x75\x61\x48\x52\x74\x62\x41\x3d\x3d'
url_principal = base64.b64decode(url_b64_principal)


if sys.argv[1] == 'clearEPG':
    Path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode("utf-8")
    arquivo = os.path.join(Path, "RHAEPG.xml")
    exists = os.path.isfile(arquivo)
    if exists:
        try:
            os.remove(arquivo)
        except:
            pass
    xbmcaddon.Addon().setSetting("epg_last", "")
    xbmcgui.Dialog().ok('Sucesso', '[B][COLOR yellow]EPG excluído com sucesso![/COLOR][/B]', 'Não se esqueça de salvar as configurações clicando em OK.')
    xbmc.sleep(2000)
    exit()
   

if sys.argv[1] == 'SetPassword':
    addonID = xbmcaddon.Addon().getAddonInfo('id')
    addon_data_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', addonID))
    if os.path.exists(addon_data_path)==False:
        os.mkdir(addon_data_path)
    xbmc.sleep(4)
    #Path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode("utf-8")
    #arquivo = os.path.join(Path, "password.txt")
    arquivo = os.path.join(addon_data_path, "password.txt")
    exists = os.path.isfile(arquivo)
    keyboard = xbmcaddon.Addon().getSetting("keyboard")    
    if exists == False:
        password = '0069'
        p_encoded = base64.b64encode(password.encode()).decode('utf-8')
        p_file1 = open(arquivo,'w')
        p_file1.write(p_encoded)
        p_file1.close()
        xbmc.sleep(4)
        p_file = open(arquivo,'r+')
        p_file_read = p_file.read()
        p_file_b64_decode = base64.b64decode(p_file_read).decode('utf-8')
        dialog = xbmcgui.Dialog()
        if int(keyboard) == 0:
            ps = dialog.numeric(0, 'Insira a senha atual:')
        else:            
            ps = dialog.input('Insira a senha atual:', option=xbmcgui.ALPHANUM_HIDE_INPUT)
        if ps == p_file_b64_decode:
            if int(keyboard) == 0:
                ps2 = dialog.numeric(0, 'Insira a nova senha:')
            else:
                ps2 = dialog.input('Insira a senha atual:', option=xbmcgui.ALPHANUM_HIDE_INPUT)
            if ps2 != '':
                ps2_b64 = base64.b64encode(ps2.encode()).decode('utf-8')
                p_file = open(arquivo,'w')
                p_file.write(ps2_b64)
                p_file.close()
                xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','A Senha foi alterada com sucesso!')
            else:
                xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Não foi possivel alterar a senha!')
        else:
            xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Senha invalida!, se não alterou utilize a senha padrão')                
    else:
        p_file = open(arquivo,'r+')
        p_file_read = p_file.read()
        p_file_b64_decode = base64.b64decode(p_file_read).decode('utf-8')
        dialog = xbmcgui.Dialog()
        if int(keyboard) == 0:
            ps = dialog.numeric(0, 'Insira a senha atual:')
        else:
            ps = dialog.input('Insira a senha atual:', option=xbmcgui.ALPHANUM_HIDE_INPUT)
        if ps == p_file_b64_decode:
            if int(keyboard) == 0:
                ps2 = dialog.numeric(0, 'Insira a nova senha:')
            else:
                ps2 = dialog.input('Insira a senha atual:', option=xbmcgui.ALPHANUM_HIDE_INPUT)
            if ps2 != '':
                ps2_b64 = base64.b64encode(ps2.encode()).decode('utf-8')
                p_file = open(arquivo,'w')
                p_file.write(ps2_b64)
                p_file.close()
                xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','A Senha foi alterada com sucesso!')
            else:
                xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Não foi possivel alterar a senha!')
        else:
            xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Senha invalida!, se não alterou utilize a senha padrão') 
    exit()
    

epg_url = "http://bit.ly/one_epg"
epgEnabled = xbmcaddon.Addon().getSetting("epg")
epgLast = xbmcaddon.Addon().getSetting("epg_last")
epgDays = xbmcaddon.Addon().getSetting("epg_days")


addon_handle = int(sys.argv[1])
__addon__ = xbmcaddon.Addon()
addon = __addon__
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
addon_version = __addon__.getAddonInfo('version')
profile = xbmc.translatePath(__addon__.getAddonInfo('profile').decode('utf-8'))
home = xbmc.translatePath(__addon__.getAddonInfo('path').decode('utf-8'))



def notify(message, timeShown=5000):
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, message, timeShown, __icon__))



def getRequest(url, count):
    proxy_mode = addon.getSetting('proxy')
    if proxy_mode == 'true':
        try:
            import requests
            import random
            headers={'User-agent': useragent, 
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
            'Content-Type': 'text/html'}       
            if int(count) > 0:
                attempt = int(count)-1
            else:
                attempt = 0 
            #print('tentativa: '+str(attempt)+'')
            ### https://proxyscrape.com/free-proxy-list
            ##http            
            data_proxy1 = getRequest2('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=BR&ssl=no&anonymity=anonymous', '')
            list1 = data_proxy1.splitlines()
            total1 = len(list1)
            number_http = random.randint(1,total1)
            proxy_http = 'http://'+list1[number_http]+''
            ##https
            data_proxy2 = getRequest2('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=BR&ssl=yes&anonymity=all', '')
            list2 = data_proxy2.splitlines()
            total2 = len(list2)
            number_https = random.randint(1,total2)
            proxy_https = 'https://'+list2[number_https]+''
            #print(proxy_https)
            proxyDict = {"http" : proxy_http, "https" : proxy_https}
            req = requests.get(url, headers=headers, proxies=proxyDict)
            req.encoding = 'utf-8'
            #status = req.status_code
            response = req.text
            return response
        except:
            proxy_number = addon.getSetting('proxy_try')
            if int(attempt) > 0:
                limit = int(attempt)
            elif int(count) == 1 and int(attempt) == 0:
                limit = int(proxy_number)+1+1
            if int(limit) > 1:
                #print('ativar outro proxy')
                data = getRequest(url, int(limit))         
                return data
            else:
                notify('[COLOR red]Erro ao utilizar o proxy ou servidor![/COLOR]')
                response = ''
                return response
                
    else:
        try:
            try:
                import urllib.request as urllib2
            except ImportError:
                import urllib2
            request_headers = {    
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,ru;q=0.7,de-DE;q=0.6,de;q=0.5,de-AT;q=0.4,de-CH;q=0.3,ja;q=0.2,zh-CN;q=0.1,zh;q=0.1,zh-TW;q=0.1,es;q=0.1,ar;q=0.1,en-GB;q=0.1,hi;q=0.1,cs;q=0.1,el;q=0.1,he;q=0.1,en-US;q=0.1",
            "User-Agent": useragent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
            }
            request = urllib2.Request(url, headers=request_headers)
            response = urllib2.urlopen(request).read().decode('utf-8')
            return response
        except urllib2.URLError, e:            
            if hasattr(e, 'code'):
                xbmc.executebuiltin("XBMC.Notification(Falha, código de erro - "+str(e.code)+",10000,"+__icon__+")")               
            elif hasattr(e, 'reason'):
                xbmc.executebuiltin("XBMC.Notification(Falha, motivo - "+str(e.reason)+",10000,"+__icon__+")")
            response = ''
            return response





def getRequest2(url, ref):
    try:
        try:
            import urllib.request as urllib2
        except ImportError:
            import urllib2
        if ref > '':
            ref2 = ref
        else:
            ref2 = url
        request_headers = {    
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,ru;q=0.7,de-DE;q=0.6,de;q=0.5,de-AT;q=0.4,de-CH;q=0.3,ja;q=0.2,zh-CN;q=0.1,zh;q=0.1,zh-TW;q=0.1,es;q=0.1,ar;q=0.1,en-GB;q=0.1,hi;q=0.1,cs;q=0.1,el;q=0.1,he;q=0.1,en-US;q=0.1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Referer": ref2
        }
        request = urllib2.Request(url, headers=request_headers)
        response = urllib2.urlopen(request).read().decode('utf-8')
        return response
    except:
        #pass
        response = ''
        return response



def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r


def re_me(data, re_patten):
    match = ''
    m = re.search(re_patten, data)
    if m != None:
        match = m.group(1)
    else:
        match = ''
    return match 


def resolve_data(url):
    if url.startswith(url_server_vip) == True:
        data = getRequest2(url, '')
    else:
        data = getRequest(url, 1)
    return data
    

def getData(url, fanart):
    adult = xbmcaddon.Addon().getSetting("adult")
    uhdtv = addon.getSetting('uhdtv')
    fhdtv = addon.getSetting('fhdtv')
    hdtv = addon.getSetting('hdtv')
    sdtv = addon.getSetting('sdtv')
    futebol = addon.getSetting('futebol')
    data = resolve_data(url)
    #soup = BeautifulSoup(data, 'html.parser')
    soup = BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
    #if isinstance(soup,BeautifulSoup):
    if isinstance(soup,BeautifulSOAP):
        #if len(soup('layoutype')) > 0:
        #    SetViewLayout = "thumbnail"		    

        if len(soup('channels')) > 0:
            channels = soup('channel')
            for channel in channels:
#                print channel

                linkedUrl=''
                lcount=0
                try:
                    linkedUrl =  channel('externallink')[0].string
                    lcount=len(channel('externallink'))
                except: pass
                #print 'linkedUrl',linkedUrl,lcount
                if lcount>1: linkedUrl=''

                name = channel('name')[0].string
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    thumbnail = ''

                try:
                    if not channel('fanart'):
                        if __addon__.getSetting('use_thumb') == "true":
                            fanArt = thumbnail
                        else:
                            fanArt = fanart
                    else:
                        fanArt = channel('fanart')[0].string
                    if fanArt == None:
                        raise                      
                except:
                    fanArt = fanart

                try:
                    desc = channel('info')[0].string
                    if desc == None:
                        raise
                except:
                    desc = ''

                try:
                    if linkedUrl=='':
                        #addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),2,thumbnail,fanArt,desc,genre,date,credits,True)
                        addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),2,thumbnail,fanArt,desc)
                    else:
                        #print linkedUrl
                        #addDir(name.encode('utf-8'),linkedUrl.encode('utf-8'),1,thumbnail,fanArt,desc,genre,date,None,'source')
                        if adult == 'false' and re.search("ADULTOS",name,re.IGNORECASE) and name.find('(+18)') >=0:
                            pass
                        else:
                            addDir(name.encode('utf-8', 'ignore'),linkedUrl.encode('utf-8'),1,thumbnail,fanArt,desc)
                except:
                    notify('[COLOR red]Erro ao Carregar os dados![/COLOR]')
        elif re.search("#EXTM3U",data) or re.search("#EXTINF",data):
            if epgEnabled == "true": epginfo = epgParseData()
            content = data.rstrip()
            match = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\r\n]+)').findall(content)
            for other,channel_name,stream_url in match:
                if 'tvg-logo' in other:
                    thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
                    if thumbnail:
                        if thumbnail.startswith('http'):
                            thumbnail = thumbnail
                        #elif not addon.getSetting('logo-folderPath') == "":
                        #    logo_url = addon.getSetting('logo-folderPath')
                        #    thumbnail = logo_url + thumbnail

                        else:
                            thumbnail = ''
                    else:
                        thumbnail = ''
                else:
                    thumbnail = ''
                try:
                    if xbmcaddon.Addon().getSetting("epg") == "true":
                        if uhdtv == 'false' and re.search("4K",channel_name):
                            pass
                        elif fhdtv == 'false' and re.search("FHD",channel_name):
                            pass
                        elif hdtv == 'false' and re.search("HD",channel_name):
                            pass
                        elif sdtv == 'false' and re.search("SD",channel_name):
                            pass
                        elif futebol == 'true' and not re.search("SPORTV",channel_name,re.IGNORECASE) and not re.search("DAZN",channel_name,re.IGNORECASE) and not re.search("ESPN Brasil",channel_name,re.IGNORECASE) and not re.search("PREMIERE",channel_name,re.IGNORECASE):
                            pass
                        else:
                            epg, desc_epg = getEPG(epginfo,getID_EPG(channel_name))
                        name1 = channel_name+epg.replace('&amp;', '&').replace("&#39;", "'")
                        cleaname = channel_name
                        desc1 = desc_epg.replace('&amp;', '&').replace("&#39;", "'")
                    else:
                        name1 = channel_name
                        cleaname = ''
                        desc1 = ''
                except:
                    name1 = channel_name
                    cleaname = ''
                    desc1 = ''
                 
                try:
                    if url.startswith(url_server_vip) == True:
                        resolver_final = resolver_vip(stream_url, channel_name, thumbnail)
                    else:
                       resolver_final = resolver(stream_url, channel_name, thumbnail)
                    #addLink(channel_name.encode('utf-8', 'ignore'), resolver(stream_url, channel_name).encode('utf-8'), '', '', thumbnail, '', '')
                    if uhdtv == 'false' and re.search("4K",channel_name):
                        pass
                    elif fhdtv == 'false' and re.search("FHD",channel_name):
                        pass
                    elif hdtv == 'false' and re.search("HD",channel_name):
                        pass
                    elif sdtv == 'false' and re.search("SD",channel_name):
                        pass
                    elif futebol == 'true' and not re.search("SPORTV",channel_name,re.IGNORECASE) and not re.search("DAZN",channel_name,re.IGNORECASE) and not re.search("ESPN Brasil",channel_name,re.IGNORECASE) and not re.search("PREMIERE",channel_name,re.IGNORECASE):
                        pass
                    #elif cleaname > '' and re.search("[XXX]",name1) or re.search("ADULT",name1,re.IGNORECASE) or re.search("Blue Hustler",name1,re.IGNORECASE) or re.search("PlayBoy",name1,re.IGNORECASE) or re.search("Redlight",name1,re.IGNORECASE) or re.search("Sextreme",name1,re.IGNORECASE) or re.search("SexyHot",name1,re.IGNORECASE) or re.search("Venus",name1,re.IGNORECASE) or re.search("AST TV",name1,re.IGNORECASE) or re.search("ASTTV",name1,re.IGNORECASE) or re.search("AST.TV",name1,re.IGNORECASE) or re.search("BRAZZERS",name1,re.IGNORECASE) or re.search("CANDY",name1,re.IGNORECASE) or re.search("CENTOXCENTO",name1,re.IGNORECASE) or re.search("DORCEL",name1,re.IGNORECASE) or re.search("EROXX",name1,re.IGNORECASE) or re.search("PASSION",name1,re.IGNORECASE) or re.search("PENTHOUSE",name1,re.IGNORECASE) or re.search("PINK-O",name1,re.IGNORECASE) or re.search("PINK O",name1,re.IGNORECASE) or re.search("PRIVATE",name1,re.IGNORECASE) or re.search("RUSNOCH",name1,re.IGNORECASE) or re.search("SCT",name1,re.IGNORECASE) or re.search("SEXT6SENSO",name1,re.IGNORECASE) or re.search("SHALUN TV",name1,re.IGNORECASE) or re.search("VIVID RED",name1,re.IGNORECASE):
                    elif cleaname > '' and re.search("ADULT",name1,re.IGNORECASE) or re.search("Blue Hustler",name1,re.IGNORECASE) or re.search("PlayBoy",name1,re.IGNORECASE) or re.search("Redlight",name1,re.IGNORECASE) or re.search("Sextreme",name1,re.IGNORECASE) or re.search("SexyHot",name1,re.IGNORECASE) or re.search("Venus",name1,re.IGNORECASE) or re.search("AST TV",name1,re.IGNORECASE) or re.search("ASTTV",name1,re.IGNORECASE) or re.search("AST.TV",name1,re.IGNORECASE) or re.search("BRAZZERS",name1,re.IGNORECASE) or re.search("CANDY",name1,re.IGNORECASE) or re.search("CENTOXCENTO",name1,re.IGNORECASE) or re.search("DORCEL",name1,re.IGNORECASE) or re.search("EROXX",name1,re.IGNORECASE) or re.search("PASSION",name1,re.IGNORECASE) or re.search("PENTHOUSE",name1,re.IGNORECASE) or re.search("PINK-O",name1,re.IGNORECASE) or re.search("PINK O",name1,re.IGNORECASE) or re.search("PRIVATE",name1,re.IGNORECASE) or re.search("RUSNOCH",name1,re.IGNORECASE) or re.search("SCT",name1,re.IGNORECASE) or re.search("SEXT6SENSO",name1,re.IGNORECASE) or re.search("SHALUN TV",name1,re.IGNORECASE) or re.search("VIVID RED",name1,re.IGNORECASE):
                        addDir2(name1.encode('utf-8', 'ignore'),resolver_final.encode('utf-8'),10,'',channel_name,thumbnail,'',desc1.encode('utf-8'),False)
                    #elif re.search("[XXX]",name1) or re.search("ADULT",name1,re.IGNORECASE) or re.search("Blue Hustler",name1,re.IGNORECASE) or re.search("PlayBoy",name1,re.IGNORECASE) or re.search("Redlight",name1,re.IGNORECASE) or re.search("Sextreme",name1,re.IGNORECASE) or re.search("SexyHot",name1,re.IGNORECASE) or re.search("Venus",name1,re.IGNORECASE) or re.search("AST TV",name1,re.IGNORECASE) or re.search("ASTTV",name1,re.IGNORECASE) or re.search("AST.TV",name1,re.IGNORECASE) or re.search("BRAZZERS",name1,re.IGNORECASE) or re.search("CANDY",name1,re.IGNORECASE) or re.search("CENTOXCENTO",name1,re.IGNORECASE) or re.search("DORCEL",name1,re.IGNORECASE) or re.search("EROXX",name1,re.IGNORECASE) or re.search("PASSION",name1,re.IGNORECASE) or re.search("PENTHOUSE",name1,re.IGNORECASE) or re.search("PINK-O",name1,re.IGNORECASE) or re.search("PINK O",name1,re.IGNORECASE) or re.search("PRIVATE",name1,re.IGNORECASE) or re.search("RUSNOCH",name1,re.IGNORECASE) or re.search("SCT",name1,re.IGNORECASE) or re.search("SEXT6SENSO",name1,re.IGNORECASE) or re.search("SHALUN TV",name1,re.IGNORECASE) or re.search("VIVID RED",name1,re.IGNORECASE):
                    elif re.search("ADULT",name1,re.IGNORECASE) or re.search("Blue Hustler",name1,re.IGNORECASE) or re.search("PlayBoy",name1,re.IGNORECASE) or re.search("Redlight",name1,re.IGNORECASE) or re.search("Sextreme",name1,re.IGNORECASE) or re.search("SexyHot",name1,re.IGNORECASE) or re.search("Venus",name1,re.IGNORECASE) or re.search("AST TV",name1,re.IGNORECASE) or re.search("ASTTV",name1,re.IGNORECASE) or re.search("AST.TV",name1,re.IGNORECASE) or re.search("BRAZZERS",name1,re.IGNORECASE) or re.search("CANDY",name1,re.IGNORECASE) or re.search("CENTOXCENTO",name1,re.IGNORECASE) or re.search("DORCEL",name1,re.IGNORECASE) or re.search("EROXX",name1,re.IGNORECASE) or re.search("PASSION",name1,re.IGNORECASE) or re.search("PENTHOUSE",name1,re.IGNORECASE) or re.search("PINK-O",name1,re.IGNORECASE) or re.search("PINK O",name1,re.IGNORECASE) or re.search("PRIVATE",name1,re.IGNORECASE) or re.search("RUSNOCH",name1,re.IGNORECASE) or re.search("SCT",name1,re.IGNORECASE) or re.search("SEXT6SENSO",name1,re.IGNORECASE) or re.search("SHALUN TV",name1,re.IGNORECASE) or re.search("VIVID RED",name1,re.IGNORECASE):
                        addDir2(name1.encode('utf-8', 'ignore'),resolver_final.encode('utf-8'),10,'',cleaname,thumbnail,'',desc1.encode('utf-8'),False)                
                    elif cleaname > '':
                        addLink(name1.encode('utf-8', 'ignore'),resolver_final.encode('utf-8'),'',cleaname,thumbnail,'',desc1)
                    else:
                       addLink(name1.encode('utf-8', 'ignore'),resolver_final.encode('utf-8'),'',cleaname,thumbnail,'',desc1) 
                except:
                    #notify('[COLOR red]Erro ao Carregar os dados![/COLOR]')
                    pass
        else:
            getItems(soup('item'),fanart)
            #getItems(soup('item'))
    else:
        #parse_m3u(soup)
        notify('[COLOR red]Erro ao Carregar os dados![/COLOR]')


def getChannelItems(name,url,fanart):
        data = resolve_data(url)
        soup = BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        channel_list = soup.find('channel', attrs={'name' : name.decode('utf-8')})
        items = channel_list('item')
        try:
            fanArt = channel_list('fanart')[0].string
            if fanArt == None:
                raise
        except:
            fanArt = fanart
        for channel in channel_list('subchannel'):
            name = channel('name')[0].string
            try:
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    raise
            except:
                thumbnail = ''
            try:
                if not channel('fanart'):
                    if __addon__.getSetting('use_thumb') == "true":
                        fanArt = thumbnail
                else:
                    fanArt = channel('fanart')[0].string
                if fanArt == None:
                    raise
            except:
                pass
            try:
                desc = channel('info')[0].string
                if desc == None:
                    raise
            except:
                desc = ''

            try:
                #addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),3,thumbnail,fanArt,desc,genre,credits,date)
                addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),3,thumbnail,fanArt,desc)
            except:
                notify('[COLOR red]Erro ao Carregar os dados![/COLOR]')
        getItems(items,fanArt)
        #getItems(items)

def getItems(items, fanart):
    if epgEnabled == "true": epginfo = epgParseData()
    use_thumb = addon.getSetting('use_thumb')
    for item in items:
        try:
            name = item('title')[0].string.replace(";", "")
            if name is None:
                name = 'unknown?'
        except:
            name = ''

        try:
            name3 = item('title')[0].string.replace(";", "")
            if name3 is None:
                name3 = 'unknown?'
        except:
            name3 = ''             
            
        try:
            thumbnail = item('thumbnail')[0].string
            if thumbnail == None:
                raise
        except:
            thumbnail = ''
        try:
            if not item('fanart'):
                if __addon__.getSetting('use_thumb') == "true":
                    fanArt = thumbnail
                else:
                    fanArt = fanart
            else:
                fanArt = item('fanart')[0].string
            if fanArt == None:
                raise
        except:
            fanArt = fanart        
        
        try:
            desc = item('info')[0].string
            if desc == None:
                raise
        except:
            desc = ''
            
        try:
            if item('epgid'):
                epgid = item('epgid')[0].string
                #if len(epgid)>0:
                if epgid > '':
                    name2 = item('title')[0].string.replace(";", "")
                    if name2 is None:
                        name2 = 'unknown?'
                    if xbmcaddon.Addon().getSetting("epg") == "true":
                        epg, desc_epg = getEPG(epginfo,epgid)
                        name = name2+epg.replace('&amp;', '&').replace("&#39;", "'")
                        cleaname = name2.encode('utf-8', 'ignore')
                        desc = desc_epg.replace('&amp;', '&').replace("&#39;", "'")
                    else:
                        cleaname = ''
                        desc = item('info')[0].string
                else:
                    cleaname = ''
                    desc = item('info')[0].string
            else:
                cleaname = ''
                desc = item('info')[0].string
        except:
            cleaname = ''
            desc = ''
            
        try:
            if item('category'):
                category = item('category')[0].string
            else:
                category = ''
        except:
            category = ''
            
        
        try:
            if item('subtitle') and len(item('subtitle')) >0:
                subtitle = item('subtitle')[0].string
                subtitle2  = item('subtitle')
            else:
                subtitle = ''
                subtitle2 = ''
        except:
            subtitle = ''
            subtitle2 = ''
            
        try:
            if item('utube') and len(item('utube')) >0:
                utube = item('utube')[0].string
            else:
                utube = ''
        except:
            utube = ''

            
        try:
            if len(item('jsonrpc')) >0:
                url = item('jsonrpc')[0].string
            elif len(item('externallink')) >0:
                url = item('externallink')[0].string
            elif len(item('link')) >0:
                try:
                    url = item('link')[0].string
                    url2 = item('link')                   
                except:
                    url = item('link')[0].string
                    url2 = ''
            else:
                url = ''
                url2 = ''
        except: 
            url = ''
            url2 = ''

        try:              
            if resolver(url, name, thumbnail).startswith('plugin://plugin.video.youtube/playlist') == True or resolver(url, name, thumbnail).startswith('plugin://plugin.video.youtube/channel') == True or resolver(url, name, thumbnail).startswith('plugin://plugin.video.youtube/user') == True or resolver(url, name, thumbnail).startswith('Plugin://plugin.video.youtube/playlist') == True:
                addDir(name.encode('utf-8', 'ignore'),resolver(url, name, thumbnail).encode('utf-8'),6,thumbnail,fanArt,desc)
            elif utube > '' and len(utube) == 11:
                link_youtube = 'plugin://plugin.video.youtube/play/?video_id='+utube
                addLink(name.encode('utf-8', 'ignore'), link_youtube.encode('utf-8'), subtitle, cleaname, thumbnail, fanArt, desc)
            elif len(item('externallink')) >0:
                addDir(name.encode('utf-8', 'ignore'),resolver(url, name, thumbnail).encode('utf-8'),1,thumbnail,fanArt,desc)
            elif len(url2) >1 and cleaname == '' and len(subtitle2) >1 and re.search(playlist_command,url,re.IGNORECASE):
                addDir2(name.encode('utf-8', 'ignore')+'[COLOR aquamarine] ('+str(len(url2))+' itens)[/COLOR]'.encode('utf-8', 'ignore'),str(url2).replace(',','||').replace('$'+playlist_command+'','#'+playlist_command+''),11,str(subtitle2).replace(',','||'),cleaname,thumbnail,fanArt,desc.encode('utf-8'),False)
            elif len(url2) >1 and cleaname == '' and re.search(playlist_command,url,re.IGNORECASE):
                addDir2(name.encode('utf-8', 'ignore')+'[COLOR aquamarine] ('+str(len(url2))+' itens)[/COLOR]'.encode('utf-8', 'ignore'),str(url2).replace(',','||').replace('$'+playlist_command+'','#'+playlist_command+''),11,subtitle,cleaname,thumbnail,fanArt,desc.encode('utf-8'),False)
            elif cleaname > '' and category == 'Adult':
                addDir2(name.encode('utf-8', 'ignore'),resolver(url, cleaname, thumbnail).encode('utf-8'),10,subtitle,cleaname,thumbnail,fanArt,desc.encode('utf-8'),False)
            elif category == 'Adult':
                addDir2(name.encode('utf-8', 'ignore'),resolver(url, name, thumbnail).encode('utf-8'),10,subtitle,cleaname,thumbnail,fanArt,desc.encode('utf-8'),False)
            elif cleaname > '':
                addLink(name.encode('utf-8', 'ignore'), resolver(url, cleaname, thumbnail).encode('utf-8'), subtitle, cleaname, thumbnail, fanArt, desc)
            else:
                addLink(name.encode('utf-8', 'ignore'), resolver(url, name, thumbnail).encode('utf-8'), subtitle, cleaname, thumbnail, fanArt, desc)
        except:
            notify('[COLOR red]Erro ao Carregar os items![/COLOR]')
        


def getSubChannelItems(name,url,fanart):
    data = resolve_data(url)
    soup = BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
    channel_list = soup.find('subchannel', attrs={'name' : name.decode('utf-8')})
    items = channel_list('subitem')
    getItems(items,fanart)




def updateEPG():
    try:
        Path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode("utf-8")
        arquivo = os.path.join(Path, "RHAEPG.xml")
        exists = os.path.isfile(arquivo)
        if exists == False:
            downloadEPG()
        else:
            if epgLast == "":
                downloadEPG()
            else:
                ultimo = datetime(int(epgLast[6:10]), int(epgLast[3:5]), int(epgLast[:2]), int(epgLast[11:13]), int(epgLast[14:16]), int(epgLast[17:]))
                agora = datetime.now()
                diff = agora - ultimo
                days_to_hours = diff.days * 24
                diff_btw_two_times = (diff.seconds) / 3600
                result = abs(days_to_hours + diff_btw_two_times)
                horas = (int(epgDays) + 1) * 24
                if result >= horas: downloadEPG()
    except:
        notify('[COLOR red]Erro ao atualizar EPG![/COLOR][CR]Limpe os dados e tente novamente.')


def downloadEPG():
    try:
        import downloader_epg
        Path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode("utf-8")
        arquivo = os.path.join(Path, "RHAEPG.xml")
        exists = os.path.isfile(arquivo)
        dp = xbmcgui.DialogProgress()
        dp.create('Baixando EPG...','Por favor aguarde...')
        if exists:
            try:
                os.remove(arquivo)
            except:
                pass
        #downloader_epg.download(base64.b64decode(epg_url), arquivo, dp)
        downloader_epg.download(epg_url, arquivo, dp)
        xbmc.sleep(2000)
        data = datetime.now()
        data = data.strftime("%d/%m/%Y %H:%M:%S")
        xbmcaddon.Addon().setSetting("epg_last", data)
        notify('[COLOR aquamarine]EPG atualizado com sucesso![/COLOR]',2000)
    except:
        notify('[COLOR red]Erro ao atualizar EPG![/COLOR][CR]Limpe os dados e tente novamente.')


def epgParseData():
    try:        
        Path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode("utf-8")
        arquivo = os.path.join(Path, "RHAEPG.xml").decode("utf8")
        xml = ET.parse(arquivo)
        return xml.getroot()
    except:
        notify('[COLOR red]Erro ao carregar EPG![/COLOR][CR]Limpe os dados e tente novamente.')
        return None


def getID_EPG(channel):
    if re.search("A&E",channel,re.IGNORECASE):
        channel_id = 'Ae.br'
    elif re.search("AMC",channel,re.IGNORECASE):
        channel_id = 'Amc.br'
    elif re.search("Animal Planet",channel,re.IGNORECASE):
        channel_id = 'Animalplanet.br'
    elif re.search("Arte 1",channel,re.IGNORECASE):
        channel_id = 'Arte1.br'
    elif re.search("AXN",channel,re.IGNORECASE):
        channel_id = 'Axn.br'
    elif re.search("Baby TV",channel,re.IGNORECASE) or re.search("BabyTV",channel,re.IGNORECASE):
        channel_id = 'BabyTV.br'
    elif re.search("Band",channel,re.IGNORECASE) and not re.search("Band News",channel,re.IGNORECASE) and not re.search("Band Sports",channel,re.IGNORECASE):
        channel_id = 'BandRede.br'
    elif re.search("Band News",channel,re.IGNORECASE):
        channel_id = 'Bandnews.br'
    elif re.search("Band Sports",channel,re.IGNORECASE):
        channel_id = 'Bandsportshd.br'
    elif re.search("BIS",channel,re.IGNORECASE):
        channel_id = 'Bishd.br'
    elif re.search("Boomerang",channel,re.IGNORECASE):
        channel_id = 'Boomerang.br'
    elif re.search("Canal Brasil",channel,re.IGNORECASE):
        channel_id = 'Canalbrasil.br'
    elif re.search("Cancao Nova",channel,re.IGNORECASE) or re.search("Canção Nova",channel,re.IGNORECASE):
        channel_id = 'CancaoNova.br'
    elif re.search("Cartoon Network",channel,re.IGNORECASE):
        channel_id = 'Cartoonnetwork.br'
    elif re.search("Cinemax",channel,re.IGNORECASE):
        channel_id = 'Cinemax.br'
    elif re.search("Combate",channel,re.IGNORECASE):
        channel_id = 'Combatehd.br'
    elif re.search("Comedy Central",channel,re.IGNORECASE):
        channel_id = 'Comedycentral.br'
    elif re.search("Cultura",channel,re.IGNORECASE):
        channel_id = 'Tvcultura.br'
    elif re.search("Curta!",channel,re.IGNORECASE) or re.search("Curta",channel,re.IGNORECASE):
        channel_id = 'Curta.br'
    elif re.search("Discovery Channel",channel,re.IGNORECASE):
        channel_id = 'Discovery.br'
    elif re.search("Discovery Civilization",channel,re.IGNORECASE):
        channel_id = 'DiscoveryCivilization.br'
    elif re.search("Discovery Home Health",channel,re.IGNORECASE) or re.search("Discovery H&H",channel,re.IGNORECASE):
        channel_id = 'Homehealth.br'
    elif re.search("Discovery Kids",channel,re.IGNORECASE):
        channel_id = 'Discoverykids.br'
    elif re.search("Discovery Science",channel,re.IGNORECASE):
        channel_id = 'DiscoveryScience.br'
    elif re.search("Discovery Theater",channel,re.IGNORECASE):
        channel_id = 'Hdtheater.br'
    elif re.search("Discovery Turbo",channel,re.IGNORECASE):
        channel_id = 'Discturbohd.br'
    elif re.search("Discovery World",channel,re.IGNORECASE):
        channel_id = 'Discoveryworldhd.br'
    elif re.search("Disney Channel",channel,re.IGNORECASE):
        channel_id = 'Disneychannel.br'
    elif re.search("Disney Junior",channel,re.IGNORECASE) or re.search("Disney Jr",channel,re.IGNORECASE):
        channel_id = 'Disneyjrhd.br'
    elif re.search("Disney XD",channel,re.IGNORECASE):
        channel_id = 'Disneyxd.br'
    elif re.search("E!",channel,re.IGNORECASE):
        channel_id = 'E.br'
    elif re.search("E!",channel,re.IGNORECASE):
        channel_id = 'E.br'
    elif re.search("ESPN",channel,re.IGNORECASE) and not re.search("ESPN Brasil",channel,re.IGNORECASE) and not re.search("ESPN Extra",channel,re.IGNORECASE):
        channel_id = 'ESPNInternational.br'
    elif re.search("ESPN 2",channel,re.IGNORECASE):
        channel_id = 'ESPN+.br'
    elif re.search("ESPN Brasil",channel,re.IGNORECASE):
        channel_id = 'Espnbrasil.br'
    elif re.search("ESPN Extra",channel,re.IGNORECASE):
        channel_id = 'Espnextra.br'
    elif re.search("FishTV",channel,re.IGNORECASE) or re.search("Fish TV",channel,re.IGNORECASE):
        channel_id = 'Fishtv.br'
    elif re.search("Food Network",channel,re.IGNORECASE):
        channel_id = 'Foodnetworkhd.br'
    elif re.search("Fox",channel,re.IGNORECASE) and not re.search("Fox Life",channel,re.IGNORECASE) and not re.search("FOX Premium 1",channel,re.IGNORECASE) and not re.search("FOX Premium 2",channel,re.IGNORECASE) and not re.search("Fox Sports",channel,re.IGNORECASE) and not re.search("Fox Sports 2",channel,re.IGNORECASE) and not re.search("Fox 25",channel,re.IGNORECASE):
        channel_id = 'Fox.br'
    elif re.search("Fox Life",channel,re.IGNORECASE):
        channel_id = 'Foxlife.br'
    elif re.search("FOX Premium 1",channel,re.IGNORECASE):
        channel_id = 'Foxpremium1.br'
    elif re.search("FOX Premium 2",channel,re.IGNORECASE):
        channel_id = 'Foxpremium2.br'
    elif re.search("Fox Sports",channel,re.IGNORECASE):
        channel_id = 'Foxsports.br'
    elif re.search("Fox Sports 2",channel,re.IGNORECASE):
        channel_id = 'Foxsports2.br'
    elif re.search("Futura",channel,re.IGNORECASE):
        channel_id = 'Futura.br'
    elif re.search("FX",channel,re.IGNORECASE):
        channel_id = 'Fx.br'
    elif re.search("Globo News",channel,re.IGNORECASE):
        channel_id = 'Globonews.br'
    elif re.search("Globo RBS TV Poa",channel,re.IGNORECASE) or re.search("RBS TV",channel,re.IGNORECASE):
        channel_id = 'GloboPortoAlegre.br'
    elif re.search("Globo RJ",channel,re.IGNORECASE):
        channel_id = 'Globorj.br'
    elif re.search("Globo TV Tem Bauru",channel,re.IGNORECASE) or re.search("TV Tem Bauru",channel,re.IGNORECASE) or re.search("TVTem Bauru",channel,re.IGNORECASE):
        channel_id = 'Tvtembauru.br'
    elif re.search("Globo TV Tribuna",channel,re.IGNORECASE) or re.search("TV Tribuna",channel,re.IGNORECASE):
        channel_id = 'Tvtribuna.br'
    elif re.search("Globo TV Vanguarda",channel,re.IGNORECASE) or re.search("TV Vanguarda",channel,re.IGNORECASE):
        channel_id = 'Vangsaojchd.br'
    elif re.search("Gloob",channel,re.IGNORECASE):
        channel_id = 'Gloob.br'
    elif re.search("GNT",channel,re.IGNORECASE):
        channel_id = 'Gnt.br'
    elif re.search("HBO",channel,re.IGNORECASE):
        channel_id = 'Hbo.br'
    elif re.search("HBO 2",channel,re.IGNORECASE):
        channel_id = 'Hbo2.br'
    elif re.search("HBO Family",channel,re.IGNORECASE):
        channel_id = 'Hbofamily.br'
    elif re.search("HBO Plus",channel,re.IGNORECASE):
        channel_id = 'Hboplus.br'
    elif re.search("HBO Signature",channel,re.IGNORECASE):
        channel_id = 'Hbosignature.br'
    elif re.search("History Channel",channel,re.IGNORECASE):
        channel_id = 'Historychannel.br'
    elif re.search("Ideal TV",channel,re.IGNORECASE):
        channel_id = 'Idealtv.br'
    elif re.search("Investigação Discovery",channel,re.IGNORECASE):
        channel_id = 'Investigacaodiscoveryid.br'
    elif re.search("i.Sat",channel,re.IGNORECASE):
        channel_id = 'iSat.br'
    elif re.search("i.Sat",channel,re.IGNORECASE):
        channel_id = 'Lifetime.br'
    elif re.search("Max",channel,re.IGNORECASE) and not re.search("Max Prime",channel,re.IGNORECASE) and not re.search("Max UP",channel,re.IGNORECASE):
        channel_id = 'Max.br'
    elif re.search("Max Prime",channel,re.IGNORECASE):
        channel_id = 'Maxprime.br'
    elif re.search("Max UP",channel,re.IGNORECASE):
        channel_id = 'Maxup.br'
    elif re.search("Megapix",channel,re.IGNORECASE):
        channel_id = 'Megapix.br'
    elif re.search("MTV",channel,re.IGNORECASE):
        channel_id = 'Mtv.br'
    elif re.search("Multishow",channel,re.IGNORECASE):
        channel_id = 'Multishow.br'
    elif re.search("Nat Geo Kids",channel,re.IGNORECASE):
        channel_id = 'Natgeokids.br'
    elif re.search("Nat Geo Wild",channel,re.IGNORECASE):
        channel_id = 'Natgeowildhd.br'
    elif re.search("National Geographic",channel,re.IGNORECASE):
        channel_id = 'Nationalgeographic.br'
    elif re.search("NBR",channel,re.IGNORECASE):
        channel_id = 'Nbr.br'
    elif re.search("Nickelodeon",channel,re.IGNORECASE) and not re.search("Nick Jr",channel,re.IGNORECASE) and not re.search("Nick Junior",channel,re.IGNORECASE):
        channel_id = 'Nickelodeon.br'
    elif re.search("Nick Jr",channel,re.IGNORECASE):
        channel_id = 'NickJr.br'
    elif re.search("Novo Tempo",channel,re.IGNORECASE):
        channel_id = 'Tvnovotempo.br'
    elif re.search("Off",channel,re.IGNORECASE):
        channel_id = 'Off.br'    
    elif re.search("PlayBoy",channel,re.IGNORECASE):
        channel_id = 'Playboytv.br'   
    elif re.search("Paramount",channel,re.IGNORECASE):
        channel_id = 'Paramounthd.br'
    elif re.search("Paramount",channel,re.IGNORECASE):
        channel_id = 'Playtv.br'
    elif re.search("Premiere 2",channel,re.IGNORECASE):
        channel_id = 'Premiere2.br'
    elif re.search("Premiere 3",channel,re.IGNORECASE):
        channel_id = 'Premiere3.br'
    elif re.search("Premiere 4",channel,re.IGNORECASE):
        channel_id = 'Premiere4.br'
    elif re.search("Premiere 5",channel,re.IGNORECASE):
        channel_id = 'Premiere5.br'
    elif re.search("Premiere 6",channel,re.IGNORECASE):
        channel_id = 'Premiere6.br'
    elif re.search("Premiere 7",channel,re.IGNORECASE):
        channel_id = 'Premiere7.br'
    elif re.search("Premiere 8",channel,re.IGNORECASE):
        channel_id = 'Premiere8.br'
    elif re.search("Premiere 9",channel,re.IGNORECASE):
        channel_id = 'Premiere9.br'
    elif re.search("Premiere Clubes",channel,re.IGNORECASE):
        channel_id = 'Premierefchd.br'
    elif re.search("Prime Box",channel,re.IGNORECASE):
        channel_id = 'Primeboxbrazil.br'
    elif re.search("Ra Tim Bum",channel,re.IGNORECASE):
        channel_id = 'Tvratimbum.br'
    elif re.search("Record News",channel,re.IGNORECASE):
        channel_id = 'Recordnews.br'
    elif re.search("Record News",channel,re.IGNORECASE):
        channel_id = 'Recordnews.br'
    elif re.search("RecordTV",channel,re.IGNORECASE) or re.search("Record TV",channel,re.IGNORECASE) or re.search("Record SP",channel,re.IGNORECASE):
        channel_id = 'Recordrede.br'
    elif re.search("Rede Brasil",channel,re.IGNORECASE):
        channel_id = 'Redebrasil.br'
    elif re.search("Rede TV",channel,re.IGNORECASE) or re.search("RedeTV",channel,re.IGNORECASE):
        channel_id = 'Redetv.br'
    elif re.search("Rede Vida",channel,re.IGNORECASE):
        channel_id = 'Redevida.br'
    elif re.search("RIT",channel,re.IGNORECASE):
        channel_id = 'Rit.br'
    elif re.search("RPC Parana",channel,re.IGNORECASE) or re.search("RPC Curitiba",channel,re.IGNORECASE):
        channel_id = 'Rpccuritiba.br'
    elif re.search("SBT",channel,re.IGNORECASE):
        channel_id = 'Sbt.br'
    elif re.search("Sexy Hot",channel,re.IGNORECASE) or re.search("SexyHot",channel,re.IGNORECASE):
        channel_id = 'Sexyhot.br'
    elif re.search("Sony",channel,re.IGNORECASE):
        channel_id = 'Sony.br'
    elif re.search("Space",channel,re.IGNORECASE):
        channel_id = 'Space.br'
    elif re.search("Sportv",channel,re.IGNORECASE) and not re.search("Sportv 2",channel,re.IGNORECASE) and not re.search("Sportv 3",channel,re.IGNORECASE):
        channel_id = 'Sportv.br'
    elif re.search("Sportv 2",channel,re.IGNORECASE):
        channel_id = 'Sportv2.br'
    elif re.search("Sportv 3",channel,re.IGNORECASE):
        channel_id = 'Sportv3.br'
    elif re.search("Studio Universal",channel,re.IGNORECASE):
        channel_id = 'Studiouniversal.br'
    elif re.search("Syfy",channel,re.IGNORECASE):
        channel_id = 'Syfy.br'
    elif re.search("TBS",channel,re.IGNORECASE):
        channel_id = 'Tbs.br'
    elif re.search("TCM",channel,re.IGNORECASE):
        channel_id = 'Tcm.br'
    elif re.search("Telecine Action",channel,re.IGNORECASE):
        channel_id = 'Tcaction.br'
    elif re.search("Telecine Action",channel,re.IGNORECASE):
        channel_id = 'Tcaction.br'
    elif re.search("Telecine Cult",channel,re.IGNORECASE):
        channel_id = 'Tccult.br'
    elif re.search("Telecine Fun",channel,re.IGNORECASE):
        channel_id = 'Tcfun.br'
    elif re.search("Telecine Pipoca",channel,re.IGNORECASE):
        channel_id = 'Tcpipoca.br'
    elif re.search("Telecine Premium",channel,re.IGNORECASE):
        channel_id = 'Tcpremium.br'
    elif re.search("Telecine Touch",channel,re.IGNORECASE):
        channel_id = 'Tctouch.br'
    elif re.search("Terra Viva",channel,re.IGNORECASE):
        channel_id = 'Terraviva.br'
    elif re.search("TLC",channel,re.IGNORECASE):
        channel_id = 'Tlc.br'
    elif re.search("TNT",channel,re.IGNORECASE) and not re.search("TNT Series",channel,re.IGNORECASE) and not re.search("TNT Séries",channel,re.IGNORECASE):
        channel_id = 'Tnt.br'
    elif re.search("TNT Series",channel,re.IGNORECASE) or re.search("TNT Séries",channel,re.IGNORECASE):
        channel_id = 'TNTSerie.br'
    elif re.search("Tooncast",channel,re.IGNORECASE):
        channel_id = 'Tooncast.br'
    elif re.search("truTV",channel,re.IGNORECASE):
        channel_id = 'Trutv.br'
    elif re.search("TV Aparecida",channel,re.IGNORECASE):
        channel_id = 'Tvaparecida.br'
    elif re.search("Tv Brasil",channel,re.IGNORECASE):
        channel_id = 'Tvbrasil.br'
    elif re.search("Tv Camara",channel,re.IGNORECASE):
        channel_id = 'Tvcamara.br'
    elif re.search("Tv Escola",channel,re.IGNORECASE):
        channel_id = 'Tvescola.br'
    elif re.search("TV Gazeta",channel,re.IGNORECASE):
        channel_id = 'TVGazeta.br'
    elif re.search("Tv Justica",channel,re.IGNORECASE):
        channel_id = 'Tvjustica.br'
    elif re.search("Tv Senado",channel,re.IGNORECASE):
        channel_id = 'Tvsenado.br'
    elif re.search("VH1",channel,re.IGNORECASE) and not re.search("VH1 Megahits",channel,re.IGNORECASE):
        channel_id = 'VH1HD.br'
    elif re.search("VH1 Megahits",channel,re.IGNORECASE):
        channel_id = 'VH1MegaHits.br'
    elif re.search("Viva",channel,re.IGNORECASE):
        channel_id = 'Viva.br'
    elif re.search("Warner Channel",channel,re.IGNORECASE) or re.search("Warner",channel,re.IGNORECASE):
        channel_id = 'Warnerchannel.br'
    elif re.search("WooHoo",channel,re.IGNORECASE):
        channel_id = 'Woohoo.br'
    elif re.search("Zoomoo",channel,re.IGNORECASE):
        channel_id = 'Zoomoo.br'
    elif re.search("H2",channel,re.IGNORECASE):
        channel_id = 'H2.br'
    else:
        channel_id = ''
    return channel_id
    
        
        

def getEPG(root,chan):
    try:        
        programas = root.findall("./programme[@channel='"+chan+"']")
        agora = datetime.now()
        agora = agora.strftime("%Y%m%d%H%M%S")
        #print(agora)
        for item in programas:
            start = item.get('start')[:-6]
            stop = item.get('stop')[:-6]
            if int(start) <= int(agora) < int(stop):
                epg = '\n[COLOR aquamarine][B]' + start[8:-4] + ':' + start[10:-2] + '[/B] ' + item.find('title').text + '[/COLOR]'
                encerramento = '\n\n[COLOR orange][B]ENCERRA ÀS:[/B][/COLOR] ' + stop[8:-4] + ':' + stop[10:-2]
                desc = item.find('desc')
                if desc is None:
                    sinopse = '\n\n[COLOR lime][B]SINOPSE:[/B][/COLOR] Indisponivel'
                else:
                    sinopse = '\n\n[COLOR lime][B]SINOPSE:[/B][/COLOR] '+ desc.text
                cat = item.findall('category')
                if cat is None or len(cat) == 0:
                    genero = '\n\n[COLOR lightblue][B]GÊNERO:[/B][/COLOR] Desconhecido'
                elif len(cat) == 1:                    
                    genero = '\n\n[COLOR lightblue][B]GÊNERO:[/B][/COLOR] '+ cat[0].text
                else:
                    genero = '\n\n[COLOR lightblue][B]GÊNERO:[/B][/COLOR] '+ cat[0].text + '/' + cat[1].text
                desc_epg = encerramento+sinopse+genero
        return epg, desc_epg;
    except:
        epg = '\n[COLOR orange]Epg Indisponível[/COLOR]'
        desc_epg = ''
        return epg, desc_epg;


def adult(name, url, cleaname, iconimage, description, subtitle):
    Path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode("utf-8")
    arquivo = os.path.join(Path, "password.txt")
    exists = os.path.isfile(arquivo) 
    keyboard = xbmcaddon.Addon().getSetting("keyboard")
    if exists == False:
        parental_password()
        xbmc.sleep(4)
        p_file = open(arquivo,'r+')
        p_file_read = p_file.read()
        p_file_b64_decode = base64.b64decode(p_file_read).decode('utf-8')
        dialog = xbmcgui.Dialog()
        if int(keyboard) == 0:
            ps = dialog.numeric(0, 'Insira a senha atual:')
        else:            
            ps = dialog.input('Insira a senha atual:', option=xbmcgui.ALPHANUM_HIDE_INPUT)
        if ps == p_file_b64_decode:
            if url.startswith("plugin://plugin.video.f4mTester"):
                xbmc.executebuiltin('RunPlugin(' + url + ')')
            elif url.startswith('plugin://plugin.video.youtube/playlist') == True or url.startswith('plugin://plugin.video.youtube/channel') == True or url.startswith('plugin://plugin.video.youtube/user') == True or url.startswith('Plugin://plugin.video.youtube/playlist') == True:
                xbmc.executebuiltin("ActivateWindow(10025," + url + ",return)")
            else:
                li = xbmcgui.ListItem(name, path=url, iconImage=iconimage, thumbnailImage=iconimage)
                if cleaname > '':
                    li.setInfo(type='video', infoLabels={'Title': cleaname, 'plot': description })
                else:
                    li.setInfo(type='video', infoLabels={'Title': name, 'plot': description })
                if subtitle > '':
                    li.setSubtitles([subtitle])
                xbmc.Player().play(item=url, listitem=li)
        else:
            xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Senha invalida!, se não alterou utilize a senha padrão')
    else:
        p_file = open(arquivo,'r+')
        p_file_read = p_file.read()
        p_file_b64_decode = base64.b64decode(p_file_read).decode('utf-8')
        dialog = xbmcgui.Dialog()
        if int(keyboard) == 0:
            ps = dialog.numeric(0, 'Insira a senha atual:')
        else:            
            ps = dialog.input('Insira a senha atual:', option=xbmcgui.ALPHANUM_HIDE_INPUT)
        if ps == p_file_b64_decode:
            if url.startswith("plugin://plugin.video.f4mTester"):
                xbmc.executebuiltin('RunPlugin(' + url + ')')
            elif url.startswith('plugin://plugin.video.youtube/playlist') == True or url.startswith('plugin://plugin.video.youtube/channel') == True or url.startswith('plugin://plugin.video.youtube/user') == True or url.startswith('Plugin://plugin.video.youtube/playlist') == True:
                xbmc.executebuiltin("ActivateWindow(10025," + url + ",return)")
            else:
                li = xbmcgui.ListItem(name, path=url, iconImage=iconimage, thumbnailImage=iconimage)
                if cleaname > '':
                    li.setInfo(type='video', infoLabels={'Title': cleaname, 'plot': description })
                else:
                    li.setInfo(type='video', infoLabels={'Title': name, 'plot': description })
                if subtitle > '':
                    li.setSubtitles([subtitle])
                xbmc.Player().play(item=url, listitem=li)
        else:
            xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Senha invalida!, se não alterou utilize a senha padrão')
    

def playlist(name, url, cleaname, iconimage, description, subtitle):
    playlist_command1 = playlist_command
    dialog = xbmcgui.Dialog()
    links = re.compile('<link>([\s\S]*?)#'+playlist_command1+'', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(url)
    names = re.compile('#'+playlist_command1+'=([\s\S]*?)</link>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(url)
    subtitles = re.compile('<subtitle>([\s\S]*?)</subtitle>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(subtitle)
    if links !=[] and names !=[]:
        index = dialog.select(dialog_playlist, names)
        if index >= 0:    
            playname=names[index]
            if playname > '':
                playname1 = playname
            else:
                playname1 = 'Desconhecido'
            playlink=links[index]
            if subtitles !=[]:
                playsub=subtitles[index]
            else:
                playsub = ''
            urlresolver = resolver(playlink, playname1, iconimage)
            if urlresolver.startswith("plugin://plugin.video.f4mTester"):
                xbmc.executebuiltin('RunPlugin(' + urlresolver + ')')
            elif urlresolver.startswith('plugin://plugin.video.youtube/playlist') == True or urlresolver.startswith('plugin://plugin.video.youtube/channel') == True or urlresolver.startswith('plugin://plugin.video.youtube/user') == True or urlresolver.startswith('Plugin://plugin.video.youtube/playlist') == True:
                xbmc.executebuiltin("ActivateWindow(10025," + urlresolver + ",return)")
            else:
                li = xbmcgui.ListItem(playname1, path=urlresolver, iconImage=iconimage, thumbnailImage=iconimage)
                if cleaname > '':
                    li.setInfo(type='video', infoLabels={'Title': cleaname, 'plot': description })
                else:
                    li.setInfo(type='video', infoLabels={'Title': playname1, 'plot': description })
                if subtitle > '':
                    li.setSubtitles([playsub])
                xbmc.Player().play(item=urlresolver, listitem=li)


#NETCINE
def netcine_resolver(url):
    link_decoded = url
    if not link_decoded.startswith("plugin://plugin") and link_decoded.startswith('https://netcine.info/') == True:
        try:
            try:
                import urllib.request as urllib2
            except ImportError:
                import urllib2
            request_headers = {
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,ru;q=0.7,de-DE;q=0.6,de;q=0.5,de-AT;q=0.4,de-CH;q=0.3,ja;q=0.2,zh-CN;q=0.1,zh;q=0.1,zh-TW;q=0.1,es;q=0.1,ar;q=0.1,en-GB;q=0.1,hi;q=0.1,cs;q=0.1,el;q=0.1,he;q=0.1,en-US;q=0.1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
            }
            url2 = 'https://netcine.info/'
            request = urllib2.Request(url2, headers=request_headers)
            response = urllib2.urlopen(request)
            result_host = response.geturl()
            #return response
        except:
            result_host = 'https://netcine.info/'
        host_final = result_host.replace('tvshows/', '').replace('?filmes/', '').replace('?filmes', '')
        referer = host_final.replace('https://', 'https://p.')
        link_atualizado = link_decoded.replace('https://netcine.info/', host_final)
        #print(link_atualizado)
        procurar_idioma = re.compile('.+?idioma=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_atualizado)
        #print(find_idioma[0])
        if procurar_idioma[0] == 'legendado':
            #print(procurar_idioma[0])
            link_normal = link_atualizado.replace('$idioma=legendado','')
            #print(link_normal)
            data = getRequest2(link_normal, host_final)
            #print(data)
            #result1 = re.compile('<p><iframe src="(.+?)".+?</p>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
            result1 = re.compile('<iframe src="(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
            #print(result1)
            for link in result1:
                if link.find('leg') >= 0:
                    #print(link)
                    data2 = getRequest2(link, referer)
                    #print(data2)
                    result2 = re.compile('<iframe src="(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data2)
                    #print(result2)
                    link2 = result2[0]
                    data3 = getRequest2(link2, referer)
                    #print(data3)
                    #print('Teste\n'+data3+'\n#########')
                    result3 = re.compile('<a href ="(.+?)".+?target="_blank"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data3)
                    #print(result3[1])
                    link3 = result3[1]
                    #print(link3)
                    #link4 = link3.replace('https://p.netcine.info/redirecionar.php?data=','')
                    result_redirect = re.compile('.+?data=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link3)
                    link4 = result_redirect[0]
                    #print(link4)
                    data4 = getRequest2(link4, referer)
                    #print(data4)
                    result4 = re.compile("location.href='(.+?)'", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data4)
                    #print(result4[2])
                    #print(result4)
                    if result4 !=[]:
                        for player in result4:
                            if player.find('desktop') >= 0:
                                #print(result4[2])
                                link5 = player
                                data5 = getRequest2(link5, referer)
                                #print(data5)
                                link6 = re.compile("file':'(.+?)'", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data5)
                                for video_url in link6:
                                    if video_url.find('-ALTO') >= 0:
                                        #print(video_url)
                                        #resolved = video_url+'|Referer='+getlink2
                                        resolved = video_url
                                        #print(resolved)
                                        return resolved
                                    else:
                                        resolved = ''
                            else:
                                resolved = ''
                    else:
                        link6 = re.compile("file':'(.+?)'", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data4)
                        for video_url in link6:
                            if video_url.find('-ALTO') >= 0:
                                #print(video_url)
                                #resolved = video_url+'|Referer='+getlink2
                                resolved = video_url
                                #print(resolved)
                                return resolved
                            else:
                                resolved = ''                              
                                
                #elif link.find('LEG') >= 0 or link.find('nv32.php') >= 0 and link.find('filmes') >= 0:
                elif link.find('filmes') >= 0 and link.find('LEG') >=0:
                    #print(link)
                    data2 = getRequest2(link, referer)
                    #print(data2)
                    result2 = re.compile('<iframe src="(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data2)
                    #print(result2)
                    link2 = result2[0]
                    data3 = getRequest2(link2, referer)
                    #print(data3)
                    #print('Teste\n'+data3+'\n#########')
                    result3 = re.compile('<a href ="(.+?)".+?target="_blank"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data3)
                    #print(result3[1])
                    link3 = result3[1]
                    #print(link3)
                    #link4 = link3.replace('https://p.netcine.info/redirecionar.php?data=','')
                    result_redirect = re.compile('.+?data=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link3)
                    link4 = result_redirect[0]
                    #print(link4)
                    data4 = getRequest2(link4, referer)
                    #print(data4)
                    result4 = re.compile("location.href='(.+?)'", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data4)
                    #print(result4[2])
                    if result4 !=[]:
                        for player in result4:
                            if player.find('desktop') >= 0:
                                #print(result4[2])
                                link5 = player
                                data5 = getRequest2(link5, referer)
                                #print(data5)
                                link6 = re.compile("file':'(.+?)'", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data5)
                                for video_url in link6:
                                    if video_url.find('-ALTO') >= 0:
                                        #print(video_url)
                                        #resolved = video_url+'|Referer='+getlink2
                                        resolved = video_url
                                        #print(resolved)
                                        return resolved
                                    else:
                                        resolved = ''
                            else:
                                resolved = ''
                    else:
                        link6 = re.compile("file':'(.+?)'", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data4)
                        for video_url in link6:
                            if video_url.find('-ALTO') >= 0:
                                #print(video_url)
                                #resolved = video_url+'|Referer='+getlink2
                                resolved = video_url
                                #print(resolved)
                                return resolved
                            else:
                                resolved = ''
                else:
                    resolved = ''                    
        elif procurar_idioma[0] == 'dublado':
            #print(procurar_idioma[0])
            link_normal = link_atualizado.replace('$idioma=dublado','')
            #print(link_normal)
            data = getRequest2(link_normal, host_final)
            #print(data)
            #result1 = re.compile('<p><iframe src="(.+?)".+?</p>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
            result1 = re.compile('<iframe src="(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
            #print(result1)
            for link in result1:
                if link.find('dub') >= 0:
                    #print(link)
                    data2 = getRequest2(link, referer)
                    #print(data2)
                    result2 = re.compile('<iframe src="(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data2)
                    #print(result2)
                    link2 = result2[0]
                    data3 = getRequest2(link2, referer)
                    #print(data3)
                    #print('Teste\n'+data3+'\n#########')
                    result3 = re.compile('<a href ="(.+?)".+?target="_blank"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data3)
                    #print(result3[1])
                    link3 = result3[1]
                    #print(link3)
                    #link4 = link3.replace('https://p.netcine.info/redirecionar.php?data=','')
                    result_redirect = re.compile('.+?data=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link3)
                    link4 = result_redirect[0]
                    #print(link4)
                    data4 = getRequest2(link4, referer)
                    #print(data4)
                    result4 = re.compile("location.href='(.+?)'", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data4)
                    #print(result4[2])
                    if result4 !=[]:
                        for player in result4:
                            if player.find('desktop') >= 0:
                                #print(result4[2])
                                link5 = player
                                data5 = getRequest2(link5, referer)
                                #print(data5)
                                link6 = re.compile("file':'(.+?)'", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data5)
                                for video_url in link6:
                                    if video_url.find('-ALTO') >= 0:
                                        #print(video_url)
                                        #resolved = video_url+'|Referer='+getlink2
                                        resolved = video_url
                                        #print(resolved)
                                        return resolved
                                    else:
                                        resolved = ''
                            else:
                                resolved = ''
                    else:
                        link6 = re.compile("file':'(.+?)'", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data4)
                        for video_url in link6:
                            if video_url.find('-ALTO') >= 0:
                                #print(video_url)
                                #resolved = video_url+'|Referer='+getlink2
                                resolved = video_url
                                #print(resolved)
                                return resolved
                            else:
                                resolved = ''
                #elif link.find('nv26.php') >= 0 or link.find('DUB') >=0 and link.find('filmes') >= 0:
                elif link.find('filmes') >= 0 and link.find('DUB') >=0:
                    #print(link)
                    data2 = getRequest2(link, referer)
                    #print(data2)
                    result2 = re.compile('<iframe src="(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data2)
                    #print(result2)
                    link2 = result2[0]
                    data3 = getRequest2(link2, referer)
                    #print(data3)
                    #print('Teste\n'+data3+'\n#########')
                    result3 = re.compile('<a href ="(.+?)".+?target="_blank"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data3)
                    #print(result3[1])
                    link3 = result3[1]
                    #print(link3)
                    #link4 = link3.replace('https://p.netcine.info/redirecionar.php?data=','')
                    result_redirect = re.compile('.+?data=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link3)
                    link4 = result_redirect[0]
                    #print(link4)
                    data4 = getRequest2(link4, referer)
                    #print(data4)
                    result4 = re.compile("location.href='(.+?)'", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data4)
                    #print(result4[2])
                    if result4 !=[]:
                        for player in result4:
                            if player.find('desktop') >= 0:
                                #print(result4[2])
                                link5 = player
                                data5 = getRequest2(link5, referer)
                                #print(data5)
                                link6 = re.compile("file':'(.+?)'", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data5)
                                for video_url in link6:
                                    if video_url.find('-ALTO') >= 0:
                                        #print(video_url)
                                        #resolved = video_url+'|Referer='+getlink2
                                        resolved = video_url
                                        #print(resolved)
                                        return resolved
                                    else:
                                        resolved = ''
                            else:
                                resolved = ''
                    else:
                        link6 = re.compile("file':'(.+?)'", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data4)
                        for video_url in link6:
                            if video_url.find('-ALTO') >= 0:
                                #print(video_url)
                                #resolved = video_url+'|Referer='+getlink2
                                resolved = video_url
                                #print(resolved)
                                return resolved
                            else:
                                resolved = ''
                else:
                    resolved = ''
                    
        else:
            resolved = ''
            



def youtube(url):
    plugin_url = url
    xbmc.executebuiltin("ActivateWindow(10025," + plugin_url + ",return)")


def youtube_resolver(url):
    link_youtube = url
    if link_youtube.startswith('https://www.youtube.com/watch?v') == True or link_youtube.startswith('https://youtube.com/watch?v') == True:
        get_id1 = re.compile('v=(.+?)&', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_youtube)
        get_id2 = re.compile('v=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_youtube)
        if get_id1 !=[]:
            #print('tem')
            id_video = get_id1[0]
            #print(id)
            resolve = 'plugin://plugin.video.youtube/play/?video_id='+id_video
        elif get_id2 !=[]:
            #print('tem2')
            id_video = get_id2[0]
            #print(id)
            resolve = 'plugin://plugin.video.youtube/play/?video_id='+id_video
        else:
            resolve = ''
    elif link_youtube.startswith('https://www.youtube.com/playlist?') == True or link_youtube.startswith('https://youtube.com/playlist?') == True:      
        get_id1 = re.compile('list=(.+?)&', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_youtube)
        get_id2 = re.compile('list=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_youtube)
        if get_id1 !=[]:
            #print('tem')
            id_video = get_id1[0]
            #print(id)
            resolve = 'plugin://plugin.video.youtube/playlist/'+id_video+'/?page=0'
        elif get_id2 !=[]:
            #print('tem2')
            id_video = get_id2[0]
            #print(id)
            resolve = 'plugin://plugin.video.youtube/playlist/'+id_video+'/?page=0'
        else:
            resolve = ''
    elif link_youtube.startswith('https://www.youtube.com/channel') == True or link_youtube.startswith('https://youtube.com/channel') == True:      
        get_id1 = re.compile('channel/(.+?)&', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_youtube)
        get_id2 = re.compile('channel/(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_youtube)
        if get_id1 !=[]:
            #print('tem')
            id_video = get_id1[0]
            #print(id)
            resolve = 'plugin://plugin.video.youtube/channel/'+id_video+'/'
        elif get_id2 !=[]:
            #print('tem2')
            id_video = get_id2[0]
            #print(id)
            resolve = 'plugin://plugin.video.youtube/channel/'+id_video+'/'
        else:
            resolve = ''
    elif link_youtube.startswith('https://www.youtube.com/user') == True or link_youtube.startswith('https://youtube.com/user') == True:      
        get_id1 = re.compile('user/(.+?)&', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_youtube)
        get_id2 = re.compile('user/(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_youtube)
        if get_id1 !=[]:
            #print('tem')
            id_video = get_id1[0]
            #print(id)
            resolve = 'plugin://plugin.video.youtube/user/'+id_video+'/'
        elif get_id2 !=[]:
            #print('tem2')
            id_video = get_id2[0]
            #print(id)
            resolve = 'plugin://plugin.video.youtube/user/'+id_video+'/'
        else:
            resolve = ''
            
    else:
        resolve = ''    
    return resolve


###REDECANAIS FUNCTION

def redecanais():
    try:
        try:
            import urllib.request as urllib2
        except ImportError:
            import urllib2
        request_headers = {
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,ru;q=0.7,de-DE;q=0.6,de;q=0.5,de-AT;q=0.4,de-CH;q=0.3,ja;q=0.2,zh-CN;q=0.1,zh;q=0.1,zh-TW;q=0.1,es;q=0.1,ar;q=0.1,en-GB;q=0.1,hi;q=0.1,cs;q=0.1,el;q=0.1,he;q=0.1,en-US;q=0.1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        url = 'https://canaisgratis.info/'
        request = urllib2.Request(url, headers=request_headers)
        response = urllib2.urlopen(request)
        result_host = response.geturl()
        #return response
    except:
        result_host = 'https://canaisgratis.info/'
    
    try:      
        #data1 = getRequest2(result_host+'player3/canais.php?canal=telecinefun&img=telecinefun', result_host+'assistir-telecine-fun-online-24-horas-ao-vivo_a536c2b27.html')
        #host_popup = re.compile('action="(.+?)instagram/.+?"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data1)
        #if host_popup !=[]:
        #    host_popup_final = host_popup[0].replace('www.', '')
        #else:
        #    host_popup_final = ''
        host_popup_final = 'https://noticiasfix.com/'
        data2 = getRequest2(result_host+'player3/canais-bk.php?canal=telecinefun&img=telecinefun', host_popup_final)
        #if host_popup_final > '':
        #    data2 = getRequest2(result_host+'player3/canais-bk.php?canal=telecinefun&img=telecinefun', host_popup_final)
        #else:
        #    data2 = ''
        host2 = re.compile('source.+?src="(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data2)
        if host2 !=[]:
            host3 = re.compile("(.+?)/hl", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(host2[0])
            host_new = host3[0]
            #print(host_new)
            servidor_rc = host_new
        else:
            servidor_rc = '' 
    except:
        servidor_rc = ''
        
    servidor1_rc = result_host
    servidor2_rc = servidor_rc
    if servidor1_rc > '' and servidor2_rc > '':
        referer_rc = servidor1_rc+'player3/canais-bk.php'
    else:
        referer_rc = ''
    return servidor1_rc, servidor2_rc, referer_rc;
    
   
servidor1_rc, servidor2_rc, referer_rc  = redecanais()


def resolver(link, name, thumbnail):
    try:
        link_decoded = base64.b32decode(link).decode('utf-8')
    except:
        link_decoded = link
    try:
        f4m = __addon__.getSetting('f4m')
        if not link_decoded.startswith("plugin://plugin") and link_decoded.startswith('https://drive.google.com') == True:
            #print('verdadeiro')          
            resolved = link_decoded.replace('http','plugin://plugin.video.gdrive?mode=streamURL&amp;url=http')
            #print(resolved)
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.startswith('http://drive.google.com') == True:
            #print('verdadeiro')
            resolved = link_decoded.replace('http','plugin://plugin.video.gdrive?mode=streamURL&amp;url=http')
            #print(resolved)
        #Rede Canais
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('hls1') >= 0 and link_decoded.find('wmsAuthSign') >= 0  and link_decoded.find('.m3u8') >= 0:
            try:
                clear1 = re.compile("Referer(.*)", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                clear2 = re.compile("User-Agent(.*)", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                if clear1 !=[] and clear2 !=[]:
                    link_clear = link_decoded.replace(clear1[0],'').replace(clear2[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                elif clear1 !=[]:
                    link_clear = link_decoded.replace(clear1[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                elif clear2 !=[]:
                    link_clear = link_decoded.replace(clear2[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                else:
                    link_clear = link_decoded
                host = re.compile("(.+?)/hl", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_clear)
                if host !=[] and servidor1_rc > '' and servidor2_rc > '':
                    link_final = link_clear.replace(host[0], servidor2_rc)
                    #print(link_final)
                if link_final and servidor1_rc > '' and servidor2_rc > '':
                    link_final2 = link_final+'|Referer='+referer_rc+'|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
                    #print(link_final2)
                else:
                    link_final2 = link_decoded
                    #print(link_final2)
            except:
                link_final2 = link_decoded
            if int(f4m) == 0:
                #print('f4m ativado')
                try:            
                    clear3 = re.compile("Referer(.*)", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_final2)
                    clear4 = re.compile("User-Agent(.*)", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_final2)
                    if clear3 !=[] and clear4 !=[]:
                        link_clear2 = link_final2.replace(clear3[0],'').replace(clear4[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                    elif clear3 !=[]:
                        link_clear2 = link_final2.replace(clear3[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                    elif clear4 !=[]:
                        link_clear2 = link_final2.replace(clear4[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                    else:
                        link_clear2 = link_final2
                        #print(link_clear)
                    get_referer = re.compile("Referer=(.*).+?User-Agent", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_final2)
                    get_referer2 = re.compile('Referer=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_final2)
                    get_user = re.compile('User-Agent=(.*).+?Referer', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_final2)
                    get_user2 = re.compile('User-Agent=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_final2)
                    if get_referer !=[]:
                        ref = get_referer[0]
                        referer = 'Referer='+ref+''
                    elif get_referer2 !=[]:
                        ref = get_referer2[0]
                        referer = 'Referer='+ref+''
                    else:
                        referer = ''
                    if get_user !=[]:
                        user = get_user[0]
                        user_agent = 'User-Agent='+user+''
                    elif get_user2 !=[]:
                        user = get_user2[0]
                        user_agent = 'User-Agent='+user+''
                    else:
                        user_agent = ''
                    if referer > '' and user_agent > '':
                        result = '|'+referer+'|'+user_agent
                    elif referer > '':
                        result = '|'+referer
                    elif user_agent > '':
                        result = '|'+user_agent
                    else:
                        result = ''
                    name2 = name.replace('&','e').replace('BR | ','').replace('BR : ','').replace('BR: ','').replace('BR| ','').replace('|','')
                    url_quote = urllib.quote_plus(link_clear2)
                    resolved1 = url_quote.replace('http','plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&amp;name='+urllib.quote_plus(name2)+'&amp;iconImage='+urllib.quote_plus(thumbnail)+'&amp;thumbnailImage='+urllib.quote_plus(thumbnail)+'&amp;url=http')
                    resolved = resolved1+urllib.quote_plus(result)
                    #print(resolved)
                except:
                    resolved = link_final2
            else:
                resolved = link_final2
                #print(resolved)       
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.mp4') >= 0 and not link_decoded.find('live.cinexplay.com') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.mkv') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.wmv') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.avi') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.mp3') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.ac3') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.rmvb') >= 0:
            resolved = link_decoded             
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.torrent') >= 0:
            resolved = 'plugin://plugin.video.elementum/play?uri='+link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.startswith('magnet:?xt=') == True:
            resolved = 'plugin://plugin.video.elementum/play?uri='+link_decoded
        #netcine.info
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.startswith('https://netcine.info/') == True:
            try:
                resultado = netcine_resolver(link_decoded)
                if resultado==None:
                    #print('vazio')
                    resolved = ''
                else:
                    resolved = resultado
            except:
                resolved = ''
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.startswith('https://youtube.com/') == True or link_decoded.startswith('https://www.youtube.com/') == True:
            try:
                resultado = youtube_resolver(link_decoded)
                if resultado==None:
                    #print('vazio')
                    resolved = ''
                else:
                    resolved = resultado
            except:
                resolved = ''
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('https://photos.app') >= 0:
            try:
                data = getRequest2(link_decoded, 'https://photos.google.com/')
                result = re.compile('<meta property="og:video" content="(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
                if result !=[]:
                    resolved = result[0].replace('-m18','-m22')
                else:
                    resolved = ''
            except:
                resolved = ''
        elif not link_decoded.startswith("plugin://plugin") and not link_decoded.find('live.cinexplay.com') >= 0 and link_decoded.find('.m3u8') >= 0:
            if int(f4m) == 0:
                clear1 = re.compile("Referer(.*)", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                clear2 = re.compile("User-Agent(.*)", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                if clear1 !=[] and clear2 !=[]:
                    link_clear = link_decoded.replace(clear1[0],'').replace(clear2[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                elif clear1 !=[]:
                    link_clear = link_decoded.replace(clear1[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                elif clear2 !=[]:
                    link_clear = link_decoded.replace(clear2[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                else:
                    link_clear = link_decoded
                #print(link_clear)
                get_referer = re.compile("Referer=(.*).+?User-Agent", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_referer2 = re.compile('Referer=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_user = re.compile('User-Agent=(.*).+?Referer', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_user2 = re.compile('User-Agent=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                if get_referer !=[]:
                    ref = get_referer[0]
                    referer = 'Referer='+ref+''
                elif get_referer2 !=[]:
                    ref = get_referer2[0]
                    referer = 'Referer='+ref+''
                else:
                    referer = ''
                if get_user !=[]:
                    user = get_user[0]
                    user_agent = 'User-Agent='+user+''
                elif get_user2 !=[]:
                    user = get_user2[0]
                    user_agent = 'User-Agent='+user+''
                else:
                    user_agent = ''
                if referer > '' and user_agent > '':
                    result = '|'+referer+'|'+user_agent
                elif referer > '':
                    result = '|'+referer
                elif user_agent > '':
                    result = '|'+user_agent
                else:
                    result = ''
                name2 = name.replace('&','e').replace('BR | ','').replace('BR : ','').replace('BR: ','').replace('BR| ','').replace('|','')
                url_quote = urllib.quote_plus(link_clear)
                resolved1 = url_quote.replace('http','plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&amp;name='+urllib.quote_plus(name2)+'&amp;iconImage='+urllib.quote_plus(thumbnail)+'&amp;thumbnailImage='+urllib.quote_plus(thumbnail)+'&amp;url=http')
                resolved = resolved1+urllib.quote_plus(result)
            else:
                resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.ts') >= 0:
            if int(f4m) == 0:
                clear1 = re.compile("Referer(.*)", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                clear2 = re.compile("User-Agent(.*)", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                if clear1 !=[] and clear2 !=[]:
                    link_clear = link_decoded.replace(clear1[0],'').replace(clear2[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                elif clear1 !=[]:
                    link_clear = link_decoded.replace(clear1[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                elif clear2 !=[]:
                    link_clear = link_decoded.replace(clear2[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                else:
                    link_clear = link_decoded
                #print(link_clear)
                get_referer = re.compile("Referer=(.*).+?User-Agent", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_referer2 = re.compile('Referer=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_user = re.compile('User-Agent=(.*).+?Referer', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_user2 = re.compile('User-Agent=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                if get_referer !=[]:
                    ref = get_referer[0]
                    referer = 'Referer='+ref+''
                elif get_referer2 !=[]:
                    ref = get_referer2[0]
                    referer = 'Referer='+ref+''
                else:
                    referer = ''
                if get_user !=[]:
                    user = get_user[0]
                    user_agent = 'User-Agent='+user+''
                elif get_user2 !=[]:
                    user = get_user2[0]
                    user_agent = 'User-Agent='+user+''
                else:
                    user_agent = ''
                if referer > '' and user_agent > '':
                    result = '|'+referer+'|'+user_agent
                elif referer > '':
                    result = '|'+referer
                elif user_agent > '':
                    result = '|'+user_agent
                else:
                    result = ''
                name2 = name.replace('&','e').replace('BR | ','').replace('BR : ','').replace('BR: ','').replace('BR| ','').replace('|','')
                url_quote = urllib.quote_plus(link_clear)
                resolved1 = url_quote.replace('http','plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name='+urllib.quote_plus(name2)+'&amp;iconImage='+urllib.quote_plus(thumbnail)+'&amp;thumbnailImage='+urllib.quote_plus(thumbnail)+'&amp;url=http')
                resolved = resolved1+urllib.quote_plus(result)
            else:
                resolved = link_decoded      
        elif not link_decoded.startswith("plugin://plugin") and not link_decoded.find('googlevideo.com') >= 0 and not link_decoded.find('blogspot.com') >= 0 and not link_decoded.find('googleusercontent.com') >= 0 and not link_decoded.find('p.netcine.info') >= 0 and not link_decoded.find('live.cinexplay.com') >= 0 and not link_decoded.find('youtube.com') >= 0 and int(link_decoded.count(":")) == 2 and int(link_decoded.count("/")) > 3:
            if int(f4m) == 0:
                clear1 = re.compile("Referer(.*)", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                clear2 = re.compile("User-Agent(.*)", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                if clear1 !=[] and clear2 !=[]:
                    link_clear = link_decoded.replace(clear1[0],'').replace(clear2[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                elif clear1 !=[]:
                    link_clear = link_decoded.replace(clear1[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                elif clear2 !=[]:
                    link_clear = link_decoded.replace(clear2[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                else:
                    link_clear = link_decoded
                #print(link_clear)
                get_referer = re.compile("Referer=(.*).+?User-Agent", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_referer2 = re.compile('Referer=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_user = re.compile('User-Agent=(.*).+?Referer', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_user2 = re.compile('User-Agent=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                if get_referer !=[]:
                    ref = get_referer[0]
                    referer = 'Referer='+ref+''
                elif get_referer2 !=[]:
                    ref = get_referer2[0]
                    referer = 'Referer='+ref+''
                else:
                    referer = ''
                if get_user !=[]:
                    user = get_user[0]
                    user_agent = 'User-Agent='+user+''
                elif get_user2 !=[]:
                    user = get_user2[0]
                    user_agent = 'User-Agent='+user+''
                else:
                    user_agent = ''
                if referer > '' and user_agent > '':
                    result = '|'+referer+'|'+user_agent
                elif referer > '':
                    result = '|'+referer
                elif user_agent > '':
                    result = '|'+user_agent
                else:
                    result = ''
                name2 = name.replace('&','e').replace('BR | ','').replace('BR : ','').replace('BR: ','').replace('BR| ','').replace('|','')
                url_quote = urllib.quote_plus(link_clear)
                resolved1 = url_quote.replace('http','plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name='+urllib.quote_plus(name2)+'&amp;iconImage='+urllib.quote_plus(thumbnail)+'&amp;thumbnailImage='+urllib.quote_plus(thumbnail)+'&amp;url=http')
                resolved = resolved1+urllib.quote_plus(result)
            else:
               resolved = link_decoded 
        else:
            #print('falso')
            resolved = link_decoded
        return resolved
    except:
        resolved = ''
        return resolved
        #pass
        #notify('[COLOR red]Não foi possivel resolver um link![/COLOR]')


def resolver_vip(link, name, thumbnail):
    link_decoded = link
    try:
        f4mvip = __addon__.getSetting('f4mvip')
        if not link_decoded.startswith("plugin://plugin") and not link_decoded.find('live.cinexplay.com') >= 0 and link_decoded.find('.m3u8') >= 0:
            if int(f4mvip) == 0:
                clear1 = re.compile("Referer(.*)", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                clear2 = re.compile("User-Agent(.*)", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                if clear1 !=[] and clear2 !=[]:
                    link_clear = link_decoded.replace(clear1[0],'').replace(clear2[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                elif clear1 !=[]:
                    link_clear = link_decoded.replace(clear1[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                elif clear2 !=[]:
                    link_clear = link_decoded.replace(clear2[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                else:
                    link_clear = link_decoded
                #print(link_clear)
                get_referer = re.compile("Referer=(.*).+?User-Agent", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_referer2 = re.compile('Referer=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_user = re.compile('User-Agent=(.*).+?Referer', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_user2 = re.compile('User-Agent=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                if get_referer !=[]:
                    ref = get_referer[0]
                    referer = 'Referer='+ref+''
                elif get_referer2 !=[]:
                    ref = get_referer2[0]
                    referer = 'Referer='+ref+''
                else:
                    referer = ''
                if get_user !=[]:
                    user = get_user[0]
                    user_agent = 'User-Agent='+user+''
                elif get_user2 !=[]:
                    user = get_user2[0]
                    user_agent = 'User-Agent='+user+''
                else:
                    user_agent = ''
                if referer > '' and user_agent > '':
                    result = '|'+referer+'|'+user_agent
                elif referer > '':
                    result = '|'+referer
                elif user_agent > '':
                    result = '|'+user_agent
                else:
                    result = ''
                name2 = name.replace('&','e').replace('BR | ','').replace('BR : ','').replace('BR: ','').replace('BR| ','').replace('|','')
                url_quote = urllib.quote_plus(link_clear)
                resolved1 = url_quote.replace('http','plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&amp;name='+urllib.quote_plus(name2)+'&amp;iconImage='+urllib.quote_plus(thumbnail)+'&amp;thumbnailImage='+urllib.quote_plus(thumbnail)+'&amp;url=http')
                resolved = resolved1+urllib.quote_plus(result)
            else:
                resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.ts') >= 0:
            if int(f4mvip) == 0:
                clear1 = re.compile("Referer(.*)", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                clear2 = re.compile("User-Agent(.*)", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                if clear1 !=[] and clear2 !=[]:
                    link_clear = link_decoded.replace(clear1[0],'').replace(clear2[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                elif clear1 !=[]:
                    link_clear = link_decoded.replace(clear1[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                elif clear2 !=[]:
                    link_clear = link_decoded.replace(clear2[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                else:
                    link_clear = link_decoded
                #print(link_clear)
                get_referer = re.compile("Referer=(.*).+?User-Agent", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_referer2 = re.compile('Referer=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_user = re.compile('User-Agent=(.*).+?Referer', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_user2 = re.compile('User-Agent=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                if get_referer !=[]:
                    ref = get_referer[0]
                    referer = 'Referer='+ref+''
                elif get_referer2 !=[]:
                    ref = get_referer2[0]
                    referer = 'Referer='+ref+''
                else:
                    referer = ''
                if get_user !=[]:
                    user = get_user[0]
                    user_agent = 'User-Agent='+user+''
                elif get_user2 !=[]:
                    user = get_user2[0]
                    user_agent = 'User-Agent='+user+''
                else:
                    user_agent = ''
                if referer > '' and user_agent > '':
                    result = '|'+referer+'|'+user_agent
                elif referer > '':
                    result = '|'+referer
                elif user_agent > '':
                    result = '|'+user_agent
                else:
                    result = ''
                name2 = name.replace('&','e').replace('BR | ','').replace('BR : ','').replace('BR: ','').replace('BR| ','').replace('|','')
                url_quote = urllib.quote_plus(link_clear)
                resolved1 = url_quote.replace('http','plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name='+urllib.quote_plus(name2)+'&amp;iconImage='+urllib.quote_plus(thumbnail)+'&amp;thumbnailImage='+urllib.quote_plus(thumbnail)+'&amp;url=http')
                resolved = resolved1+urllib.quote_plus(result)
            else:
                resolved = link_decoded      
        elif not link_decoded.startswith("plugin://plugin") and not link_decoded.find('googlevideo.com') >= 0 and not link_decoded.find('blogspot.com') >= 0 and not link_decoded.find('googleusercontent.com') >= 0 and not link_decoded.find('p.netcine.info') >= 0 and not link_decoded.find('live.cinexplay.com') >= 0 and not link_decoded.find('youtube.com') >= 0 and int(link_decoded.count(":")) == 2 and int(link_decoded.count("/")) > 3:
            if int(f4mvip) == 0:
                clear1 = re.compile("Referer(.*)", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                clear2 = re.compile("User-Agent(.*)", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                if clear1 !=[] and clear2 !=[]:
                    link_clear = link_decoded.replace(clear1[0],'').replace(clear2[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                elif clear1 !=[]:
                    link_clear = link_decoded.replace(clear1[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                elif clear2 !=[]:
                    link_clear = link_decoded.replace(clear2[0],'').replace('|Referer','').replace('|referer','').replace('|User-Agent','').replace('|user-agent','').replace('|User-agent','').replace('|user-Agent','')
                else:
                    link_clear = link_decoded
                #print(link_clear)
                get_referer = re.compile("Referer=(.*).+?User-Agent", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_referer2 = re.compile('Referer=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_user = re.compile('User-Agent=(.*).+?Referer', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                get_user2 = re.compile('User-Agent=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)
                if get_referer !=[]:
                    ref = get_referer[0]
                    referer = 'Referer='+ref+''
                elif get_referer2 !=[]:
                    ref = get_referer2[0]
                    referer = 'Referer='+ref+''
                else:
                    referer = ''
                if get_user !=[]:
                    user = get_user[0]
                    user_agent = 'User-Agent='+user+''
                elif get_user2 !=[]:
                    user = get_user2[0]
                    user_agent = 'User-Agent='+user+''
                else:
                    user_agent = ''
                if referer > '' and user_agent > '':
                    result = '|'+referer+'|'+user_agent
                elif referer > '':
                    result = '|'+referer
                elif user_agent > '':
                    result = '|'+user_agent
                else:
                    result = ''
                name2 = name.replace('&','e').replace('BR | ','').replace('BR : ','').replace('BR: ','').replace('BR| ','').replace('|','')
                url_quote = urllib.quote_plus(link_clear)
                resolved1 = url_quote.replace('http','plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name='+urllib.quote_plus(name2)+'&amp;iconImage='+urllib.quote_plus(thumbnail)+'&amp;thumbnailImage='+urllib.quote_plus(thumbnail)+'&amp;url=http')
                resolved = resolved1+urllib.quote_plus(result)
            else:
               resolved = link_decoded 
        else:
            #print('falso')
            resolved = link_decoded
        return resolved
    except:
        resolved = ''
        return resolved
        #pass
        #notify('[COLOR red]Não foi possivel resolver um link![/COLOR]')   






def addDir(name,url,mode,iconimage,fanart,description,folder=True):
    if mode == 1:
        if url > '':
            #u=sys.argv[0]+"?url="+urllib.quote_plus(base64.b64encode(url))+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
            u=sys.argv[0]+"?url="+urllib.quote_plus(codecs.encode(base64.b32encode(base64.b16encode(url)), '\x72\x6f\x74\x31\x33'))+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
        else:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(5)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
    else:
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
    if folder==True:
        li=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    else:
        li=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    li.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    if fanart > '':
        li.setProperty('fanart_image', fanart)        
    else:
        li.setProperty('fanart_image', ''+home+'/fanart.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=li, isFolder=folder)


def addDir2(name,url,mode,subtitle,cleaname,iconimage,fanart,description,folder=True):
    if mode == 1:
        if url > '':
            #u=sys.argv[0]+"?url="+urllib.quote_plus(base64.b64encode(url))+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
            u=sys.argv[0]+"?url="+urllib.quote_plus(codecs.encode(base64.b32encode(base64.b16encode(url)), '\x72\x6f\x74\x31\x33'))+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
        else:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(5)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
    else:
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)+"&iconimage="+urllib.quote_plus(iconimage)+"&subtitle="+urllib.quote_plus(subtitle)+"&cleaname="+urllib.quote_plus(cleaname)+"&description="+urllib.quote_plus(description)
    if folder==True:
        li=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    else:
        li=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    li.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    if fanart > '':
        li.setProperty('fanart_image', fanart)        
    else:
        li.setProperty('fanart_image', ''+home+'/fanart.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=li, isFolder=folder)


        

def addLink(name,url,subtitle,cleaname,iconimage,fanart,description,folder=False):
    if iconimage > '':
        thumbnail = iconimage
    else:
        thumbnail = 'DefaultVideo.png'
    li = xbmcgui.ListItem(name, iconImage=thumbnail, thumbnailImage=thumbnail)
    if url.startswith("plugin://plugin.video.f4mTester"):
        li.setProperty('IsPlayable', 'false')
    else:
        li.setProperty('IsPlayable', 'true')
    if fanart > '':
        li.setProperty('fanart_image', fanart)        
    else:
        li.setProperty('fanart_image', ''+home+'/fanart.jpg')
    if cleaname > '':
        li.setInfo(type='video', infoLabels={'Title': cleaname, 'plot': description })
    else:
        li.setInfo(type='video', infoLabels={'plot': description })
    if subtitle > '':
        li.setSubtitles([subtitle])
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=folder)
    


def parental_password():
    addonID = xbmcaddon.Addon().getAddonInfo('id')
    addon_data_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', addonID))
    if os.path.exists(addon_data_path)==False:
        os.mkdir(addon_data_path)
    xbmc.sleep(4)
    #Path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode("utf-8")
    #arquivo = os.path.join(Path, "password.txt")
    arquivo = os.path.join(addon_data_path, "password.txt")
    exists = os.path.isfile(arquivo)
    if exists == False:
        password = '0069'
        p_encoded = base64.b64encode(password.encode()).decode('utf-8')
        p_file = open(arquivo,'w')
        p_file.write(p_encoded)
        p_file.close()




def check_addon():
    try:
        check_file = xbmc.translatePath(home+'/check.txt')
        exists = os.path.isfile(check_file)
        check_addon = addon.getSetting('check_addon')
        #check_file = 'check.txt'
        if exists == True:
            #print('existe')
            fcheck = open(check_file,'r+')
            elementum = addon.getSetting('elementum')
            if fcheck and fcheck.read() == '1' and check_addon == 'true':
                #print('valor 1')
                fcheck.close()
                link = getRequest2('https://raw.githubusercontent.com/OnePlayHD/OneRepo/master/verificar_addons.txt','').replace('\n','').replace('\r','')
                match = re.compile('addon_name="(.+?)".+?ddon_id="(.+?)".+?ir="(.+?)".+?rl_zip="(.+?)".+?escription="(.+?)"').findall(link)
                for addon_name,addon_id,directory,url_zip,description in match:                  
                    #if addon_id == id_elementum:
                    if addon_id == 'plugin.video.elementum' and elementum == 'false':
                        pass
                    else:
                        existe = xbmc.translatePath(directory)
                        #print('Path dir:'+existe)
                        if os.path.exists(existe)==False:
                            install_wizard(addon_name,addon_id,url_zip,directory,description)
                            anti_bug(addon_id)
                            if addon_id == 'plugin.video.elementum':
                                xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','FECHE O KODI E ABRA NOVAMENTE PARA ATIVAR O ELEMENTUM')
                        else:
                            pass
        elif check_addon == 'true':
            #print('nao existe')
            fcheck = open(check_file,'w')
            fcheck.write('1')
            fcheck.close()
            xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','FECHE O KODI E ABRA NOVAMENTE PARA VERIFICAR COMPLEMENTOS')
    except:
        pass



def install_wizard(name,addon_id,url,directory,description):
    try:
        import downloader
        import extract
        import ntpath
        #import zipfile
        path = xbmc.translatePath(os.path.join('special://','home/','addons', 'packages'))
        print('Path download:'+path)
        filename = ntpath.basename(url)
        dp = xbmcgui.DialogProgress()
        dp.create("Install addons","Baixando "+name+"....",'', '')
        lib=os.path.join(path, filename)
        try:
         os.remove(lib)
        except:
            pass
        #downloader.download(url, lib, dp)
        downloader.download(url, name, lib, dp)
        addonfolder = xbmc.translatePath(os.path.join('special://','home/','addons'))
        #time.sleep(2)
        xbmc.sleep(100)
        dp.update(0,"", "Instalando "+name+", Por Favor Espere")
        #extract.all(lib,addonfolder,dp)
        #### zip
        #zf = zipfile.ZipFile(lib)
        #zf.extractall(addonfolder)
        try:
            xbmc.executebuiltin("Extract("+lib+","+addonfolder+")")
        except:
            extract.all(lib,addonfolder,dp) 
        #############
        #time.sleep(2)
        xbmc.sleep(100)
        xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
        notify(name+' Instalado com Sucesso!')
        import database
        database.enable_addon(0, addon_id)
        database.check_database(addon_id)
        #xbmc.executebuiltin("XBMC.Container.Refresh()")
        xbmc.executebuiltin("XBMC.Container.Update()")
        #xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]',''+name+' instalado, feche e abra o Kodi novamente')
    except:
        notify('Erro ao baixar o complemento')



def anti_bug(addon_id):
    import database
    database.enable_addon(0, addon_id)


def CheckUpdate(msg):
	try:
		uversao = urllib2.urlopen( "http://raw.githubusercontent.com/OnePlayHD/OneRepo/master/plugin.video.OnePlay/version.txt" ).read().replace('','').replace('','')
		uversao = re.compile('[a-zA-Z\.\d]+').findall(uversao)[0]
		#xbmcgui.Dialog().ok(Versao, uversao)
		if uversao != Versao:
			Update()
			#xbmc.executebuiltin("XBMC.Container.Refresh()")
		elif msg==True:
			xbmcgui.Dialog().ok('[COLOR aquamarine][B]ONE[/COLOR][COLOR white]PLAY[/B][/COLOR]', "O addon já está atualizado na [COLOR aquamarine]Versão: 3.0[/COLOR] em: "+Versao+"\nAs atualizações normalmente são automáticas caso não atualize baixe o add-on no site oficial.\n[COLOR aquamarine][B]Use esse recurso caso não esteja recebendo automático.[/B][/COLOR]")
			xbmc.executebuiltin("XBMC.Container.Refresh()")
	except urllib2.URLError, e:
		if msg==True:
			xbmcgui.Dialog().ok('[COLOR aquamarine][B]ONE[/COLOR][COLOR white]PLAY[/B][/COLOR]', "Não foi possível atualizar. Tente novamente mais tarde.")


def Update():
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') ).decode("utf-8")
	try:
		fonte = urllib2.urlopen( "http://raw.githubusercontent.com/OnePlayHD/OneRepo/master/plugin.video.OnePlayLite/main.py" ).read().replace('','')
		prog = re.compile('checkintegrity13122019').findall(fonte)
		if prog:
			py = os.path.join( Path, "main.py")
			file = open(py, "w")
			file.write(fonte)
			file.close()
		fonte = urllib2.urlopen( "http://raw.githubusercontent.com/OnePlayHD/OneRepo/master/plugin.video.OnePlayLite/resources/settings.xml" ).read().replace('','')
		prog = re.compile('</settings>').findall(fonte)
		if prog:
			py = os.path.join( Path, "resources/settings.xml")
			file = open(py, "w")
			file.write(fonte)
			file.close()
		fonte = urllib2.urlopen( "http://raw.githubusercontent.com/OnePlayHD/OneRepo/master/plugin.video.OnePlayLite/addon.xml" ).read().replace('','')
		prog = re.compile('</addon>').findall(fonte)
		if prog:
			py = os.path.join( Path, "addon.xml")
			file = open(py, "w")
			file.write(fonte)
			file.close()
		xbmc.executebuiltin("Notification({0}, {1}, 9000, {2})".format(__addonname__, "Atualizando o add-on. Aguarde...", __icon__))
	except:
		xbmcgui.Dialog().ok('[COLOR aquamarine][B]ONE[/COLOR][COLOR white]PLAY[/B][/COLOR]', "A Sua versão está desatualizada, mas não se preocupe que a atualização é automática, Caso ocorrer algum erro\n[COLOR aquamarine]Atualize o add-on no repositorio ou baixe o zip no site oficial[/COLOR].")




def suporte():
    import xbmc
    import webbrowser
    dialog = xbmcgui.Dialog()
    link = dialog.select('[B][COLOR white]SUPORTE[/COLOR] [COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR][/B]', ['[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: SITE', '[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: REPOSITÓRIO','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: APP [COLOR gold](VIP)[/COLOR] PLAYSTORE','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: FACEBOOK','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: TELEGRAM','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: [B][COLOR white]ENTRAR NO ADDON[/COLOR][/B]'])
    if link == 0:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://oneplayhd.tk'))
        else:
            webbrowser.open('https://oneplayhd.tk')

    if link == 1:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://oneplayhd.tk/oneplay'))
        else:
            webbrowser.open('https://oneplayhd.tk/oneplay')

    if link == 2:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://play.google.com/store/apps/details?id=com.pp.ppvpn'))
        else:
            webbrowser.open('https://play.google.com/store/apps/details?id=com.pp.ppvpn')

    if link == 3:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://www.facebook.com/groups/oneplay2019' ))
        else:
            webbrowser.open('https://www.facebook.com/groups/oneplay2019')

    if link == 4:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://t.me/oneplay2019' ))
        else:
            webbrowser.open('https://t.me/oneplay2019')


def doacao():
    import xbmc
    import webbrowser
    dialog = xbmcgui.Dialog()
    link = dialog.select('[B][COLOR white]FAÇA UMA DOAÇÃO AO[/COLOR] [COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR][/B]', ['[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: DOAÇÃO [COLOR steelblue]MERCADO[/COLOR][COLOR skyblue]PAGO[/COLOR] R$10,00','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: DOAÇÃO [COLOR steelblue]MERCADO[/COLOR][COLOR skyblue]PAGO[/COLOR] R$15,00','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: DOAÇÃO [COLOR steelblue]MERCADO[/COLOR][COLOR skyblue]PAGO[/COLOR] R$20,00','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: DOAÇÃO [COLOR lime]PYCPAY[/COLOR]','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: DOAÇÃO [COLOR white]PAG[/COLOR][COLOR lime]SEGURO[/COLOR]','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: DOAÇÃO [COLOR white]DEPOSITO[/COLOR][COLOR dodgerblue]CAIXA[/COLOR]','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: DOAÇÃO [COLOR white]COM ANÚNCIO[/COLOR]','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: [B][COLOR white]CONTINUAR NO ADDON[/COLOR][/B]'])
 
    if link == 0:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=157151682-e75906b8-d000-4cfc-8fa5-407387a96445' ))
        else:
            webbrowser.open('https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=157151682-e75906b8-d000-4cfc-8fa5-407387a96445')
    if link == 1:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=157151682-5396b567-001a-43e2-b83b-a587eaa2a203' ))
        else:
            webbrowser.open('https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=157151682-5396b567-001a-43e2-b83b-a587eaa2a203')
    if link == 2:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=157151682-5b8b20bc-df56-4c95-9c3e-a64cc0a7ee58' ))
        else:
            webbrowser.open('https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=157151682-5b8b20bc-df56-4c95-9c3e-a64cc0a7ee58')
    if link == 3:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://app.picpay.com/user/paulo9493' ))
        else:
            webbrowser.open('https://app.picpay.com/user/paulo9493')
    if link == 4:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://pag.ae/7V4uYahnJ' ))
        else:
            webbrowser.open('https://pag.ae/7V4uYahnJ')
    if link == 5:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://oneplayhd.tk/oneplay/doar.jpg' ))
        else:
            webbrowser.open('https://oneplayhd.tk/oneplay/doar.jpg')
    #pagina anuncio
    if link == 6:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://oneplayhd.tk/' ))
        else:
            webbrowser.open('https://oneplayhd.tk/')


def vip():
    username_vip = addon.getSetting('username')
    password_vip = addon.getSetting('password')
    #tipo_servidor = addon.getSetting('servidor')
    vip_menu = addon.getSetting('exibirvip')
    saida_transmissao = addon.getSetting('saida')
    if vip_menu == 'true':
        #if tipo_servidor=='OnePlay':
        if username_vip > '' and password_vip > '':
            url = ''+url_server_vip+'?username=%s&password=%s&type=m3u_plus&output=%s'%(username_vip,password_vip,saida_transmissao)
            #addDir(name,url,mode,iconimage,fanart,description)
            addDir(titulo_vip,url,1,thumbnail_vip,fanart_vip,getRequest2(url_vip_descricao, ''))
        else:
            #if tipo_servidor=='Desativado':
            #addDir(name,url,mode,iconimage,fanart,description)
            addDir(titulo_vip,'',9,thumbnail_vip,fanart_vip,getRequest2(url_vip_descricao, ''))


        

def Pesquisa(): # 43
	d = xbmcgui.Dialog().input("A Pesquisa pode demorar a carregar os resultados").replace(" ", "+")
	if d > '':
            #addDir('[COLOR white][B]PESQUISAR NOVAMENTE...[/B][/COLOR]','',43,thumb_pesquisar,fanart_pesquisar,descricao(url_desc_pesquisa),'','','')
            addDir('[COLOR white][B]PESQUISAR NOVAMENTE...[/B][/COLOR]','',7,thumb_pesquisar,fanart_pesquisar,getRequest2(url_desc_pesquisa, ''))
            #getData('https://localhost/get.php?pesquisar='+d,'')
            getData(url_pesquisa+'?pesquisar='+d, '')
            xbmcplugin.endOfDirectory(addon_handle)           
        else:
            xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]',mensagem_busca_invalida)
            xbmc.executebuiltin("XBMC.Container.Refresh()")
# ----------------- FIM PESQUISA
   
    


def SetView(name):
    if name == 'Wall':
        try:
            xbmc.executebuiltin('Container.SetViewMode(500)')
        except:
            pass
    if name == 'List':
        try:
            xbmc.executebuiltin('Container.SetViewMode(50)')
        except:
            pass
    if name == 'Poster':
        try:
            xbmc.executebuiltin('Container.SetViewMode(51)')
        except:
            pass
    if name == 'Shift':
        try:
            xbmc.executebuiltin('Container.SetViewMode(53)')
        except:
            pass
    if name == 'InfoWall':
        try:
            xbmc.executebuiltin('Container.SetViewMode(54)')
        except:
            pass
    if name == 'WideList':
        try:
            xbmc.executebuiltin('Container.SetViewMode(55)')
        except:
            pass
    if name == 'Fanart':
        try:
            xbmc.executebuiltin('Container.SetViewMode(502)')
        except:
            pass
    
def SKindex():
    #addDir(name,url,mode,iconimage,fanart,description)
    CheckUpdate(False)
    if addon.getSetting('mensagem1') == 'true':
        xbmcgui.Dialog().ok(titulo_boas_vindas,mensagem_bem_vindo)
    if addon.getSetting('popupsupport') == 'true':
        suporte()
    addDir(title_menu,url_title,1,__icon__,'',getRequest2(url_title_descricao, ''))
    ### VIP ##############
    vip()
    addDir('[B][COLOR aquamarine]DOAÇÃO[/COLOR][/B]','',8,'https://i.imgur.com/UB6K2Xt.png','','Faça uma doação ao ONEPLAY entrando aqui e escolhendo umas das opções')
    if addon.getSetting('pesquisa') == 'true':
        addDir(menu_pesquisar,'',7,thumb_pesquisar,fanart_pesquisar,getRequest2(url_desc_pesquisa, ''))
    getData(url_principal, '')
    addDir(menu_atualizacao,'',12,thumb_update,'',desc_atualizacao)
    addDir(menu_configuracoes,'',4,thumb_icon_config,'',desc_configuracoes)
    if addon.getSetting('mensagem2') == 'true':
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,getRequest2(url_mensagem, ''), time_msg, __icon__))
    xbmcplugin.endOfDirectory(addon_handle)


def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
        
                      
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None

xbmcplugin.setContent(addon_handle, 'movies')


try:
    #url=urllib.unquote(params["url"])
    url=urllib.unquote_plus(params["url"]).decode('utf-8')
except:
    pass
    
try:
    #name=urllib.unquote(params["name"])
    name=urllib.unquote_plus(params["name"])
except:
    pass
    
try:
    #iconimage=urllib.unquote(params["iconimage"])
    iconimage=urllib.unquote_plus(params["iconimage"])
except:
    pass
    
try:        
    mode=int(params["mode"])
except:
    pass
    
try:        
    #fanart=urllib.unquote(params["fanart"])
    fanart=urllib.unquote_plus(params["fanart"])
except:
    pass

try:        
    #description=urllib.unquote(params["description"])
    description=urllib.unquote_plus(params["description"])
except:
    pass
        
try:
    subtitle=urllib.unquote_plus(params["subtitle"])
except:
    pass
    
try:
    cleaname=urllib.unquote_plus(params["cleaname"])
except:
    pass
    


if mode==None:
    check_addon()
    parental_password()
    if epgEnabled == "true": updateEPG()    
    SKindex()
    SetView('List')

elif mode==1:
    url = base64.b16decode(base64.b32decode(codecs.decode(url, '\x72\x6f\x74\x31\x33')))
    #url = base64.b64decode(url)
    getData(url, fanart)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode==2:
    getChannelItems(name,url,fanart)
    xbmcplugin.endOfDirectory(addon_handle)
    
elif mode==3:    
    getSubChannelItems(name,url,fanart)
    xbmcplugin.endOfDirectory(addon_handle)


#Configurações
elif mode==4:
    xbmcaddon.Addon().openSettings()
    xbmc.executebuiltin("XBMC.Container.Refresh")
    xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','FECHE O KODI E ABRA NOVAMENTE PARA ATUALIZAR AS CONFIGURAÇÕES')
    xbmc.executebuiltin("XBMC.Container.Refresh")

#Link Vazio
elif mode==5:
    xbmc.executebuiltin("XBMC.Container.Refresh")
    
elif mode==6:
    youtube(url)
    xbmcplugin.endOfDirectory(addon_handle)
    
elif mode == 7:
	Pesquisa()
    
elif mode == 8:
	doacao()
    
elif mode==9:   
    #xbmcgui.Dialog().ok('[COLOR gold][B](VIP) [/B][/COLOR][COLOR aquamarine][B]AREA ASSINANTES[/B][/COLOR]', dialog4)    
    xbmcgui.Dialog().ok(titulo_vip, getRequest2(url_vip_dialogo, ''))
    xbmcaddon.Addon().openSettings()
    xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','FECHE O KODI E ABRA NOVAMENTE PARA ATUALIZAR AS CONFIGURAÇÕES')
    xbmc.executebuiltin("XBMC.Container.Refresh")
    
elif mode==10: 
    adult(name, url, cleaname, iconimage, description, subtitle)
    xbmcplugin.endOfDirectory(addon_handle)
    
elif mode==11: 
    playlist(name, url, cleaname, iconimage, description, subtitle)
    xbmcplugin.endOfDirectory(addon_handle)
    
elif mode==12:
	CheckUpdate(True)