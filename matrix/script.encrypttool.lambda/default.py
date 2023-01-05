# -*- coding: utf-8 -*-
import six
import os
import zlib
import base64
from kodi_six import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')
translate = xbmcvfs.translatePath if six.PY3 else xbmc.translatePath
home = translate(addon.getAddonInfo('path')) if six.PY3 else translate(addon.getAddonInfo('path')).decode('utf-8')
new_file = os.path.join(home, 'output','new_default.py')
output = os.path.join(home, 'output')
max_camadas = 5


def platform():
    from kodi_six import xbmc

    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux') or xbmc.getCondVisibility('system.platform.linux.Raspberrypi'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios') or xbmc.getCondVisibility('system.platform.darwin'):
        return 'ios'


def open_file():
    dialog = xbmcgui.Dialog()
    try:
        file = dialog.browseSingle(1, 'Select python file', 'files', '', False, False)
    except:
        file = ''
    if file:
        if '.py' in file:
            return file
    return False


def run_comand():
    if platform() == 'windows':
        os.system('explorer %s'%output)
    elif platform() == 'linux':
        os.system('nautilus %s'%output)

def make_encript_file():
    py = open_file()
    if py:
        if xbmcvfs.exists(new_file):
            try:
                os.remove(new_file)
            except:
                pass
        if six.PY3:
            try:
                with open(py, 'r', encoding='utf-8') as f:
                    try:
                        codigo = f.read().encode('utf-8')
                    except:
                        codigo = f.read()
                    camadas = 0
                    while True:
                        camadas +=1
                        codigo_comprimido_zlib = zlib.compress(codigo) 
                        codigo_base64 = base64.b64encode(codigo_comprimido_zlib)
                        invertido = codigo_base64[::-1]
                        codigo = "exec((_)(%s))"%invertido
                        codigo = codigo.encode('utf-8')
                        if camadas == max_camadas:
                            try:
                                codigo = codigo.decode('utf-8')
                            except:
                                pass
                            break                       
                    if not xbmcvfs.exists(output):
                        try:
                            xbmcvfs.mkdir(output)
                        except:
                            pass
                    with open(new_file, 'w', encoding='utf-8') as f2:
                        file = "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));%s"%codigo
                        f2.write(file)
            except:
                xbmcgui.Dialog().ok(addonname, 'Failed make file!')
        else:
            try:
                with open(py, 'r') as f:
                    try:
                        codigo = f.read().encode('utf-8','ignore')
                    except:
                        codigo = f.read()
                    camadas = 0
                    while True:
                        camadas +=1
                        codigo_comprimido_zlib = zlib.compress(codigo) 
                        codigo_base64 = base64.b64encode(codigo_comprimido_zlib)
                        invertido = codigo_base64[::-1]
                        codigo = "exec((_)(b'"+str(invertido)+"'))"
                        codigo = codigo.encode('utf-8', 'ignore')
                        if camadas == max_camadas:
                            try:
                                codigo = codigo.decode('utf-8')
                            except:
                                pass
                            break                       
                    if not xbmcvfs.exists(output):
                        try:
                            xbmcvfs.mkdir(output)
                        except:
                            pass
                    with open(new_file, 'w') as f2:
                        file = "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));%s"%codigo
                        f2.write(file)
            except:
                xbmcgui.Dialog().ok(addonname, 'Failed make file!')                    

        if xbmcvfs.exists(new_file):
            run_comand()
    else:
        xbmcgui.Dialog().ok(addonname, 'this file is not python script!')


def menu():
    if platform() == 'windows' or platform() == 'linux':
        make_encript_file()
    else:
        xbmcgui.Dialog().ok(addonname, 'Your system is not windows or linux!')



if __name__ == '__main__': menu()