#!/usr/bin/python2

# Ben Formosa 2016-06-18
"""
Passes your HTTP_PROXY environment variable to docker.
Converts hostnames to IPs so you don't have to configure DNS on your image.
"""

import os
import sys
from socket import gethostbyname
from urlparse import urlparse
from subprocess import call

# Docker commands and their respective argument for environment variables
docker_commands = {
        'build': '--build-arg',
        'run': '--env',
        }

# The environment variables to set
env_vars = (
        'HTTP_PROXY',
        'HTTPS_PROXY',
        'FTP_PROXY',
        'http_proxy',
        'https_proxy',
        'ftp_proxy',
        )

# Print usage
if (set(['--help', '-h']).intersection(sys.argv)) or (len(sys.argv) <= 1):
    print 'usage: docker_proxy.py [{}] ...'.format('|'.join(docker_commands.keys()))
    print 'use in place of `docker` for selected commands.'
    sys.exit(0)

# Set docker command and check if supported
subcommand = sys.argv[1]
if subcommand not in docker_commands.keys():
    print 'Unsupported docker subcommand. Please use one of: ' + ' '.join(docker_commands.keys())
    sys.exit(1)

command = ['docker', subcommand]

# Get the proxy from environment variables
proxy = os.getenv('HTTP_PROXY', "")
if not proxy:
    proxy = os.getenv('http_proxy', "")

proxy_args = []

if proxy:
    o = urlparse(proxy)

    # Split the host:port part, convert to an IP and put it back together
    host = gethostbyname(o.netloc.split(':')[0])
    port = o.netloc.split(':')[1]
    netloc = '{}:{}'.format(host, port)

    # Overwrite the URL with the converted IP
    proxy = o._replace(netloc=netloc).geturl()

    # Set all the arguments
    for env in env_vars:
        proxy_args.append('{}={}={}'.format(docker_commands[subcommand], env, proxy))

else:
    print 'HTTP_PROXY and HTTP_PROXY are not set.'

command = (command + proxy_args + sys.argv[2:])
print ' '.join(command)
call(command)
