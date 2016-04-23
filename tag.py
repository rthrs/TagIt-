from recognize import recognize
from database import getTags
import eyed3
import os

def tagFolder(path):
    res = []
    if path[-1:] != "/":
        path = path+"/"
        
    for song in os.listdir(path):
        tagFile(path+song)

def tagFile(path):
    """
        Tags a single file.
        Retruns -1 if tagging failed, 0 otherwise.
    """
    # TODO: options for naming file
    
    # print("Tagging: "+path)
    song_id = recognize(path)
    if song_id == -1:
        return -1
    tags = getTags(song_id)
    af = eyed3.load(path)
    af.tag.artist = unicode(tags['artist'])
    af.tag.title = unicode(tags['title'])
    if tags['album'] != None:
        af.tag.album = unicode(tags['album'])
    else:
        af.tag.album = u'';
    if tags['track'] != None:
        af.tag.track_num = tags['track']
    af.tag.save()
    
    filename, fileExtension = os.path.splitext(path)
    os.rename(path, os.path.dirname(path)+"/"+tags['artist']+" - "+tags['title']+fileExtension)

def tag(path):
    """
        Tags folder or a single music file.
        Returns list of files for which tagging failed.
    """
    
