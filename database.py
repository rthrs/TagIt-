"""
    Functions for operating on database.
"""

from pg import DB
import dbConfig

def connect():
    """
        Connects to the database using data from dbConfig.py.
        Returns:
            Handler of database connection.
    """
    return DB(dbname=DBNAME, host=HOST, user=USER, passwd=PASSWD)
    
def getTags(song_id):
    """
        Gets tags of a given song.
        Args:
            song_id: id of a song in database.
        Returns:
            Dictionary containing tags of a song. If tag is missing from database its value will be represented as None.
    """
    return connect().query("SELECT * FROM songs WHERE song_id="+str(song_id)).dictresult()[0]
