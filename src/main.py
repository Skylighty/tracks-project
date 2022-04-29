from sqlite3 import connect as sqlcon
from time import time
import parser
import csv

# Decorator for function execution to stdout
def timing(func):
    # This function shows the execution time of 
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function: {func.__name__!r} executed in: {(t2-t1):.4f}s')
        return result
    return wrap_func


# Create sqlite 3 database function
@timing
def create_db(dbpath):
    sqlt = sqlcon(dbpath)
    sqlc = sqlt.cursor()
    sqlc.execute('''
                 CREATE TABLE tracks (
                     sid INT PRIMARY KEY,
                     pid INT,
                     title VARCHAR(255),
                     artist VARCHAR(255),
                     listened INT
                     
                 )
                 ''')
    return sqlt, sqlc



# Files format
# triplets - UserID - TrackID - ListenDate - LF
# uniquie tracks - PerfID-TrackID-Artist-Title-LF
# !!! INPUT FORMAT - TrackID - Artist - Title - Listen#
# Process triplets to dictionary: {<str>'TrackID' : <int>#-of-plays}
@timing
def process_trips(trips_path):
    trackid_count = {}
    # Well done!
    with open(trips_path, 'r', encoding='iso8859', errors='') as tfile:
        for line in tfile:
            splitted = line.rstrip()
            splitted = splitted.split('<SEP>')
            if splitted[1] in trackid_count.keys():
                trackid_count[str(splitted[1])] += 1
            else:
                trackid_count[str(splitted[1])] = 1
        #trackid_count = dict(sorted(trackid_count.items(), key=lambda item: item[1]))
        return trackid_count
    # TEST PRINT print(trackid_count)

@timing
def process_songs(uniqs_path, kvtracks):
    sortd = []
    with open(uniqs_path, 'r', encoding='iso8859', errors='') as ufile:
        for line in ufile:
            splitted = line.rstrip()
            splitted = splitted.split('<SEP>')
            splitted.pop(0)
            if splitted[0] in kvtracks.keys():
                splitted.append(kvtracks[splitted[0]])
            else:
                splitted.append(0)
            sortd.append(splitted)
    # May go with REVERSE=TRUE
    return sorted(sortd, key = lambda item: item[3])
            # else: splitted.append(0)
            # if sortd: 
            #     if splitted[3] >= sortd[0][3]: sortd.insert(0,splitted)
            #     else: sortd.append(splitted)
            # else:
            #     sortd.append(splitted)
            # return sortd
            #print(kvtracks[splitted[0]])
            #except:
            #    continue
            #print(splitted)
            #with open('dbready.csv', 'w') as dbrfile:
            #    writer = csv.writer(dbrfile)
            #    writer.writerow(splitted)
#    with open('unique1000.txt', 'r', encoding='iso-8859', errors='') as ufile:
#        for line in ufile:
            

@timing
def inject_to_db(sorted_lines):
    pass


def readtest(uniqs_path):
    with open(uniqs_path, 'r', encoding='iso8859', errors='') as f:
        for line in f:
            #print(line)
            splitted = line.rstrip()
            #print(splitted)
            splitted = splitted.split('<SEP>')
            print (splitted)

@timing
def main(args):
    #dbconn, dbcurs = create_db(args.db)
    #readtest(args.songs)
    pairs = process_trips(args.trips)
    #print(kvtracks.keys())
    #print(kvtracks.values())
    #print(kvtracks)
    sortyd = process_songs(args.songs, pairs)    
    print(sortyd)
    #print(type(dbconn)) - type <sqlite3.Connection>
    #print(type(dbcurs)) - type <sqlite3.Cursor>
    #print(args.db) - type <str>


if __name__=="__main__":
    args = parser.parsing() #vars(args) - args.Namespace to dict
    main(args)

