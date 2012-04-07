import sys, os, re, xbmc, xbmcgui, xbmcaddon, xbmcplugin, urllib2

addon      = xbmcaddon.Addon(id='plugin.video.ziggo.tv')
version    = addon.getAddonInfo('version')
pluginpath = addon.getAddonInfo('path')
imagepath  = os.path.join(xbmc.translatePath(pluginpath),'resources','images')

def log(message):
  xbmc.log((u"### [%s-%s] - %s" % ('plugin.video.ziggo.tv', version, message,)).encode('utf-8'),level=xbmc.LOGDEBUG )

def additem(channel_id, title):
    url = 'http://webtv-rqr.ziggo.nl/' + channel_id + '.m3u8'
    try:
        response = urllib2.urlopen(url)
    except:
        log('Error connecting tot url: ' + url)
        ok = xbmcgui.Dialog().ok('Ziggo TV streams error', 'There was a problem connecting to Ziggo.', 'Debuglog has more info.')
    else:
        match = re.match('(http://.*/)', response.url)
        if match:
            urlstart = match.group(1)
            if 'x-mpegurl' in response.info().getheader('Content-Type'):
                content = response.read()
                bandwith = 0
                urlend = None
                for matches in re.finditer('#EXT-X-STREAM-INF:PROGRAM-ID=\d+,BANDWIDTH=(\d+)[\n\r]+([^\r\n]*?)[\n\r]+', content, re.IGNORECASE | re.DOTALL):
                    if int(matches.group(1)) > bandwith:
                        urlend = matches.group(2)
                if urlend:
                    streamurl= urlstart + urlend
                    log('Adding stream for ' + title + ': ' + streamurl)
                    listitem = xbmcgui.ListItem(title, thumbnailImage = os.path.join(imagepath,title + '.gif'))
                    xbmcplugin.addDirectoryItem(int(sys.argv[1]), streamurl, listitem, totalItems=12)
                else:
                    log('Unexpected format of "x-mpegurl" content received from url: ' +  response.url)
                    ok = xbmcgui.Dialog().ok('Ziggo TV streams error', 'Unexpected format of "x-mpegurl" (.m3u8) content.', 'Debuglog has more info.')
            else:
                log('No ''x-mpegurl'' content received from url: ' +  response.url)
                ok = xbmcgui.Dialog().ok('Ziggo TV streams error', 'No "x-mpegurl" content received.', 'Debuglog has more info.')
        else:
            log('No ''302'' redirection location received from url: ' + url)
            ok = xbmcgui.Dialog().ok('Ziggo TV streams', 'No "302" redirection location received.', 'Debuglog has more info.')

additem('Ned1', 'Nederland 1')
additem('Ned2', 'Nederland 2')
additem('Ned3', 'Nederland 3')
additem('RTL4', 'RTL 4')
additem('RTL5', 'RTL 5')
additem('SBS6', 'SBS 6')
additem('RTL7', 'RTL 7')
additem('Net5', 'Net 5')
additem('Vero', 'Veronica & Disney XD')
additem('RTL8', 'RTL 8')
additem('NGC',  'National Geographic')
additem('ESP',  'Eurosport')
xbmcplugin.endOfDirectory(int(sys.argv[1]))
