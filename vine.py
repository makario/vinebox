import urllib2
import os
import datetime
import json
import time
from filelock import FileLock

# max number of files to download
MAX_CACHE = 100 

VIDEO_DIR = os.getenv('HOME') + os.sep + ".vine"
LOG_LAST_UPDATE = VIDEO_DIR + os.sep + "last_updated.txt"

FETCH_DELAY_SEC = 10

FETCH_URL_BASE = "http://search.twitter.com/search.json?q=vine.co&rpp=100"

def download(url, dest):
   stream = urllib2.urlopen(url)
   content = stream.read()
   stream.close()
   file = open(dest, 'wb')
   file.write(content)
   file.close

def get_redirected_url(url):
   opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
   request = opener.open(url)
   return request.url

def getResults(since=None, num=0):
   if since: print "Getting search results since last_id: " + since
   else: print "Gettings search results..."

   if since:
      search = FETCH_URL_BASE + '&since_id=' + since
   else:
      search = FETCH_URL_BASE
   request = urllib2.urlopen(search)
   results = request.read()
   request.close()

   j = json.loads(results)
   tweets = j['results']
   since = j['max_id_str']

   for tweet in tweets:
      try:
	      text = tweet['text']
	      start = text.find('http://t.co')
	      end = start + 21 # as of now all t.co urls are 21 in length
	      url = text[start:end+1]
	      real_url = get_redirected_url(url)
	
	      conn = urllib2.urlopen(real_url)
	      body = conn.read()
	      start = body.find('<source src="') + len('<source src="')
	      end = body.find('" type="video/mp4"', start)
	      video_url = body[start:end]
              basename = "%s%s%03d" % (VIDEO_DIR, os.sep, num)
	      print "Downloading to", basename + ".mp4", "...",
              with FileLock(basename):
                 download(video_url, basename + ".mp4")
	      print "done."

	      log = open(basename + ".vlog", 'w')
	      log.write("@%s: " % tweet['from_user'])
	      log.write(text.encode('ascii', 'ignore').strip() + "\n")
	      created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a, %d %b %Y %H:%M:%S +0000'))
	      log.write("Created at %s\n" % created_at)
	      log.close()

	      num = (num + 1) % MAX_CACHE
	      
      except:
         pass

   f = open(LOG_LAST_UPDATE, "w")
   now = datetime.datetime.now()
   f.write(since + "\n")
   f.write("Last updated: %s" % now.strftime("%Y-%m-%d %H:%M:%S"))
   f.close()
   return since, num
   
   
since = None
num = 0	

if os.path.exists(LOG_LAST_UPDATE):
	f = open(LOG_LAST_UPDATE, 'r')
	since = f.readline()
        os.remove(LOG_LAST_UPDATE)

if not os.path.exists(VIDEO_DIR):
	os.makedirs(VIDEO_DIR)


while num < MAX_CACHE: # this should loop forever since num always > MAX_CACHE
   since, num = getResults(since=since, num=num)
   time.sleep(FETCH_DELAY_SEC)
