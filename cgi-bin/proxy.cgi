#!"c:\Python27\python.exe"


"""This is a blind proxy that we use to get around browser
restrictions that prevent the Javascript from loading pages not on the
same server as the Javascript.  This has several problems: it's less
efficient, it might break some sites, and it's a security risk because
people can use this proxy to browse the web and possibly do bad stuff
with it.  It only loads pages via http and https, but it can load any
content type. It supports GET and POST requests."""

import urllib2
import cgi
import sys
import os


# Designed to prevent Open Proxy type stuff.
# Adapted from original version from openlayers.org

# Add your domains to be proxied here.
# Do this only if you trust the entire domain, for any subdomain!
allowedDomains = [
'lsagis.net'
'google.com'
	'52.40.78.184',
	'52.40.78.184:80',
	'172.31.29.34',
    '228.72',   #  129.206.228.72 is watzmann-geog.urz.uni-heidelberg.de
    'alterra.nl',
    'atlasleefomgeving.nl',
    'demis.nl',
    'boundlessgeo.com',
    'dinonet.nl',
    'dinoservices.nl',
    'drenthe.info',
    'fao.org',
    'fi-ware.org',
    'fryslan.nl',
    'geonovum.nl',
    'gov.uk',
    'hansjebrinker.com',
    'heron-mc.org',
    'iastate.edu',
    'inspire-provincies.nl',
    'geodan.nl',
    'kademo.nl',
    'kich.nl',
    'knmi.nl',
    'ma.us',
    'mapquestapi.com',
    'nationaalgeoregister.nl',
    'nlr.nl',
    'nasa.gov',
    'opengeo.org',
    'opentraces.org',
    'pdok.nl',
    'provinciaalgeoregister.nl',
    'provinciegroningen.nl',
    'ruimtelijkeplannen.nl',
    'rwsgeoweb.nl',
    'zuid-holland.nl'
    'sara.nl',
    'tno.nl',
    'ucdavis.edu',
    'sensors.geonovum.nl',
    'zeeland.nl'
]

# Add to have specific hosts, mostly IP-addresses
allowedHosts = [
	'52.40.78.184',
	'52.40.78.184:80',
    '144.76.93.238',
	'172.31.28.34'
]

method = os.environ["REQUEST_METHOD"]

# Fetch the url query param
if method == "POST":
    qs = os.environ["QUERY_STRING"]
    d = cgi.parse_qs(qs)
    if d.has_key("url"):
        url = d["url"][0]
    else:
        url = "http://www.openlayers.org"
else:
    fs = cgi.FieldStorage()
    url = fs.getvalue('url', "http://www.openlayers.org")

try:
    # Gives: www.openlayers.org
    host = url.split("/")[2].split(':')[0]

    # Gives: openlayers.org
    domain = '.'.join(host.split(".")[-2:])

    if (allowedDomains and domain not in allowedDomains) and (allowedHosts and not host in allowedHosts):
        print "Status: 502 Bad Gateway"
        print "Content-Type: text/plain"
        print
        print "Blocked access to host/domain: %s/%s" % (host, domain)
        print
        print os.environ

    elif url.startswith("http://") or url.startswith("https://"):
        headers = {}

        if os.environ.get("HTTP_ACCEPT"):
            headers['Accept'] = os.environ["HTTP_ACCEPT"]
        if os.environ.get("HTTP_FIWARE_SERVICE"):
            headers['FIWARE-Service'] = os.environ["HTTP_FIWARE_SERVICE"]
            if os.environ.get("HTTP_FIWARE_SERVICEPATH"):
                headers['FIWARE-Servicepath'] = os.environ["HTTP_FIWARE_SERVICEPATH"]
            if os.environ.get("HTTP_X_AUTH_TOKEN"):
                headers['X-FI-WARE-OAuth-Header-Name'] = 'X-Auth-Token'
                headers['X-FI-WARE-OAuth-Token'] = 'true'
                headers['X-Auth-Token'] = os.environ.get("HTTP_X_AUTH_TOKEN")

        if method == "POST":
            length = int(os.environ["CONTENT_LENGTH"])
            headers['Content-Type'] = os.environ["CONTENT_TYPE"]

            body = sys.stdin.read(length)
            r = urllib2.Request(url, body, headers)
            y = urllib2.urlopen(r)
        else:
            r = urllib2.Request(url, headers=headers)
            y = urllib2.urlopen(r)

        # print content type header
        i = y.info()
        if i.has_key("Content-Type"):
            print "Content-Type: %s" % (i["Content-Type"])
        else:
            print "Content-Type: text/plain"

        if i.has_key("Content-Disposition"):
            print "Content-Disposition: %s" % (i["Content-Disposition"])

        print
        # print str(os.environ)
        print y.read()

        y.close()
    else:
        print "Content-Type: text/plain"
        print
        print "proxy.cgi: illegal proxy request."

except Exception, E:
    print "Status: 500 Unexpected Error"
    print "Content-Type: text/plain"
    print
    print "proxy.cgi: some unexpected error occurred. Error text was:", E