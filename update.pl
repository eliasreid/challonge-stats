#!/usr/bin/perl

##
## update.pl
## by Naomi Peori (naomi@peori.ca)
##

use strict;
use warnings;

use JSON;
use Data::Dumper;

use Chess::Elo qw(:all);

##
## Configuration
##

my $csvFile = "matches.csv";

my $eloDefault = 1200;

my %eloOverride =
(
#  'SFV: Season 2' => { 'OneEyedJack' => 1600 }
);

my %seasons =
(
  'Tekken 7: Season 1' => [ "2018-08-28", "2018-09-04","2018-09-27","2018-10-11","2018-10-18","2018-10-25","2018-11-01", "2018-12-06","2018-12-13"],
  'Tekken 7: Season 2' => [ "2019-01-03","2019-01-17","2019-01-24","2019-01-31","2019-02-07","2019-02-28","2019-03-07","2019-03-14","2019-03-21","2019-03-28"],
);

my %aliases =
(
  'SmithSyn' => ["Smithsyn"],
  'Shleepy'           => [ "Shleeepy" ],
  'SS-Gangsta'           => [ "SSGangsta" ],
  'Elray'    => ["elray", "El-Ray", "El-ray" ],
  'Dru-Gatti'  => [ "PromiseFace", "Drugatti", "Dru-gatti" ],
);

##
## Parse the data files.
##

if ( ! open OUTFILE, "> $csvFile" )
{
  print "ERROR: Could not open CSV file for output. ($csvFile)\n";
}
else
{
  foreach my $season ( sort keys %seasons )
  {
    my %eloPrevious = ( );
    my %eloCurrent  = ( );

    foreach my $event ( sort @{$seasons{$season}} )
    {
      @eloPrevious{ sort keys %eloPrevious } = @eloCurrent{ sort keys %eloCurrent };

      if ( ! open INFILE, "< $event.json" )
      {
        print "ERROR: Could not open JSON file for input. ($event.json)\n";
      }
      else
      {
        my $fileData = <INFILE>;
        close INFILE;

        my $jsonData = decode_json ( $fileData );

        #JSON from challonge stores player IDs (generated per event I'm guessing), rather than player names
        #so, need to create a hash to map IDs to names
        my %IDtoName = ();
        foreach my $player ( @{$jsonData->{tournament}{participants}} )
        {   
          $IDtoName{$player->{participant}{id}} = $player->{participant}{name};
        }

        foreach my $match ( @{$jsonData->{tournament}{matches}} )
        {
          if ($match->{match}{winner_id} != "null")
          {

            my $winner = $IDtoName{$match->{match}{winner_id}};
            my $loser  = $IDtoName{$match->{match}{loser_id}};

            foreach my $alias ( keys %aliases )
            {
              if ( $winner ~~ $aliases{$alias} ) { $winner = $alias };
              if ( $loser  ~~ $aliases{$alias} ) { $loser  = $alias };
            }

            if ( ! exists $eloPrevious{$winner} ) { $eloPrevious{$winner} = exists $eloOverride{$season}{$winner} ? $eloOverride{$season}{$winner} : $eloDefault; }
            if ( ! exists $eloPrevious{$loser}  ) { $eloPrevious{$loser}  = exists $eloOverride{$season}{$loser}  ? $eloOverride{$season}{$loser}  : $eloDefault; }

            if ( ! exists $eloCurrent{$loser}  ) { $eloCurrent{$loser}  = $eloPrevious{$loser};  }
            if ( ! exists $eloCurrent{$winner} ) { $eloCurrent{$winner} = $eloPrevious{$winner}; }

            my @results = elo ( $eloPrevious{$winner}, 1, $eloPrevious{$loser} );
            my $eloChange = $results[ 0 ] - $eloPrevious{$winner};

            $eloCurrent{$winner} += $eloChange;
            $eloCurrent{$loser}  -= $eloChange;

            print OUTFILE "$season,$event,$winner,$eloPrevious{$winner},$loser,$eloPrevious{$loser},$eloChange\n";
          }
        }
      }
    }


    #actually, want to do this within season - what variables do I have access to?

    #these
    #my %eloPrevious = ( );
    #my %eloCurrent  = ( );

    @eloPrevious{ sort keys %eloPrevious } = @eloCurrent{ sort keys %eloCurrent };

    #ok, now everyone should be up to date in eloPrevious hash - print it out

    # foreach my $player ( keys %eloPrevious )
    # {
    #   print OUTFILE "$season,$player,$eloPrevious{$player}\n";
    # }

    foreach my $player (sort{$eloPrevious{$b} <=> $eloPrevious{$a}} keys %eloPrevious)
    {
      print OUTFILE "$season,$player,$eloPrevious{$player}\n";
    }

  }

  close OUTFILE;
}
