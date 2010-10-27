#!/bin/sh

curl -b /tmp/cookieJarSafari -c /tmp/cookieJarSafari -v -A 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_4; en-us) AppleWebKit/528.4+ (KHTML, like Gecko) Version/4.0dp1 Safari/526.11.2' -H 'Accept: text/html,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-us,en;q=0.5'   -H 'Accept-Encoding: gzip,deflate'   -H 'Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7' -H 'Keep-Alive: 300'     -H 'Connection: keep-alive'    -H 'Cache-Control: max-age=0' --referer $2 $1
