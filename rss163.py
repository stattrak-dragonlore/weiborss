#  encoding: utf-8
from time import gmtime, strftime, time
from django.utils import simplejson as json
from google.appengine.api.urlfetch import fetch
from google.appengine.ext import webapp


def fetch_tweets(user, since_timeline=None):
    since_id = ""
    time_since = ""
    if since_timeline:
        since_id = since_timeline['id']
        time_since = since_timeline['time']
    url = "http://t.163.com/statuses/user_timeline/%s.json?since_id=%s&timeSince=%s&enableEmotions=1" % (user, since_id, time_since)
    res = fetch(url)
    if res.status_code != 200:
        return False
    if not res.content.startswith('[{"user":'):
        return False
    return res.content


def genrss_item(user, tweet):
    text = tweet['text']
    link = "http://t.163.com/" + user + '/status/' + tweet['id'];
    pubDate = strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime(long(tweet['timeline']['time'])/1000))
    if tweet['user']['screen_name'] != user:
        text = ("RT: @%s: " % tweet['user']['name']) + text
    else:
        text = "%s: " % tweet['user']['name'] + text
    if tweet['rootReplyUserName']:
        text = text + " ||@%s :%s" % (tweet['rootReplyUserName'], tweet['rootReplyText'])
    return u"""       <item>
          <title>%s</title>
          <description>%s</description>
          <link>%s</link>
          <pubDate>%s</pubDate>
          <guid isPermaLink=\"true\">%s</guid>
       </item>
""" % (text, text, link, pubDate, link)


class Rss163(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain; charset=utf-8'

        user = self.request.path[5:]

        header = u"""<?xml version="1.0" encoding="utf-8" ?>
<rss version="2.0">
  <channel>
     <title>t.163.com/%s</title>
     <link>http://t.163.com/%s</link>
     <description>t.163.com/%s</description>
     <lastBuildDate>%s</lastBuildDate>
     <ttl>30</ttl>
""" % (user, user, user, strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()))
        self.response.out.write(header)

        MAX_REQ = 1
        i = 0
        last_timeline = None
        while i < MAX_REQ:
            content = fetch_tweets(user, last_timeline)
            if content:
                tweets = json.loads(content)
                for t in tweets:
                    self.response.out.write(genrss_item(user, t))
                    last_timeline = t['timeline']
                i += 1
            else:
                break

        footer = u"""
  </channel>
</rss>
"""
        self.response.out.write(footer)

