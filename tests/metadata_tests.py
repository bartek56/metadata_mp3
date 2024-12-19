from curses import meta
import shutil
from unittest import TestCase
import sys
import os
import sys
import shutil
import unittest
from mutagen.easyid3 import EasyID3

import metadata_mp3

class TestRenameSongName(TestCase):
    songNameExpected = "Counting Crows - Colorblind"
    def setUp(self):
        self.metadata_mp3 = metadata_mp3.MetadataManager()

    def test_1_1(self):
        songNameBefore = "Counting Crows - Colorblind (Official Video) "
        songNameAfter = self.metadata_mp3._removeSheetFromSongName(songNameBefore)
        self.assertEqual(self.songNameExpected, songNameAfter)

    def test_1_2(self):
        songNameBefore = "Counting Crows - Colorblind ( ) "
        songNameAfter = self.metadata_mp3._removeSheetFromSongName(songNameBefore)
        self.assertEqual(self.songNameExpected, songNameAfter)

    def test_1_3(self):
        songNameBefore = "Counting Crows - Colorblind [] "
        songNameAfter = self.metadata_mp3._removeSheetFromSongName(songNameBefore)
        self.assertEqual(self.songNameExpected, songNameAfter)

    def test_2_1(self):
        songNameBefore = "Counting Crows - Colorblind test"
        songNameAfter = self.metadata_mp3._removeSheetFromSongName(songNameBefore)
        self.assertEqual(songNameBefore, songNameAfter)

class TestConvertSongnameOnMetadata(TestCase):
    def setUp(self):
        self.metadata_mp3 = metadata_mp3.MetadataManager()

    def checkArtistAndTitle(self, metadata:dict, artist, title):
        self.assertEqual(metadata['artist'], artist)
        self.assertEqual(metadata['title'], title)

    def test_1(self):
        songNameBefore = "Counting Crows - Colorblind"
        metadataSongName = self.metadata_mp3._convertSongnameOnMetadata(songNameBefore)
        self.checkArtistAndTitle(metadataSongName, "Counting Crows", "Colorblind")

    def test_2(self):
        songNameBefore = "Counting Crows - Colorblind test"
        metadataSongName = self.metadata_mp3._convertSongnameOnMetadata(songNameBefore)
        self.checkArtistAndTitle(metadataSongName, "Counting Crows", "Colorblind test")

    def test_3(self):
        songNameBefore = "Counting Crows-Colorblind"
        metadataSongName = self.metadata_mp3._convertSongnameOnMetadata(songNameBefore)
        self.checkArtistAndTitle(metadataSongName, "Counting Crows", "Colorblind")

    def test_4(self):
        songNameBefore = "Counting Crows-Colorblind-test"
        metadataSongName = self.metadata_mp3._convertSongnameOnMetadata(songNameBefore)
        self.checkArtistAndTitle(metadataSongName, "", songNameBefore)

    def test_5(self):
        songNameBefore = "Counting Crows - Colorblind-test"
        metadataSongName = self.metadata_mp3._convertSongnameOnMetadata(songNameBefore)
        self.checkArtistAndTitle(metadataSongName, "Counting Crows", "Colorblind-test")

    def test_6(self):
        songNameBefore = "Counting Crows - Colorblind - test"
        metadataSongName = self.metadata_mp3._convertSongnameOnMetadata(songNameBefore)
        self.checkArtistAndTitle(metadataSongName, "Counting Crows", "Colorblind-test")

    def test_removeSheet(self):
        songNameBefore = "Counting Crows - Colorblind (Official Video) []"
        songName = self.metadata_mp3._removeSheetFromSongName(songNameBefore)
        metadataSongName = self.metadata_mp3._convertSongnameOnMetadata(songName)
        self.checkArtistAndTitle(metadataSongName, "Counting Crows", "Colorblind")

class TestLookingForFileAccordWithYTFilename(TestCase):
    artist = "Counting Crows"
    def setUp(self):
        self.metadata_mp3 = metadata_mp3.MetadataManager()

    def tearDown(self):
        os.remove(self.testFileNameWithPath)

    def setTestFileName(self, testFileName):
        self.testFileName = testFileName
        self.testFileNameWithPath = self.renameTestFile(self.testFileName)
        self.songNameExpected = self.testFileName.replace(".mp3", "")

    def renameTestFile(self, testFileName):
        originalTestFileName = "test.mp3"

        self.currentDirectory = os.path.dirname(os.path.realpath(__file__))
        originalTestFileNameWithPath = os.path.join(self.currentDirectory,originalTestFileName)
        testFileNameWithPath = os.path.join(self.currentDirectory, testFileName)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)
        return testFileNameWithPath

    def test_1(self):
        self.setTestFileName("Counting Crows - Colorblind.mp3")
        title = "Colorblind"

        resultSongName = self.metadata_mp3.lookingForFileAccordWithYTFilename(self.currentDirectory, title, self.artist)

        self.assertEqual(resultSongName, self.songNameExpected)

    def test_2(self):
        self.setTestFileName("Counting Crows - Colorblind-test.mp3")
        title = "Colorblind-test"

        resultSongName = self.metadata_mp3.lookingForFileAccordWithYTFilename(self.currentDirectory, title, self.artist)

        self.assertEqual(resultSongName, self.songNameExpected)

    def test_3(self):
        self.setTestFileName("Colorblind.mp3")
        title = "Colorblind"

        resultSongName = self.metadata_mp3.lookingForFileAccordWithYTFilename(self.currentDirectory, title, self.artist)

        self.assertEqual(resultSongName, self.songNameExpected)

class TestAddMetadataSong(TestCase):
    title = "Colorblind"
    artist = "Counting Crows"
    artistEmpty = ""
    album="album"
    website="abcdefgh"
    date="2000-01-01"

    fileNameTitleTest = "Colorblind.mp3"
    fileNameTitleAndArtistTest = "Counting Crows - Colorblind.mp3"
    songNameTitleAndArtistTest = "Counting Crows - Colorblind"

    def setUp(self):
        self.metadata_mp3 = metadata_mp3.MetadataManager()

    def tearDown(self):
        testfileWithPath = os.path.join(self.currentDirectory, self.newFileNameWithPath)
        if os.path.isfile(testfileWithPath):
            os.remove(testfileWithPath)

    def renameFile(self, testFileName):
        originalTestFileName = "test.mp3"

        self.currentDirectory = os.path.dirname(os.path.realpath(__file__))
        originalTestFileNameWithPath = os.path.join(self.currentDirectory,originalTestFileName)
        testFileNameWithPath = os.path.join(self.currentDirectory, testFileName)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)
        return testFileNameWithPath

    def setInputParameters(self, title, artist, album, fileName, website=website, date=date):
        self.titleInput = title
        self.artistInput = artist
        self.albumInput = album
        self.fileNameInput = fileName
        self.songNameInput = fileName.replace(".mp3", "")
        self.website = website
        self.date=date

    def setExpectedParameters(self, title, artist, album, fileName):
        self.titleExpected = title
        self.artistExpected = artist
        self.albumExpected = album
        self.fileNameExpected = fileName

    def renameAndAddMetadataToSongCall(self):
        self.renameFile(self.fileNameInput)
        self.newFileNameWithPath = self.metadata_mp3.renameAndAddMetadataToSong(self.currentDirectory,
                                                                                self.albumInput,  self.artistInput, self.songNameInput, self.website, self.date)

    def checkSongMetadata(self, fileNameWithPath, isWebsite=True, isDate=True):
        self.assertTrue(os.path.isfile(fileNameWithPath))
        metatag = EasyID3(fileNameWithPath)
        self.assertIn('title', metatag)
        self.assertIn('artist', metatag)
        self.assertIn('album', metatag)
        if isWebsite:
            self.assertIn('website', metatag)
        else:
            self.assertNotIn('website', metatag)

        if isDate:
            self.assertIn('date', metatag)
        else:
            self.assertNotIn('date', metatag)

        self.assertEqual(metatag['title'][0], self.titleExpected)
        self.assertEqual(metatag['artist'][0], self.artistExpected)
        self.assertEqual(metatag['album'][0], self.albumExpected)
        if isWebsite:
            self.assertEqual(metatag['website'][0], self.website)
        if isDate:
            self.assertEqual(metatag['date'][0], self.date)
        self.assertEqual(fileNameWithPath, str(
            self.currentDirectory +"/"+ self.fileNameExpected))

    def checkSongMetadataWithoutArtist(self, fileNameWithPath):
        self.assertTrue(os.path.isfile(fileNameWithPath))
        metatag = EasyID3(fileNameWithPath)
        self.assertIn('title', metatag)
        self.assertNotIn('artist', metatag)
        self.assertIn('album', metatag)

        self.assertEqual(metatag['title'][0], self.titleExpected)
        self.assertEqual(metatag['album'][0], self.albumExpected)
        self.assertEqual(fileNameWithPath, str(
            self.currentDirectory +"/"+ self.fileNameExpected))

    def test_artistIsKnownFromInput(self):
        self.setInputParameters(self.title, self.artist, self.album, self.fileNameTitleTest)
        self.setExpectedParameters(self.title, self.artist, self.album, self.fileNameTitleAndArtistTest)

        self.renameAndAddMetadataToSongCall()

        self.checkSongMetadata(self.newFileNameWithPath)

    def test_artistIsKnownFromInput_fileExist(self):
        self.setInputParameters(self.title, self.artist, self.album, self.fileNameTitleTest)
        self.setExpectedParameters(self.title, self.artist, self.album, self.fileNameTitleAndArtistTest)

        self.renameAndAddMetadataToSongCall()
        oldFileNameWithPath = self.newFileNameWithPath
        self.checkSongMetadata(self.newFileNameWithPath)

        self.renameAndAddMetadataToSongCall()


        self.fileNameExpected = self.fileNameExpected.replace(".mp3", " (1).mp3")
        self.checkSongMetadata(self.newFileNameWithPath)

        # TODO
        os.remove(oldFileNameWithPath)

    def test_artistIsKnownFromFileAndFromInput(self):
        self.setInputParameters(self.title, self.artist, self.album, self.fileNameTitleAndArtistTest)
        self.setExpectedParameters(self.title, self.artist, self.album, self.fileNameTitleAndArtistTest)

        self.renameAndAddMetadataToSongCall()

        self.checkSongMetadata(self.newFileNameWithPath)

    def test_websiteIsEmpty(self):
        self.setInputParameters(self.title, self.artist, self.album, self.fileNameTitleAndArtistTest, website='')
        self.setExpectedParameters(self.title, self.artist, self.album, self.fileNameTitleAndArtistTest)

        self.renameAndAddMetadataToSongCall()

        self.checkSongMetadata(self.newFileNameWithPath, isWebsite=False)

    def test_dateIsEmpty(self):
        self.setInputParameters(self.title, self.artist, self.album, self.fileNameTitleAndArtistTest, date='')
        self.setExpectedParameters(self.title, self.artist, self.album, self.fileNameTitleAndArtistTest)

        self.renameAndAddMetadataToSongCall()

        self.checkSongMetadata(self.newFileNameWithPath,isDate=False)

    def test_artistIsKnownFromFileAndFromInput_removeSheed(self):
        fileNameTest = "Counting Crows - Colorblind (Official Video).mp3"
        self.setInputParameters(self.title, self.artist, self.album, fileNameTest)
        self.setExpectedParameters(self.title, self.artist, self.album, self.fileNameTitleAndArtistTest)

        self.renameAndAddMetadataToSongCall()

        self.checkSongMetadata(self.newFileNameWithPath)

    def test_artistIsKnownFromFile(self):
        self.setInputParameters(self.title, self.artistEmpty, self.album, self.fileNameTitleAndArtistTest)
        self.setExpectedParameters(self.title, self.artist, self.album, self.fileNameTitleAndArtistTest)

        self.renameAndAddMetadataToSongCall()

        self.checkSongMetadata(self.newFileNameWithPath)

    def test_artistIsNotKnown(self):
        self.setInputParameters(self.title, self.artistEmpty, self.album, self.fileNameTitleTest)
        self.setExpectedParameters(self.title, self.artistEmpty, self.album, self.fileNameTitleTest)

        self.renameAndAddMetadataToSongCall()

        self.checkSongMetadataWithoutArtist(self.newFileNameWithPath)

    def test_artistIsTooLong(self):

        artistTooLong = "Alan Walker, Sasha Alex Sloan, Alan Walker, Kasper, Alan Walker, Kristin Carpenter, Rasmus Budny, Fredrik Borch Olsen, Gunnar Greve, Marcus Arnbekk, Mats Lie Skåre, Kristin Carpenter, Rasmus Budny, Fredrik Borch Olsen, Gunnar Greve, Marcus Arnbekk, Mats Lie Skåre"
        artistTooLongExpected = "Alan Walker, Sasha Alex Sloan, Kasper, Kristin Carpenter, Rasmus Budny"

        fileNameTitleAndLongArtistTest = "%s - %s.mp3"%(artistTooLongExpected, self.title)

        self.setInputParameters(self.title, artistTooLong, self.album, self.fileNameTitleTest)
        self.setExpectedParameters(self.title, artistTooLongExpected, self.album, fileNameTitleAndLongArtistTest)

        self.renameAndAddMetadataToSongCall()

        self.checkSongMetadata(self.newFileNameWithPath)

class TestAddMetadataPlaylist(TestCase):
    playlistName = "spokojne-sad"
    title = "Colorblind"
    artist = "Counting Crows"
    album = "album test"
    website = "abcdefghijk"
    date="2000-01-01"

    trackNumber = 1
    artistEmpty = ""
    albumEmpty=""

    fileNameTitleTest = "Colorblind.mp3"
    fileNameTitleAndArtistTest = "Counting Crows - Colorblind.mp3"
    songNameTitleAndArtistTest = "Counting Crows - Colorblind"
    trackNumberStr = str(trackNumber)

    def setUp(self):
        self.metadata_mp3 = metadata_mp3.MetadataManager()
        self.currentDirectory = os.path.dirname(os.path.realpath(__file__))

    def tearDown(self):
        testfileWithPath = os.path.join(self.currentDirectory, self.playlistName)
        if os.path.isdir(testfileWithPath):
            shutil.rmtree(testfileWithPath)

    def setInputParameters(self, title, artist, album, fileName, website=website):
        self.titleInput = title
        self.artistInput = artist
        self.albumInput = album
        self.fileNameInput = fileName
        self.songNameInput = fileName.replace(".mp3", "")
        self.website = website

    def setExpectedParameters(self, title, artist, fileName):
        self.titleExpected = title
        self.artistExpected = artist
        self.fileNameExpected = fileName

    def renameFile(self, testFileName, albumTest):
        originalTestFileName = "test.mp3"

        self.currentDirectory = os.path.dirname(os.path.realpath(__file__))
        originalTestFileNameWithPath = os.path.join(self.currentDirectory, originalTestFileName)
        albumDirectory = os.path.join(self.currentDirectory, albumTest)

        if not os.path.exists(albumDirectory):
            os.mkdir(albumDirectory)

        testFileNameWithPath = os.path.join(self. currentDirectory, albumTest, testFileName)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)

        return testFileNameWithPath

    def checkMetadataFromPlaylistFile(self, fileNameWithPath, artistExist=True, artistAlbumExist=True):
        self.assertTrue(os.path.isfile(fileNameWithPath))
        metatag = EasyID3(fileNameWithPath)
        self.assertIn('title', metatag)
        self.assertIn('website', metatag)
        if artistExist:
            self.assertIn('artist', metatag)
        else:
             self.assertNotIn('artist', metatag)
        self.assertIn('album', metatag)
        if artistAlbumExist:
            self.assertIn('albumartist', metatag)
        else:
            self.assertNotIn('albumartist', metatag)
        self.assertIn('tracknumber', metatag)

        self.assertEqual(metatag['title'][0], self.titleExpected)
        if artistExist:
            self.assertEqual(metatag['artist'][0], self.artistExpected)
        self.assertEqual(metatag['album'][0], "YT "+ self.playlistName)
        if artistAlbumExist:
            self.assertEqual(metatag['albumartist'][0], self.album)
        self.assertEqual(metatag['tracknumber'][0], self.trackNumberStr)
        self.assertEqual(metatag["website"][0], self.website)
        self.assertEqual(fileNameWithPath, str(
            self.currentDirectory+"/"+self.playlistName + "/" +self.fileNameExpected))

    def renameAndAddMetadataToPlatlistCall(self):
        self.renameFile(self.fileNameInput, self.playlistName)
        return self.metadata_mp3.renameAndAddMetadataToPlaylist(
            self.currentDirectory, 1, self.playlistName, self.artistInput, self.albumInput, self.songNameInput, self.website, self.date)

    def test_artistIsKnownFromInput(self):
        self.setInputParameters(self.title, self.artist, self.album, self.fileNameTitleTest)
        self.setExpectedParameters(self.title, self.artist, self.fileNameTitleAndArtistTest)

        newFileNameWithPath = self.renameAndAddMetadataToPlatlistCall()

        self.checkMetadataFromPlaylistFile(newFileNameWithPath)

    def test_artistIsKnownFromFileAndFromInputRemoveSheet(self):
        fileNameTest = str(self.artist + " - " + self.title + " (Official Video).mp3")
        self.setInputParameters(self.title, self.artist, self.album, fileNameTest)
        self.setExpectedParameters(self.title, self.artist, str(self.artist + " - " + self.title+".mp3"))

        newFileNameWithPath = self.renameAndAddMetadataToPlatlistCall()

        self.checkMetadataFromPlaylistFile(newFileNameWithPath)

    def test_artistIsKnownFromFileAndFromInput(self):
        self.setInputParameters(self.title, self.artist, self.album, self.fileNameTitleAndArtistTest)
        self.setExpectedParameters(self.title, self.artist, self.fileNameTitleAndArtistTest)

        newFileNameWithPath = self.renameAndAddMetadataToPlatlistCall()

        self.checkMetadataFromPlaylistFile(newFileNameWithPath)

    def test_artistIsKnownFromFile(self):
        self.setInputParameters(self.title, self.artistEmpty, self.album, self.fileNameTitleAndArtistTest)
        self.setExpectedParameters(self.title, self.artist, self.fileNameTitleAndArtistTest)

        newFileNameWithPath = self.renameAndAddMetadataToPlatlistCall()

        self.checkMetadataFromPlaylistFile(newFileNameWithPath)

    def test_artistIsNotKnown(self):
        self.setInputParameters(self.title, self.artistEmpty, self.album, self.fileNameTitleTest)
        self.setExpectedParameters(self.title, self.artistEmpty, self.fileNameTitleTest)

        newFileNameWithPath = self.renameAndAddMetadataToPlatlistCall()

        self.checkMetadataFromPlaylistFile(newFileNameWithPath, artistExist=False)

    def test_artistIsTooLong(self):
        artistTooLong = "aaaaaaaaaa bbbbbbbbbbb cccccccccc dddddddddd eeeeeeeeee fffffffff gggggggg hhhhhh iiiiiiii jjjjjjjj"
        artistTooLongExpected = "aaaaaaaaaa bbbbbbbbbbb cccccccccc dddddddddd eeeeeeeeee fffffffff gggggggg"
        fileNameTitleAndLongArtistTest = "%s - %s.mp3"%(artistTooLongExpected, self.title)

        self.setInputParameters(self.title, artistTooLong, self.album, self.fileNameTitleTest)
        self.setExpectedParameters(self.title, artistTooLongExpected, fileNameTitleAndLongArtistTest)

        newFileNameWithPath = self.renameAndAddMetadataToPlatlistCall()

        self.checkMetadataFromPlaylistFile(newFileNameWithPath)

    def test_artistIsTooLong2(self):
        artistTooLong = "aaaaaaaaaa, bbbbbbbbbbb, cccccccccc, dddddddddd, eeeeeeeeee, fffffffff, gggggggg, hhhhhh, iiiiiiii, jjjjjjjj"
        artistTooLongExpected = "aaaaaaaaaa, bbbbbbbbbbb, cccccccccc, dddddddddd, eeeeeeeeee, fffffffff, gggggggg"
        fileNameTitleAndLongArtistTest = "%s - %s.mp3"%(artistTooLongExpected, self.title)

        self.setInputParameters(self.title, artistTooLong, self.album, self.fileNameTitleTest)
        self.setExpectedParameters(self.title, artistTooLongExpected, fileNameTitleAndLongArtistTest)

        newFileNameWithPath = self.renameAndAddMetadataToPlatlistCall()

        self.checkMetadataFromPlaylistFile(newFileNameWithPath)

    def test_artistIsTooLongDuplicates1(self):
        artistTooLong = "aaaaaaaaaa, bbbbbbbbbbb, cccccccccc, dddddddddd, bbbbbbbbbbb, bbbbbbbbbbb, gggggggg, hhhhhh, iiiiiiii, bbbbbbbbbbb"
        artistTooLongExpected = "aaaaaaaaaa, bbbbbbbbbbb, cccccccccc, dddddddddd, gggggggg, hhhhhh, iiiiiiii"
        fileNameTitleAndLongArtistTest = "%s - %s.mp3"%(artistTooLongExpected, self.title)

        self.setInputParameters(self.title, artistTooLong, self.album, self.fileNameTitleTest)
        self.setExpectedParameters(self.title, artistTooLongExpected, fileNameTitleAndLongArtistTest)

        newFileNameWithPath = self.renameAndAddMetadataToPlatlistCall()

        self.checkMetadataFromPlaylistFile(newFileNameWithPath)

    def test_artistIsTooLongDuplicates2(self):
        artistTooLong = "aaaaaaaaaa cccccccccc bbbbbbbbbbb cccccccccc dddddddddd bbbbbbbbbbb bbbbbbbbbbb gggggggg hhhhhh iiiiiiii bbbbbbbbbbb"
        artistTooLongExpected = "aaaaaaaaaa cccccccccc bbbbbbbbbbb dddddddddd gggggggg hhhhhh iiiiiiii"
        fileNameTitleAndLongArtistTest = "%s - %s.mp3"%(artistTooLongExpected, self.title)

        self.setInputParameters(self.title, artistTooLong, self.album, self.fileNameTitleTest)
        self.setExpectedParameters(self.title, artistTooLongExpected, fileNameTitleAndLongArtistTest)

        newFileNameWithPath = self.renameAndAddMetadataToPlatlistCall()

        self.checkMetadataFromPlaylistFile(newFileNameWithPath)

    def test_artistIsTooLongDuplicates3(self):
        artistTooLong = "aa, aa, cccc, bbbb"
        artistTooLongExpected = "aa, cccc, bbbb"
        fileNameTitleAndLongArtistTest = "%s - %s.mp3"%(artistTooLongExpected, self.title)

        self.setInputParameters(self.title, artistTooLong, self.album, self.fileNameTitleTest)
        self.setExpectedParameters(self.title, artistTooLongExpected, fileNameTitleAndLongArtistTest)

        newFileNameWithPath = self.renameAndAddMetadataToPlatlistCall()

        self.checkMetadataFromPlaylistFile(newFileNameWithPath)

    def test_artistIsTooLong4(self):
        artistTooLong = "aaaaaaaaaa, bbbbbbbbbbb, cccccccccc, dddddddddd, eeeeeeeeee, fffffffffff, ggggggggggg, hhhhhh, iiiiiiii, jjjjjjjj, "
        artistTooLongExpected = "aaaaaaaaaa, bbbbbbbbbbb, cccccccccc, dddddddddd, eeeeeeeeee, fffffffffff"
        fileNameTitleAndLongArtistTest = "%s - %s.mp3"%(artistTooLongExpected, self.title)

        self.setInputParameters(self.title, artistTooLong, self.album, self.fileNameTitleTest)
        self.setExpectedParameters(self.title, artistTooLongExpected, fileNameTitleAndLongArtistTest)

        newFileNameWithPath = self.renameAndAddMetadataToPlatlistCall()

        self.checkMetadataFromPlaylistFile(newFileNameWithPath)

    def test_artistIsTooLong5(self):
        artistTooLong = "Alan Walker, Sasha Alex Sloan, Alan Walker, Kasper, Alan Walker"
        artistTooLongExpected = "Alan Walker, Sasha Alex Sloan, Kasper"
        fileNameTitleAndLongArtistTest = "%s - %s.mp3"%(artistTooLongExpected, self.title)

        self.setInputParameters(self.title, artistTooLong, self.album, self.fileNameTitleTest)
        self.setExpectedParameters(self.title, artistTooLongExpected, fileNameTitleAndLongArtistTest)

        newFileNameWithPath = self.renameAndAddMetadataToPlatlistCall()

        self.checkMetadataFromPlaylistFile(newFileNameWithPath)

    def test_cutShortSongName(self):
        result = self.metadata_mp3._cutLenght("aaaaaaaaaaaaaaaaaa", 4)
        self.assertEqual(result, "aaaa")

    def test_artistalbumIsNotKnown(self):
        self.setInputParameters(self.title, self.artist, self.albumEmpty, self.fileNameTitleTest)
        self.setExpectedParameters(self.title, self.artist, self.fileNameTitleAndArtistTest)

        newFileNameWithPath = self.renameAndAddMetadataToPlatlistCall()

        self.checkMetadataFromPlaylistFile(newFileNameWithPath, artistAlbumExist=False)

class TestUpdateMetadataYoutube(TestCase):
    def setUp(self):
        self.metadata_mp3 = metadata_mp3.MetadataManager()

    def test_1(self):
        originalTestFileName = "test.mp3"
        testFileName1 = "Counting Crows - Colorblind.mp3"
        testFileName2 = "Eels - I Need Some Sleep.mp3"
        testFileName3 = "Paramore - The Only Exception.mp3"
        artistTestList = []
        artistTestList.append("Counting Crows")
        titleTestList = []
        titleTestList.append("Colorblind")
        artistTestList.append("Eels")
        titleTestList.append("I Need Some Sleep")
        artistTestList.append("Paramore")
        titleTestList.append("The Only Exception")
        albumTest = "spokojne-sad"

        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        originalTestFileNameWithPath = os.path.join(currentDirectory,originalTestFileName)
        albumDirectory = os.path.join(currentDirectory,albumTest)


        if not os.path.exists(albumDirectory):
            os.mkdir(albumDirectory)
        testFileNameWithPath = os.path.join(currentDirectory,albumTest, testFileName1)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)
        testFileNameWithPath = os.path.join(currentDirectory,albumTest, testFileName2)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)
        testFileNameWithPath = os.path.join(currentDirectory,albumTest, testFileName3)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)

        newFilesList = self.metadata_mp3.updateMetadataYoutube(currentDirectory,albumTest)
        i = 0
        for newFile in newFilesList:
            self.assertTrue(os.path.isfile(newFile))
            metatag = EasyID3(newFile)

            self.assertEqual(metatag['artist'][0], artistTestList[i])
            self.assertEqual(metatag['title'][0], titleTestList[i])
            self.assertEqual(metatag['album'][0], "YT "+albumTest)

            i = i+1

        shutil.rmtree(os.path.join(currentDirectory,albumTest))

class TestUpdateMetadata(TestCase):

    def setUp(self):
        self.metadata_mp3 = metadata_mp3.MetadataManager()

    def test_1(self):
        originalTestFileName = "test.mp3"
        testFileName1 = "Counting Crows - Colorblind.mp3"
        testFileName2 = "Eels - I Need Some Sleep.mp3"
        testFileName3 = "Paramore - The Only Exception.mp3"
        artistTestList = []
        artistTestList.append("Counting Crows")
        titleTestList = []
        titleTestList.append("Colorblind")
        artistTestList.append("Eels")
        titleTestList.append("I Need Some Sleep")
        artistTestList.append("Paramore")
        titleTestList.append("The Only Exception")
        albumTest = "spokojne-sad"

        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        originalTestFileNameWithPath = os.path.join(currentDirectory,originalTestFileName)
        albumDirectory = os.path.join(currentDirectory, albumTest)


        if not os.path.exists(albumDirectory):
            os.mkdir(albumDirectory)
        testFileNameWithPath = os.path.join(currentDirectory, albumTest, testFileName1)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)
        testFileNameWithPath = os.path.join(currentDirectory, albumTest, testFileName2)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)
        testFileNameWithPath = os.path.join(currentDirectory, albumTest, testFileName3)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)

        newFilesList = self.metadata_mp3.updateMetadata(albumDirectory, albumTest)
        i = 0
        for newFile in newFilesList:
            print(newFile)
            self.assertTrue(os.path.isfile(newFile))
            metatag = EasyID3(newFile)

            self.assertEqual(metatag['artist'][0], artistTestList[i])
            self.assertEqual(metatag['title'][0], titleTestList[i])
            self.assertEqual(metatag['album'][0], albumTest)

            i = i+1

        shutil.rmtree(os.path.join(currentDirectory,albumTest))

    def test_UpdateIsNotNeeded(self):
        originalTestFileName = "test.mp3"
        testFileName1 = "Counting Crows - Colorblind.mp3"
        testFileName2 = "Eels - I Need Some Sleep.mp3"
        testFileName3 = "Paramore - The Only Exception.mp3"
        artistTestList = []
        artistTestList.append("Counting Crows")
        titleTestList = []
        titleTestList.append("Colorblind")
        artistTestList.append("Eels")
        titleTestList.append("I Need Some Sleep")
        artistTestList.append("Paramore")
        titleTestList.append("The Only Exception")
        albumTest = "spokojne-sad"

        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        originalTestFileNameWithPath = os.path.join(currentDirectory,originalTestFileName)
        albumDirectory = os.path.join(currentDirectory, albumTest)


        if not os.path.exists(albumDirectory):
            os.mkdir(albumDirectory)
        testFileNameWithPath = os.path.join(currentDirectory, albumTest, testFileName1)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)
        testFileNameWithPath = os.path.join(currentDirectory, albumTest, testFileName2)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)
        testFileNameWithPath = os.path.join(currentDirectory, albumTest, testFileName3)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)

        newFilesList = self.metadata_mp3.updateMetadata(albumDirectory, albumTest)
        i = 0
        for newFile in newFilesList:
            print(newFile)
            self.assertTrue(os.path.isfile(newFile))
            metatag = EasyID3(newFile)

            self.assertEqual(metatag['artist'][0], artistTestList[i])
            self.assertEqual(metatag['title'][0], titleTestList[i])
            self.assertEqual(metatag['album'][0], albumTest)

            i = i+1
        newFilesList = self.metadata_mp3.updateMetadata(albumDirectory, albumTest)
        self.assertEqual(len(newFilesList), 0)


        shutil.rmtree(os.path.join(currentDirectory,albumTest))

class TestSetAlbum(TestCase):
    def setUp(self):
        self.metadata_mp3 = metadata_mp3.MetadataManager()


    def test_1(self):
        originalTestFileName = "test.mp3"
        testFileName1 = "test1.mp3"
        testFileName2 = "test2.mp3"
        testCatalog = "test_1"

        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        originalTestFileNameWithPath = os.path.join(currentDirectory,originalTestFileName)
        testCatalogWithPath = os.path.join(currentDirectory, testCatalog)


        if not os.path.exists(testCatalogWithPath):
            os.mkdir(testCatalogWithPath)
        testFileNameWithPath = os.path.join(currentDirectory,testCatalog, testFileName1)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)
        testFileNameWithPath = os.path.join(currentDirectory,testCatalog, testFileName2)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)

        newFilesList = self.metadata_mp3.setAlbum(testCatalogWithPath, "album test")
        for newFile in newFilesList:
            newFileWithPath = os.path.join(testCatalogWithPath,newFile)
            self.assertTrue(os.path.isfile(newFileWithPath))
            metatag = EasyID3(newFileWithPath)
            self.assertEqual(metatag['album'][0], "album test")


        shutil.rmtree(os.path.join(currentDirectory,testCatalog))

class TestSetArtist(TestCase):
    def setUp(self):
        self.metadata_mp3 = metadata_mp3.MetadataManager()

    def test_1(self):
        originalTestFileName = "test.mp3"
        testFileName1 = "test1.mp3"
        testFileName2 = "test2.mp3"
        testCatalog = "test_1"

        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        originalTestFileNameWithPath = os.path.join(currentDirectory,originalTestFileName)
        testCatalogWithPath = os.path.join(currentDirectory, testCatalog)


        if not os.path.exists(testCatalogWithPath):
            os.mkdir(testCatalogWithPath)
        testFileNameWithPath = os.path.join(currentDirectory,testCatalog, testFileName1)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)
        testFileNameWithPath = os.path.join(currentDirectory,testCatalog, testFileName2)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)

        newFilesList = self.metadata_mp3.setArtist(testCatalogWithPath, "artist test")
        for newFile in newFilesList:
            newFileWithPath = os.path.join(testCatalogWithPath,newFile)
            self.assertTrue(os.path.isfile(newFileWithPath))
            metatag = EasyID3(newFileWithPath)
            self.assertEqual(metatag['artist'][0], "artist test")

        shutil.rmtree(os.path.join(currentDirectory,testCatalog))

class TestSetMetadata(TestCase):
    def setUp(self):
        self.metadata_mp3 = metadata_mp3.MetadataManager()

    def test_1(self):
        originalTestFileName = "test.mp3"
        testFileName = "test1.mp3"
        testCatalog = "test_1"

        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        originalTestFileNameWithPath = os.path.join(currentDirectory,originalTestFileName)
        testCatalogWithPath = os.path.join(currentDirectory, testCatalog)

        if not os.path.exists(testCatalogWithPath):
            os.mkdir(testCatalogWithPath)
        testFileNameWithPath = os.path.join(currentDirectory,testCatalog, testFileName)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)

        self.metadata_mp3.setMetadata(testFileNameWithPath, "title test", "artist test", "album test", 5)

        metatag = EasyID3(testFileNameWithPath)
        self.assertEqual(metatag['title'][0], "title test")
        self.assertEqual(metatag['artist'][0], "artist test")
        self.assertEqual(metatag['album'][0], "album test")
        self.assertEqual(metatag['tracknumber'][0], "5")

        shutil.rmtree(os.path.join(currentDirectory,testCatalog))

class TestSetMetadataArguments(TestCase):
    def setUp(self):
        self.metadata_mp3 = metadata_mp3.MetadataManager()

    def test_1(self):
        originalTestFileName = "test.mp3"
        testFileName = "test1.mp3"
        testCatalog = "test_1"

        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        originalTestFileNameWithPath = os.path.join(currentDirectory,originalTestFileName)
        testCatalogWithPath = os.path.join(currentDirectory, testCatalog)

        if not os.path.exists(testCatalogWithPath):
            os.mkdir(testCatalogWithPath)
        testFileNameWithPath = os.path.join(currentDirectory,testCatalog, testFileName)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)

        self.metadata_mp3.setMetadataArguments(testFileNameWithPath, title="title test", artist="artist test", album="album test", dfdfds="dsfd", tracknumber=5)

        metatag = EasyID3(testFileNameWithPath)
        self.assertEqual(metatag['title'][0], "title test")
        self.assertEqual(metatag['artist'][0], "artist test")
        self.assertEqual(metatag['album'][0], "album test")
        self.assertEqual(metatag['tracknumber'][0], "5")

        shutil.rmtree(os.path.join(currentDirectory,testCatalog))

if __name__=='__main__':
    unittest.main()
