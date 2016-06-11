"""
    Functions for music files recognition.
"""

from fingerprints import generateFingerprints
from database import connect
import operator

from config import *

def fingerprintRecognize(path):
    """
        Recognizes song using fingerprinting.
        Args:
            path: path to the song.
        Returns:
            id of a song in databse if song was found.
            -1 if song was not recognized or path does not contain a valid audio file.
    """
    
    # Fingerprint first 7 seconds of a song.
    # TODO: Maybe this value should be randed or added to config.
    start = 0
    stop = 10000
    fp = generateFingerprints(path, startTime=start, endTime=stop)
    
    if fp == []:
        return -1
    
    db = connect()
    hits = {}
    endSearch = False
    for fingerprint in fp:
        if endSearch:
            break
        result = db.query("SELECT song_id, off FROM fingerprints WHERE hash='"+fingerprint[0]+"'").getresult()
        for res in result:
            resTuple = (res[0], res[1]-fingerprint[1])
            if resTuple in hits:
                hits[resTuple] += 1
            else:
                hits[resTuple] = 1
    
    
    if hits != {}:
        res = max(hits.iteritems(), key=operator.itemgetter(1))[0]
    
    if hits != {} and hits[res] >= THRESHOLD:
        # print(res)
        return res[0]
    else:
        return -1
    

def recognize(path):    
    """
        Recognizes song from path.
        Args:
            path: path to the song.
        Returns:
            id of a song in databse if song was found.
            -1 if song was not recognized or path does not contain a valid audio file.
    """
    # TODO: other recognition methods
    return fingerprintRecognize(path)
