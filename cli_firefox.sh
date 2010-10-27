#!/bin/sh

set -x

curl -b /tmp/cookieJarFirefox3 -c /tmp/cookieJarFirefox3 -v -A 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.13) Gecko/2009080315 Ubuntu/9.04 (jaunty) Firefox/3.0.13' -H 'Accept: text/html,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-us,en;q=0.5'   -H 'Accept-Encoding: gzip,deflate'   -H 'Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7' -H 'Keep-Alive: 300'     -H 'Connection: keep-alive'    -H 'Cache-Control: max-age=0' --referer $2 $1

