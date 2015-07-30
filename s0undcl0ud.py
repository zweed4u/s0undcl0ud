import mechanize
import urllib
import cookielib
import BeautifulSoup
import html2text
import re
import sys
import json


#prompt for song name and author and best guess download
print '\nPlease enter a Soundcloud track URL: '

soundURL = raw_input('')
print ""

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(False)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Chrome')]

try:
	br.open(soundURL)
        #br.select_form(nr=0)
    
	#scrape page for anything jsonUrl
        regex='<meta name="twitter:audio:source" content=(.+?)>'
        pattern = re.compile(regex)
        htmltext = br.open(soundURL).read()
        jsonURL = re.findall(pattern,htmltext)
	jsonURL = jsonURL[0].split('"')[1]
	
	try:
		response = urllib.urlopen(jsonURL)
		data = json.loads(response.read())
		#print data.values()
		pageData = data.values()
		print "Title: " +  pageData[0][0][u'title'].encode('ascii','ignore')
		
		print "Unique track id: " + pageData[1].encode('ascii','ignore').split('tracks:')[1]
		

		#prompt for which format should be used
		
		print "Downloading your song...\n"
		#hls bitrate (m3u8) url
		#pageData[0][0][u'sources'][0][u'url'].encode('ascii','ignore')


		#progressive bitrate (mp3) url
		#get current folder and make a songs directory
		#name mp3
		urllib.urlretrieve(pageData[0][0][u'sources'][1][u'url'].encode('ascii','ignore'), "/home/zack/Desktop/s0undcl0ud/1.mp3")

		#saved to current directory/var uinstead of fixed string
		print "Download complete! Saved to: /home/zack/Desktop/s0undcl0ud/1.mp3\n"
	except:
		print "Can't open json page\n"


except:
	print "Tags Not Found!!! \n"




