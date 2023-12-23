from __future__ import unicode_literals
import sys
import getopt
import os
import warnings
import logging
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

logger = logging.getLogger(__name__)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class FileData:
    def __init__(self, title_:str, artist_:str, newFileName_:str):
        self.title = title_
        self.artist = artist_
        self.newFileName = newFileName_

class MetadataManager:
    def __init__(self):
        self.mp3ext = ".mp3"
        self.maxLenghtOfArtist = 80
        self.maxLenghtOfTitle = 120

    def showMP3Info(self, fileNameWithPath):
        print (bcolors.OKGREEN + fileNameWithPath + bcolors.ENDC)
        audio = MP3(fileNameWithPath, ID3=EasyID3)
        print (audio.pprint())

    def _removeSheetFromSongName(self, songName):

        unsupportedName = ["Oficial Video HD",
                        "Official Video",
                        "official video",
                        "Oficial video",
                        "Oficial Video",
                        "oficial video",
                        "OFFICIAL VIDEO",
                        "Video Official",
                        "VIDEO OFFICIAL",
                        "Oficjalne Video",
                        "Oficjalne video",
                        "oficjalne video",
                        "Oficjalne Wideo",
                        "Oficjalne Wideo",
                        "oficjalne Wideo",
                        "Official Video HD",
                        "Official Video HQ",
                        "Official Music Video",
                        "Official Lyric Video",
                        "Radio Edit",
                        "Radio edit"
                        "radio edit",
                        "Radio Mix",
                        "radio mix",
                        "Radio mix",
                        "Official Audio",
                        "Official audio",
                        "official audio",
                        "Lyrics",
                            "()","( )","(  )","[]", "[ ]", "[  ]","｜", "⧸" ]

        for x in unsupportedName:
            songName = songName.replace(x,"")

        songName = songName.replace(" -", " - ")

        songName = songName.replace("- ", " - ")
        songName = songName.replace("   ", " ")
        songName = songName.replace("  ", " ")
        songName = songName.replace("  ", " ")
        songName = songName.replace(" _", "")

        # remove spaces on the end of filename
        if songName[-1] == ' ':
            songName = songName[:-1]

        return songName

    def _removeSheetFromFilename(self, path, originalFileName):

        fileNameWithoutExtension = originalFileName.replace(self.mp3ext, "")

        fileNameWithoutExtension = self._removeSheetFromSongName(fileNameWithoutExtension)
        fileNameWithExtension = "%s%s"%(fileNameWithoutExtension, self.mp3ext)

        originalFileNameWithPath=os.path.join(path, originalFileName)
        fileNameWithPath = os.path.join(path, fileNameWithExtension)
        os.rename(originalFileNameWithPath, fileNameWithPath)

        return fileNameWithExtension

    def _convertSongnameOnMetadata(self, songName):
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

    def _cutLenght(self, text:str, maxLength):
        #max filename size is 255
        originalText = text
        if ", " in text:
            splitSign = ", "
        else:
            splitSign = " "
        counter = 0
        limit = maxLength/4
        while len(text)>maxLength:
            temp = text.rsplit(splitSign, 1)
            text = temp[0]
            counter+=1
            # if werid text is here, break loop
            if counter >= limit:
                return originalText[0:maxLength]
        return text

    def _analyzeAndRenameFilename(self, path, fileName, artist):
        songName = fileName.replace(self.mp3ext, "")
        originalFileNameWithPath = os.path.join(path, fileName)
        artist = self._cutLenght(artist, self.maxLenghtOfArtist)
        if len(songName) > self.maxLenghtOfTitle:
            print("too long songname")
            print(songName)
            songName = self._cutLenght(songName, self.maxLenghtOfTitle)

        # any condition has to verify variables: title, artist, newFileName
        # if songName doesn't contain artist and artist is known
        # rename filename
        if not " - " in songName and len(artist)>1:
            newFileName = "%s - %s%s"%(artist, songName, self.mp3ext)
            newFileNameWithPath = os.path.join(path, newFileName)
            os.rename(originalFileNameWithPath, newFileNameWithPath)
            fileName=newFileName
            title = songName
            return FileData(title, artist, newFileName)

        # artist is known from file and from input
        if " - " in songName and len(artist)>1:
            metadataSongName = self._convertSongnameOnMetadata(songName)
            title = metadataSongName['title']
            newFileName = "%s - %s%s"%(artist, title, self.mp3ext)
            newFileNameWithPath = os.path.join(path, newFileName)
            os.rename(originalFileNameWithPath, newFileNameWithPath)
            return FileData(title, artist, newFileName)

        # ----- do not modify filename, because do not have enough information ----
        # get artist from filename, when we do not know artist
        if " - " in songName and (artist is None or len(artist)==0):
            metadataSongName = self._convertSongnameOnMetadata(songName)
            newFileName = "%s%s"%(songName, self.mp3ext)
            artist = metadataSongName['artist']
            title = metadataSongName['title']
            return FileData(title, artist, newFileName)

        # artist is unknown
        if not " - " in songName and (artist is None or len(artist)==0):
            warningInfo="WARNING: artist for song %s is not known"%(songName)
            print (bcolors.WARNING + warningInfo + bcolors.ENDC)
            newFileName = "%s%s"%(songName, self.mp3ext)
            title = songName
            artist = None
            return FileData(title, artist, newFileName)

        # something wrong
        return None

    #youtubedl
    def renameAndAddMetadataToSong(self, MUSIC_PATH, albumName, artist, songName):
        path=MUSIC_PATH

        fileName="%s%s"%(songName,self.mp3ext)

        if not os.path.isfile(os.path.join(path, fileName)):
            warningInfo="WARNING: %s not exist"%(fileName)
            print (bcolors.WARNING + warningInfo + bcolors.ENDC)
            return

        #rename song file to remove useless text
        fileName = self._removeSheetFromFilename(path, fileName)

        analyzeResult = self._analyzeAndRenameFilename(path, fileName, artist)
        if analyzeResult is None:
            warningInfo="ERROR: Unknown situation with fileName"
            print (bcolors.FAIL + warningInfo + bcolors.ENDC)
            return

        # saving metadata
        title = analyzeResult.title
        artist = analyzeResult.artist
        newFileName = analyzeResult.newFileName

        newFileNameWithPath = os.path.join(path, newFileName)
        metatag = EasyID3(newFileNameWithPath)
        if albumName is not None:
            metatag['album'] = albumName
        if artist is not None:
            metatag['artist'] = artist
        metatag['title'] = title
        metatag.save()
        print (bcolors.OKGREEN + "[ID3] Added metadata" + bcolors.ENDC)
        self.showMP3Info(newFileNameWithPath)
        return newFileNameWithPath

    #youtubedl
    def renameAndAddMetadataToPlaylist(self, PLAYLISTS_PATH, trackNumber, playlistName, artist, songName):
        path=os.path.join(PLAYLISTS_PATH, playlistName)
        albumName="YT "+playlistName
        fileName="%s%s"%(songName,self.mp3ext)

        if not os.path.isfile(os.path.join(path, fileName)):
            warningInfo="WARNING: %s not exist"%(fileName)
            print (bcolors.WARNING + warningInfo + bcolors.ENDC)
            return

        #rename song file to remove useless text
        fileName = self._removeSheetFromFilename(path, fileName)
        analyzeResult = self._analyzeAndRenameFilename(path, fileName, artist)
        if analyzeResult is None:
            warningInfo="ERROR: Unknown situation with fileName"
            print (bcolors.FAIL + warningInfo + bcolors.ENDC)
            return

        newFileName = analyzeResult.newFileName
        artist = analyzeResult.artist
        title = analyzeResult.title

        newFileNameWithPath = os.path.join(path, newFileName)
        metatag = EasyID3(newFileNameWithPath)
        metatag['album'] = albumName
        if artist is not None:
            metatag['artist'] = artist
        metatag['title'] = title
        metatag['tracknumber'] = str(trackNumber)
        metatag.save()
        print (bcolors.OKGREEN + "[ID3] Added metadata" + bcolors.ENDC)
        self.showMP3Info(newFileNameWithPath)
        return newFileNameWithPath

    #youtubedl
    def lookingForFileAccordWithYTFilename(self, path, songName, artist):

        songName = self._removeSheetFromSongName(songName)
        fileName="%s%s"%(songName,self.mp3ext)

        if os.path.isfile(os.path.join(path, fileName)):
            return songName

        songName = "%s - %s"%(artist, songName)
        fileName="%s%s"%(songName,self.mp3ext)
        if os.path.isfile(os.path.join(path, fileName)):
            return songName
        else:
            return None

    def updateMetadataYoutube(self, PLAYLISTS_PATH, playlistName):
        path=os.path.join(PLAYLISTS_PATH,playlistName)
        albumName="YT "+playlistName
        newFilesList = []

        filesList = [f for f in os.listdir(path) if f.endswith(self.mp3ext)]
        filesList.sort()
        for x in range(len(filesList)):
            originalFileName = filesList[x]

            newFileName = self._removeSheetFromFilename(path, originalFileName)
            newSongName = newFileName.replace(self.mp3ext, "")

            metadataSongName = self._convertSongnameOnMetadata(newSongName)
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
            self.showMP3Info(newFileNameWithPath)
        return newFilesList

    def updateMetadata(self, catalog, albumName):
        newFilesList = []

        filesList = [f for f in os.listdir(catalog) if f.endswith(self.mp3ext)]
        filesList.sort()
        for x in range(len(filesList)):
            originalFileName = filesList[x]

            newFileName = self._removeSheetFromFilename(catalog, originalFileName)
            newSongName = newFileName.replace(self.mp3ext, "")

            metadataSongName = self._convertSongnameOnMetadata(newSongName)
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
            self.showMP3Info(newFileNameWithPath)
        return newFilesList

    def setAlbum(self, catalog, albumName):
        filesList = [f for f in os.listdir(catalog) if f.endswith(self.mp3ext)]
        filesList.sort()
        for fileName in filesList:
            fileNameWithPath = os.path.join(catalog, fileName)
            metatag = EasyID3(fileNameWithPath)
            metatag['album'] = albumName
            metatag.save()
            self.showMP3Info(fileNameWithPath)

        return filesList

    def setArtist(self, catalog, artistName):
        filesList = [f for f in os.listdir(catalog) if f.endswith(self.mp3ext)]
        filesList.sort()
        for fileName in filesList:
            fileNameWithPath = os.path.join(catalog, fileName)
            metatag = EasyID3(fileNameWithPath)
            metatag['artist'] = artistName
            metatag.save()
            self.showMP3Info(fileNameWithPath)

        return filesList
