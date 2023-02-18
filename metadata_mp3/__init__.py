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


class MetadataManager:

    def showMP3Info(self, fileNameWithPath):
        print (bcolors.OKGREEN + fileNameWithPath + bcolors.ENDC)
        audio = MP3(fileNameWithPath, ID3=EasyID3)
        print (audio.pprint())


    def remove_sheet_from_songName(self, songName):

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

    def remove_sheet_from_filename(self, path, originalFileName):

        ext = ".mp3"

        fileNameWithoutExtension = originalFileName.replace(ext, "")

        fileNameWithoutExtension = self.remove_sheet_from_songName(fileNameWithoutExtension)
        fileNameWithExtension = "%s%s"%(fileNameWithoutExtension, ext)

        originalFileNameWithPath=os.path.join(path, originalFileName)
        fileNameWithPath = os.path.join(path, fileNameWithExtension)
        os.rename(originalFileNameWithPath, fileNameWithPath)

        return fileNameWithExtension

    def convert_songname_on_metadata(self, songName):
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
    def rename_and_add_metadata_to_song(self, MUSIC_PATH, albumName, artist, songName):
        path=MUSIC_PATH

        mp3ext=".mp3"
        fileName="%s%s"%(songName,mp3ext)

        if not os.path.isfile(os.path.join(path, fileName)):
            warningInfo="WARNING: %s not exist"%(fileName)
            print (bcolors.WARNING + warningInfo + bcolors.ENDC)
            return

        #rename song file to remove useless text
        fileName = self.remove_sheet_from_filename(path, fileName)
        songName = fileName.replace(mp3ext, "")

        # if songName doesn't contain artist and artist is known
        # rename filename
        if not " - " in songName and len(artist)>1:
            originalFileNameWithPath = os.path.join(path, fileName)
            newFileName = "%s - %s%s"%(artist, songName, mp3ext)
            newFileNameWithPath = os.path.join(path, newFileName)
            os.rename(originalFileNameWithPath, newFileNameWithPath)
            fileName=newFileName
            title = songName
        # artist is known from file and from input
        elif " - " in songName and len(artist)>1:
            metadataSongName = self.convert_songname_on_metadata(songName)
            title = metadataSongName['title']
            newFileName = "%s - %s%s"%(artist, title, mp3ext)
            newFileNameWithPath = os.path.join(path, newFileName)
            originalFileNameWithPath = os.path.join(path, fileName)
            os.rename(originalFileNameWithPath, newFileNameWithPath)
            fileName=newFileName
        # get artist from filename, when we do not know artist
        elif " - " in songName and (artist is None or len(artist)==0):
            # get metadata from filename
            metadataSongName = self.convert_songname_on_metadata(songName)
            newFileNameWithPath = os.path.join(path, newFileName)
            artist = metadataSongName['artist']
            title = metadataSongName['title']
        # artist is unknown
        elif not " - " in songName and (artist is None or len(artist)==0):
            warningInfo="WARNING: artist for song %s is not known"%(songName)
            print (bcolors.WARNING + warningInfo + bcolors.ENDC)
            title = songName
            artist = None
        else:
            warningInfo="ERROR: Unknown situation with songname"
            print (bcolors.FAIL + warningInfo + bcolors.ENDC)
            return

        # saving metadata
        metatag = EasyID3(newFileNameWithPath)
        if albumName is not None:
            metatag['album'] = albumName
        if artist is not None:
            metatag['artist'] = artist
        metatag['title'] = title
        metatag.save()
        print (bcolors.OKGREEN + "[ID3] Added metadata" + bcolors.ENDC)
        print (newFileNameWithPath)
        audio = MP3(newFileNameWithPath, ID3=EasyID3)
        print (audio.pprint())
        return newFileNameWithPath

    def lookingForFileAccordWithYTFilename(self, path, songName, artist):
        mp3ext=".mp3"

        songName = songName.replace("-", " - ")
        fileName="%s%s"%(songName,mp3ext)
        if os.path.isfile(os.path.join(path, fileName)):
            return songName

        songName = self.remove_sheet_from_songName(songName)
        fileName="%s%s"%(songName,mp3ext)

        if os.path.isfile(os.path.join(path, fileName)):
            return songName

        songName = "%s - %s"%(artist, songName)
        fileName="%s%s"%(songName,mp3ext)
        if os.path.isfile(os.path.join(path, fileName)):
            return songName
        else:
            return None

    # youtubedl
    def add_metadata_playlist(self, PLAYLISTS_PATH, trackNumber, playlistName, artist, songName):
        path=os.path.join(PLAYLISTS_PATH,playlistName)
        albumName="YT "+playlistName

        mp3ext=".mp3"
        fileName="%s%s"%(songName,mp3ext)

        if not os.path.isfile(os.path.join(path, fileName)):
            songName = songName.replace("-", " - ")
            fileName="%s%s"%(songName,mp3ext)
            if not os.path.isfile(os.path.join(path, fileName)):
                songName = self.remove_sheet_from_songName(songName)
                fileName="%s%s"%(songName,mp3ext)
            if not os.path.isfile(os.path.join(path, fileName)):
                fileName="%s - %s%s"%(artist, songName, mp3ext)
            if not os.path.isfile(os.path.join(path, fileName)):
                warningInfo="WARNING: %s not exist"%(fileName)
                print (bcolors.WARNING + warningInfo + bcolors.ENDC)
                return

        if not " - " in songName and len(artist)>1:
            originalFileNameWithPath = os.path.join(path, fileName)
            newFileName = "%s - %s%s"%(artist, songName, mp3ext)
            newFileNameWithPath = os.path.join(path, newFileName)
            os.rename(originalFileNameWithPath, newFileNameWithPath)
            fileName=newFileName

        newFileName = self.remove_sheet_from_filename(path, fileName)
        newSongName = newFileName.replace(mp3ext, "")

        metadataSongName = self.convert_songname_on_metadata(newSongName)
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

    def update_metadata_youtube(self, PLAYLISTS_PATH, playlistName):
        path=os.path.join(PLAYLISTS_PATH,playlistName)
        albumName="YT "+playlistName
        newFilesList = []

        filesList = [f for f in os.listdir(path) if f.endswith(".mp3")]
        filesList.sort()
        for x in range(len(filesList)):
            originalFileName = filesList[x]

            newFileName = self.remove_sheet_from_filename(path, originalFileName)
            newSongName = newFileName.replace(".mp3", "")

            metadataSongName = self.convert_songname_on_metadata(newSongName)
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

    def update_metadata(self, catalog, albumName):
        newFilesList = []

        filesList = [f for f in os.listdir(catalog) if f.endswith(".mp3")]
        filesList.sort()
        for x in range(len(filesList)):
            originalFileName = filesList[x]

            newFileName = self. remove_sheet_from_filename(catalog, originalFileName)
            newSongName = newFileName.replace(".mp3", "")

            metadataSongName = self.convert_songname_on_metadata(newSongName)
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
        filesList = [f for f in os.listdir(catalog) if f.endswith(".mp3")]
        filesList.sort()
        for fileName in filesList:
            fileNameWithPath = os.path.join(catalog, fileName)
            metatag = EasyID3(fileNameWithPath)
            metatag['album'] = albumName
            metatag.save()
            self.showMP3Info(fileNameWithPath)

        return filesList

    def setArtist(self, catalog, artistName):
        filesList = [f for f in os.listdir(catalog) if f.endswith(".mp3")]
        filesList.sort()
        for fileName in filesList:
            print(fileName)
            fileNameWithPath = os.path.join(catalog, fileName)
            metatag = EasyID3(fileNameWithPath)
            metatag['artist'] = artistName
            metatag.save()
            self.showMP3Info(fileNameWithPath)

        return filesList
