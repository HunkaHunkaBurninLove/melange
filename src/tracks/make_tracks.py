#!/usr/bin/env python3
"""
read csv file containing 'pings' and output 'tracks'

csv files must contain (at least) columns of timestamp, id, lat, lon

rows unsuccessfully parsed are dropped
"""

import bisect
import csv
import argparse
import dateutil.parser
import sys
import json
import logging
from collections import namedtuple, defaultdict

DEFAULT_COLUMNS = [ "ID",
                    "TIMESTAMP",
                    "LAT",
                    "LON" ]

Ping = namedtuple( "Ping", "id timestamp lat lon" )

def parse_row( row, columns=DEFAULT_COLUMNS ):
    """return a Ping from a row of the CSV file"""

    id, timestamp, lat, lon = columns
    try:
        ##
        timestamp = dateutil.parser.parse( row[timestamp] ).timestamp()
    except TypeError as err:
        logging.warning(err)
        try:
            ## already a unix timestamp?
            timestamp = float( row[timetstamp] )
        except Exception as e:
            raise e

    id = row[id]
    lat, lon = map( float, [ row[lat], row[lon] ] )

    return Ping( id, timestamp, lat, lon )

def add_ping_to_tracks( tracks, ping, dedupe=True ):
    """update tracks in place

    tracks: [ id: [ (t0,x0,y0), (t1,x1,y1), ...] ]
    ping: a Ping
    dedupe: ignore dupes if True
    """

    id = ping.id
    p = ping[1:]

    if tracks[id]:
        if dedupe:
            j = bisect.bisect_left( tracks[id], p )
            ## insert p if new
            if j == len(tracks[id]) or tracks[id][j] != p:
                tracks[id].insert( j, p )
        else:
            ## insert anyway
            bisect.insort_left( tracks[id], p )
    else:
        tracks[id] = [p]

def parse_args():
    """command-line parse"""

    parser = argparse.ArgumentParser( description=__doc__ )
    
    parser.add_argument( "infiles",
                         metavar="FILE",
                         nargs="*",
                         default=[sys.stdin],
                         type=argparse.FileType("r"),
                         help="file(s) to ingest [default= STDIN]" )

    parser.add_argument( "-o", "--outfile",
                         dest="outfile",
                         default=sys.stdout,
                         type=argparse.FileType("w"),
                         help="output file [default= STDOUT]" )

    parser.add_argument( "-c", "--columns",
                         dest="columns",
                         default=DEFAULT_COLUMNS,
                         help=( "comma-separated list of index numbers " +
                                "(0-based) or names; need to extract " +
                                "ID, TIMESTAMP, LAT, LON (in that order); " +
                                "default= " + ','.join(DEFAULT_COLUMNS) ) )

    args = parser.parse_args()

    if args.columns != DEFAULT_COLUMNS:
        args.columns = [ c.strip() for c in args.columns.split(",") ]
        assert len(args.columns) == 4
    return args

if __name__ == "__main__":
    """doc here"""

    args = parse_args()

    loglevel = loggin.INFO
    logging.basicConfig( level=loglevel,
                         format=( "%(created)d: %(levelname)s: %(filename)s: " +
                                  "%(lineno)3d: %(message)s" ),
                         style="%" )
    logging.info( "reading inputs" )

    rows_read = 0
    rows_skipped = 0
    tracks = defaultdict(list)
    ## { id: [ (t,x,y), (t,x,y), ... ] }
    
    ## args.infiles is a list of open filehandles
    for fd in args.infiles:
        reader = csv.DictReader(fd)
        for row in reader:
            rows_read += 1
            try:
                ping = parse_row( row, columns=args.columns )
            except Exception as e:
                logging.debug( str(e) + " for row " + str(rows_read) +
                               ": " + row )
                rows_skipped += 1
                continue
            add_ping_to_tracks( tracks, ping )

    logging.info( "read " + str(rows_read) + " from " +
                  str(len(args.infiles)) + " rows" )
    logging.info( "failed to parse " + str(rows_skipped) + " rows" )
    logging.info( "made tracks for " + str(len(tracks)) )

    ## write tracks to JSON
    logging.info( "writing tracks to " + args.outfile.name )

    tracks_json = json.dumps(tracks)

    args.outfile.write(tracksd_json)

    ## clean exit
    logging.info( "end" )
    sys.exit(0)

    
                
