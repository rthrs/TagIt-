from recognize import recognize
from database import getTags
import eyed3
import os

def tagFolder(path):
    """
        Tags all file in a given folder.
        Args:
            path: path to the folder.
        Returns:
            List of files which couldn't be tagged.
    """
    # TODO: Deal with other file extensions than mp3.
    
    res = []

    for root, dirs, files in os.walk(path):
        for filename in files:
            if ".mp3" in filename:
                path = root+"/"+filename
                if tagFile (path)== -1:
                    res.append(path)        
    return res

def tagFile(path):
    """
        Tags single file and renames it in format Artist - Song name.
        Args:
            path: path to the file.
        Retruns:
            0 if tagging was successful.
            -1 if tagging failed.
    """
    # TODO: options for naming file
    
    # print("Tagging: "+path)
    song_id = recognize(path)
    if song_id == -1:
        return -1
    tags = getTags(song_id)
    af = eyed3.load(path)
    af.tag.artist = tags['artist'].decode('utf-8')
    af.tag.title = tags['title'].decode('utf-8')
    if tags['album'] != None:
        af.tag.album = tags['album'].decode('utf-8')
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
        Args:
            path: path to file or folder.
        Returns:
            List of files for which tagging failed.
    """
    # TODO: implement it using 
    pass
    
