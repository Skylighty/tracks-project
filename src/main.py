import parser
import csv
from sqlite3 import connect as sqlcon


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


    """
        Najpierw opierdol pliki i wrzuc to do slownika.
        Dopiero jak beda gotowe to wpierdol do db.
        plan prcoessingu:
        1. 
    """

# Files format
# triplets - UserID - TrackID - ListenDate - LF
# uniquie tracks - PerfID-TrackID-Artist-Title-LF
# !!! INPUT FORMAT - TrackID - Artist - Title - Listen#
def process_files(trips_path, uniqs_path):
    trackid_count = {}
    # Well done!
    with open(trips_path, 'r', encoding='iso8859', errors='') as tfile:
        for line in tfile:
            splitted = line.strip()
            splitted = line.split('<SEP>')
            if splitted[1] in trackid_count.keys():
                trackid_count[splitted[1]] += 1
            else:
                trackid_count[splitted[1]] = 1
        dict(sorted(trackid_count.items(), key=lambda item: item[1]))
    # TEST PRINT print(trackid_count)
    with open(uniqs_path, 'r', encoding='iso8859', errors='') as ufile:
        for line in ufile:
            splitted = line.strip()
            splitted = line.split('<SEP>')
            splitted.pop(0)
            try:
                splitted.append[trackid_count[splitted[0]]]
            except:
                pass
            with open('dbready.csv', 'w') as dbrfile:
                writer = csv.writer(dbrfile)
                writer.writerow(splitted)
#    with open('unique1000.txt', 'r', encoding='iso-8859', errors='') as ufile:
#        for line in ufile:
            

def main(args):
    #dbconn, dbcurs = create_db(args.db)
    process_files(args.trips, args.songs)    
    #print(type(dbconn)) - type <sqlite3.Connection>
    #print(type(dbcurs)) - type <sqlite3.Cursor>
    #print(args.db) - type <str>


if __name__=="__main__":
    args = parser.parsing() #vars(args) - args.Namespace to dict
    main(args)

