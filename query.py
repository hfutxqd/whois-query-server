#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import socket
import json
import re

f = open('servers.json')
servers = json.loads(f.read())
f.close()


def query_whois_server(top):
    server = "whois.iana.org"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(30)
        s.connect((server, 43))
        s.sendall(bytes(top + '\r\n', 'utf-8'))
        data = s.recv(16 * 1024)
    response = str(data, 'utf8')
    matcher = re.search('whois:\s*(.+)', response)
    if matcher:
        print(matcher.group(1))
        return matcher.group(1)
    else:
        return None
    pass


def query(domain):
    top = domain[domain.rfind('.') + 1:]

    if top in servers:
        query_server = servers[top]
    else:
        query_server = query_whois_server(top)
        servers[top] = query_server

    if query_server is None:
        print('*.{} is not supported!'.format(top))
        return '*.{} is not supported!'.format(top)

    print('query ' + domain)
    print('querying on ' + query_server + ' ...')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(30)
        s.connect((query_server, 43))
        s.sendall(bytes(domain + '\r\n', 'utf-8'))
        data = s.recv(16 * 1024)

    response = str(data, 'utf8')
    print(response)
    return response


# domain = '导航.中国'
# query(domain)
