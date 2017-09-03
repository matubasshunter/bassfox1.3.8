import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,uuid,os,re,sys,base64,json,time,shutil,urlresolver,random,liveresolver,hashlib,smtplib
from resources.libs.common_addon import Addon
from metahandler import metahandlers
from HTMLParser import HTMLParser
from datetime import datetime


addon_id            = 'plugin.video.bassfox'
addon               = Addon(addon_id, sys.argv)
selfAddon           = xbmcaddon.Addon(id=addon_id)
AddonTitle          = '[COLOR yellow]BassFox[/COLOR]'
addonPath           = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.bassfox')
fanarts             = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'fanart.jpg'))
fanart              = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'fanart.jpg'))
icon                = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
dp                  = xbmcgui.DialogProgress()
dialog              = xbmcgui.Dialog()
thumbnaildir        = xbmc.translatePath (os.path.join('special://home/userdata/Thumbnails'))
cache               = xbmc.translatePath (os.path.join('special://home/cache'))


def open_url(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
        response = urllib2.urlopen(req, timeout=5)
        link=response.read()
        response.close()
        link=link.replace('\n','').replace('\r','').replace('<fanart></fanart>','<fanart>x</fanart>').replace('<thumbnail></thumbnail>','<thumbnail>x</thumbnail>').replace('<utube>','<link>https://www.youtube.com/watch?v=').replace('</utube>','</link>')
        return link
    except:quit()
    
def open_url2(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        
        return link
        
def addDir(name,url,mode,iconimage,fanart,description=''):
    
    if not "http" in iconimage:
        iconimage = icon
    if not "http" in fanart:
        fanart = fanarts
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setProperty( "fanart_Image", fanart )
    liz.setProperty( "icon_Image", iconimage )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name, url, mode, iconimage, fanart, description=''):
    if not "http" in iconimage:
        iconimage = icon
    if not "http" in fanart:
        fanart = fanarts
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setProperty( "fanart_Image", fanart )
    liz.setProperty( "icon_Image", iconimage )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok
        
def PLAYLINK(name,url,iconimage):

    import urlresolver
    
    if urlresolver.HostedMediaFile(url).valid_url(): 
        stream_url = urlresolver.HostedMediaFile(url).resolve()
        liz = xbmcgui.ListItem(name,iconImage=icon, thumbnailImage=icon)
        liz.setPath(stream_url)
        xbmc.Player ().play(stream_url, liz, False)
        quit()
    else:
        stream_url=url
        liz = xbmcgui.ListItem(name,iconImage=icon, thumbnailImage=icon)
        liz.setPath(stream_url)
        xbmc.Player ().play(stream_url, liz, False)
        quit()
        
def SET_VIEW():

    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if version >= 11.0 and version <= 11.9:
        codename = 'Eden'
    elif version >= 12.0 and version <= 12.9:
        codename = 'Frodo'
    elif version >= 13.0 and version <= 13.9:
        codename = 'Gotham'
    elif version >= 14.0 and version <= 14.9:
        codename = 'Helix'
    elif version >= 15.0 and version <= 15.9:
        codename = 'Isengard'
    elif version >= 16.0 and version <= 16.9:
        codename = 'Jarvis'
    elif version >= 17.0 and version <= 17.9:
        codename = 'Krypton'
    else: codename = "Decline"
    
    if codename == "Jarvis":
        xbmc.executebuiltin('Container.SetViewMode(50)')
    elif codename == "Krypton":
        xbmc.executebuiltin('Container.SetViewMode(55)')
    else: xbmc.executebuiltin('Container.SetViewMode(50)')
        

def CLEANUP(text):

    text = str(text)
    text = text.replace('\\r','')
    text = text.replace('\\n','')
    text = text.replace('\\t','')
    text = text.replace('\\','')
    text = text.replace('<br />','\n')
    text = text.replace('<hr />','')
    text = text.replace('&#039;',"'")
    text = text.replace('&#39;',"'")
    text = text.replace('&quot;','"')
    text = text.replace('&rsquo;',"'")
    text = text.replace('&amp;',"&")
    text = text.replace('&#8211;',"&")
    text = text.replace('&#8217;',"'")
    text = text.replace('&#038;',"&")
    text = text.lstrip(' ')
    text = text.lstrip('	')

    return text


def GetMenu():

    url = base64.b64decode(b'aHR0cDovL2Jhc3Nmb3gub3JnLw==')
    link = open_url(url).replace('\n', '').replace('\r','').replace('\t','')
    match = re.compile ('<nav class="genres">(.+?)</nav>').findall(link)[0]
    grab = re.compile ('<a href="(.+?)" >(.+?)</a>.+?<i>(.+?)</i>').findall(match)
    iconimage = 'http://bassfox.org/wp-content/uploads/2017/05/icon.png'
    for url,title,num in grab:
        title = CLEANUP(title)
        addDir("[COLOR yellow]" + title + " :: " + num + "[/COLOR]",url,3,iconimage,fanart)
        
def GET_CONTENTS(url):

    link = open_url(url)
    match = re.compile ('<div class="poster">(.+?)<div class="texto">').findall(link)
    for links in match:
        title = re.compile ('</i>(.+?)</div>').findall(links)[0]
        icon = re.compile ('<img src="(.+?)"').findall(links)[0]
        url = re.compile ('<a href="(.+?)"').findall(links)[0]
        title = CLEANUP(title)
        addDir("[COLOR yellow]" + title  +"[/COLOR]",url,4,icon,fanart)
        
def GET_MOVIE_LINKS(url,iconimage):

    link = open_url(url)
    match = re.compile ('<div id="option-.+?"(.+?)</iframe>').findall(link)
    i = 0
    for links in match:
        url = re.compile ('src="(.+?)"').findall(links)[0]
        i += 1
        title = 'Link ' + str(i)
        addLink("[COLOR yellow]" + title  +"[/COLOR]",url,2,iconimage,fanart)
    
    
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

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: fanart=urllib.unquote_plus(params["fanart"])
except: pass
 
if mode==None or url==None or len(url)<1: GetMenu()

elif mode==1:GetContent(name,url,iconimage,fanart)
elif mode==2:PLAYLINK(name,url,iconimage)
elif mode==3:GET_CONTENTS(url)
elif mode==4:GET_MOVIE_LINKS(url,iconimage)



if mode==None or url==None or len(url)<1: xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
else: xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=True)

# dialog.ok("Debug", str (next_page))
# dialog.notification(AddonTitle, 'Sponsored By @Nemzzy668', xbmcgui.NOTIFICATION_INFO, 5000)