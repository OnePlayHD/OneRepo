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
from BeautifulSoup import BeautifulStoneSoup, BeautifulSOAP
from bs4 import BeautifulSoup
try:
    import json
except:
    import simplejson as json

Versao_data = "04.08.2020"
Versao_numero = "3.0.7"
nome_contador = "OnePlay-3.0.7"

##CONFIGURAÇÕES
####  TITULO DO MENU  #################################################################
title_menu = '[B][COLOR aquamarine]:::[/COLOR][COLOR white]BEM-VINDOS AO ONEPLAY[/COLOR][COLOR aquamarine]:::[/COLOR][/B]'
###  DESCRIÇÃO DO ADDON ###############################################################
url_title_descricao = 'https://pastebin.com/raw/gVEzmZwm'
####  LINK DO TITULO DE MENU  #########################################################
## OBS: POR PADRÃO JÁ TEM UM MENU EM BRANCO PARA NÃO TER ERRO AO CLICAR ###############
url_b64_title = '\x61\x48\x52\x30\x63\x44\x6f\x76\x4c\x32\x4a\x70\x64\x43\x35\x73\x65\x53\x39\x50\x62\x6d\x56\x51\x62\x47\x46\x35\x56\x6b\x6c\x51'
url_title = base64.b64decode(url_b64_title).decode('utf-8')

#### MENSAGEM BEM VINDOS  #############################################################
titulo_boas_vindas = 'BEM-VINDOS'
url_mensagem_bem_vindo = 'https://pastebin.com/raw/2dGv18zq'
####  MENSAGEM SECUNDARIA ######################################################
url_mensagem = 'https://pastebin.com/raw/gZHzn7v9'
####  TEMPO DA MENSAGEM EM MILISEGUNDOS ###############################################
time_msg = 15000

##### PESQUISA - get.php
url_b64_pesquisa = '\x61\x48\x52\x30\x63\x48\x4d\x36\x4c\x79\x39\x76\x62\x6d\x56\x77\x62\x47\x46\x35\x61\x47\x51\x75\x59\x32\x39\x74\x4c\x31\x42\x46\x55\x31\x46\x56\x53\x56\x4e\x42\x4c\x32\x64\x6c\x64\x43\x35\x77\x61\x48\x41\x3d'
url_pesquisa = base64.b64decode(url_b64_pesquisa).decode('utf-8')
menu_pesquisar = '[COLOR white][B]PESQUISAR...[/B][/COLOR]'
thumb_pesquisar = 'https://i.imgur.com/EinrK5v.png'
fanart_pesquisar = 'https://i.imgur.com/Cr8VMcr.jpg'
#### Descrição Pesquisa
url_desc_pesquisa = 'https://pastebin.com/raw/jy1i34SJ'
## MENU DOAÇÃO
menu_doacao = '[B][COLOR aquamarine]DOAÇÃO[/COLOR][/B]'
thumb_icon_doacao = 'https://i.imgur.com/UB6K2Xt.png'
desc_doacao = '[B][COLOR red]AVISO IMPORTANTE[/COLOR][/B]\n\nA Doação é para ajudar no projeto gratuito do addon que estamos fazendo para vocês, Quem fez doação acima de 10 tem direito a acesso ao grupo oficial WhatsApp, entre em contato e envie o comprovante.\n\nOBS: Sobre o VIP é outro departamento, entre em contato e pergunte para mais informações.'
## MENU ATUALIZAÇÃO
menu_atualizacao = '[B][COLOR aquamarine]ATUALIZAÇÃO[/COLOR][/B]'
thumb_update = 'https://i.imgur.com/flpknUR.png'
desc_atualizacao = 'Faça atualização automática no ONEPLAY usando esse recurso, só entrar que a atualização é verificada e atualizado.'
## MENU CONFIGURAÇÕES
menu_configuracoes = '[B][COLOR white]CONFIGURAÇÕES[/COLOR][/B]'
thumb_icon_config = 'https://i.imgur.com/PuULJQp.png'
desc_configuracoes = 'Configure o addon OnePlay conforme desejado Desativando ou ativando as notificações e muito mais.'

## FAVORITOS
menu_favoritos = '[B][COLOR white]FAVORITOS[/COLOR][/B]'
thumb_favoritos = 'https://i.imgur.com/q09OJRb.png'
desc_favoritos = 'Adicione Itens aos Favoritos, pressionando OK do controle ou clicando o direito e selecionando Adicionar aos favoritos do Oneplay'

#### MENU VIP ################################################################
titulo_vip = '[COLOR aquamarine][B]ÁREA DE ACESSO[/B][/COLOR] [COLOR gold][B](VIP)[/B][/COLOR]'
thumbnail_vip = 'https://i.imgur.com/5rgqF8K.png'
fanart_vip = 'https://i.imgur.com/nTIPRcu.png'
#### DESCRIÇÃO VIP ###########################################################
url_vip_descricao = 'https://pastebin.com/raw/0ZXHJ06u'
#### DIALOGO VIP - SERVIDOR DESATIVADO - CLICK ###################################
url_vip_dialogo = 'https://pastebin.com/raw/6wTe6Kgd'
##SERIVODR VIP
url_server_vip = 'http://tv.fxplay.me/get.php'


## MULTLINK
## nome para $nome, padrão: lsname para $lsname
playlist_command = 'nome'
dialog_playlist = 'Selecione um item'


# user - Padrão: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0
useragent = base64.b32decode('\x47\x42\x58\x47\x4b\x55\x42\x52\x47\x52\x34\x53\x36\x4d\x5a\x4f\x47\x41\x58\x44\x4f\x3d\x3d\x3d').decode('utf-8')

# Base
url_b64_principal = '\x61\x48\x52\x30\x63\x44\x6f\x76\x4c\x32\x4a\x70\x64\x43\x35\x73\x65\x53\x39\x50\x62\x6d\x56\x51\x62\x47\x46\x35\x51\x6d\x46\x7a\x5a\x51\x3d\x3d'
url_principal = base64.b64decode(url_b64_principal).decode('utf-8')


if sys.argv[1] == 'limparEPG':
    Path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode("utf-8")
    arquivo = os.path.join(Path, "xmltv.xml")
    exists = os.path.isfile(arquivo)
    if exists:
        try:
            os.remove(arquivo)
        except:
            pass
    xbmcaddon.Addon().setSetting("epg_last", "")
    xbmcgui.Dialog().ok('Sucesso', '[B][COLOR aquamarine]EPG excluído com sucesso![/COLOR][/B]', 'Não se esqueça de salvar as configurações clicando em OK.')
    xbmc.sleep(2000)
    exit()


if sys.argv[1] == 'limparFavoritos':
    Path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode("utf-8")
    arquivo = os.path.join(Path, "favorites.dat")
    exists = os.path.isfile(arquivo)
    if exists:
        try:
            os.remove(arquivo)
        except:
            pass
    xbmcgui.Dialog().ok('Sucesso', '[B][COLOR aquamarine]Favoritos limpo com sucesso![/COLOR][/B]')
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



addon_handle = int(sys.argv[1])
__addon__ = xbmcaddon.Addon()
addon = __addon__
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
addon_version = __addon__.getAddonInfo('version')
profile = xbmc.translatePath(__addon__.getAddonInfo('profile').decode('utf-8'))
home = xbmc.translatePath(__addon__.getAddonInfo('path').decode('utf-8'))
favorites = os.path.join(profile, 'favorites.dat')
favoritos = xbmcaddon.Addon().getSetting("favoritos")

if os.path.exists(favorites)==True:
    FAV = open(favorites).read()
else:
    FAV = []


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
            number_http = random.randint(0,total1-1)
            proxy_http = 'http://'+list1[number_http]
            ##https
            data_proxy2 = getRequest2('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=BR&ssl=yes&anonymity=all', '')
            list2 = data_proxy2.splitlines()
            total2 = len(list2)
            number_https = random.randint(0,total2-1)
            proxy_https = 'https://'+list2[number_https]
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



def getRequest2(url,ref,userargent=False):
    try:
        try:
            import urllib.request as urllib2
        except ImportError:
            import urllib2
        if ref > '':
            ref = ref
        else:
            ref = url
        if userargent:
            client_user = userargent
        else:
            client_user = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        request_headers = {
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,ru;q=0.7,de-DE;q=0.6,de;q=0.5,de-AT;q=0.4,de-CH;q=0.3,ja;q=0.2,zh-CN;q=0.1,zh;q=0.1,zh-TW;q=0.1,es;q=0.1,ar;q=0.1,en-GB;q=0.1,hi;q=0.1,cs;q=0.1,el;q=0.1,he;q=0.1,en-US;q=0.1",
        "User-Agent": client_user,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Referer": ref
        }
        request = urllib2.Request(url, headers=request_headers)
        response = urllib2.urlopen(request).read().decode('utf-8')
        #response = urllib2.urlopen(request).read()
        return response
    except:
        pass



epg_download = base64.b64decode('aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3LzREd01oaFo2').decode('utf-8')
epg_url = getRequest2(epg_download, '')
epgEnabled = xbmcaddon.Addon().getSetting("epg")
epgLast = xbmcaddon.Addon().getSetting("epg_last")
epgDays = xbmcaddon.Addon().getSetting("epg_days")



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



def getData(url, fanart, pesquisa=False):
    adult = xbmcaddon.Addon().getSetting("adult")
    adult2 = xbmcaddon.Addon().getSetting("adult2")
    uhdtv = addon.getSetting('uhdtv')
    fhdtv = addon.getSetting('fhdtv')
    hdtv = addon.getSetting('hdtv')
    sdtv = addon.getSetting('sdtv')
    filtrar = addon.getSetting('filtrar')
    data = resolve_data(url)
    soup = BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
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
                        #raise
                        fanArt = ''
                except:
                    fanArt = fanart

                try:
                    desc = channel('info')[0].string
                    if desc == None:
                        #raise
                        desc = ''
                except:
                    desc = ''

                try:
                    if linkedUrl=='':
                        #addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),2,thumbnail,fanArt,desc,genre,date,credits,True)
                        if pesquisa:
                            addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),2,thumbnail,fanArt,desc,True,True)
                        else:
                            addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),2,thumbnail,fanArt,desc)
                    else:
                        #print linkedUrl
                        #addDir(name.encode('utf-8'),linkedUrl.encode('utf-8'),1,thumbnail,fanArt,desc,genre,date,None,'source')
                        if adult == 'false' and re.search("ADULTOS",name,re.IGNORECASE) and name.find('(+18)') >=0:
                            pass
                        else:
                            if pesquisa:
                                addDir(name.encode('utf-8', 'ignore'),linkedUrl.encode('utf-8'),1,thumbnail,fanArt,desc,True,True)
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

                if 'group-title' in other:
                    cat = re_me(other,'group-title=[\'"](.*?)[\'"]')
                else:
                    cat = ''

                try:
                    if xbmcaddon.Addon().getSetting("epg") == "true":
                        if uhdtv == 'false' and re.search("4K",channel_name):
                            pass
                        elif fhdtv == 'false' and re.search("FHD",channel_name):
                            pass
                        elif hdtv == 'false' and re.search("HD",channel_name) and not re.search("FHD",channel_name):
                            pass
                        elif sdtv == 'false' and re.search("SD",channel_name):
                            pass
                        elif sdtv == 'false' and not re.search("SD",channel_name) and not re.search("HD",channel_name) and not re.search("4K",channel_name):
                            pass
                        #Futebol
                        elif int(filtrar) == 1 and re.search("Praia",channel_name,re.IGNORECASE):
                            pass
                        elif int(filtrar) == 1 and not re.search("SPORTV",channel_name,re.IGNORECASE) and not re.search("DAZN",channel_name,re.IGNORECASE) and not re.search("ESPN Brasil",channel_name,re.IGNORECASE) and not re.search("PREMIERE",channel_name,re.IGNORECASE) and not re.search("COPA",channel_name,re.IGNORECASE):
                            pass
                        #Esportes
                        elif int(filtrar) == 2 and re.search("Praia",channel_name,re.IGNORECASE):
                            pass
                        elif int(filtrar) == 2 and not re.search("Band Sports",channel_name,re.IGNORECASE) and not re.search("Combate",channel_name,re.IGNORECASE) and not re.search("Fox Sports",channel_name,re.IGNORECASE) and not re.search("SPORTV",channel_name,re.IGNORECASE) and not re.search("DAZN",channel_name,re.IGNORECASE) and not re.search("ESPN",channel_name,re.IGNORECASE) and not re.search("PREMIERE",channel_name,re.IGNORECASE) and not re.search("COPA",channel_name,re.IGNORECASE):
                            pass
                        #Filmes e Series
                        elif int(filtrar) == 3 and re.search("Sports",channel_name,re.IGNORECASE):
                            pass
                        elif int(filtrar) == 3 and re.search("XY Max",channel_name,re.IGNORECASE):
                            pass
                        elif int(filtrar) == 3 and not re.search("AMC",channel_name,re.IGNORECASE) and not re.search("Canal Brasil",channel_name,re.IGNORECASE) and not re.search("Cinemax",channel_name,re.IGNORECASE) and not re.search("HBO",channel_name,re.IGNORECASE) and not re.search("Max",channel_name,re.IGNORECASE) and not re.search("Megapix",channel_name,re.IGNORECASE) and not re.search("Paramount",channel_name,re.IGNORECASE) and not re.search("SPACE",channel_name,re.IGNORECASE) and not re.search("TCM",channel_name,re.IGNORECASE) and not re.search("Telecine Action",channel_name,re.IGNORECASE) and not re.search("TC Action",channel_name,re.IGNORECASE) and not re.search("Telecine Cult",channel_name,re.IGNORECASE) and not re.search("TC Cult",channel_name,re.IGNORECASE) and not re.search("TC Cult",channel_name,re.IGNORECASE) and not re.search("Telecine Fun",channel_name,re.IGNORECASE) and not re.search("TC Fun",channel_name,re.IGNORECASE) and not re.search("Telecine Pipoca",channel_name,re.IGNORECASE) and not re.search("TC Pipoca",channel_name,re.IGNORECASE) and not re.search("Telecine Premium",channel_name,re.IGNORECASE) and not re.search("TC Premium",channel_name,re.IGNORECASE) and not re.search("Telecine Touch",channel_name,re.IGNORECASE) and not re.search("TC Touch",channel_name,re.IGNORECASE) and not re.search("TNT",channel_name,re.IGNORECASE) and not re.search("A&E",channel_name,re.IGNORECASE) and not re.search("AXN",channel_name,re.IGNORECASE) and not re.search("AXN",channel_name,re.IGNORECASE) and not re.search("FOX",channel_name,re.IGNORECASE) and not re.search("FX",channel_name,re.IGNORECASE) and not re.search("SONY",channel_name,re.IGNORECASE) and not re.search("Studio Universal",channel_name,re.IGNORECASE) and not re.search("SyFy",channel_name,re.IGNORECASE) and not re.search("Universal Channel",channel_name,re.IGNORECASE) and not re.search("Universal TV",channel_name,re.IGNORECASE) and not re.search("Warner",channel_name,re.IGNORECASE):
                            pass
                        #Infantil
                        elif int(filtrar) == 4 and re.search("FM",channel_name,re.IGNORECASE):
                            pass
                        elif int(filtrar) == 4 and not re.search("Baby TV",channel_name,re.IGNORECASE) and not re.search("BOOMERANG",channel_name,re.IGNORECASE) and not re.search("CARTOON NETWORK",channel_name,re.IGNORECASE) and not re.search("DISCOVERY KIDS",channel_name,re.IGNORECASE) and not re.search("DISNEY",channel_name,re.IGNORECASE) and not re.search("GLOOB",channel_name,re.IGNORECASE) and not re.search("NAT GEO KIDS",channel_name,re.IGNORECASE) and not re.search("NICKELODEON",channel_name,re.IGNORECASE) and not re.search("NICK JR",channel_name,re.IGNORECASE) and not re.search("PLAYKIDS",channel_name,re.IGNORECASE) and not re.search("TOONCAST",channel_name,re.IGNORECASE) and not re.search("ZOOMOO",channel_name,re.IGNORECASE):
                            pass
                        #Documentario
                        elif int(filtrar) == 5  and re.search("Kids",channel_name,re.IGNORECASE):
                            pass
                        elif int(filtrar) == 5 and not re.search("Discovery",channel_name,re.IGNORECASE) and not re.search("H2 HD",channel_name,re.IGNORECASE) and not re.search("H2 SD",channel_name,re.IGNORECASE) and not re.search("H2 FHD",channel_name,re.IGNORECASE) and not re.search("History",channel_name,re.IGNORECASE) and not re.search("Nat Geo Wild",channel_name,re.IGNORECASE) and not re.search("National Geographic",channel_name,re.IGNORECASE):
                            pass
                        #Abertos
                        elif int(filtrar) == 6 and re.search("Brasileirinhas",channel_name,re.IGNORECASE):
                            pass
                        elif int(filtrar) == 6 and re.search("News",channel_name,re.IGNORECASE) or int(filtrar) == 6 and re.search("Sat",channel_name,re.IGNORECASE) or int(filtrar) == 6 and re.search("FM",channel_name,re.IGNORECASE):
                            pass
                        elif int(filtrar) == 6 and not re.search("Globo",channel_name,re.IGNORECASE) and not re.search("RECORD",channel_name,re.IGNORECASE) and not re.search("RedeTV",channel_name,re.IGNORECASE) and not re.search("Rede Vida",channel_name,re.IGNORECASE) and not re.search("SBT",channel_name,re.IGNORECASE) and not re.search("TV Brasil",channel_name,re.IGNORECASE) and not re.search("TV Cultura",channel_name,re.IGNORECASE) and not re.search("TV Diario",channel_name,re.IGNORECASE) and not re.search("BAND",channel_name,re.IGNORECASE):
                            pass
                        #Reality show
                        elif int(filtrar) == 7 and not re.search("BBB",channel_name,re.IGNORECASE) and not re.search("Big Brother Brasil",channel_name,re.IGNORECASE) and not re.search("A Fazenda",channel_name,re.IGNORECASE):
                            pass
                        #Noticias
                        elif int(filtrar) == 8 and re.search("FM",channel_name,re.IGNORECASE):
                            pass
                        elif int(filtrar) == 8 and not re.search("CNN",channel_name,re.IGNORECASE) and not re.search("NEWS",channel_name,re.IGNORECASE):
                            pass
                        elif adult2 == 'false' and re.search("Adult",cat,re.IGNORECASE) or adult2 == 'false' and re.search("ADULT",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Blue Hustler",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("PlayBoy",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Redlight",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Sextreme",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("SexyHot",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Venus",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("AST TV",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("ASTTV",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("AST.TV",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("BRAZZERS",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("CANDY",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("CENTOXCENTO",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("DORCEL",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("EROXX",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("PASSION",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("PENTHOUSE",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("PINK-O",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("PINK O",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("PRIVATE",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("RUSNOCH",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("SCT",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("SEXT6SENSO",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("SHALUN TV",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("VIVID RED",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Porn",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("XY Plus",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("XY Mix",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("XY Mad",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("XXL",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Desire",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Bizarre",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Sexy HOT",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Reality Kings",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Prive TV",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Hustler TV",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Extasy",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Evil Angel",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Erox",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("DUSK",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Brazzers",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Brasileirinhas",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Pink Erotic",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Passion",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Passie",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Meiden Van Holland Hard",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Sext & Senso",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Super One",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Vivid TV",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Hustler HD",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("SCT",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Sex Ation",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Hot TV",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Hot HD",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("MILF",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("ANAL",channel_name,re.IGNORECASE) and not re.search("CANAL",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("PUSSY",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("ROCCO",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("BABES",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("BABIE",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("XY Max",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("TUSHY",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("BLACKED",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("FAKE TAXI",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("XXX",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("18",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Porno",channel_name,re.IGNORECASE):
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
                    if uhdtv == 'false' and re.search("4K",channel_name):
                        pass
                    elif fhdtv == 'false' and re.search("FHD",channel_name):
                        pass
                    elif hdtv == 'false' and re.search("HD",channel_name) and not re.search("FHD",channel_name):
                        pass
                    elif sdtv == 'false' and re.search("SD",channel_name):
                        pass
                    elif sdtv == 'false' and not re.search("SD",channel_name) and not re.search("HD",channel_name) and not re.search("4K",channel_name):
                        pass
                    #Futebol
                    elif int(filtrar) == 1 and re.search("Praia",channel_name,re.IGNORECASE):
                        pass
                    elif int(filtrar) == 1 and not re.search("SPORTV",channel_name,re.IGNORECASE) and not re.search("DAZN",channel_name,re.IGNORECASE) and not re.search("ESPN Brasil",channel_name,re.IGNORECASE) and not re.search("PREMIERE",channel_name,re.IGNORECASE) and not re.search("COPA",channel_name,re.IGNORECASE):
                        pass
                    #Esportes
                    elif int(filtrar) == 2 and re.search("Praia",channel_name,re.IGNORECASE):
                        pass
                    elif int(filtrar) == 2 and not re.search("Band Sports",channel_name,re.IGNORECASE) and not re.search("Combate",channel_name,re.IGNORECASE) and not re.search("Fox Sports",channel_name,re.IGNORECASE) and not re.search("SPORTV",channel_name,re.IGNORECASE) and not re.search("DAZN",channel_name,re.IGNORECASE) and not re.search("ESPN",channel_name,re.IGNORECASE) and not re.search("PREMIERE",channel_name,re.IGNORECASE) and not re.search("COPA",channel_name,re.IGNORECASE):
                        pass
                    #Filmes e Series
                    elif int(filtrar) == 3 and re.search("Sports",channel_name,re.IGNORECASE):
                        pass
                    elif int(filtrar) == 3 and re.search("XY Max",channel_name,re.IGNORECASE):
                        pass
                    elif int(filtrar) == 3 and not re.search("AMC",channel_name,re.IGNORECASE) and not re.search("Canal Brasil",channel_name,re.IGNORECASE) and not re.search("Cinemax",channel_name,re.IGNORECASE) and not re.search("HBO",channel_name,re.IGNORECASE) and not re.search("Max",channel_name,re.IGNORECASE) and not re.search("Megapix",channel_name,re.IGNORECASE) and not re.search("Paramount",channel_name,re.IGNORECASE) and not re.search("SPACE",channel_name,re.IGNORECASE) and not re.search("TCM",channel_name,re.IGNORECASE) and not re.search("Telecine Action",channel_name,re.IGNORECASE) and not re.search("TC Action",channel_name,re.IGNORECASE) and not re.search("Telecine Cult",channel_name,re.IGNORECASE) and not re.search("TC Cult",channel_name,re.IGNORECASE) and not re.search("TC Cult",channel_name,re.IGNORECASE) and not re.search("Telecine Fun",channel_name,re.IGNORECASE) and not re.search("TC Fun",channel_name,re.IGNORECASE) and not re.search("Telecine Pipoca",channel_name,re.IGNORECASE) and not re.search("TC Pipoca",channel_name,re.IGNORECASE) and not re.search("Telecine Premium",channel_name,re.IGNORECASE) and not re.search("TC Premium",channel_name,re.IGNORECASE) and not re.search("Telecine Touch",channel_name,re.IGNORECASE) and not re.search("TC Touch",channel_name,re.IGNORECASE) and not re.search("TNT",channel_name,re.IGNORECASE) and not re.search("A&E",channel_name,re.IGNORECASE) and not re.search("AXN",channel_name,re.IGNORECASE) and not re.search("AXN",channel_name,re.IGNORECASE) and not re.search("FOX",channel_name,re.IGNORECASE) and not re.search("FX",channel_name,re.IGNORECASE) and not re.search("SONY",channel_name,re.IGNORECASE) and not re.search("Studio Universal",channel_name,re.IGNORECASE) and not re.search("SyFy",channel_name,re.IGNORECASE) and not re.search("Universal Channel",channel_name,re.IGNORECASE) and not re.search("Universal TV",channel_name,re.IGNORECASE) and not re.search("Warner",channel_name,re.IGNORECASE):
                        pass
                    #Infantil
                    elif int(filtrar) == 4 and re.search("FM",channel_name,re.IGNORECASE):
                        pass
                    elif int(filtrar) == 4 and not re.search("Baby TV",channel_name,re.IGNORECASE) and not re.search("BOOMERANG",channel_name,re.IGNORECASE) and not re.search("CARTOON NETWORK",channel_name,re.IGNORECASE) and not re.search("DISCOVERY KIDS",channel_name,re.IGNORECASE) and not re.search("DISNEY",channel_name,re.IGNORECASE) and not re.search("GLOOB",channel_name,re.IGNORECASE) and not re.search("NAT GEO KIDS",channel_name,re.IGNORECASE) and not re.search("NICKELODEON",channel_name,re.IGNORECASE) and not re.search("NICK JR",channel_name,re.IGNORECASE) and not re.search("PLAYKIDS",channel_name,re.IGNORECASE) and not re.search("TOONCAST",channel_name,re.IGNORECASE) and not re.search("ZOOMOO",channel_name,re.IGNORECASE):
                        pass
                    #Documentario
                    elif int(filtrar) == 5  and re.search("Kids",channel_name,re.IGNORECASE):
                        pass
                    elif int(filtrar) == 5 and not re.search("Discovery",channel_name,re.IGNORECASE) and not re.search("H2 HD",channel_name,re.IGNORECASE) and not re.search("H2 SD",channel_name,re.IGNORECASE) and not re.search("H2 FHD",channel_name,re.IGNORECASE) and not re.search("History",channel_name,re.IGNORECASE) and not re.search("Nat Geo Wild",channel_name,re.IGNORECASE) and not re.search("National Geographic",channel_name,re.IGNORECASE):
                        pass
                    #Abertos
                    elif int(filtrar) == 6 and re.search("Brasileirinhas",channel_name,re.IGNORECASE):
                        pass
                    elif int(filtrar) == 6 and re.search("News",channel_name,re.IGNORECASE) or int(filtrar) == 6 and re.search("Sat",channel_name,re.IGNORECASE) or int(filtrar) == 6 and re.search("FM",channel_name,re.IGNORECASE):
                        pass
                    elif int(filtrar) == 6 and not re.search("Globo",channel_name,re.IGNORECASE) and not re.search("RECORD",channel_name,re.IGNORECASE) and not re.search("RedeTV",channel_name,re.IGNORECASE) and not re.search("Rede Vida",channel_name,re.IGNORECASE) and not re.search("SBT",channel_name,re.IGNORECASE) and not re.search("TV Brasil",channel_name,re.IGNORECASE) and not re.search("TV Cultura",channel_name,re.IGNORECASE) and not re.search("TV Diario",channel_name,re.IGNORECASE) and not re.search("BAND",channel_name,re.IGNORECASE):
                        pass
                    #Reality show
                    elif int(filtrar) == 7 and not re.search("BBB",channel_name,re.IGNORECASE) and not re.search("Big Brother Brasil",channel_name,re.IGNORECASE) and not re.search("A Fazenda",channel_name,re.IGNORECASE):
                        pass
                    #Noticias
                    elif int(filtrar) == 8 and re.search("FM",channel_name,re.IGNORECASE):
                        pass
                    elif int(filtrar) == 8 and not re.search("CNN",channel_name,re.IGNORECASE) and not re.search("NEWS",channel_name,re.IGNORECASE):
                        pass
                    elif adult2 == 'false' and re.search("Adult",cat,re.IGNORECASE) or adult2 == 'false' and re.search("ADULT",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Blue Hustler",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("PlayBoy",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Redlight",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Sextreme",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("SexyHot",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Venus",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("AST TV",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("ASTTV",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("AST.TV",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("BRAZZERS",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("CANDY",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("CENTOXCENTO",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("DORCEL",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("EROXX",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("PASSION",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("PENTHOUSE",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("PINK-O",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("PINK O",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("PRIVATE",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("RUSNOCH",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("SCT",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("SEXT6SENSO",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("SHALUN TV",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("VIVID RED",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Porn",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("XY Plus",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("XY Mix",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("XY Mad",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("XXL",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Desire",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Bizarre",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Sexy HOT",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Reality Kings",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Prive TV",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Hustler TV",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Extasy",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Evil Angel",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Erox",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("DUSK",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Brazzers",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Brasileirinhas",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Pink Erotic",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Passion",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Passie",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Meiden Van Holland Hard",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Sext & Senso",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Super One",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Vivid TV",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Hustler HD",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("SCT",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Sex Ation",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Hot TV",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Hot HD",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("MILF",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("ANAL",channel_name,re.IGNORECASE) and not re.search("CANAL",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("PUSSY",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("ROCCO",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("BABES",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("BABIE",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("XY Max",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("TUSHY",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("BLACKED",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("FAKE TAXI",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("XXX",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("18",channel_name,re.IGNORECASE) or adult2 == 'false' and re.search("Porno",channel_name,re.IGNORECASE):
                        pass
                    elif cleaname > '' and re.search("Adult",cat,re.IGNORECASE) or cleaname > '' and re.search("ADULT",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Blue Hustler",channel_name,re.IGNORECASE) or cleaname > '' and re.search("PlayBoy",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Redlight",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Sextreme",channel_name,re.IGNORECASE) or cleaname > '' and re.search("SexyHot",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Venus",channel_name,re.IGNORECASE) or cleaname > '' and re.search("AST TV",channel_name,re.IGNORECASE) or cleaname > '' and re.search("ASTTV",channel_name,re.IGNORECASE) or cleaname > '' and re.search("AST.TV",channel_name,re.IGNORECASE) or cleaname > '' and re.search("BRAZZERS",channel_name,re.IGNORECASE) or cleaname > '' and re.search("CANDY",channel_name,re.IGNORECASE) or cleaname > '' and re.search("CENTOXCENTO",channel_name,re.IGNORECASE) or cleaname > '' and re.search("DORCEL",channel_name,re.IGNORECASE) or cleaname > '' and re.search("EROXX",channel_name,re.IGNORECASE) or cleaname > '' and re.search("PASSION",channel_name,re.IGNORECASE) or cleaname > '' and re.search("PENTHOUSE",channel_name,re.IGNORECASE) or cleaname > '' and re.search("PINK-O",channel_name,re.IGNORECASE) or cleaname > '' and re.search("PINK O",channel_name,re.IGNORECASE) or cleaname > '' and re.search("PRIVATE",channel_name,re.IGNORECASE) or cleaname > '' and re.search("RUSNOCH",channel_name,re.IGNORECASE) or cleaname > '' and re.search("SCT",channel_name,re.IGNORECASE) or cleaname > '' and re.search("SEXT6SENSO",channel_name,re.IGNORECASE) or cleaname > '' and re.search("SHALUN TV",channel_name,re.IGNORECASE) or cleaname > '' and re.search("VIVID RED",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Porn",channel_name,re.IGNORECASE) or cleaname > '' and re.search("XY Plus",channel_name,re.IGNORECASE) or cleaname > '' and re.search("XY Mix",channel_name,re.IGNORECASE) or cleaname > '' and re.search("XY Mad",channel_name,re.IGNORECASE) or cleaname > '' and re.search("XXL",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Desire",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Bizarre",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Sexy HOT",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Reality Kings",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Prive TV",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Hustler TV",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Extasy",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Evil Angel",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Erox",channel_name,re.IGNORECASE) or cleaname > '' and re.search("DUSK",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Brazzers",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Brasileirinhas",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Pink Erotic",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Passion",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Passie",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Meiden Van Holland Hard",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Sext & Senso",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Super One",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Vivid TV",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Hustler HD",channel_name,re.IGNORECASE) or cleaname > '' and re.search("SCT",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Sex Ation",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Hot TV",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Hot HD",channel_name,re.IGNORECASE) or cleaname > '' and re.search("MILF",channel_name,re.IGNORECASE) or cleaname > '' and re.search("ANAL",channel_name,re.IGNORECASE) and not re.search("CANAL",channel_name,re.IGNORECASE) or cleaname > '' and re.search("PUSSY",channel_name,re.IGNORECASE) or cleaname > '' and re.search("ROCCO",channel_name,re.IGNORECASE) or cleaname > '' and re.search("BABES",channel_name,re.IGNORECASE) or cleaname > '' and re.search("BABIE",channel_name,re.IGNORECASE) or cleaname > '' and re.search("XY Max",channel_name,re.IGNORECASE) or cleaname > '' and re.search("TUSHY",channel_name,re.IGNORECASE) or cleaname > '' and re.search("FAKE TAXI",channel_name,re.IGNORECASE) or cleaname > '' and re.search("BLACKED",channel_name,re.IGNORECASE) or cleaname > '' and re.search("XXX",channel_name,re.IGNORECASE) or cleaname > '' and re.search("18",channel_name,re.IGNORECASE) or cleaname > '' and re.search("Porno",channel_name,re.IGNORECASE):
                        addDir2(name1.encode('utf-8', 'ignore'),stream_url.encode('utf-8'),10,'',channel_name,thumbnail,'',desc1.encode('utf-8'),False)
                    elif re.search("Adult",cat,re.IGNORECASE) or re.search("ADULT",channel_name,re.IGNORECASE) or re.search("Blue Hustler",channel_name,re.IGNORECASE) or re.search("PlayBoy",channel_name,re.IGNORECASE) or re.search("Redlight",channel_name,re.IGNORECASE) or re.search("Sextreme",channel_name,re.IGNORECASE) or re.search("SexyHot",channel_name,re.IGNORECASE) or re.search("Venus",channel_name,re.IGNORECASE) or re.search("AST TV",channel_name,re.IGNORECASE) or re.search("ASTTV",channel_name,re.IGNORECASE) or re.search("AST.TV",channel_name,re.IGNORECASE) or re.search("BRAZZERS",channel_name,re.IGNORECASE) or re.search("CANDY",channel_name,re.IGNORECASE) or re.search("CENTOXCENTO",channel_name,re.IGNORECASE) or re.search("DORCEL",channel_name,re.IGNORECASE) or re.search("EROXX",channel_name,re.IGNORECASE) or re.search("PASSION",channel_name,re.IGNORECASE) or re.search("PENTHOUSE",channel_name,re.IGNORECASE) or re.search("PINK-O",channel_name,re.IGNORECASE) or re.search("PINK O",channel_name,re.IGNORECASE) or re.search("PRIVATE",channel_name,re.IGNORECASE) or re.search("RUSNOCH",channel_name,re.IGNORECASE) or re.search("SCT",channel_name,re.IGNORECASE) or re.search("SEXT6SENSO",channel_name,re.IGNORECASE) or re.search("SHALUN TV",channel_name,re.IGNORECASE) or re.search("VIVID RED",channel_name,re.IGNORECASE) or re.search("Porn",channel_name,re.IGNORECASE) or re.search("XY Plus",channel_name,re.IGNORECASE) or re.search("XY Mix",channel_name,re.IGNORECASE) or re.search("XY Mad",channel_name,re.IGNORECASE) or re.search("XXL",channel_name,re.IGNORECASE) or re.search("Desire",channel_name,re.IGNORECASE) or re.search("Bizarre",channel_name,re.IGNORECASE) or re.search("Sexy HOT",channel_name,re.IGNORECASE) or re.search("Reality Kings",channel_name,re.IGNORECASE) or re.search("Prive TV",channel_name,re.IGNORECASE) or re.search("Hustler TV",channel_name,re.IGNORECASE) or re.search("Extasy",channel_name,re.IGNORECASE) or re.search("Evil Angel",channel_name,re.IGNORECASE) or re.search("Erox",channel_name,re.IGNORECASE) or re.search("DUSK",channel_name,re.IGNORECASE) or re.search("Brazzers",channel_name,re.IGNORECASE) or re.search("Brasileirinhas",channel_name,re.IGNORECASE) or re.search("Pink Erotic",channel_name,re.IGNORECASE) or re.search("Passion",channel_name,re.IGNORECASE) or re.search("Passie",channel_name,re.IGNORECASE) or re.search("Meiden Van Holland Hard",channel_name,re.IGNORECASE) or re.search("Sext & Senso",channel_name,re.IGNORECASE) or re.search("Super One",channel_name,re.IGNORECASE) or re.search("Vivid TV",channel_name,re.IGNORECASE) or re.search("Hustler HD",channel_name,re.IGNORECASE) or re.search("SCT",channel_name,re.IGNORECASE) or re.search("Sex Ation",channel_name,re.IGNORECASE) or re.search("Hot TV",channel_name,re.IGNORECASE) or re.search("Hot HD",channel_name,re.IGNORECASE) or re.search("MILF",channel_name,re.IGNORECASE) or re.search("ANAL",channel_name,re.IGNORECASE) and not re.search("CANAL",channel_name,re.IGNORECASE) or re.search("PUSSY",channel_name,re.IGNORECASE) or re.search("ROCCO",channel_name,re.IGNORECASE) or re.search("BABES",channel_name,re.IGNORECASE) or re.search("BABIE",channel_name,re.IGNORECASE) or re.search("XY Max",channel_name,re.IGNORECASE) or re.search("TUSHY",channel_name,re.IGNORECASE) or re.search("FAKE TAXI",channel_name,re.IGNORECASE) or re.search("BLACKED",channel_name,re.IGNORECASE) or re.search("XXX",channel_name,re.IGNORECASE) or re.search("18",channel_name,re.IGNORECASE) or re.search("Porno",channel_name,re.IGNORECASE):
                        addDir2(name1.encode('utf-8', 'ignore'),stream_url.encode('utf-8'),10,'',cleaname,thumbnail,'',desc1.encode('utf-8'),False)
                    else:
                        #addLink(name1.encode('utf-8', 'ignore'),resolver_final.encode('utf-8'),'',cleaname,thumbnail,'',desc1)
                        addDir2(name1.encode('utf-8', 'ignore'),resolver_final.encode('utf-8'),18,'',cleaname,thumbnail,'',desc1.encode('utf-8'),False)
                except:
                    #notify('[COLOR red]Erro ao Carregar os dados![/COLOR]')
                    pass
        else:
            #getItems(soup('item'),fanart)
            if pesquisa:
                getItems(soup('item'),fanart, True)
            else:
                getItems(soup('item'),fanart)
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
                #raise
                fanArt = ''
        except:
            fanArt = fanart
        for channel in channel_list('subchannel'):
            name = channel('name')[0].string
            try:
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    #raise
                    thumbnail = ''
            except:
                thumbnail = ''
            try:
                if not channel('fanart'):
                    if __addon__.getSetting('use_thumb') == "true":
                        fanArt = thumbnail
                else:
                    fanArt = channel('fanart')[0].string
                if fanArt == None:
                    #raise
                    fanArt = ''
            except:
                pass
            try:
                desc = channel('info')[0].string
                if desc == None:
                    #raise
                    desc = ''
            except:
                desc = ''

            try:
                #addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),3,thumbnail,fanArt,desc,genre,credits,date)
                addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),3,thumbnail,fanArt,desc)
            except:
                notify('[COLOR red]Erro ao Carregar os dados![/COLOR]')
        #getItems(items)
        getItems(items,fanArt)



def getItems(items, fanart, pesquisa=False):
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
                #raise
                thumbnail = ''
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
                #raise
                fanArt = ''
        except:
            fanArt = fanart

        try:
            desc = item('info')[0].string
            if desc == None:
                #raise
                desc = ''
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
                        info = item('info')[0].string
                        if info == None:
                            desc = ''
                        elif info == '':
                            desc = ''
                        else:
                            desc = info
                else:
                    cleaname = ''
                    info = item('info')[0].string
                    if info == None:
                        desc = ''
                    elif info == '':
                        desc = ''
                    else:
                        desc = info
            else:
                cleaname = ''
                info = item('info')[0].string
                if info == None:
                    desc = ''
                elif info == '':
                    desc = ''
                else:
                    desc = info
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
            if item('utubelive') and len(item('utubelive')) >0:
                utubelive = item('utubelive')[0].string
            else:
                utubelive = ''
        except:
            utubelive = ''


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
            if name > '' and url == '' and not utube > '' and not utubelive > '':
                addLink(name.encode('utf-8', 'ignore'), 'None', '', '', thumbnail, fanArt, desc)
            elif name > '' and url == None and not utube > '' and not utubelive > '':
                addLink(name.encode('utf-8', 'ignore'), 'None', '', '', thumbnail, fanArt, desc)
            elif category == 'Adult' and url.find('redecanais') >= 0 and url.find('m3u8') >= 0:
                addDir2(name.encode('utf-8', 'ignore'),url.encode('utf-8'),10,subtitle,cleaname,thumbnail,fanArt,desc.encode('utf-8'),False)
            elif url.find('redecanais') >= 0 and url.find('m3u8') >= 0:
                addDir2(name.encode('utf-8', 'ignore'),url.encode('utf-8'),16,subtitle,cleaname,thumbnail,fanArt,desc.encode('utf-8'),False)
            elif url.find('topcanais') >= 0 and url.find('m3u8') >= 0:
                addDir2(name.encode('utf-8', 'ignore'),url.encode('utf-8'),16,subtitle,cleaname,thumbnail,fanArt,desc.encode('utf-8'),False)
            elif url.find('redecanais_vod') >= 0:
                addDir2(name.encode('utf-8', 'ignore'),url.encode('utf-8'),16,subtitle,cleaname,thumbnail,fanArt,desc.encode('utf-8'),False)
            elif resolver(url, name, thumbnail).startswith('plugin://plugin.video.youtube/playlist') == True or resolver(url, name, thumbnail).startswith('plugin://plugin.video.youtube/channel') == True or resolver(url, name, thumbnail).startswith('plugin://plugin.video.youtube/user') == True or resolver(url, name, thumbnail).startswith('Plugin://plugin.video.youtube/playlist') == True:
                addDir(name.encode('utf-8', 'ignore'),resolver(url, name, thumbnail).encode('utf-8'),6,thumbnail,fanArt,desc)
            elif utube > '' and len(utube) == 11:
                link_youtube = 'plugin://plugin.video.youtube/play/?video_id='+utube
                addLink(name.encode('utf-8', 'ignore'), link_youtube.encode('utf-8'), subtitle, cleaname, thumbnail, fanArt, desc)
            elif utubelive > '' and len(utubelive) == 11:
                link_live = 'https://www.youtube.com/watch?v='+utubelive
                addDir2(name.encode('utf-8', 'ignore'),link_live.encode('utf-8'),17,subtitle,cleaname,thumbnail,fanArt,desc.encode('utf-8'),False)
            elif len(item('externallink')) >0:
                addDir(name.encode('utf-8', 'ignore'),resolver(url, name, thumbnail).encode('utf-8'),1,thumbnail,fanArt,desc)
            ##Pesquisa e multilink
            elif pesquisa and len(url2) >1 and cleaname == '' and len(subtitle2) >1 and re.search(playlist_command,url,re.IGNORECASE):
                addDir2(name.encode('utf-8', 'ignore')+'[COLOR aquamarine] ('+str(len(url2))+' itens)[/COLOR]'.encode('utf-8', 'ignore'),str(url2).replace(',','||').replace('$'+playlist_command+'','#'+playlist_command+''),11,str(subtitle2).replace(',','||'),cleaname,thumbnail,fanArt,desc.encode('utf-8'),False,True)
            elif pesquisa and len(url2) >1 and cleaname == '' and re.search(playlist_command,url,re.IGNORECASE):
                addDir2(name.encode('utf-8', 'ignore')+'[COLOR aquamarine] ('+str(len(url2))+' itens)[/COLOR]'.encode('utf-8', 'ignore'),str(url2).replace(',','||').replace('$'+playlist_command+'','#'+playlist_command+''),11,subtitle,cleaname,thumbnail,fanArt,desc.encode('utf-8'),False,True)
            ##Multilink
            elif len(url2) >1 and cleaname == '' and len(subtitle2) >1 and re.search(playlist_command,url,re.IGNORECASE):
                addDir2(name.encode('utf-8', 'ignore')+'[COLOR aquamarine] ('+str(len(url2))+' itens)[/COLOR]'.encode('utf-8', 'ignore'),str(url2).replace(',','||').replace('$'+playlist_command+'','#'+playlist_command+''),11,str(subtitle2).replace(',','||'),cleaname,thumbnail,fanArt,desc.encode('utf-8'),False)
            elif len(url2) >1 and cleaname == '' and re.search(playlist_command,url,re.IGNORECASE):
                addDir2(name.encode('utf-8', 'ignore')+'[COLOR aquamarine] ('+str(len(url2))+' itens)[/COLOR]'.encode('utf-8', 'ignore'),str(url2).replace(',','||').replace('$'+playlist_command+'','#'+playlist_command+''),11,subtitle,cleaname,thumbnail,fanArt,desc.encode('utf-8'),False)
            elif category == 'Adult':
                addDir2(name.encode('utf-8', 'ignore'),url.encode('utf-8'),10,subtitle,cleaname,thumbnail,fanArt,desc.encode('utf-8'),False)
            elif pesquisa:
                addDir2(name.encode('utf-8', 'ignore'),url.encode('utf-8'),16,subtitle,cleaname,thumbnail,fanArt,desc.encode('utf-8'),False,True)
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
        arquivo = os.path.join(Path, "xmltv.xml")
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
        notify('[COLOR red]Erro ao atualizar EPG![/COLOR][CR]Limpe o EPG e tente novamente.')



def downloadEPG():
    try:
        import downloader_epg
        Path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode("utf-8")
        arquivo = os.path.join(Path, "xmltv.xml")
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
        notify('[COLOR red]Erro ao atualizar EPG![/COLOR][CR]Limpe o EPG e tente novamente.')



def epgParseData():
    try:
        Path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode("utf-8")
        arquivo = os.path.join(Path, "xmltv.xml").decode("utf8")
        xml = ET.parse(arquivo)
        return xml.getroot()
    except:
        notify('[COLOR red]Erro ao carregar EPG![/COLOR][CR]Limpe o EPG e tente novamente..')
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
    elif re.search("Disney",channel,re.IGNORECASE):
        channel_id = 'Disneychannel.br'
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
    elif re.search("Fox",channel,re.IGNORECASE) and not re.search("Fox Life",channel,re.IGNORECASE) and not re.search("FOX Premium 1",channel,re.IGNORECASE) and not re.search("FOX Premium 2",channel,re.IGNORECASE) and not re.search("Fox Sports",channel,re.IGNORECASE) and not re.search("Fox Sports 2",channel,re.IGNORECASE) and not re.search("Fox 25",channel,re.IGNORECASE) and not re.search("News",channel,re.IGNORECASE):
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
    elif re.search("FX",channel,re.IGNORECASE) and not re.search("US",channel,re.IGNORECASE):
        channel_id = 'Fx.br'
    elif re.search("Film & Arts",channel,re.IGNORECASE):
        channel_id = 'FilmArts.br'
    elif re.search("Globo Brasilia",channel,re.IGNORECASE) or re.search("Globo Brasília",channel,re.IGNORECASE):
        channel_id = 'GloboBrasilia.br'
    elif re.search("Globo Campinas",channel,re.IGNORECASE) or re.search("Globo EPTV Campinas",channel,re.IGNORECASE):
        channel_id = 'GloboEPTVCampinas.br'
    elif re.search("Globo Minas",channel,re.IGNORECASE):
        channel_id = 'Globominas.br'
    elif re.search("Globo News",channel,re.IGNORECASE):
        channel_id = 'Globonews.br'
    elif re.search("Globo RBS TV Poa",channel,re.IGNORECASE) or re.search("RBS TV",channel,re.IGNORECASE) or re.search("RBS Porto Alegre",channel,re.IGNORECASE):
        channel_id = 'GloboPortoAlegre.br'
    elif re.search("Globo RJ",channel,re.IGNORECASE):
        channel_id = 'Globorj.br'
    elif re.search("Globo SP",channel,re.IGNORECASE):
        channel_id = 'Globosp.br'
    elif re.search("Globo TV Anhanguera",channel,re.IGNORECASE):
        channel_id = 'GloboAnhangueraGoias.br'
    elif re.search("Globo TV Bahia",channel,re.IGNORECASE):
        channel_id = 'Tvbahia.br'
    elif re.search("Globo TV Tem Bauru",channel,re.IGNORECASE) or re.search("TV Tem Bauru",channel,re.IGNORECASE) or re.search("TVTem Bauru",channel,re.IGNORECASE):
        channel_id = 'Tvtembauru.br'
    elif re.search("Globo TV Tribuna",channel,re.IGNORECASE) or re.search("TV Tribuna",channel,re.IGNORECASE):
        channel_id = 'Tvtribuna.br'
    elif re.search("Globo TV Vanguarda",channel,re.IGNORECASE) or re.search("TV Vanguarda",channel,re.IGNORECASE):
        channel_id = 'Vangsaojchd.br'
    elif re.search("Globo Inter TV Alto Litoral",channel,re.IGNORECASE):
        channel_id = 'Inttvaltolit.br'
    elif re.search("Globo Inter TV Grande Minas",channel,re.IGNORECASE) or re.search("Globo Inter TV Minas",channel,re.IGNORECASE):
        channel_id = 'Intertvgminas.br'
    elif re.search("Globo NSC Florianopolis",channel,re.IGNORECASE):
        channel_id = 'NSCTV.br'
    elif re.search("Globo Nordeste",channel,re.IGNORECASE):
        channel_id = 'Globorecife.br'
    elif re.search("Globo Nordeste",channel,re.IGNORECASE):
        channel_id = 'Globorecife.br'
    elif re.search("Globo RPC Parana",channel,re.IGNORECASE) or re.search("Globo RPC Curitiba",channel,re.IGNORECASE):
        channel_id = 'Rpccuritiba.br'
    elif re.search("Gloob",channel,re.IGNORECASE):
        channel_id = 'Gloob.br'
    elif re.search("GNT",channel,re.IGNORECASE):
        channel_id = 'Gnt.br'
    elif re.search("HBO",channel,re.IGNORECASE) and not re.search("HBO 2",channel,re.IGNORECASE) and not re.search("HBO 2",channel,re.IGNORECASE) and not re.search("HBO Family",channel,re.IGNORECASE) and not re.search("HBO Plus",channel,re.IGNORECASE) and not re.search("HBO Signature",channel,re.IGNORECASE) and not re.search("HBO Mundi",channel,re.IGNORECASE) and not re.search("HBO Extreme",channel,re.IGNORECASE) and not re.search("HBO Pop",channel,re.IGNORECASE):
        channel_id = 'Hbo.br'
    elif re.search("HBO 2",channel,re.IGNORECASE):
        channel_id = 'Hbo2.br'
    elif re.search("HBO Family",channel,re.IGNORECASE):
        channel_id = 'Hbofamily.br'
    elif re.search("HBO Plus",channel,re.IGNORECASE):
        channel_id = 'Hboplus.br'
    elif re.search("HBO Signature",channel,re.IGNORECASE):
        channel_id = 'Hbosignature.br'
    elif re.search("HBO Mundi",channel,re.IGNORECASE):
        channel_id = 'Max.br'
    elif re.search("HBO Extreme",channel,re.IGNORECASE):
        channel_id = 'Maxprime.br'
    elif re.search("HBO Pop",channel,re.IGNORECASE):
        channel_id = 'Maxup.br'
    elif re.search("History Channel",channel,re.IGNORECASE):
        channel_id = 'Historychannel.br'
    elif re.search("Ideal TV",channel,re.IGNORECASE):
        channel_id = 'Idealtv.br'
    elif re.search("Investigação Discovery",channel,re.IGNORECASE) or re.search("Investigacao Discovery",channel,re.IGNORECASE):
        channel_id = 'Investigacaodiscoveryid.br'
    elif re.search("i.Sat",channel,re.IGNORECASE):
        channel_id = 'iSat.br'
    elif re.search("i.Sat",channel,re.IGNORECASE):
        channel_id = 'Lifetime.br'
    elif re.search("Lifetime",channel,re.IGNORECASE):
        channel_id = 'Lifetime.br'
    elif re.search("Mais GloboSat",channel,re.IGNORECASE):
        channel_id = '+globosat.br'
    elif re.search("Max",channel,re.IGNORECASE) and not re.search("Max Prime",channel,re.IGNORECASE) and not re.search("Max UP",channel,re.IGNORECASE):
        channel_id = 'Max.br'
    elif re.search("Max Prime",channel,re.IGNORECASE):
        channel_id = 'Maxprime.br'
    elif re.search("Max UP",channel,re.IGNORECASE):
        channel_id = 'Maxup.br'
    elif re.search("Megapix",channel,re.IGNORECASE):
        channel_id = 'Megapix.br'
    elif re.search("MTV",channel,re.IGNORECASE) and not re.search("US",channel,re.IGNORECASE):
        channel_id = 'Mtv.br'
    elif re.search("Multishow",channel,re.IGNORECASE):
        channel_id = 'Multishow.br'
    elif re.search("Nat Geo Kids",channel,re.IGNORECASE) and not re.search("Nat Geo Wild",channel,re.IGNORECASE) and not re.search("National Geographic",channel,re.IGNORECASE):
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
    elif re.search("Off",channel,re.IGNORECASE) and not re.search("CNN",channel,re.IGNORECASE):
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
        channel_id = 'Rederecord.br'
    elif re.search("Rede Brasil",channel,re.IGNORECASE):
        channel_id = 'Redebrasil.br'
    elif re.search("Rede TV",channel,re.IGNORECASE) or re.search("RedeTV",channel,re.IGNORECASE):
        channel_id = 'Redetv.br'
    elif re.search("Rede Vida",channel,re.IGNORECASE):
        channel_id = 'Redevida.br'
    elif re.search("Rede Amazonica",channel,re.IGNORECASE) or re.search("Rede Amazonas",channel,re.IGNORECASE):
        channel_id = 'Redeamazonica.br'
    elif re.search("RIT",channel,re.IGNORECASE):
        channel_id = 'Rit.br'
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
    elif re.search("Tv Diario Fortaleza",channel,re.IGNORECASE):
        channel_id = 'Tvdiario.br'
    elif re.search("Tv Escola",channel,re.IGNORECASE):
        channel_id = 'Tvescola.br'
    elif re.search("TV Gazeta Alagoas",channel,re.IGNORECASE):
        channel_id = 'TVGazetaal.br'
    elif re.search("TV Gazeta",channel,re.IGNORECASE) and not re.search("TV Gazeta Sul",channel,re.IGNORECASE) and not re.search("TV Gazeta Vitoria",channel,re.IGNORECASE):
        channel_id = 'TVGazeta.br'
    elif re.search("Tv Justica",channel,re.IGNORECASE):
        channel_id = 'Tvjustica.br'
    elif re.search("TV Liberal Belem",channel,re.IGNORECASE):
        channel_id = 'Tvliberalbelem.br'
    elif re.search("Tv Senado",channel,re.IGNORECASE):
        channel_id = 'Tvsenado.br'
    elif re.search("Tv Verdes Mares",channel,re.IGNORECASE):
        channel_id = 'Verdesmares.br'
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
    elif re.search("CNN Brasil",channel,re.IGNORECASE) and not re.search("CNN INTERNACIONAL",channel,re.IGNORECASE):
        channel_id = 'Cnnbrasil.br'
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
                encerramento = '\n\n[COLOR orange][B]TERMINA ÀS:[/B][/COLOR] ' + stop[8:-4] + ':' + stop[10:-2]
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
        xbmc.sleep(10)
        p_file = open(arquivo,'r+')
        p_file_read = p_file.read()
        p_file_b64_decode = base64.b64decode(p_file_read).decode('utf-8')
        dialog = xbmcgui.Dialog()
        if int(keyboard) == 0:
            ps = dialog.numeric(0, 'Insira a senha atual:')
        else:
            ps = dialog.input('Insira a senha atual:', option=xbmcgui.ALPHANUM_HIDE_INPUT)
        if ps == p_file_b64_decode:
            resolver1 = url_server_vip.replace('http://', '').replace('https://', '').replace('/get.php', '')
            if url.find(resolver1) >= 0:
                if cleaname > '':
                    urlresolver = resolver_vip(url, cleaname, iconimage)
                else:
                    urlresolver = resolver_vip(url, name, iconimage)
            else:
                if cleaname > '':
                    urlresolver = resolver(url, cleaname, iconimage)
                else:
                    urlresolver = resolver(url, name, iconimage)
            if urlresolver.startswith("plugin://plugin.video.f4mTester"):
                xbmc.executebuiltin('RunPlugin(' + urlresolver + ')')
            elif urlresolver.startswith('plugin://plugin.video.youtube/playlist') == True or urlresolver.startswith('plugin://plugin.video.youtube/channel') == True or urlresolver.startswith('plugin://plugin.video.youtube/user') == True or urlresolver.startswith('Plugin://plugin.video.youtube/playlist') == True:
                xbmc.executebuiltin("ActivateWindow(10025," + urlresolver + ",return)")
            else:
                li = xbmcgui.ListItem(name, path=urlresolver, iconImage=iconimage, thumbnailImage=iconimage)
                if cleaname > '':
                    li.setInfo(type='video', infoLabels={'Title': cleaname, 'plot': description })
                else:
                    li.setInfo(type='video', infoLabels={'Title': name, 'plot': description })
                if subtitle > '':
                    li.setSubtitles([subtitle])
                xbmc.Player().play(item=urlresolver, listitem=li)
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
            resolver1 = url_server_vip.replace('http://', '').replace('https://', '').replace('/get.php', '')
            if url.find(resolver1) >= 0:
                if cleaname > '':
                    urlresolver = resolver_vip(url, cleaname, iconimage)
                else:
                    urlresolver = resolver_vip(url, name, iconimage)
            else:
                if cleaname > '':
                    urlresolver = resolver(url, cleaname, iconimage)
                else:
                    urlresolver = resolver(url, name, iconimage)
            if urlresolver.startswith("plugin://plugin.video.f4mTester"):
                xbmc.executebuiltin('RunPlugin(' + urlresolver + ')')
            elif urlresolver.startswith('plugin://plugin.video.youtube/playlist') == True or urlresolver.startswith('plugin://plugin.video.youtube/channel') == True or urlresolver.startswith('plugin://plugin.video.youtube/user') == True or urlresolver.startswith('Plugin://plugin.video.youtube/playlist') == True:
                xbmc.executebuiltin("ActivateWindow(10025," + urlresolver + ",return)")
            else:
                li = xbmcgui.ListItem(name, path=urlresolver, iconImage=iconimage, thumbnailImage=iconimage)
                if cleaname > '':
                    li.setInfo(type='video', infoLabels={'Title': cleaname, 'plot': description })
                else:
                    li.setInfo(type='video', infoLabels={'Title': name, 'plot': description })
                if subtitle > '':
                    li.setSubtitles([subtitle])
                xbmc.Player().play(item=urlresolver, listitem=li)
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



def individual_player(name, url, cleaname, iconimage, description, subtitle):
    if cleaname > '':
        urlresolver = resolver(url, cleaname, iconimage)
    else:
        urlresolver = resolver(url, name, iconimage)
    if urlresolver.startswith("plugin://plugin.video.f4mTester"):
        xbmc.executebuiltin('RunPlugin(' + urlresolver + ')')
    else:
        li = xbmcgui.ListItem(name, path=urlresolver, iconImage=iconimage, thumbnailImage=iconimage)
        if cleaname > '':
            li.setInfo(type='video', infoLabels={'Title': cleaname, 'plot': description })
        else:
            li.setInfo(type='video', infoLabels={'Title': name, 'plot': description })
        if subtitle > '':
            li.setSubtitles([subtitle])
        xbmc.Player().play(item=urlresolver, listitem=li)


def m3u8_player(name, url, cleaname, iconimage, description, subtitle):
    if url.startswith("plugin://plugin.video.f4mTester"):
        xbmc.executebuiltin('RunPlugin(' + url + ')')
    else:
        li = xbmcgui.ListItem(name, path=url, iconImage=iconimage, thumbnailImage=iconimage)
        if cleaname > '':
            li.setInfo(type='video', infoLabels={'Title': cleaname, 'plot': description })
        else:
            li.setInfo(type='video', infoLabels={'Title': name, 'plot': description })
        if subtitle > '':
            li.setSubtitles([subtitle])
        xbmc.Player().play(item=url, listitem=li)



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



def ascii(string):
    if isinstance(string, basestring):
        if isinstance(string, unicode):
           string = string.encode('ascii', 'ignore')
    return string
def uni(string, encoding = 'utf-8'):
    if isinstance(string, basestring):
        if not isinstance(string, unicode):
            string = unicode(string, encoding, 'ignore')
    return string
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def sendJSON(command):
    data = ''
    try:
        data = xbmc.executeJSONRPC(uni(command))
    except UnicodeEncodeError:
        data = xbmc.executeJSONRPC(ascii(command))

    return uni(data)


def pluginquerybyJSON(url):
    json_query = uni('{"jsonrpc":"2.0","method":"Files.GetDirectory","params":{"directory":"%s","media":"video","properties":["thumbnail","title","year","dateadded","fanart","rating","season","episode","studio"]},"id":1}') %url

    json_folder_detail = json.loads(sendJSON(json_query))
    for i in json_folder_detail['result']['files'] :
        url = i['file']
        name = removeNonAscii(i['label'])
        thumbnail = removeNonAscii(i['thumbnail'])
        try:
            fanart = removeNonAscii(i['fanart'])
        except Exception:
            fanart = ''
        try:
            date = i['year']
        except Exception:
            date = ''
        try:
            episode = i['episode']
            season = i['season']
            if episode == -1 or season == -1:
                description = ''
            else:
                description = '[COLOR yellow] S' + str(season)+'[/COLOR][COLOR hotpink] E' + str(episode) +'[/COLOR]'
        except Exception:
            description = ''
        try:
            studio = i['studio']
            if studio:
                description += '\n Studio:[COLOR steelblue] ' + studio[0] + '[/COLOR]'
        except Exception:
            studio = ''

        desc = description+'\n\nDate: '+str(date)

        if i['filetype'] == 'file':
            #addLink(url,name,thumbnail,fanart,description,'',date,'',None,'',total=len(json_folder_detail['result']['files']))
            addLink(name.encode('utf-8', 'ignore'),url.encode('utf-8'),'','',thumbnail,fanart,desc)
            #xbmc.executebuiltin("Container.SetViewMode(500)")

        else:
            #addDir(name,url,53,thumbnail,fanart,description,'',date,'')
            addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),6,iconimage,fanart,desc)
            #xbmc.executebuiltin("Container.SetViewMode(500)")



def youtube_live(url):
    data = getRequest2(url, 'https://www.youtube.com/')
    #print(data)
    match = re.compile('"hlsManifestUrl.+?"(.+?).m3u8', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    if match !=[]:
        stream = match[0].replace(':\\"https:', 'https:').replace('\/', '/').replace('\n', '')+'.m3u8|Referer=https://www.youtube.com/|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        #print(stream)
        return stream
    else:
        stream = ''
        return stream


def youtube_live_player(name, url, cleaname, iconimage, description, subtitle):
        li = xbmcgui.ListItem(name, path=youtube_live(url), iconImage=iconimage, thumbnailImage=iconimage)
        if cleaname > '':
            li.setInfo(type='video', infoLabels={'Title': cleaname, 'plot': description })
        else:
            li.setInfo(type='video', infoLabels={'Title': name, 'plot': description })
        if subtitle > '':
            li.setSubtitles([subtitle])
        xbmc.Player().play(item=youtube_live(url), listitem=li)



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



def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


def getInfoPlaylistYoutube(url):
    try:
        import requests
        sourceCode = requests.get(url).text
    except:
        sourceCode = ''
    soup = BeautifulSoup(sourceCode, 'html.parser')
    #print(soup)
    info_web = str(soup.find(id="eow-description")).replace("<br/>", "\n")
    info = cleanhtml(info_web)
    return info


def youtube_restore(url):
    if url.find('/?video_id=') >= 0:
        find_id = re.compile('/?video_id=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(url)
        normal_url = 'https://www.youtube.com/watch?v='+str(find_id[0])
    elif url.find('youtube/playlist/') >= 0:
        find_id = re.compile('/playlist/(.+?)/', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(url)
        normal_url = 'https://www.youtube.com/playlist?list='+str(find_id[0])
    else:
        normal_url = ''
    return normal_url


def data_youtube(url, ref):
    try:
        try:
            import cookielib
        except ImportError:
            import http.cookiejar as cookielib
        try:
            import urllib2
        except ImportError:
            import urllib.request as urllib2
        if ref > '':
            ref2 = ref
        else:
            ref2 = url
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders=[('Accept-Language', 'en-US,en;q=0.9;q=0.8'),('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'),('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'), ('Referer', ref2)]
        data = opener.open(url).read()
        response = data.decode('utf-8')
        return response
    except:
        #pass
        response = ''
        return response


def getPlaylistLinksYoutube(url):
    try:
        sourceCode = data_youtube(youtube_restore(url), '')
    except:
        sourceCode = ''
    ytb_re = re.compile('views"}},"simpleText":"(.+?)"},"index".+?watch.+?{"videoId":"(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(sourceCode)
    for name, video_id in ytb_re:
        original_name = str(name).replace(r"\u0026","&").replace('\\', '')
        thumbnail = "https://img.youtube.com/vi/%s/0.jpg" % video_id
        fanart = "https://i.ytimg.com/vi/%s/hqdefault.jpg" % video_id
        plugin_url = 'plugin://plugin.video.youtube/play/?video_id='+video_id
        urlfinal = str(plugin_url)
        description = ''
        addLink(original_name.encode('utf-8', 'ignore'),urlfinal.encode('utf-8'),'','',str(thumbnail),str(fanart),description)



def rc_pro4(channel):
    try:
        canal = str(re.compile('redecanais_m3u8=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(channel)[0]).replace('.m3u8','')
        url = '\x61\x48\x52\x30\x63\x48\x4d\x36\x4c\x79\x39\x33\x64\x33\x63\x75\x62\x32\x35\x6c\x63\x47\x78\x68\x65\x57\x68\x6b\x4c\x6d\x4e\x76\x62\x53\x39\x42\x59\x32\x56\x7a\x63\x32\x39\x51\x63\x6d\x39\x70\x59\x6d\x6c\x6b\x62\x79\x39\x42\x5a\x47\x52\x76\x62\x69\x39\x50\x62\x6d\x56\x51\x62\x47\x46\x35\x4c\x31\x52\x57\x4c\x31\x4e\x6c\x63\x6e\x5a\x70\x5a\x47\x39\x79\x4c\x54\x49\x76\x63\x6d\x56\x6e\x5a\x58\x68\x66\x63\x6d\x4d\x75\x64\x48\x68\x30'
        url_decode = base64.b64decode(url).decode('utf-8')
        regex = getRequest2(url_decode,'',useragent).replace('\n','').replace('\r','')
        match_data = re.compile('player="(.+?)".+?eferer="(.+?)".+?eferer_canal="(.+?)".+?pt_player="(.+?)".+?pt_referer_canal="(.+?)".+?odo_opt="(.+?)".+?odo_opt_referer_canal="(.+?)"').findall(regex)
        player = match_data[0][0].replace('\n','').replace('\r','')
        referer = match_data[0][1].replace('\n','').replace('\r','')
        referer_canal = match_data[0][2].replace('\n','').replace('\r','')
        opt_player = match_data[0][3].replace('\n','').replace('\r','')
        opt_referer_canal = match_data[0][4].replace('\n','').replace('\r','')
        modo_opt = match_data[0][5].replace('\n','').replace('\r','')
        modo_opt_referer_canal = match_data[0][6].replace('\n','').replace('\r','')
        if str(modo_opt) == 'false':
            #data = getRequest2(str(player)+canal, str(referer)+canal)
            data = getRequest2(str(player)+canal, str(referer))
            referer_m3u8 = str(referer_canal)+canal
        else:
            data = getRequest2(str(player)+canal+str(opt_player), str(referer)+canal)
            if modo_opt_referer_canal == 'true':
                referer_m3u8 = str(referer_canal)+canal+str(opt_referer_canal)
            else:
                referer_m3u8 = str(referer_canal)+canal
        source = re.compile('source.+?"(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)[0].replace('\n','').replace('\r','')
        servidor_rc = source
        referer_rc = urllib.quote_plus(referer_m3u8)
        #referer_rc = referer_m3u8
        return servidor_rc, referer_rc
    except:
        servidor_rc = ''
        referer_rc = ''
        return servidor_rc, referer_rc


def top_pro(channel):
    try:
        canal = str(re.compile('topcanais_m3u8=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(channel)[0]).replace('.m3u8','')
        url = '\x61\x48\x52\x30\x63\x48\x4d\x36\x4c\x79\x39\x33\x64\x33\x63\x75\x62\x32\x35\x6c\x63\x47\x78\x68\x65\x57\x68\x6b\x4c\x6d\x4e\x76\x62\x53\x39\x42\x59\x32\x56\x7a\x63\x32\x39\x51\x63\x6d\x39\x70\x59\x6d\x6c\x6b\x62\x79\x39\x42\x5a\x47\x52\x76\x62\x69\x39\x50\x62\x6d\x56\x51\x62\x47\x46\x35\x4c\x31\x52\x57\x4c\x31\x4e\x6c\x63\x6e\x5a\x70\x5a\x47\x39\x79\x4c\x54\x49\x76\x63\x6d\x56\x6e\x5a\x58\x68\x66\x64\x47\x39\x77\x59\x32\x46\x75\x59\x57\x6c\x7a\x4c\x6e\x52\x34\x64\x41\x3d\x3d'
        url_decode = base64.b64decode(url).decode('utf-8')
        regex = getRequest2(url_decode,'',useragent).replace('\n','').replace('\r','')
        match_data = re.compile('player="(.+?)".+?eferer="(.+?)".+?pt_player="(.+?)".+?odo_opt="(.+?)"').findall(regex)
        #print(canal)
        player = match_data[0][0].replace('\n','').replace('\r','')
        referer = match_data[0][1].replace('\n','').replace('\r','')
        opt_player = match_data[0][2].replace('\n','').replace('\r','')
        modo_opt = match_data[0][3].replace('\n','').replace('\r','')
        if str(modo_opt) == 'false':
            data = getRequest2(str(player)+canal, str(referer))
        else:
            data = getRequest2(str(player)+canal+str(opt_player), str(referer))
        source = re.compile('source.+?"(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)[0].replace('\n','').replace('\r','')
        servidor_topcanais = source
        referer_m3u8 = str(referer)
        referer_topcanais = urllib.quote_plus(referer_m3u8)
        return servidor_topcanais, referer_topcanais
    except:
        servidor_topcanais = ''
        referer_topcanais  = ''
        return servidor_topcanais, referer_topcanais



def resolver(link, name, thumbnail):
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
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('redecanais_vod') >= 0:
            try:
                video = str(re.compile('redecanais_vod=(.*)', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(link_decoded)[0])
                url = '\x61\x48\x52\x30\x63\x48\x4d\x36\x4c\x79\x39\x33\x64\x33\x63\x75\x62\x32\x35\x6c\x63\x47\x78\x68\x65\x57\x68\x6b\x4c\x6d\x4e\x76\x62\x53\x39\x42\x59\x32\x56\x7a\x63\x32\x39\x51\x63\x6d\x39\x70\x59\x6d\x6c\x6b\x62\x79\x39\x42\x5a\x47\x52\x76\x62\x69\x39\x50\x62\x6d\x56\x51\x62\x47\x46\x35\x4c\x33\x4a\x6a\x58\x33\x5a\x76\x5a\x43\x35\x30\x65\x48\x51\x3d'
                url_decode = base64.b64decode(url).decode('utf-8')
                regex = getRequest2(url_decode,'',useragent).replace('\n','').replace('\r','')
                match_data = re.compile('host="(.+?)"').findall(regex)
                host = match_data[0].replace('\n','').replace('\r','')
                resolved = host+video
            except:
                resolved = ''
        #Rede Canais
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('redecanais') >= 0 and link_decoded.find('m3u8') >= 0:
            try:
                servidor_rc, referer_rc = rc_pro4(link_decoded)
                if servidor_rc > '' and referer_rc > '':
                    link_final2 = servidor_rc+'|Referer='+referer_rc+'|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
                    #print(link_final2)
                else:
                    link_final2 = ''
                    #print(link_final2)
            except:
                link_final2 = ''
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
                    resolved1 = url_quote.replace('http','plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&amp;name='+urllib.quote_plus(str(name2))+'&amp;iconImage='+urllib.quote_plus(thumbnail)+'&amp;thumbnailImage='+urllib.quote_plus(thumbnail)+'&amp;url=http')
                    resolved = resolved1+urllib.quote_plus(result)
                    #print(resolved)
                except:
                    resolved = link_final2
            else:
                resolved = link_final2
                #print(resolved)
        #topcanais        
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('topcanais') >= 0 and link_decoded.find('m3u8') >= 0:
            try:
                servidor_topcanais, referer_topcanais = top_pro(link_decoded)
                if servidor_topcanais > '' and referer_topcanais > '':
                    link_final2 = servidor_topcanais+'|Referer='+referer_topcanais+'|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
                    #print(link_final2)
                else:
                    link_final2 = ''
                    #print(link_final2)
            except:
                link_final2 = ''
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
                    resolved1 = url_quote.replace('http','plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&amp;name='+urllib.quote_plus(str(name2))+'&amp;iconImage='+urllib.quote_plus(thumbnail)+'&amp;thumbnailImage='+urllib.quote_plus(thumbnail)+'&amp;url=http')
                    resolved = resolved1+urllib.quote_plus(result)
                    #print(resolved)
                except:
                    resolved = link_final2
            else:
                resolved = link_final2
                #print(resolved)                
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
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.startswith('https://photos.app') == True:
            try:
                data = getRequest2(link_decoded, 'https://photos.google.com/')
                result = re.compile('<meta property="og:video" content="(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
                if result !=[]:
                    resolved = result[0].replace('-m18','-m22')
                else:
                    resolved = ''
            except:
                resolved = ''
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.startswith('magnet:?xt=') == True:
            resolved = 'plugin://plugin.video.elementum/play?uri='+link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.torrent') >= 0:
            resolved = 'plugin://plugin.video.elementum/play?uri='+link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.mp4') >= 0 and not link_decoded.startswith('magnet:?xt=') == True and not link_decoded.find('.torrent') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.mkv') >= 0 and not link_decoded.startswith('magnet:?xt=') == True and not link_decoded.find('.torrent') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.wmv') >= 0 and not link_decoded.startswith('magnet:?xt=') == True and not link_decoded.find('.torrent') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.wma') >= 0 and not link_decoded.startswith('magnet:?xt=') == True and not link_decoded.find('.torrent') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.avi') >= 0 and not link_decoded.startswith('magnet:?xt=') == True and not link_decoded.find('.torrent') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.mp3') >= 0 and not link_decoded.startswith('magnet:?xt=') == True and not link_decoded.find('.torrent') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.ac3') >= 0 and not link_decoded.startswith('magnet:?xt=') == True and not link_decoded.find('.torrent') >= 0:
            resolved = link_decoded
        elif not link_decoded.startswith("plugin://plugin") and link_decoded.find('.rmvb') >= 0 and not link_decoded.startswith('magnet:?xt=') == True and not link_decoded.find('.torrent') >= 0:
            resolved = link_decoded
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
                resolved1 = url_quote.replace('http','plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&amp;name='+urllib.quote_plus(str(name2))+'&amp;iconImage='+urllib.quote_plus(thumbnail)+'&amp;thumbnailImage='+urllib.quote_plus(thumbnail)+'&amp;url=http')
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
                resolved1 = url_quote.replace('http','plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name='+urllib.quote_plus(str(name2))+'&amp;iconImage='+urllib.quote_plus(thumbnail)+'&amp;thumbnailImage='+urllib.quote_plus(thumbnail)+'&amp;url=http')
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
                resolved1 = url_quote.replace('http','plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name='+urllib.quote_plus(str(name2))+'&amp;iconImage='+urllib.quote_plus(thumbnail)+'&amp;thumbnailImage='+urllib.quote_plus(thumbnail)+'&amp;url=http')
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
                resolved1 = url_quote.replace('http','plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&amp;name='+urllib.quote_plus(str(name2))+'&amp;iconImage='+urllib.quote_plus(thumbnail)+'&amp;thumbnailImage='+urllib.quote_plus(thumbnail)+'&amp;url=http')
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
                resolved1 = url_quote.replace('http','plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name='+urllib.quote_plus(str(name2))+'&amp;iconImage='+urllib.quote_plus(thumbnail)+'&amp;thumbnailImage='+urllib.quote_plus(thumbnail)+'&amp;url=http')
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
                resolved1 = url_quote.replace('http','plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name='+urllib.quote_plus(str(name2))+'&amp;iconImage='+urllib.quote_plus(thumbnail)+'&amp;thumbnailImage='+urllib.quote_plus(thumbnail)+'&amp;url=http')
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



###FAVORITOS
def getFavorites():
    try:
        items = json.loads(open(favorites).read())
        total = len(items)
        for i in items:
            name = i[0]
            url = i[1]
            try:
                urldecode = base64.b64decode(base64.b16decode(url))
            except:
                urldecode = url
            try:
                urlrep = urldecode.replace('redtube.com/braziilian/oneplay1',base64.b64decode('\x62\x32\x35\x6c\x63\x47\x78\x68\x65\x57\x68\x6b\x4c\x6d\x4e\x76\x62\x53\x39\x42\x59\x32\x56\x7a\x63\x32\x39\x51\x63\x6d\x39\x70\x59\x6d\x6c\x6b\x62\x79\x39\x42\x5a\x47\x52\x76\x62\x69\x39\x50\x62\x6d\x56\x51\x62\x47\x46\x35').decode('utf-8'))
            except:
                urlrep = urldecode
            mode = i[2]
            subtitle = i[3]
            try:
                subtitledecode = base64.b64decode(base64.b16decode(subtitle))
            except:
                subtitledecode = subtitle
            cleaname = i[4]
            iconimage = i[5]
            try:
                fanArt = i[6]
                if fanArt == None:
                    raise
            except:
                if addon.getSetting('use_thumb') == "true":
                    fanArt = iconimage
                else:
                    fanArt = fanart
            description = i[7]

            if mode == 0:
                try:
                    addLink(name,urlrep,subtitledecode,cleaname,iconimage,fanArt,description)
                except:
                    pass
            elif mode == 11 or mode == 16 or mode == 17 or mode == 18:
                try:
                    addDir2(str(name).encode('utf-8', 'ignore'),str(urlrep),mode,str(subtitledecode),cleaname.encode('utf-8', 'ignore'),iconimage,fanArt,description.encode('utf-8'),False)
                except:
                    pass
            elif mode > 0 and mode < 7:
                try:
                    addDir(name,urlrep,mode,iconimage,fanArt,description)
                except:
                    pass
            else:
                try:
                    addDir2(str(name).encode('utf-8', 'ignore'),str(urlrep),mode,str(subtitledecode),cleaname.encode('utf-8', 'ignore'),iconimage,fanArt,description.encode('utf-8'))
                except:
                    pass
    except:
        pass


def addFavorite(name,url,fav_mode,subtitle,cleaname,iconimage,fanart,description):
    favList = []
    try:
        # seems that after
        name = name.encode('utf-8', 'ignore')
    except:
        pass
    if os.path.exists(favorites)==False:
        addonID = xbmcaddon.Addon().getAddonInfo('id')
        addon_data_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', addonID))
        if os.path.exists(addon_data_path)==False:
            os.mkdir(addon_data_path)
        xbmc.sleep(7)
        favList.append((name,url,fav_mode,subtitle,cleaname,iconimage,fanart,description))
        a = open(favorites, "w")
        a.write(json.dumps(favList))
        a.close()
        notify('Adicionado aos Favoritos do Oneplay!')
        xbmc.executebuiltin("XBMC.Container.Refresh")
    else:
        a = open(favorites).read()
        data = json.loads(a)
        data.append((name,url,fav_mode,subtitle,cleaname,iconimage,fanart,description))
        b = open(favorites, "w")
        b.write(json.dumps(data))
        b.close()
        notify('Adicionado aos Favoritos do Oneplay!')
        xbmc.executebuiltin("XBMC.Container.Refresh")


def rmFavorite(name):
    data = json.loads(open(favorites).read())
    for index in range(len(data)):
        if data[index][0]==name:
            del data[index]
            b = open(favorites, "w")
            b.write(json.dumps(data))
            b.close()
            break
    notify('Removido dos Favoritos do Oneplay!')
    xbmc.executebuiltin("XBMC.Container.Refresh")




def addDir(name,url,mode,iconimage,fanart,description,folder=True,pesquisa=False):
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
    ##FAV
    if favoritos == 'true' and  mode !=4 and mode !=7 and mode !=8 and mode !=9 and mode !=10 and mode !=12 and mode !=15 and not pesquisa and not url.startswith(url_title) and not url.find('username') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x54\x56\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x46\x69\x6c\x6d\x65\x73\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x53\x65\x72\x69\x65\x73\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x44\x65\x73\x65\x6e\x68\x6f\x73\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x41\x6e\x69\x6d\x65\x73\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x54\x6f\x6b\x75\x73\x61\x74\x73\x75\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x4e\x6f\x76\x65\x6c\x61\x73\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x52\x61\x64\x69\x6f\x73\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x53\x68\x6f\x77\x73\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x53\x65\x72\x69\x65\x73\x2d\x50\x72\x69\x6e\x63\x69\x70\x61\x6c\x2e\x68\x74\x6d\x6c') >= 0:
        try:
            url_fav = url.replace(base64.b64decode('\x62\x32\x35\x6c\x63\x47\x78\x68\x65\x57\x68\x6b\x4c\x6d\x4e\x76\x62\x53\x39\x42\x59\x32\x56\x7a\x63\x32\x39\x51\x63\x6d\x39\x70\x59\x6d\x6c\x6b\x62\x79\x39\x42\x5a\x47\x52\x76\x62\x69\x39\x50\x62\x6d\x56\x51\x62\x47\x46\x35').decode('utf-8'),'redtube.com/braziilian/oneplay1')
        except:
            url_fav = url
        try:
            name_fav = json.dumps(name)
        except:
            name_fav =  name
        try:
            contextMenu = []
            if name_fav in FAV:
                try:
                    contextMenu.append(('Remover dos Favoritos do Oneplay','XBMC.RunPlugin(%s?mode=14&name=%s)'%(sys.argv[0], urllib.quote_plus(name))))
                except:
                    contextMenu.append(('Remover dos Favoritos do Oneplay','XBMC.RunPlugin(%s?mode=14&name=%s)'%(sys.argv[0], urllib.quote_plus(name.encode('utf-8', 'ignore')))))
            else:
                try:
                    fav_params = ('%s?mode=13&name=%s&url=%s&subtitle=%s&cleaname=%s&iconimage=%s&fanart=%s&description=%s&fav_mode=%s'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(base64.b16encode(base64.b64encode(url_fav.encode('utf-8')))), '', '', urllib.quote_plus(iconimage), urllib.quote_plus(fanart), urllib.quote_plus(description), str(mode)))
                except:
                    fav_params = ('%s?mode=13&name=%s&url=%s&subtitle=%s&cleaname=%s&iconimage=%s&fanart=%s&description=%s&fav_mode=%s'%(sys.argv[0], urllib.quote_plus(name.encode('utf-8', 'ignore')), urllib.quote_plus(base64.b16encode(base64.b64encode(url_fav.encode('utf-8')))), '', '', urllib.quote_plus(iconimage.encode("utf-8")), urllib.quote_plus(fanart.encode("utf-8")), urllib.quote_plus(description.encode("utf-8")), str(mode)))
                contextMenu.append(('Adicionar aos Favoritos do Oneplay','XBMC.RunPlugin(%s)' %fav_params))
            li.addContextMenuItems(contextMenu)
        except:
            pass
    xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=li, isFolder=folder)



def addDir2(name,url,mode,subtitle,cleaname,iconimage,fanart,description,folder=True,pesquisa=False):
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
    ##FAV
    if favoritos == 'true' and  mode !=4 and mode !=7 and mode !=8 and mode !=9 and mode !=10 and mode !=12 and mode !=15 and not pesquisa and not url.startswith(url_title) and not url.find('username') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x54\x56\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x46\x69\x6c\x6d\x65\x73\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x53\x65\x72\x69\x65\x73\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x44\x65\x73\x65\x6e\x68\x6f\x73\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x41\x6e\x69\x6d\x65\x73\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x54\x6f\x6b\x75\x73\x61\x74\x73\x75\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x4e\x6f\x76\x65\x6c\x61\x73\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x52\x61\x64\x69\x6f\x73\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x4d\x65\x6e\x75\x2d\x53\x68\x6f\x77\x73\x2e\x68\x74\x6d\x6c') >= 0 and not url.find('\x53\x65\x72\x69\x65\x73\x2d\x50\x72\x69\x6e\x63\x69\x70\x61\x6c\x2e\x68\x74\x6d\x6c') >= 0:
        try:
            url_fav = url.replace(base64.b64decode('\x62\x32\x35\x6c\x63\x47\x78\x68\x65\x57\x68\x6b\x4c\x6d\x4e\x76\x62\x53\x39\x42\x59\x32\x56\x7a\x63\x32\x39\x51\x63\x6d\x39\x70\x59\x6d\x6c\x6b\x62\x79\x39\x42\x5a\x47\x52\x76\x62\x69\x39\x50\x62\x6d\x56\x51\x62\x47\x46\x35').decode('utf-8'),'redtube.com/braziilian/oneplay1')
        except:
            url_fav = url
        try:
            name_fav = json.dumps(name)
        except:
            name_fav =  name
        try:
            contextMenu = []
            if name_fav in FAV:
                try:
                    contextMenu.append(('Remover dos Favoritos do Oneplay','XBMC.RunPlugin(%s?mode=14&name=%s)'%(sys.argv[0], urllib.quote_plus(name))))
                except:
                    contextMenu.append(('Remover dos Favoritos do Oneplay','XBMC.RunPlugin(%s?mode=14&name=%s)'%(sys.argv[0], urllib.quote_plus(name.encode('utf-8', 'ignore')))))
            else:
                try:
                    fav_params = ('%s?mode=13&name=%s&url=%s&subtitle=%s&cleaname=%s&iconimage=%s&fanart=%s&description=%s&fav_mode=%s'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(base64.b16encode(base64.b64encode(url_fav.encode('utf-8')))), urllib.quote_plus(base64.b16encode(base64.b64encode(subtitle.encode('utf-8')))), urllib.quote_plus(cleaname), urllib.quote_plus(iconimage), urllib.quote_plus(fanart), urllib.quote_plus(description), str(mode)))
                except:
                    fav_params = ('%s?mode=13&name=%s&url=%s&subtitle=%s&cleaname=%s&iconimage=%s&fanart=%s&description=%s&fav_mode=%s'%(sys.argv[0], urllib.quote_plus(name.encode('utf-8', 'ignore')), urllib.quote_plus(base64.b16encode(base64.b64encode(url_fav.encode('utf-8')))), urllib.quote_plus(base64.b16encode(base64.b64encode(subtitle.encode('utf-8')))), urllib.quote_plus(cleaname.encode("utf-8")), urllib.quote_plus(iconimage.encode("utf-8")), urllib.quote_plus(fanart.encode("utf-8")), urllib.quote_plus(description.encode("utf-8")), str(mode)))
                contextMenu.append(('Adicionar aos Favoritos do Oneplay','XBMC.RunPlugin(%s)' %fav_params))
            li.addContextMenuItems(contextMenu)
        except:
            pass
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
        try:
            name_fav = json.dumps(cleaname)
        except:
            name_fav =  cleaname
        name2_fav = cleaname
        desc_fav = ''
        li.setInfo(type='video', infoLabels={'Title': cleaname, 'plot': description })
    else:
        try:
            name_fav = json.dumps(name)
        except:
            name_fav = name
        name2_fav = name
        desc_fav = description
        li.setInfo(type='video', infoLabels={'plot': description })
    if subtitle > '':
        li.setSubtitles([subtitle])
    ##FAV
    if favoritos == 'true':
        try:
            contextMenu = []
            if name_fav in FAV:
                try:
                    contextMenu.append(('Remover dos Favoritos do Oneplay','XBMC.RunPlugin(%s?mode=14&name=%s)'%(sys.argv[0], urllib.quote_plus(name2_fav))))
                except:
                    contextMenu.append(('Remover dos Favoritos do Oneplay','XBMC.RunPlugin(%s?mode=14&name=%s)'%(sys.argv[0], urllib.quote_plus(name2_fav.encode('utf-8', 'ignore')))))
            else:
                try:
                    fav_params = ('%s?mode=13&name=%s&url=%s&subtitle=%s&cleaname=%s&iconimage=%s&fanart=%s&description=%s&fav_mode=0'%(sys.argv[0], urllib.quote_plus(name2_fav), urllib.quote_plus(base64.b16encode(base64.b64encode(url.encode('utf-8')))), urllib.quote_plus(base64.b16encode(base64.b64encode(subtitle.encode('utf-8')))), urllib.quote_plus(cleaname), urllib.quote_plus(iconimage), urllib.quote_plus(fanart), urllib.quote_plus(desc_fav)))
                except:
                    fav_params = ('%s?mode=13&name=%s&url=%s&subtitle=%s&cleaname=%s&iconimage=%s&fanart=%s&description=%s&fav_mode=0'%(sys.argv[0], urllib.quote_plus(name2_fav.encode('utf-8', 'ignore')), urllib.quote_plus(base64.b16encode(base64.b64encode(url.encode('utf-8')))), urllib.quote_plus(base64.b16encode(base64.b64encode(subtitle.encode('utf-8')))), urllib.quote_plus(cleaname.encode("utf-8")), urllib.quote_plus(iconimage.encode("utf-8")), urllib.quote_plus(fanart.encode("utf-8")), urllib.quote_plus(desc_fav.encode("utf-8"))))
                contextMenu.append(('Adicionar aos Favoritos do Oneplay','XBMC.RunPlugin(%s)' %fav_params))
            li.addContextMenuItems(contextMenu)
        except:
            pass
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=folder)



def parental_password():
    try:
        addonID = xbmcaddon.Addon().getAddonInfo('id')
        addon_data_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', addonID))
        if os.path.exists(addon_data_path)==False:
            os.mkdir(addon_data_path)
        xbmc.sleep(7)
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
    except:
        pass



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
            youtube = addon.getSetting('youtube')
            if fcheck and fcheck.read() == '1' and check_addon == 'true':
                #print('valor 1')
                fcheck.close()
                link = getRequest2('https://raw.githubusercontent.com/OnePlayHD/OneRepo/master/verificar_addons.txt','').replace('\n','').replace('\r','')
                match = re.compile('addon_name="(.+?)".+?ddon_id="(.+?)".+?ir="(.+?)".+?rl_zip="(.+?)".+?escription="(.+?)"').findall(link)
                for addon_name,addon_id,directory,url_zip,description in match:
                    if addon_id == 'plugin.video.elementum' and elementum == 'false':
                        pass
                    elif addon_id == 'script.module.six' and youtube == 'false':
                        pass
                    elif addon_id == 'plugin.video.youtube' and youtube == 'false':
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



def contador():
    try:
        request_headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8",
        "Referer": nome_contador,
        "Connection": "close",
        }
        request = urllib2.Request("https://whos.amung.us/pingjs/?k=6gjsucgcje", headers=request_headers)
        response = urllib2.urlopen(request).read()
        #tempo_delay = 0
        #xbmc.sleep(tempo_delay*0)
    except:
        pass
contador()



def CheckUpdate(msg):
        try:
                uversao = urllib2.urlopen( "http://raw.githubusercontent.com/OnePlayHD/OneRepo/master/plugin.video.OnePlay/version.txt" ).read().replace('','').replace('','')
                uversao = re.compile('[a-zA-Z\.\d]+').findall(uversao)[0]
                #xbmcgui.Dialog().ok(Versao, uversao)
                if uversao != Versao_data:
                        Update()
                        #xbmc.executebuiltin("XBMC.Container.Refresh()")
                elif msg==True:
                        xbmcgui.Dialog().ok('[COLOR white][B]AVISO[/B][/COLOR]', "O addon já está atualizado na [COLOR aquamarine]Versão: "+Versao_numero+"[/COLOR] em "+Versao_data+"\nAs atualizações normalmente são automáticas caso não atualize baixe o add-on no site oficial.\n[COLOR aquamarine][B]Use esse recurso caso não esteja recebendo automático.[/B][/COLOR]")
                        #xbmc.executebuiltin("XBMC.Container.Refresh()")
        except urllib2.URLError, e:
                if msg==True:
                        xbmcgui.Dialog().ok('[COLOR white][B]AVISO[/B][/COLOR]', "Não foi possível atualizar. Tente novamente mais tarde.")



def Update():
        Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') ).decode("utf-8")
        try:
                fonte = urllib2.urlopen( "http://raw.githubusercontent.com/OnePlayHD/OneRepo/master/plugin.video.OnePlay/database.py" ).read().replace('','')
                prog = re.compile('checkintegrity13122019').findall(fonte)
                if prog:
                        py = os.path.join( Path, "database.py")
                        file = open(py, "w")
                        file.write(fonte)
                        file.close()
                fonte = urllib2.urlopen( "http://raw.githubusercontent.com/OnePlayHD/OneRepo/master/plugin.video.OnePlay/downloader.py" ).read().replace('','')
                prog = re.compile('checkintegrity13122019').findall(fonte)
                if prog:
                        py = os.path.join( Path, "downloader.py")
                        file = open(py, "w")
                        file.write(fonte)
                        file.close()
                fonte = urllib2.urlopen( "http://raw.githubusercontent.com/OnePlayHD/OneRepo/master/plugin.video.OnePlay/downloader_epg.py" ).read().replace('','')
                prog = re.compile('checkintegrity13122019').findall(fonte)
                if prog:
                        py = os.path.join( Path, "downloader_epg.py")
                        file = open(py, "w")
                        file.write(fonte)
                        file.close()
                fonte = urllib2.urlopen( "http://raw.githubusercontent.com/OnePlayHD/OneRepo/master/plugin.video.OnePlay/extract.py" ).read().replace('','')
                prog = re.compile('checkintegrity13122019').findall(fonte)
                if prog:
                        py = os.path.join( Path, "extract.py")
                        file = open(py, "w")
                        file.write(fonte)
                        file.close()
                fonte = urllib2.urlopen( "http://raw.githubusercontent.com/OnePlayHD/OneRepo/master/plugin.video.OnePlay/main.py" ).read().replace('','')
                prog = re.compile('checkintegrity13122019').findall(fonte)
                if prog:
                        py = os.path.join( Path, "main.py")
                        file = open(py, "w")
                        file.write(fonte)
                        file.close()
                fonte = urllib2.urlopen( "http://raw.githubusercontent.com/OnePlayHD/OneRepo/master/plugin.video.OnePlay/resources/settings.xml" ).read().replace('','')
                prog = re.compile('</settings>').findall(fonte)
                if prog:
                        py = os.path.join( Path, "resources/settings.xml")
                        file = open(py, "w")
                        file.write(fonte)
                        file.close()
                fonte = urllib2.urlopen( "http://raw.githubusercontent.com/OnePlayHD/OneRepo/master/plugin.video.OnePlay/addon.xml" ).read().replace('','')
                prog = re.compile('</addon>').findall(fonte)
                if prog:
                        py = os.path.join( Path, "addon.xml")
                        file = open(py, "w")
                        file.write(fonte)
                        file.close()
                xbmc.executebuiltin("Notification({0}, {1}, 9000, {2})".format(__addonname__, "Add-on atualizado", __icon__))
        except:
                xbmcgui.Dialog().ok('[COLOR white][B]AVISO[/B][/COLOR]', "A Sua versão está desatualizada, Caso os conteúdos não esteja aparecendo ao carregar\n[COLOR aquamarine]Atualize o add-on no repositorio ou baixe o zip no site oficial[/COLOR].")



def suporte():
    import xbmc
    import webbrowser
    dialog = xbmcgui.Dialog()
    link = dialog.select('[B][COLOR white]SUPORTE[/COLOR] [COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR][/B]', ['[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: SITE', '[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: REPOSITÓRIO','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: FACEBOOK','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: TELEGRAM','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: APP [COLOR aquamarine](VIP)[/COLOR] PRO "RECOMENDADO"','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: APP [COLOR aquamarine](VIP)[/COLOR] LITE "OPCIONAL"','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: [COLOR gold](P2P)[/COLOR] SOMENTE APP OUTRO SISTEMA','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: [B][COLOR white]ENTRAR NO ADDON[/COLOR][/B]'])
    if link == 0:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://oneplayhd.com'))
        else:
            webbrowser.open('https://oneplayhd.com')
    if link == 1:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://oneplayhd.com/oneplay'))
        else:
            webbrowser.open('https://oneplayhd.com/oneplay')
    if link == 2:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://www.facebook.com/groups/oneplay2019' ))
        else:
            webbrowser.open('https://www.facebook.com/groups/oneplay2019')
    if link == 3:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://t.me/oneplay2019' ))
        else:
            webbrowser.open('https://t.me/oneplay2019')
    if link == 4:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://drive.google.com/file/d/1rHFO40e-sABdRguOtA1RWMGu8gu20YGZ/view?usp=sharing'))
        else:
            webbrowser.open('https://drive.google.com/file/d/1rHFO40e-sABdRguOtA1RWMGu8gu20YGZ/view?usp=sharing')
    if link == 5:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://drive.google.com/file/d/1yAwct_lTpPfx0f74wrM6PsabsR4JFADC/view?usp=sharing'))
        else:
            webbrowser.open('https://drive.google.com/file/d/1yAwct_lTpPfx0f74wrM6PsabsR4JFADC/view?usp=sharing')
    if link == 6:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://drive.google.com/file/d/1JM3XibrImwuuah8BqVXAVZXeNLa6TcLN/view?usp=sharing'))
        else:
            webbrowser.open('https://drive.google.com/file/d/1JM3XibrImwuuah8BqVXAVZXeNLa6TcLN/view?usp=sharing')


def doacao():
    import xbmc
    import webbrowser
    dialog = xbmcgui.Dialog()
    link = dialog.select('[B][COLOR white]FAÇA UMA DOAÇÃO AO[/COLOR] [COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR][/B]', ['[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: DOAÇÃO [COLOR steelblue]MERCADO[/COLOR][COLOR skyblue]PAGO[/COLOR] R$10,00','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: DOAÇÃO [COLOR steelblue]MERCADO[/COLOR][COLOR skyblue]PAGO[/COLOR] R$10,00','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: DOAÇÃO [COLOR steelblue]MERCADO[/COLOR][COLOR skyblue]PAGO[/COLOR] R$10,00','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: DOAÇÃO [COLOR lime]PYCPAY[/COLOR]','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: DOAÇÃO [COLOR lime]PYCPAY[/COLOR]','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: DOAÇÃO [COLOR white]PAG[/COLOR][COLOR lime]SEGURO[/COLOR]','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: DOAÇÃO [COLOR white]COM ANÚNCIO[/COLOR]','[COLOR aquamarine]ONE[/COLOR][COLOR white]PLAY[/COLOR]: [B][COLOR white]CONTINUAR NO ADDON[/COLOR][/B]'])
    if link == 0:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=389116232-af9b1ab4-0be4-468d-810c-00dc6814b095' ))
        else:
            webbrowser.open('https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=389116232-af9b1ab4-0be4-468d-810c-00dc6814b095')
    if link == 1:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=202603370-85e41819-ea32-4756-92eb-f025463ffcea' ))
        else:
            webbrowser.open('https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=202603370-85e41819-ea32-4756-92eb-f025463ffcea')
    if link == 2:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=157151682-e75906b8-d000-4cfc-8fa5-407387a96445' ))
        else:
            webbrowser.open('https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=157151682-e75906b8-d000-4cfc-8fa5-407387a96445')
    if link == 3:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://app.picpay.com/user/zoreu/10.0' ))
        else:
            webbrowser.open('https://app.picpay.com/user/zoreu/10.0')
    if link == 4:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://app.picpay.com/user/thiagofeitosa84/10.0' ))
        else:
            webbrowser.open('https://app.picpay.com/user/thiagofeitosa84/10.0')
    if link == 5:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://pag.ae/7V4uYahnJ' ))
        else:
            webbrowser.open('https://pag.ae/7V4uYahnJ')
    #pagina anuncio
    if link == 6:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://oneplayhd.com/' ))
        else:
            webbrowser.open('https://oneplayhd.com/')




def time_convert(timestamp):
    try:
        if timestamp > '':
            dt_object = datetime.fromtimestamp(int(timestamp))
            time_br = dt_object.strftime('%d/%m/%Y às %H:%M:%S')
            return str(time_br)
        else:
            valor = ''
            return valor
    except:
        valor = ''
        return valor


def info_vip():
    username_vip = addon.getSetting('username')
    password_vip = addon.getSetting('password')
    if username_vip > '' and password_vip > '':
        try:
            url_info = url_server_vip.replace('/get.php', '')+'/player_api.php?username=%s&password=%s'%(username_vip,password_vip)
            dados_vip = getRequest2(url_info, '')
            filtrar_info = re.compile('"status":"(.+?)".+?"exp_date":"(.+?)".+?"is_trial":"(.+?)".+?"created_at":"(.+?)".+?max_connections":"(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(dados_vip)
            if filtrar_info !=[]:
                status = str(filtrar_info[0][0])
                exp_date = str(filtrar_info[0][1])
                trial = str(filtrar_info[0][2])
                created = str(filtrar_info[0][3])
                max_connection = str(filtrar_info[0][4])
                #status do usuario
                if status > '' and status == 'Active':
                    status_result = 'Ativo'
                else:
                    status_result = 'Expirado'
                #Validade do vip
                if exp_date > '':
                    expires = time_convert(str(exp_date))
                else:
                    expires = ''
                #usuario de teste
                if trial > '' and trial == '0':
                    vip_trial = 'Não'
                else:
                    vip_trial = 'Sim'
                #criado
                if created > '':
                    created_time = time_convert(str(created))
                else:
                    created_time = ''
                #limite de conexoes
                if max_connection > '':
                    limite_conexao = max_connection
                else:
                    limite_conexao = ''

                try:
                    xbmcaddon.Addon().setSetting("status_vip", status_result)
                    xbmcaddon.Addon().setSetting("created_at", created_time)
                    xbmcaddon.Addon().setSetting("exp_date", expires)
                    xbmcaddon.Addon().setSetting("is_trial", vip_trial)
                    xbmcaddon.Addon().setSetting("max_connection", limite_conexao)
                except:
                    pass
        except:
            try:
                xbmcaddon.Addon().setSetting("status_vip", '')
                xbmcaddon.Addon().setSetting("created_at", '')
                xbmcaddon.Addon().setSetting("exp_date", '')
                xbmcaddon.Addon().setSetting("is_trial", '')
                xbmcaddon.Addon().setSetting("max_connection", '')
            except:
                pass



def vip():
    username_vip = addon.getSetting('username')
    password_vip = addon.getSetting('password')
    #tipo_servidor = addon.getSetting('servidor')
    vip_menu = addon.getSetting('exibirvip')
    saida_transmissao = addon.getSetting('saida')
    if username_vip > '' and password_vip > '':
        info_vip()
    if int(saida_transmissao) == 1:
        saida_canal = 'm3u8'
    else:
        saida_canal = 'ts'
    if vip_menu == 'true':
        #if tipo_servidor=='OnePlay':
        if username_vip > '' and password_vip > '':
            url = ''+url_server_vip+'?username=%s&password=%s&type=m3u_plus&output=%s'%(username_vip,password_vip,saida_canal)
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
            getData(url_pesquisa+'?pesquisar='+d, '', True)
            xbmcplugin.endOfDirectory(addon_handle)
            quit()
        else:
            #xbmc.executebuiltin("XBMC.Container.Refresh()")
            xbmcplugin.endOfDirectory(addon_handle)
            quit()
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
        xbmcgui.Dialog().ok(titulo_boas_vindas,getRequest2(url_mensagem_bem_vindo, ''))
    if addon.getSetting('popupsupport') == 'true':
        suporte()
    addDir(title_menu,url_title,1,__icon__,'',getRequest2(url_title_descricao, ''))
    ### VIP ##############
    vip()
    addDir(menu_doacao,'',8,thumb_icon_doacao,'',desc_doacao)
    if favoritos == 'true':
        addDir(menu_favoritos,'',15,thumb_favoritos,'',desc_favoritos)
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
subtitle=None
cleaname=None

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

try:
    fav_mode=int(params["fav_mode"])
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
    xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','FECHE O KODI E ABRA NOVAMENTE PARA ATUALIZAR AS CONFIGURAÇÕES')
    xbmc.executebuiltin("XBMC.Container.Refresh()")

#Link Vazio
elif mode==5:
    xbmc.executebuiltin("XBMC.Container.Refresh()")

elif mode==6:
    ytbmode = addon.getSetting('ytbmode')
    if int(ytbmode) == 0:
        pluginquerybyJSON(url)
    elif int(ytbmode) == 1:
        getPlaylistLinksYoutube(url)
    else:
        youtube(url)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode==7:
    Pesquisa()

elif mode==8:
    doacao()

elif mode==9:
    xbmcgui.Dialog().ok(titulo_vip, getRequest2(url_vip_dialogo, ''))
    xbmcaddon.Addon().openSettings()
    xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','FECHE O KODI E ABRA NOVAMENTE PARA ATUALIZAR AS CONFIGURAÇÕES')
    xbmc.executebuiltin("XBMC.Container.Refresh()")

elif mode==10:
    adult(name, url, cleaname, iconimage, description, subtitle)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode==11:
    playlist(name, url, cleaname, iconimage, description, subtitle)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode==12:
    CheckUpdate(True)
    xbmc.executebuiltin("XBMC.Container.Refresh()")

elif mode==13:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    addFavorite(name,url,fav_mode,subtitle,cleaname,iconimage,fanart,description)

elif mode==14:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    rmFavorite(name)

elif mode==15:
    getFavorites()
    xbmcplugin.endOfDirectory(addon_handle)

elif mode==16:
    individual_player(name, url, cleaname, iconimage, description, subtitle)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode==17:
    youtube_live_player(name, url, cleaname, iconimage, description, subtitle)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode==18:
    m3u8_player(name, url, cleaname, iconimage, description, subtitle)
    xbmcplugin.endOfDirectory(addon_handle)