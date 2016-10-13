import json
import urllib2

HTTPError = urllib2.HTTPError
URLError = urllib2.URLError

def post_json(url, data):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')

    return urllib2.urlopen(req, json.dumps(data))

def get_json(url):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req)

    return json.load(response)
