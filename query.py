#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import socket
import json

f = open('servers.json')
servers = json.loads(f.read())
f.close()


def query(domain):
    top = domain[domain.rfind('.') + 1:]

    if top in servers:
        query_server = servers[top]
    else:
        query_server = "whois.internic.net"

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


# domain = 'xqd.one'
# query(domain)
