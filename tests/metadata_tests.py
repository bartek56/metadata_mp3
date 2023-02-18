from curses import meta
import shutil
from unittest import TestCase
import sys
import os
import sys
import shutil
import unittest
from mutagen.easyid3 import EasyID3

sys.path.append("..")
import metadata_mp3


class TestRenameSongName(TestCase):
    def setUp(self):
        self.metadata_mp3 = metadata_mp3.MetadataManager()

    def test_1_1(self):
        songNameBefore = "Counting Crows - Colorblind (Official Video) "
        songNameAfter = "Counting Crows - Colorblind"
        songNameAfterTest = self.metadata_mp3.remove_sheet_from_songName(songNameBefore)
        self.assertEqual(songNameAfter, songNameAfterTest)

    def test_1_2(self):
        songNameBefore = "Counting Crows - Colorblind ( ) "
        songNameAfter = "Counting Crows - Colorblind"
        songNameAfterTest = self.metadata_mp3.remove_sheet_from_songName(songNameBefore)
        self.assertEqual(songNameAfter, songNameAfterTest)

    def test_1_2(self):
        songNameBefore = "Counting Crows - Colorblind [] "
        songNameAfter = "Counting Crows - Colorblind"
        songNameAfterTest = self.metadata_mp3.remove_sheet_from_songName(songNameBefore)
        self.assertEqual(songNameAfter, songNameAfterTest)

    def test_2_1(self):
        songNameBefore = "Counting Crows - Colorblind test"
        songNameAfter = "Counting Crows - Colorblind"
        songNameAfterTest = self.metadata_mp3.remove_sheet_from_songName(songNameBefore)
        self.assertNotEqual(songNameAfter, songNameAfterTest)

class TestConvertSongnameOnMetadata(TestCase):
    def setUp(self):
        self.metadata_mp3 = metadata_mp3.MetadataManager()

    def test_1(self):
        songNameBefore = "Counting Crows - Colorblind"
        metadataSongName = self.metadata_mp3.convert_songname_on_metadata(songNameBefore)
        self.assertEqual(metadataSongName['artist'], "Counting Crows")
        self.assertEqual(metadataSongName['title'], "Colorblind")

    def test_2(self):
        songNameBefore = "Counting Crows - Colorblind test"
        metadataSongName = self.metadata_mp3.convert_songname_on_metadata(songNameBefore)
        self.assertEqual(metadataSongName['artist'], "Counting Crows")
        self.assertEqual(metadataSongName['title'], "Colorblind test")

    def test_3(self):
        songNameBefore = "Counting Crows - Colorblind (Official Video) []"
        songName = self.metadata_mp3.remove_sheet_from_songName(songNameBefore)
        metadataSongName = self.metadata_mp3.convert_songname_on_metadata(songName)
        self.assertEqual(metadataSongName['artist'], "Counting Crows")
        self.assertEqual(metadataSongName['title'], "Colorblind")

class TestLookingForFileAccordWithYTFilename(TestCase):
    def setUp(self):
        self.metadata_mp3 = metadata_mp3.MetadataManager()

    def renameTestFile(self, testFileName):
        originalTestFileName = "test.mp3"

        self.currentDirectory = os.path.dirname(os.path.realpath(__file__))
        originalTestFileNameWithPath = os.path.join(self.currentDirectory,originalTestFileName)
        testFileNameWithPath = os.path.join(self.currentDirectory, testFileName)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)
        return testFileNameWithPath

    def test_1(self):
        testFileName = "Counting Crows - Colorblind.mp3"
        testFileNameWithPath = self.renameTestFile(testFileName)
        songName = "Counting Crows - Colorblind"
        artist = "Counting Crows"

        resultSongName = self.metadata_mp3.lookingForFileAccordWithYTFilename(self.currentDirectory, songName, artist)
        self.assertEqual(resultSongName, songName)
        os.remove(testFileNameWithPath)


class TestAddMetadataSong(TestCase):

    def setUp(self):
        self.metadata_mp3 = metadata_mp3.MetadataManager()

    def renameTestFile(self, testFileName):
        originalTestFileName = "test.mp3"

        self.currentDirectory = os.path.dirname(os.path.realpath(__file__))
        originalTestFileNameWithPath = os.path.join(self.currentDirectory,originalTestFileName)
        testFileNameWithPath = os.path.join(self.currentDirectory, testFileName)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)
        return testFileNameWithPath

    def test_1(self):
        testFileName = "Counting Crows - Colorblind.mp3"
        testFileNameWithPath = self.renameTestFile(testFileName)

        songNameTest = "Counting Crows - Colorblind"
        artistTest = "Counting Crows"
        titleTest = "Colorblind"
        albumTest = "album test"

        newFileNameWithPath = self.metadata_mp3.rename_and_add_metadata_to_song(self.currentDirectory, albumTest, artistTest, songNameTest)
        metatag = EasyID3(newFileNameWithPath)
        self.assertTrue(os.path.isfile(newFileNameWithPath))
        self.assertEqual(newFileNameWithPath, testFileNameWithPath)


        self.assertEqual(metatag['artist'][0], artistTest)
        self.assertEqual(metatag['title'][0], titleTest)
        self.assertEqual(metatag['album'][0], albumTest)
        os.remove(newFileNameWithPath)

    def test_2(self):
        fileNameTest = "Counting Crows - Colorblind (Official Video).mp3"
        testFileNameWithPath = self.renameTestFile(fileNameTest)

        songNameTest = "Counting Crows - Colorblind (Official Video)"
        artistTest = "Counting Crows"
        titleTest = "Colorblind"
        albumTest = "album test"

        newFileNameWithPath = self.metadata_mp3.rename_and_add_metadata_to_song(self.currentDirectory, albumTest, artistTest, songNameTest)
        self.assertFalse(os.path.isfile(testFileNameWithPath))
        self.assertTrue(os.path.isfile(newFileNameWithPath))
        self.assertNotEqual(newFileNameWithPath, testFileNameWithPath)

        metatag = EasyID3(newFileNameWithPath)

        self.assertEqual(metatag['artist'][0], artistTest)
        self.assertEqual(metatag['title'][0], titleTest)
        self.assertEqual(metatag['album'][0], albumTest)
        os.remove(newFileNameWithPath)

    @unittest.skip("this test need refactor for updateMetadata, not for add")
    def test_3(self):
        testFileName = "Counting Crows - Colorblind.mp3"
        testFileNameWithPath = self.renameTestFile(testFileName)

        songNameTest = "Colorblind"
        artistTest = "Counting Crows"
        titleTest = "Colorblind"
        albumTest = "album test"


        newFileNameWithPath = self.metadata_mp3.rename_and_add_metadata_to_song(self.currentDirectory, albumTest, artistTest, songNameTest)
        metatag = EasyID3(newFileNameWithPath)
        self.assertTrue(os.path.isfile(newFileNameWithPath))
        self.assertEqual(newFileNameWithPath, str(self.currentDirectory+"/"+artistTest+" - " + titleTest+".mp3"))


        self.assertEqual(metatag['artist'][0], artistTest)
        self.assertEqual(metatag['title'][0], titleTest)
        self.assertEqual(metatag['album'][0], albumTest)
        os.remove(newFileNameWithPath)

    def test_4(self):
        fileNameTest = "Colorblind.mp3"
        testFileNameWithPath = self.renameTestFile(fileNameTest)
        songNameBefore = "Colorblind"

        filenameAfter = "Counting Crows - Colorblind.mp3"
        artistTest = "Counting Crows"
        titleTest = "Colorblind"
        albumTest = "album test"

        newFileNameWithPath = self.metadata_mp3.rename_and_add_metadata_to_song(self.currentDirectory, albumTest, artistTest, songNameBefore)
        self.assertFalse(os.path.isfile(testFileNameWithPath))
        self.assertTrue(os.path.isfile(newFileNameWithPath))
        self.assertNotEqual(newFileNameWithPath, testFileNameWithPath)

        self.assertEqual(newFileNameWithPath, str(self.currentDirectory+"/"+filenameAfter))

        metatag = EasyID3(newFileNameWithPath)

        self.assertEqual(metatag['artist'][0], artistTest)
        self.assertEqual(metatag['title'][0], titleTest)
        self.assertEqual(metatag['album'][0], albumTest)
        os.remove(newFileNameWithPath)

class TestAddMetadataPlaylist(TestCase):
    def setUp(self):
        self.metadata_mp3 = metadata_mp3.MetadataManager()

    def test_1(self):
        originalTestFileName = "test.mp3"
        testFileName = "Counting Crows - Colorblind.mp3"
        songNameTest = "Counting Crows - Colorblind"
        artistTest = "Counting Crows"
        titleTest = "Colorblind"
        albumTest = "spokojne-sad"
        trackNumberTest = 1

        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        originalTestFileNameWithPath = os.path.join(currentDirectory,originalTestFileName)
        albumDirectory = os.path.join(currentDirectory,albumTest)


        if not os.path.exists(albumDirectory):
            os.mkdir(albumDirectory)
        testFileNameWithPath = os.path.join(currentDirectory,albumTest, testFileName)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)

        newFileNameWithPath = self.metadata_mp3.add_metadata_playlist(currentDirectory, trackNumberTest, albumTest, artistTest, songNameTest)
        self.assertTrue(os.path.isfile(newFileNameWithPath))
        self.assertEqual(newFileNameWithPath, testFileNameWithPath)

        metatag = EasyID3(newFileNameWithPath)

        self.assertEqual(metatag['artist'][0], artistTest)
        self.assertEqual(metatag['title'][0], titleTest)
        self.assertEqual(metatag['album'][0], "YT "+albumTest)
        self.assertEqual(metatag['tracknumber'][0],str(trackNumberTest))

        shutil.rmtree(os.path.join(currentDirectory,albumTest))

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

        newFilesList = self.metadata_mp3.update_metadata_youtube(currentDirectory,albumTest)
        i = 0
        for newFile in newFilesList:
            print(newFile)
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
        albumDirectory = os.path.join(currentDirectory,albumTest)


        if not os.path.exists(albumDirectory):
            os.mkdir(albumDirectory)
        testFileNameWithPath = os.path.join(currentDirectory,albumTest, testFileName1)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)
        testFileNameWithPath = os.path.join(currentDirectory,albumTest, testFileName2)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)
        testFileNameWithPath = os.path.join(currentDirectory,albumTest, testFileName3)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)

        newFilesList = self.metadata_mp3.update_metadata(albumDirectory,albumTest)
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


if __name__=='__main__':
    unittest.main()
