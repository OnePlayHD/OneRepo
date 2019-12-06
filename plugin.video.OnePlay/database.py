import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,os,xbmcaddon, xbmcvfs
import sqlite3
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

def get_kversion():
	full_version_info = xbmc.getInfoLabel('System.BuildVersion')
	baseversion = full_version_info.split(".")
	intbase = int(baseversion[0])
	# if intbase > 16.5:
	# 	log('HIGHER THAN 16.5')
	# if intbase < 16.5:
	# 	log('LOWER THAN 16.5')
	return  intbase
    
def set_enabled(id):
    if get_kversion() >16.5:
        try:
            dir_database = xbmc.translatePath("special://profile/Database")
            file_database = os.path.join(dir_database, 'Addons27.db')
            sqliteConnection = database.connect(file_database)
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")
            print('****DATABASE: '+file_database+'****')
            state = 1
            print('***DATABASE ID ADDON: '+id+' *****')
            cursor.execute("UPDATE installed SET enabled= ? WHERE addonID= ?", (state, id,))            
            sqliteConnection.commit()
            print("Record Updated successfully")
            xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
            #xbmc.executebuiltin("XBMC.Container.Update()")
            #xbmc.executebuiltin("XBMC.Container.Refresh()")           
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to update sqlite table", error)
        finally:
            if (cursor):
                cursor.close()
                print("The sqlite connection is closed") 
 

def enable_addon(state, id):
        try:            
            dir_database = xbmc.translatePath("special://profile/Database")
            file_database = os.path.join(dir_database, 'Addons27.db')
            sqliteConnection = database.connect(file_database)
            cursor = sqliteConnection.cursor()
            r = cursor.execute('SELECT * FROM installed WHERE enabled = ? AND addonID= ?', (state, id,))
            if r.fetchone() == None:
                print('Addons Verificados!')
            else:
                print('Addon encontrado')
                set_enabled(id)                
        except sqlite3.Error as error:
            print("Failed to check sqlite table", error)
        finally:
            if (cursor):
                cursor.close()
                print("The sqlite connection is closed")

def check_database(id):
    enable_addon(0, id)                

