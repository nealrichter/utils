#!/usr/bin/perl -w

# Author:  Neal Richter nrichter - gmail.com
# simple memcached cli using only the ascii API, echo & netcat
# 10/26/2010 - Intial version with get/set/delete/stats

use strict;
use POSIX;
use Getopt::Long qw(GetOptions);

my $cmd;
my $key;
my $value;
my $host;
my $port;
my $value_len;

GetOptions('cmd=s' => \$cmd, 'key=s' => \$key, 'value=s' => \$value, 'host=s' => \$host, 'port=s' => \$port);

die "Usage $0 --host [host name/ip] --port [port number] --cmd [memcached command] --key [the key] (optional) --value [the value] (optional)\n\n" 
  unless defined $cmd && defined $host && defined $port;


if ($cmd eq 'stats')
{
    system("echo \"stats\\nquit\"  | nc -q2 $host $port");
}
elsif ($cmd eq 'set')
{
    die unless defined $key && defined $value;
    $value_len = length($value);
    system("echo \"set $key 0 2592000 $value_len\r\n$value\r\nquit\" | nc -q2 $host $port");
}
elsif ($cmd eq 'get')
{
    die unless defined $key;
    system("echo \"get $key\r\nquit\" | nc -q2 $host $port");
}
elsif ($cmd eq 'delete')
{
    die unless defined $key;
    system("echo \"delete $key\r\nquit\" | nc -q2 $host $port");
}
elsif ($cmd eq 'flush_all')
{
    system("echo \"flush_all\\nquit\"  | nc -q2 $host $port");
}
else
{
    print "Error: $cmd not supported by this utility.";
    print "  supports:  get, set, delete, stats, flush_all";
    print "  memcache command manual is here: http://lzone.de/articles/memcached.htm";
    print "  try telnet";
}


