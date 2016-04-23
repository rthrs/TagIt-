from fingerprints import generateFingerprints
from database import connect
import operator

def fingerprintRecognize(path):
    """
        Recognizes song based on fingerprints.
        Returns -1 if song was not recognized or id of song in database.
    """
    
    # fingerprint just 1 sec. of song
    # TODO: rand those values
    start = 0
    stop = 15000
    threshold = 30
    fp = generateFingerprints(path, startTime=start, endTime=stop)
    
    if fp == []:
        return -1
    
    db = connect()
    hits = {}
    for fingerprint in fp:
        result = db.query("SELECT song_id, off FROM fingerprints WHERE hash='"+fingerprint[0]+"'").getresult()
        for res in result:
            resTuple = (res[0], res[1]-fingerprint[1])
            if resTuple in hits:
                hits[resTuple] += 1
            else:
                hits[resTuple] = 1
    
    # print(hits)
    
    if hits != {}:
        res = max(hits.iteritems(), key=operator.itemgetter(1))[0]
    
    if hits != {} and hits[res] >= threshold:
        # print(res)
        return res[0]
    else:
        return -1
    

def recognize(path):    
    """
        Recognizes song from path.
        Returns -1 if song was not recognized or id of song in database.
    """
    # TODO: other recognition methods
    return fingerprintRecognize(path)
