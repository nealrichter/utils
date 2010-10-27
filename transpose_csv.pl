#! /usr/bin/perl

###################################################################################################
#
#	 AUTHOR:  Ryan M. Castillo
#    VERSION: Version 1 (04 January 2007)
#    PURPOSE: Transpose a comma seperated values file
#    INPUT: user specified file
#    OUTPUT FILES: tr_<Name of File>
#
# Copyright Notice:
#
# Copyright 2007 Ryan Castillo
#
#  This program is free software; you can redistribute it and/or 
#  modify it under the terms of the GNU General Public License as 
#  published by the Free Software Foundation; either version 2 of 
#  the License, or any later version.
#
#  This program is distributed in the hope that it will be useful, 
#  but WITHOUT ANY WARRANTY; without even the implied warranty of 
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
#  See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License 
#  along with this program; if not, write to theim
#         Free Software Foundation, Inc., 
#         59 Temple Place, Suite 330, Boston, MA  
#         02111-1307  USA 
#  or visit http://www.gnu.org/copyleft/gpl.html
#
#  Changes:
#    4/2/2009 Neal Richter - read and write from stdin/stdout
#
###################################################################################################

my $input_path = $ARGV[0];

#### OPEN OUR INPUT & OUTPUT FILES
if(length($input_path > 0))
{
   open INPUT_FILE, "<$input_path"
	or die "Something's wrong with the input file!\n";

   my $output_path = "tr_$input_path";
   open OUTPUT_FILE, ">$output_path" 
	or die "Can't open $output_path: $!\n";

}
else
{
  *INPUT_FILE = *STDIN;
  *OUTPUT_FILE = *STDOUT;
}

my $line = <INPUT_FILE>;						# holds the current line from the input file
my @AoA;								# array that will be an array of arrays

while (defined $line){
	chomp $line;
	push @AoA, [split /\,/, $line];
	$line = <INPUT_FILE>;
}

close INPUT_FILE;

for $i (0 ... $#{$AoA[0]}){
	for $j (0 ... $#AoA){
		if ($j == $#AoA){
			print OUTPUT_FILE "$AoA[$j][$i]\n";
		}
		elsif ($AoA[$j][$i] eq ""){
			print OUTPUT_FILE "\n";
			last;
			}
		else{
			print OUTPUT_FILE "$AoA[$j][$i]\,";
		}
	}
	if ($AoA[$j][$i] eq "") {last;}
}
close OUTPUT_FILE;
