#!/usr/bin/perl -w

# Author:  Neal Richter nrichter - gmail.com
# simple system load generator in perl, uses recursive fibonacci to keep CPUs busy
# Yes there are two layers or recursion going on here
# 10/28/2010 - Intial version

# NOTE:  This program uses non-blocking system calls.  If you want to kill the child processes, use killall


use strict;
no warnings 'recursion';
use POSIX;
use Getopt::Long qw(GetOptions);

my $procs;
my $fn;

GetOptions('procs=s' => \$procs, 'fn=s' => \$fn);

die "Usage $0 --procs [number] --fn [number]\n\n" 
  unless defined $procs && defined $fn;

sub fibonacci
{
    my $index = shift;

    return 0 if $index == 0;
    return 1 if $index == 1;

    return fibonacci( $index - 1 ) + fibonacci( $index - 2 );
}


if (($procs == 0) || ($procs == 1))
{

    print "starting process $$\n";
    my $val = fibonacci($fn);
    print "process $$ = $val\n";
}
else
{
    my $procs_new = $procs - 1;
    system("$0 --procs $procs_new --fn $fn &");

    $procs_new = $procs - 2;
    system("$0 --procs $procs_new --fn $fn &");
}
