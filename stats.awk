#awk script to calculate and print distribution statistics on a list of numbers
#kudos to Mike Dierken for writing this
#usage example with random data:
# count:  10000
# sum:  2468147817
# average:  246815
# median:  183546
# 75%:  377520
# 90%:  580537
# 95%:  693844
# 99%:  839174
# 999%:  933372
BEGIN {
    sum = 0;
    num = 0;
}
{
    sum += $1;
    num += 1;
    stat[num] = $1;
}
END {
    n = asort(stat);

    print "count: ", num;
    print "sum: ", sum;
    print "average: ", sum/num;
    print "median: ", stat[int(n*.50)];
    print "75%: ", stat[int(n*.75)];
    print "90%: ", stat[int(n*.90)];
    print "95%: ", stat[int(n*.95)];
    print "99%: ", stat[int(n*.99)];
    print "99.9%: ", stat[int(n*.999)];
}
