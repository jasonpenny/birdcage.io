import json
import urllib2

HTTPError = urllib2.HTTPError

def post_json(url, data):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')

    return urllib2.urlopen(req, json.dumps(data))
