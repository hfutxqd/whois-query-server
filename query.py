#!/usr/bin/env python3

# -*- coding: utf-8 -*-
import datetime
import socket
import json
import re
from parser import WhoisEntry

BUFF_SIZE = 64 * 1024  # 64 KiB

f = open('servers.json')
servers = json.loads(f.read())
f.close()


def decode_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return int(obj.timestamp())


def parse_raw(domain, data):
    return json.dumps(WhoisEntry.load(domain, data), ensure_ascii=False, default=decode_datetime)


def get_top_domain(domain):
    parts = domain.split('.')
    top = 'com'
    for i in range(len(parts) - 1):
        top = '.'.join(parts[i + 1:])
        if top in servers:
            domain = '.'.join(parts[i:])
            break
        else:
            # 查询后缀是否都在顶级域名中
            can_query = True
            for item in parts[i + 1:]:
                if item not in servers:
                    can_query = False
                    break
                pass
            if can_query:
                top = '.'.join(parts[-1:])
                domain = '.'.join(parts[i:])
                return top, domain
        pass
    return top, domain


def send_resquest(server, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(30)
        s.connect((server, port))
        s.sendall(bytes(data, 'utf-8'))
        data = b''
        try_count = 3
        while True:
            part = s.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                try_count -= 1
                if try_count <= 0:
                    break
    response = str(data, 'utf8')
    return response

def query_whois_server(top):
    server = "whois.iana.org"
    response = send_resquest(server, 43, top + '\r\n')
    matcher = re.search('whois:\s*(.+)', response)
    if matcher:
        print(matcher.group(1))
        return matcher.group(1)
    else:
        return None
    pass


def query(domain, raw=False, recursive=True, query_server=None):
    top, domain = get_top_domain(domain)
    if query_server is None:
        if top in servers:
            query_server = servers[top]
        else:
            query_server = query_whois_server(domain)
            if query_server:
                servers[top] = query_server

    if query_server is None:
        print('*.{} is not supported!'.format(top))
        return '*.{} is not supported!'.format(top)

    print('query ' + domain)
    print('querying on ' + query_server + ' ...')

    response = response = send_resquest(query_server, 43, domain + '\r\n')
    # print(response)
    whois_entry = WhoisEntry.load(domain, response)
    whois_entry['query_from'] = query_server

    if raw:
        result = response
    else:
        result = json.dumps(whois_entry, ensure_ascii=False, default=decode_datetime)

    if not recursive:
        return result

    if whois_entry.get('whois_server', None) is not None and recursive and whois_entry['whois_server'] != query_server:
        tmp = query(domain, True, False, whois_entry['whois_server'])
        whois_tmp = WhoisEntry.load(domain, tmp)
        whois_tmp['query_from'] = whois_entry['whois_server']
        if whois_tmp.get('domain_name', None) is None:
            print('parse whois data error.')
            return result
        else:
            if raw:
                return response
            else:
                return json.dumps(whois_tmp, ensure_ascii=False, default=decode_datetime)
    else:
        return result


# domain = 'www.hfut.ca.cn'
# print(get_top_domain(domain))
#
# domain = 'www.baidu.edu.cn'
# print(get_top_domain(domain))
#
# domain = '我爱你.中国'
# print(get_top_domain(domain))