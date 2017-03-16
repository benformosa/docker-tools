#!/usr/bin/perl

use strict;
use warnings;

my @list = (
    'Docker version 0.2',
    'Docker version 1.5',
    'Docker version 1.6',
    'Docker version 17.03.0-ce, build 60ccb22',
    'Docker version 20.12.9-pe'
);

foreach my $var (@list) {
    print $var, " \t ====> ", version_gt_1point6($var), "\n";
}

# returns 1 if Docker version is greater than or equal to 1.6
sub version_gt_1point6 {
    my $input = shift(@_);
    $input =~ s/Docker version (\d{1,2}\.\d{1,2})/$1/;
    my($major, $minor) = split(/\./, $input, 2);

    if($major >= 17) {
        return 1;
    } elsif($major == 1) {
        if($minor >= 6) {
            return 1;
        }
    }
    return 0;
}
