#!/usr/bin/python2

# Ben Formosa 2016-06-18
"""
Specify proxy build args to docker build based on environment variables.
Converts hostnames to IPs so you don't have to configure DNS on your image.
"""

import os
import sys
from socket import gethostbyname
from urlparse import urlparse
from subprocess import call

proxy = os.getenv('HTTP_PROXY', "")
if(proxy == ""):
  proxy = os.getenv('http_proxy', "")

command = ['docker', 'build']
proxy_args = []

if proxy:
  o = urlparse(proxy)

  # Split the host:port part, convert to an IP and put it back together
  host = gethostbyname(o.netloc.split(':')[0])
  port = o.netloc.split(':')[1]
  netloc = '{}:{}'.format(host, port)

  # Overwrite the URL with the converted IP
  proxy = o._replace(netloc=netloc).geturl()

  proxy_args.append('--build-arg=HTTP_PROXY={}'.format(proxy))
  proxy_args.append('--build-arg=HTTPS_PROXY={}'.format(proxy))
  proxy_args.append('--build-arg=http_proxy={}'.format(proxy))
  proxy_args.append('--build-arg=https_proxy={}'.format(proxy))

command = (command + proxy_args + sys.argv[1:])
print str(command)
call(command)
