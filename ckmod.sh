#!/bin/sh
# http://forums.devshed.com/unix-help-35/how-to-check-chmod-of-a-file-directory-203403.html
ls -ld $* | awk 'BEGIN {
    v["r1"]=400; v["w2"]=200; v["x3"]=100; v["s3"]=4100; v["S3"]=4000
    v["r4"]=40 ; v["w5"]=20 ; v["x6"]=10 ; v["s6"]=2010; v["S6"]=2000
    v["r7"]=4  ; v["w8"]=2  ; v["x9"]=1  ; v["t9"]=1001; v["T9"]=1000}
    { val=0
      for (i=1;i<=9;i++) val=val+v[substr($0,i+1,1)i]
          printf "%4d %s\n",val,$NF
    }'
