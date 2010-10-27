#!/bin/sh

curl -b /tmp/cookieJarIE7 -c /tmp/cookieJarIE7 -v -A 'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)' -H 'Accept: text/html,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-us,en;q=0.5'   -H 'Accept-Encoding: gzip,deflate'   -H 'Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7' -H 'Keep-Alive: 300'     -H 'Connection: keep-alive'    -H 'Cache-Control: max-age=0' --referer $2 $1

