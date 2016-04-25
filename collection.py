"""
    Functions for creating and adding files to collections.
"""

import os
import tag
import eyed3

def moveUp(src, dst):
    """
        Moves all files from src to dst directory.
        Returns:
            -1 if src or dst is not a directory
    """
    if not (os.path.isdir(src) and os.path.isdir(dst)):
        return -1
    
    if src[-1:] != "/":
        src += "/"
    
    if dst[-1:] != "/":
        dst += "/"    
        
    for f in os.listdir(src):
        if not os.path.isdir(f):
            os.rename(src+f, dst+src.replace('/', '_')+f)

def moveFiles(path):
    """
        Moves every file from subfolders of path to path.
        Args:
            path: Path to folder.
        Returns:
            -1 if acction was unsuccessful
            1 otherwise
    """
    # TODO: may not work with weird filenames 
    if not os.path.isdir(path):
        return -1
    
    # path is a correct directory
    for d in os.listdir(path):
        newPath = path+"/"+d
        if os.path.isdir(newPath):
            moveFiles(newPath)
            moveUp(newPath, path)
            os.rmdir(newPath)
    

def createCollection(path):
    """
        Creates collection from a folder.
        Creates a new folder for each artist and copies his music to this folder.
        Moves unrecognized files to "unknown" folder.
        Args:
            path: Path to folder.
        Returns:
            -1 if path is not correct.
            1 if collection was successfully created.
    """
    if not os.path.isdir(path):
        return -1
    
    if path[-1:] != "/":
        path += "/"
    
    moveFiles(path)
    untagged = tag.tagFolder(path)
    if untagged != []:
        os.mkdir(path+"unknown")
    for f in untagged:
        os.rename(path+f, path+"unknown/"+f)
        
    tagged = []
    for f in os.listdir(path):
        if not os.path.isdir(path+f):
            tagged.append(path+f)
            
    for f in tagged:
        artist = eyed3.load(f).tag.artist
        if not os.path.isdir(path+artist):
            os.mkdir(path+artist)
        filename = os.path.split(f)[1]
        os.rename(f, path+artist+"/"+filename)
