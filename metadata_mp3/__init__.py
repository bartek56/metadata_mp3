from __future__ import unicode_literals
import sys
import getopt
import os
import warnings
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def showMP3Info(fileNameWithPath):
    print (bcolors.OKGREEN + fileNameWithPath + bcolors.ENDC)
    audio = MP3(fileNameWithPath, ID3=EasyID3)
    print (audio.pprint())


def convert_song_name(songName):
    songName = songName.replace(" -", " - ")
    songName = songName.replace("- ", " - ")

    songName = songName.replace("(Oficial Video HD)", "")
    songName = songName.replace("(Official Video HD)", "")
    songName = songName.replace("[Official Video HD]", "")
    songName = songName.replace("(Official Video HQ)", "")
    songName = songName.replace("[Official Video HQ]", "")

    songName = songName.replace("[Official Music Video]", "")
    songName = songName.replace("(Official Music Video)", "")

    songName = songName.replace("(Official Lyric Video)", "")

    songName = songName.replace("( Official Video )", "")
    songName = songName.replace("(Official Video)", "")
    songName = songName.replace("[Official Video]", "")
    songName = songName.replace("(official video)", "")
    songName = songName.replace("(Official video)", "")
    songName = songName.replace("[OFFICIAL VIDEO]", "")
    songName = songName.replace("(OFFICIAL VIDEO)", "")
    songName = songName.replace("(Video Official)", "")
    songName = songName.replace("[Video Official]", "")
    songName = songName.replace("(VIDEO OFFICIAL)", "")
      
    songName = songName.replace("(Oficial Video)", "")
    songName = songName.replace("[Oficial Video]", "")
    songName = songName.replace("(OFICIAL VIDEO)", "")
    songName = songName.replace("(Video Oficial)", "")
    songName = songName.replace("[Video Oficial]", "")
    songName = songName.replace("(VIDEO OFICIAL)", "")
  
    songName = songName.replace("Video Oficial", "")
    songName = songName.replace("Video Official", "")
    songName = songName.replace("Oficial Video", "")
    songName = songName.replace("Official Video", "")
    
    songName = songName.replace("(Oficjalne Video)", "")
    songName = songName.replace("Oficjalne Video", "")
    songName = songName.replace("(oficjalne video)", "")
    songName = songName.replace("oficjalne video", "")

    songName = songName.replace("(Oficjalne Wideo)", "")
    songName = songName.replace("Oficjalne Wideo", "")
    songName = songName.replace("(oficjalne wideo)", "")
    songName = songName.replace("oficjalne wideo", "")

    songName = songName.replace("(Radio Edit)", "")
    songName = songName.replace("(radio edit)", "")
    songName = songName.replace("[Radio Edit]", "")
    songName = songName.replace("[radio edit]", "")
   
    songName = songName.replace("(Radio Mix)", "")
    songName = songName.replace("(radio mix)", "")
    songName = songName.replace("[Radio Mix]", "")
    songName = songName.replace("[radio mix]", "")

    songName = songName.replace("(Audio)", "")

    songName = songName.replace("(Official Audio)", "")
    songName = songName.replace("[Official Audio]", "")

    songName = songName.replace("   ", " ")   
    songName = songName.replace("  ", " ")   
    songName = songName.replace("  ", " ")   
    songName = songName.replace(" _", "")

    return songName

def rename_song_name(songName):
    songName = convert_song_name(songName)
    ext = ".xyz"
    songName = "%s%s"%(songName,ext)

    songName = songName+".xyz"
    songName = songName.replace("  .xyz", ".xyz")
    songName = songName.replace(" .xyz", ".xyz")
    songName = songName.replace(".xyz", "")
    
    return songName

def rename_song_file(path, fileName):

    originalFileName = fileName 
    
    fileName = convert_song_name(fileName)

    fileName = fileName.replace("  .mp3", ".mp3")
    fileName = fileName.replace(" .mp3", ".mp3")

    originalFileNameWithPath=os.path.join(path, originalFileName)
    fileNameWithPath = os.path.join(path, fileName)
    os.rename(originalFileNameWithPath, fileNameWithPath)

    return fileName

def convert_songname_on_metadata(songName):
    slots = songName.split(" - ")
    metadata ={ 'tracknumber': "1",}
    if len(slots) == 2:
      metadata['artist'] = slots[0]
      metadata['title'] = slots[1]
    elif len(slots) < 2:
      slots = songName.split("-")
      if len(slots) == 2:
        metadata['artist'] = slots[0]
        metadata['title'] = slots[1]
      else:
        metadata['title'] = songName
        metadata['artist'] = ""
    else:
      metadata['artist'] = slots[0]
      name=""
      i=0
      for slots2 in slots:
        if i > 0:
          if i > 1:
            name+="-"
          name+=slots[i]
        i=i+1  
      metadata['title'] = name

    return metadata

#youtubedl
def add_metadata_song(MUSIC_PATH, albumName, artist, songName):
    path=MUSIC_PATH

    mp3ext=".mp3"
    fileName="%s%s"%(songName,mp3ext)

    # looking for file      
    if not os.path.isfile(os.path.join(path, fileName)):
        songName = songName.replace("/", "_")
        songName = songName.replace("|", "_")
        songName = songName.replace("\"", "'")
        songName = songName.replace(":", "-")
        fileName="%s%s"%(songName,mp3ext)
    if not os.path.isfile(os.path.join(path, fileName)):
        songName = rename_song_name(songName)
        fileName="%s%s"%(songName,mp3ext)
    if not os.path.isfile(os.path.join(path, fileName)):
        fileName="%s - %s%s"%(artist, songName, mp3ext)
    if not os.path.isfile(os.path.join(path, fileName)):
        warningInfo="WARNING: %s not exist"%(fileName)
        print (bcolors.WARNING + warningInfo + bcolors.ENDC)
        return
    
    # if filename contain artist add it to metadata
    if not " - " in songName and len(artist)>1:
        originalFileNameWithPath = os.path.join(path, fileName)
        newFileName = "%s - %s.mp3"%(artist, songName)
        newFileNameWithPath = os.path.join(path, newFileName)
        os.rename(originalFileNameWithPath, newFileNameWithPath)
        fileName=newFileName

    #rename song file to remove useless text
    newFileName = rename_song_file(path, fileName)
    newSongName = newFileName.replace(".mp3", "")

    # get metadata from filename
    metadataSongName = convert_songname_on_metadata(newSongName)
    newFileNameWithPath = os.path.join(path, newFileName)

    # saving metadata    
    metatag = EasyID3(newFileNameWithPath)
    if albumName is not None:
        metatag['album'] = albumName
    if artist is not None and len(artist)>1:
        metatag['artist'] = artist
    else:
        metatag['artist'] = metadataSongName['artist']
    metatag['title'] = metadataSongName['title']
    metatag.save()
    print (bcolors.OKGREEN + "[ID3] Added metadata" + bcolors.ENDC)
    print (newFileNameWithPath)
    audio = MP3(newFileNameWithPath, ID3=EasyID3)
    print (audio.pprint())
    return newFileNameWithPath

# youtubedl
def add_metadata_playlist(PLAYLISTS_PATH, trackNumber, playlistName, artist, songName):
    path=os.path.join(PLAYLISTS_PATH,playlistName)
    albumName="YT "+playlistName

    mp3ext=".mp3"
    fileName="%s%s"%(songName,mp3ext)

      
    if not os.path.isfile(os.path.join(path, fileName)):
        songName = songName.replace("/", "_")
        songName = songName.replace("|", "_")
        songName = songName.replace("\"", "'")
        songName = songName.replace(":", "-")
        fileName="%s%s"%(songName,mp3ext)
    if not os.path.isfile(os.path.join(path, fileName)):
        songName = songName.replace("-", " - ")
        fileName="%s%s"%(songName,mp3ext)
    if not os.path.isfile(os.path.join(path, fileName)):
        songName = rename_song_name(songName)
        fileName="%s%s"%(songName,mp3ext)
    if not os.path.isfile(os.path.join(path, fileName)):
        fileName="%s - %s%s"%(artist, songName, mp3ext)
    if not os.path.isfile(os.path.join(path, fileName)):
        warningInfo="WARNING: %s not exist"%(fileName)
        print (bcolors.WARNING + warningInfo + bcolors.ENDC)
        return

    if not " - " in songName and len(artist)>1:
        originalFileNameWithPath = os.path.join(path, fileName)
        newFileName = "%s - %s.mp3"%(artist, songName)
        newFileNameWithPath = os.path.join(path, newFileName)
        os.rename(originalFileNameWithPath, newFileNameWithPath)
        fileName=newFileName

    newFileName = rename_song_file(path, fileName)
    newSongName = newFileName.replace(".mp3", "")

    metadataSongName = convert_songname_on_metadata(newSongName)
    newFileNameWithPath = os.path.join(path, newFileName)
        
    metatag = EasyID3(newFileNameWithPath)
    metatag['album'] = albumName
    if artist is not None:
        metatag['artist'] = artist
    else:
        metatag['artist'] = metadataSongName['artist']
    metatag['title'] = metadataSongName['title']
    metatag['tracknumber'] = str(trackNumber)
    metatag.save()
    print (bcolors.OKGREEN + "[ID3] Added metadata" + bcolors.ENDC)
    print (newFileNameWithPath)
    audio = MP3(newFileNameWithPath, ID3=EasyID3)
    print (audio.pprint())
    return newFileNameWithPath

def update_metadata_youtube(PLAYLISTS_PATH, playlistName):
      path=os.path.join(PLAYLISTS_PATH,playlistName)
      albumName="YT "+playlistName
      newFilesList = []

      filesList = [f for f in os.listdir(path) if f.endswith(".mp3")]
      filesList.sort()
      for x in range(len(filesList)):
        originalFileName = filesList[x]

        newFileName = rename_song_file(path, originalFileName)
        newSongName = newFileName.replace(".mp3", "")
        
        metadataSongName = convert_songname_on_metadata(newSongName)
        newFileNameWithPath = os.path.join(path, newFileName)
        if not os.path.isfile(newFileNameWithPath):
            warningInfo="WARNING: %s not exist"%(newFileName)
            warnings.warn(warningInfo, Warning)
            print(bcolors.WARNING + warningInfo + bcolors.ENDC)
            continue
        metatag = EasyID3(newFileNameWithPath)
        metatag['album'] = albumName
        metatag['artist'] = metadataSongName['artist']
        metatag['title'] = metadataSongName['title']
        metatag.save()
        print(bcolors.OKGREEN + "[ID3] Added metadata" + bcolors.ENDC)
        showMP3Info(newFileNameWithPath)
      return newFilesList  

def update_metadata(catalog, albumName):
      newFilesList = []

      filesList = [f for f in os.listdir(catalog) if f.endswith(".mp3")]
      filesList.sort()
      for x in range(len(filesList)):
        originalFileName = filesList[x]

        newFileName = rename_song_file(catalog, originalFileName)
        newSongName = newFileName.replace(".mp3", "")
        
        metadataSongName = convert_songname_on_metadata(newSongName)
        newFileNameWithPath = os.path.join(catalog, newFileName)
        if not os.path.isfile(newFileNameWithPath):
            warningInfo="WARNING: %s not exist"%(newFileName)
            warnings.warn(warningInfo, Warning)
            print(bcolors.WARNING + warningInfo + bcolors.ENDC)
            continue
        metatag = EasyID3(newFileNameWithPath)
        metatag['album'] = albumName
        metatag['artist'] = metadataSongName['artist']
        metatag['title'] = metadataSongName['title']
        metatag.save()
        newFilesList.append(newFileNameWithPath)
        print(bcolors.OKGREEN + "[ID3] Added metadata" + bcolors.ENDC)
        showMP3Info(newFileNameWithPath)
      return newFilesList  


def setAlbum(catalog, albumName):
    filesList = [f for f in os.listdir(catalog) if f.endswith(".mp3")]
    filesList.sort()
    for fileName in filesList:
        fileNameWithPath = os.path.join(catalog, fileName)
        metatag = EasyID3(fileNameWithPath)
        metatag['album'] = albumName
        metatag.save()
        showMP3Info(fileNameWithPath)

    return filesList

def setArtist(catalog, artistName):
    filesList = [f for f in os.listdir(catalog) if f.endswith(".mp3")]
    filesList.sort()
    for fileName in filesList:
        print(fileName)
        fileNameWithPath = os.path.join(catalog, fileName)
        metatag = EasyID3(fileNameWithPath)
        metatag['artist'] = artistName
        metatag.save()
        showMP3Info(fileNameWithPath)

    return filesList
