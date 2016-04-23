"""
    Functions for operating on database.
"""
# TODO: create separate user with read-only rights for recognition.

from pg import DB

DBNAME = 'music'
HOST = 'localhost'
USER = 'wojtek'
PASSWD = 'test'

def connect():
    """
        Returns handler for database connection.
    """
    return DB(dbname=DBNAME, host=HOST, user=USER, passwd=PASSWD)
    
def getTags(song_id):
    """
        Returns dictionary with tags of a given song.
    """
    return connect().query("SELECT * FROM songs WHERE song_id="+str(song_id)).dictresult()[0]
