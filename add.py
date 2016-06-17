## @package add
#  Function for adding song to database.
##

from fingerprints import generateFingerprints
from database import connect
import eyed3


def addSong(path, tags={}):
    """
        Adds song to a database.
        Works only for mp3 files for now.
        Args:
            path: Path to the song
            tags (Optional): A dictionary of tags. If empty tags of file will
                             by used. Title and artist are required.
        Returns:
            -1 if path does not contain a valid song.
            -2 if either artist or title is missing from tags.
            1 if successful

    """
    # TODO: change method of reading tags (eyed3 supports only mp3 files and doesn't get year).

    fp = generateFingerprints(path)
    if fp == []: # path does not point to correct song
        return -1

    if tags == {}: # no tags supplied by caller
        af = eyed3.load(path)
        if af.tag.artist == None or af.tag.title == None: # artist and title are required tags
            return -2
        tags = {
            'artist' : af.tag.artist,
            'title'  : af.tag.title,
            'album'  : af.tag.album,
            'track'  : af.tag.track_num[0]
        }
    elif not ('artist' in tags and 'title' in tags): # artist and title are required tags
        # print(tags)
        return -2

    db = connect()
    added = db.insert('songs', tags) # add song to database

    db.query("BEGIN")

    # add fingerprints to database
    for fingerprint in fp:
        toAdd = {'hash' : fingerprint[0], 'off' : fingerprint[1], 'song_id' : added['song_id']}
        db.insert('fingerprints', toAdd)

    db.query("COMMIT")

    return 1
