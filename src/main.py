import parser
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

def process_files():
    pass

def main(args):
    dbconn, dbcurs = create_db(args.db)
    
    
    
    
    #print(type(dbconn)) - type <sqlite3.Connection>
    #print(type(dbcurs)) - type <sqlite3.Cursor>
    #print(args.db) - type <str>
    pass

if __name__=="__main__":
    args = parser.parsing() #vars(args) - args.Namespace to dict
    main(args)

