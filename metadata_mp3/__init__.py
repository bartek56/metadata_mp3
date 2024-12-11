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
        print (audio. pprint())

    def getMP3Info(self, fileNameWithPath):
        if not os.path.isfile(fileNameWithPath):
            print("file", fileNameWithPath, "doesn't exist")
            return
        #print (bcolors.OKGREEN + fileNameWithPath + bcolors.ENDC)
        audio = MP3(fileNameWithPath, ID3=EasyID3)
        #print (audio. pprint())
        result = {}
        for x in audio.items():
            result[x[0]] = x[1][0]
        return result

    def showMP3InfoDir(self, dir):
        if not os.path.isdir(dir):
            print("Wrong dir path")

        files = os.listdir(dir)
        listMp3 = []
        for file in files:
            if ".mp3" in file:
                fullPath = os.path.join(dir, file)
                audio = EasyID3(fullPath)
                audioDict = dict(audio)
                newDict = {}
                newDict["path"] = fullPath
                for key, value in audioDict.items():
                    newDict[key] = value[0]

                listMp3.append(newDict)

        result = sorted(listMp3, key=lambda x: float(x.get("tracknumber",0 )))
        for x in result:
            for key, value in x.items():
                print(key,":",value)
            print()

    def _removeSheetFromSongName(self, songName):

        unsupportedName = ["Oficial Video HD",
                        "Official Video",
                        "Video Edit",
                        "video edit",
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
                        "Lyric Video",
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
        result = originalFileName
        fileNameWithoutExtension = originalFileName.replace(self.mp3ext, "")

        fileNameWithoutExtension = self._removeSheetFromSongName(fileNameWithoutExtension)
        fileNameWithExtension = "%s%s"%(fileNameWithoutExtension, self.mp3ext)

        originalFileNameWithPath=os.path.join(path, originalFileName)
        fileNameWithPath = os.path.join(path, fileNameWithExtension)
        try:
            os.rename(originalFileNameWithPath, fileNameWithPath)
            result = fileNameWithExtension
        except Exception as e:
            print(bcolors.FAIL + str(e) + bcolors.ENDC)

        return result

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

    def _cutLengthAndRemoveDuplicates(self, text:str, maxLength):
        textWithoutDuplicates = self._removeDuplicates(text)

        if len(textWithoutDuplicates) <= maxLength:
            return textWithoutDuplicates
        return self._cutLenght(textWithoutDuplicates, maxLength)

    def _cutLenght(self, text:str, maxLength):
        #max filename size is 255

        splitSign = self._getSplitSign(text)
        if splitSign is None:
            return text[:maxLength]
        else:
            maxLength = maxLength+len(splitSign)
            textTemp = text[:maxLength]
            temp = textTemp.rsplit(splitSign, 1)
            return temp[0]

    def _removeDuplicates(self, text):
        splitSign = self._getSplitSign(text)
        if splitSign is None:
            return text
        textSplitted = text.split(splitSign)
        textSplittedWithoutDuplicates = []
        for x in textSplitted:
            if x not in textSplittedWithoutDuplicates:
                textSplittedWithoutDuplicates.append(x)
        textWithoutDuplicates = ""
        for x in textSplittedWithoutDuplicates:
            textWithoutDuplicates += x + splitSign
        return textWithoutDuplicates[:-len(splitSign)]

    def _getSplitSign(self, text):
        splitSign=None
        if ", " in text:
            splitSign = ", "
        elif " " in text:
            splitSign = " "
        return splitSign

    def _analyzeAndRenameFilename(self, path, fileName, artist):
        resultFileName = fileName
        songName = fileName.replace(self.mp3ext, "")
        originalFileNameWithPath = os.path.join(path, fileName)
        artist = self._cutLengthAndRemoveDuplicates(artist, self.maxLenghtOfArtist)
        if len(songName) > self.maxLenghtOfTitle:
            songName = self._cutLenght(songName, self.maxLenghtOfTitle)

        # any condition has to verify variables: title, artist, newFileName
        # if songName doesn't contain artist and artist is known
        # rename filename
        if not " - " in songName and len(artist)>1:
            newFileName = "%s - %s%s"%(artist, songName, self.mp3ext)
            newFileNameWithPath = os.path.join(path, newFileName)
            try:
                os.rename(originalFileNameWithPath, newFileNameWithPath)
                resultFileName=newFileName
            except Exception as e:
                print(bcolors.FAIL + str(e) + bcolors.ENDC)
            title = songName
            return FileData(title, artist, resultFileName)

        # artist is known from file and from input
        if " - " in songName and len(artist)>1:
            metadataSongName = self._convertSongnameOnMetadata(songName)
            title = metadataSongName['title']
            newFileName = "%s - %s%s"%(artist, title, self.mp3ext)
            newFileNameWithPath = os.path.join(path, newFileName)
            try:
                os.rename(originalFileNameWithPath, newFileNameWithPath)
                resultFileName=newFileName
            except Exception as e:
                print(bcolors.FAIL + str(e) + bcolors.ENDC)
            return FileData(title, artist, resultFileName)

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

    # TODO a lot of duplicates
    def _analyzeSongname(self, songName, artist):
        artist = self._cutLengthAndRemoveDuplicates(artist, self.maxLenghtOfArtist)
        if len(songName) > self.maxLenghtOfTitle:
            songName = self._cutLenght(songName, self.maxLenghtOfTitle)

        # any condition has to verify variables: title, artist, newFileName
        # if songName doesn't contain artist and artist is known
        # rename filename
        if not " - " in songName and len(artist)>1:
            newFileName = "%s - %s%s"%(artist, songName, self.mp3ext)
            resultFileName=newFileName
            title = songName
            return FileData(title, artist, resultFileName)

        # artist is known from file and from input
        if " - " in songName and len(artist)>1:
            metadataSongName = self._convertSongnameOnMetadata(songName)
            title = metadataSongName['title']
            newFileName = "%s - %s%s"%(artist, title, self.mp3ext)
            resultFileName=newFileName
            return FileData(title, artist, resultFileName)

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

    def _updateMetadataFromDirectory(self, path, originalFileName, albumName):

            newFileName = self._removeSheetFromFilename(path, originalFileName)
            newSongName = newFileName.replace(self.mp3ext, "")

            metadataSongName = self._convertSongnameOnMetadata(newSongName)
            newFileNameWithPath = os.path.join(path, newFileName)
            if not os.path.isfile(newFileNameWithPath):
                warningInfo="WARNING: %s not exist"%(newFileName)
                warnings.warn(warningInfo, Warning)
                print(bcolors.WARNING + warningInfo + bcolors.ENDC)
                return
            metatag = EasyID3(newFileNameWithPath)
            if "artist" in metatag and "title" in metatag and "album" in metatag:
                if metatag['album'][0] == albumName and metatag['artist'][0] == metadataSongName['artist'] and metatag['title'][0] == metadataSongName['title']:
                    print(bcolors.OKGREEN + "Metadata is correct. Update is not needed: " + bcolors.ENDC)
                    self.showMP3Info(newFileNameWithPath)
                    return

            metatag['album'] = albumName
            metatag['artist'] = metadataSongName['artist']
            metatag['title'] = metadataSongName['title']
            metatag.save()
            print(bcolors.OKGREEN + "[ID3] Added metadata" + bcolors.ENDC)
            self.showMP3Info(newFileNameWithPath)
            return newFileNameWithPath

    #youtubedl
    def renameAndAddMetadataToSong(self, MUSIC_PATH, albumName, artist, songName, website):
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
        if albumName is not None and len(albumName) > 0:
            metatag['album'] = albumName
        if artist is not None and len(artist) > 0:
            metatag['artist'] = artist
        if website is not None and len(website) > 0:
            metatag['website'] = website
        metatag['title'] = title
        metatag.save()
        print (bcolors.OKGREEN + "[ID3] Added metadata" + bcolors.ENDC)
        self.showMP3Info(newFileNameWithPath)
        return newFileNameWithPath

    #youtubedl
    def renameAndAddMetadataToPlaylist(self, PLAYLISTS_PATH, trackNumber, playlistName, artist, album, titleSongName, website):
        path=os.path.join(PLAYLISTS_PATH, playlistName)
        albumName="YT "+playlistName
        fileName="%s%s"%(titleSongName,self.mp3ext)

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
        return self.addMetadataToPlaylist(newFileNameWithPath, title, artist, album, website,trackNumber, albumName)

    def addMetadataToPlaylist(self, fileNameWithPath, title, artist, album, website, trackNumber, albumArtist):
        metatag = EasyID3(fileNameWithPath)
        if artist is not None and len(artist) > 0:
            metatag['artist'] = artist
        if albumArtist is not None and len(albumArtist) > 0:
            metatag['albumartist'] = albumArtist
        if website is not None and len(website) > 0:
            metatag['website'] = website
        metatag['title'] = title
        metatag['tracknumber'] = str(trackNumber)
        metatag['album'] = album
        metatag.save()
        print (bcolors.OKGREEN + "[ID3] Added metadata" + bcolors.ENDC)
        self.showMP3Info(fileNameWithPath)
        return fileNameWithPath

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
        """
        update metadata according to Youtube platlist analogy
        album will be updated with YT subtext; YT chillout
        artist and title will be get from file name; artist - title.mp3
        some shit from filename will be removed

        :param PLAYLISTS_PATH: path where playlists are download; /home/music/YT playlists
        :param playlistName: name of playlist which one You want update metadata; chillout
        :return: list of updated files
        """

        if not os.path.isdir(PLAYLISTS_PATH):
            print(bcolors.WARNING + "catalog doesn't exist "+ PLAYLISTS_PATH + bcolors.ENDC)
            return

        path=os.path.join(PLAYLISTS_PATH, playlistName)
        albumName="YT "+playlistName
        newFilesList = []

        filesList = [f for f in os.listdir(path) if f.endswith(self.mp3ext)]
        filesList.sort()
        for x in range(len(filesList)):
            originalFileName = filesList[x]
            newFileNameWithPath = self._updateMetadataFromDirectory(path, originalFileName, albumName)
            if newFileNameWithPath is not None:
                newFilesList.append(newFileNameWithPath)
        return newFilesList

    def updateMetadata(self, catalog, albumName):
        """
        update metadata in catalog
        artist and title will be get from file name; artist - title.mp3
        some shit from filename will be removed

        :param catalog: path where You want update metadata for songs; /home/music/Myslovitz
        :param albumName: name of album for songs in catalog;
        :return: list of updated files
        """
        if not os.path.isdir(catalog):
            print(bcolors.WARNING + "catalog doesn't exist "+ catalog + bcolors.ENDC)
            return

        filesList = [f for f in os.listdir(catalog) if f.endswith(self.mp3ext)]
        filesList.sort()
        newFilesList = []
        for x in range(len(filesList)):
            originalFileName = filesList[x]
            newFileNameWithPath = self._updateMetadataFromDirectory(catalog, originalFileName, albumName)
            if newFileNameWithPath is not None:
                newFilesList.append(newFileNameWithPath)
        return newFilesList

    def setAlbum(self, catalog, albumName):
        """
        set album for all files in directory

        :param catalog: path where You want update metadata for songs; /home/music/Myslovitz
        :param albumName: name of album for songs in catalog;
        :return: list of updated files
        """
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
        """
        set artist for all files in directory

        :param catalog: path where You want update metadata for songs; /home/music/Myslovitz
        :param artistName: name of artist for songs in catalog;
        :return: list of updated files
        """
        filesList = [f for f in os.listdir(catalog) if f.endswith(self.mp3ext)]
        filesList.sort()
        for fileName in filesList:
            fileNameWithPath = os.path.join(catalog, fileName)
            metatag = EasyID3(fileNameWithPath)
            metatag['artist'] = artistName
            metatag.save()
            self.showMP3Info(fileNameWithPath)

        return filesList

    def setTrackNumber(self, fileNameWithPath, trackNumber):
        """
        set number of track for mp3 file

        :param fileNameWithPath: whole path for file; /home/music/Myslovitz/song.mp3
        :param ytackNumber: number of track for set;
        """
        if not os.path.isfile(fileNameWithPath):
            warningInfo="ERROR: file %s doesn't exist"%(fileNameWithPath)
            print (bcolors.FAIL + warningInfo + bcolors.ENDC)
            return
        metatag = EasyID3(fileNameWithPath)
        metatag['tracknumber'] = str(trackNumber)
        metatag.save()
        self.showMP3Info(fileNameWithPath)

    def setMetadata(self, fileName, title=None, artist=None, album=None, trackNumber=None, website=None):
        """
        set metadata for song. not all parameters need to be set

        :param fileName: whole path for file; /home/music/Myslovitz/song.mp3
        :param title: title
        :param artist: artist
        :param album: album
        :param trackNumber: number of track
        """

        if not os.path.isfile(fileName):
            print(bcolors.WARNING + "file doesn't exist: "+ fileName + bcolors.ENDC)
            return

        metatag = EasyID3(fileName)
        if title is not None:
            metatag['title'] = title
        if artist is not None:
            metatag['artist'] = artist
        if album is not None:
            metatag['album'] = album
        if trackNumber is not None:
            metatag['tracknumber'] = str(trackNumber)
        if website is not None:
            metatag['website'] = website

        metatag.save()
        print(bcolors.OKGREEN + "[ID3] Added metadata" + bcolors.ENDC)
        self.showMP3Info(fileName)

    def setMetadataArguments(self, fileName, **kwargs):
        """
        set metadata for song. put argument which one You want update

        :param fileName: whole path for file; /home/music/Myslovitz/song.mp3
        :param kwargs: key and value of parameter to set, (title, artist, album, artistalbum, tracknumber)
        """
        if not os.path.isfile(fileName):
            print(bcolors.WARNING + "file doesn't exist: "+ fileName + bcolors.ENDC)
            return
        availablesKeys = EasyID3.valid_keys.keys()
        availablesKeys = list(availablesKeys)
        metatag = EasyID3(fileName)
        for x in kwargs.items():
            if x[0] in availablesKeys:
                metatag[x[0]] = str(x[1])
            else:
                print(x[0], "is not available parameter")
        metatag.save()
        print(bcolors.OKGREEN + "[ID3] Added metadata" + bcolors.ENDC)
        self.showMP3Info(fileName)

if __name__ == "__main__":
    md = MetadataManager()
    md.showMP3InfoDir("/tmp/music/test")