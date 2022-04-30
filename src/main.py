from sqlite3 import OperationalError, connect as sqlcon
from os import mkdir
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
    try: sql_table = sqlcon(dbpath)
    except: 
        OperationalError: mkdir(dbpath)
    finally: sql_table = sqlcon(dbpath)
    sql_cursor = sql_table.cursor()
    sql_cursor.execute('''
                 CREATE TABLE IF NOT EXISTS tracks (
                     sid VARCHAR(255),
                     artist VARCHAR(255),
                     title VARCHAR(255),
                     listened INT
                 )
                 ''')
    sql_table.commit()
    return sql_table, sql_cursor



# Process triplets to dictionary: {<str>'TrackID' : <int>#-of-plays}
@timing
def process_trips(trips_path):
    trackid_count = {}
    # Well done!
    with open(trips_path, 'r', encoding='iso8859', errors='') as trips_file:
        for line in trips_file:
            splitted_trip = line.rstrip()
            splitted_trip = splitted_trip.split('<SEP>')
            if splitted_trip[1] in trackid_count.keys():
                trackid_count[str(splitted_trip[1])] += 1
            else:
                trackid_count[str(splitted_trip[1])] = 1
        return trackid_count

# Process songs to list of lists of format:
# [ [<str>SID, <str>Artist, <str>Song, <int>Replays], [...] ,.., [...] ]
@timing
def process_songs(uniqs_path, kvtracks):
    songs = []
    with open(uniqs_path, 'r', encoding='iso8859', errors='') as song_file:
        for line in song_file:
            splitted_song = line.rstrip()
            splitted_song = splitted_song.split('<SEP>')
            splitted_song.pop(0)
            if splitted_song[0] in kvtracks.keys():
                splitted_song.append(kvtracks[splitted_song[0]])
            else:
                splitted_song.append(0)
            songs.append(splitted_song)
    # May go with REVERSE=TRUE
    #return sorted(songs, key = lambda item: item[3], reverse=True)
    return songs


# Inject songs in ordered format to sqlite3 db
@timing
def inject_to_db(songs, sqlite_cursor):
    for entry in songs: sqlite_cursor.execute('INSERT INTO tracks VALUES (?,?,?,?)', entry)


# Query database for artist with most replays of all
@timing
def q_top_artist(sqlite_cursor):
    query = 'SELECT artist, COUNT(listened) FROM tracks GROUP BY artist ORDER BY COUNT(listened) DESC LIMIT 5'
    print('\nTOP Artist (by # of repetetive plays):')
    for row in sqlite_cursor.execute(query):
        print(row)
    print('\n')

    
# Query database for top 5 songs, judging by replay-value
@timing 
def q_top_songs(sqlite_cursor):
    query = 'SELECT * FROM tracks ORDER BY listened DESC LIMIT 5'
    print('\n5 TOP Songs (by # of repetetive plays):')
    for row in sqlite_cursor.execute(query):
        entry = row[1] + " - " + row[2] + ", " + str(row[3]) + " plays"
        print(entry)
    print('\n')


@timing
def main(args):
    pairs = process_trips(args.trips)
    songs_dbrdy = process_songs(args.songs, pairs)
    dbconn, dbcurs = create_db(args.db)
    inject_to_db(songs_dbrdy, dbcurs) 
    q_top_artist(dbcurs)
    #q_top_songs(dbcurs)



if __name__=="__main__":
    args = parser.parsing() 
    main(args)

# def readtest(uniqs_path):
#     with open(uniqs_path, 'r', encoding='iso8859', errors='') as f:
#         for line in f:
#             #print(line)
#             splitted = line.rstrip()
#             #print(splitted)
#             splitted = splitted.split('<SEP>')
#             print (splitted)
