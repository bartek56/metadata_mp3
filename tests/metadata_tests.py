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
    def test_1(self):
        songNameBefore = "Counting Crows - Colorblind (Official Video)"
        songNameAfter = "Counting Crows - Colorblind"        
        songNameAfterTest = metadata_mp3.rename_song_name(songNameBefore)
        self.assertEqual(songNameAfter, songNameAfterTest)


    def test_2(self):
        songNameBefore = "Counting Crows - Colorblind test"
        songNameAfter = "Counting Crows - Colorblind"
        songNameAfterTest = metadata_mp3.rename_song_name(songNameBefore)
        self.assertNotEqual(songNameAfter, songNameAfterTest)

class TestConvertSongnameOnMetadata(TestCase):
    def test_1(self):
        songNameBefore = "Counting Crows - Colorblind"
        metadataSongName = metadata_mp3.convert_songname_on_metadata(songNameBefore)
        self.assertEqual(metadataSongName['artist'], "Counting Crows")
        self.assertEqual(metadataSongName['title'], "Colorblind")


    def test_2(self):
        songNameBefore = "Counting Crows - Colorblind test"
        metadataSongName = metadata_mp3.convert_songname_on_metadata(songNameBefore)
        self.assertEqual(metadataSongName['artist'], "Counting Crows")
        self.assertEqual(metadataSongName['title'], "Colorblind test")

class TestAddMetadataSong(TestCase):
    def test_1(self):
        originalTestFileName = "test.mp3"
        testFileName = "Counting Crows - Colorblind.mp3"
        songNameTest = "Counting Crows - Colorblind"
        artistTest = "Counting Crows"
        titleTest = "Colorblind"
        albumTest = "album test"


        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        originalTestFileNameWithPath = os.path.join(currentDirectory,originalTestFileName)
        testFileNameWithPath = os.path.join(currentDirectory,testFileName)
        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)

        newFileNameWithPath = metadata_mp3.add_metadata_song(currentDirectory,albumTest, artistTest, songNameTest)
        metatag = EasyID3(newFileNameWithPath)
        print(newFileNameWithPath)
        self.assertTrue(os.path.isfile(newFileNameWithPath))
        self.assertEqual(newFileNameWithPath, testFileNameWithPath)


        self.assertEqual(metatag['artist'][0], artistTest)
        self.assertEqual(metatag['title'][0], titleTest)
        self.assertEqual(metatag['album'][0], albumTest)
        os.remove(newFileNameWithPath)

    def test_2(self):
        originalTestFileName = "test.mp3"
        fileNameTest = "Counting Crows - Colorblind (Official Video).mp3"
        songNameTest = "Counting Crows - Colorblind (Official Video)"
        artistTest = "Counting Crows"
        titleTest = "Colorblind"
        albumTest = "album test"

        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        originalTestFileNameWithPath = os.path.join(currentDirectory,originalTestFileName)
        testFileNameWithPath = os.path.join(currentDirectory,fileNameTest)


        shutil.copy(originalTestFileNameWithPath, testFileNameWithPath)

        newFileNameWithPath = metadata_mp3.add_metadata_song(currentDirectory,albumTest, artistTest, songNameTest)
        self.assertFalse(os.path.isfile(testFileNameWithPath))
        self.assertTrue(os.path.isfile(newFileNameWithPath))
        self.assertNotEqual(newFileNameWithPath, testFileNameWithPath)


        metatag = EasyID3(newFileNameWithPath)
        print(newFileNameWithPath)

        self.assertEqual(metatag['artist'][0], artistTest)
        self.assertEqual(metatag['title'][0], titleTest)
        self.assertEqual(metatag['album'][0], albumTest)
        os.remove(newFileNameWithPath)

class TestAddMetadataPlaylist(TestCase):
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
        
        newFileNameWithPath = metadata_mp3.add_metadata_playlist(currentDirectory,trackNumberTest,albumTest,artistTest,songNameTest)
        #print(newFileNameWithPath)
        self.assertTrue(os.path.isfile(newFileNameWithPath))
        self.assertEqual(newFileNameWithPath, testFileNameWithPath)

        metatag = EasyID3(newFileNameWithPath)

        self.assertEqual(metatag['artist'][0], artistTest)
        self.assertEqual(metatag['title'][0], titleTest)
        self.assertEqual(metatag['album'][0], "YT "+albumTest)
        self.assertEqual(metatag['tracknumber'][0],str(trackNumberTest))

        shutil.rmtree(os.path.join(currentDirectory,albumTest))

class TestUpdateMetadataYoutube(TestCase):
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
     
        newFilesList = metadata_mp3.update_metadata_youtube(currentDirectory,albumTest)
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
     
        newFilesList = metadata_mp3.update_metadata(albumDirectory,albumTest)
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

        newFilesList = metadata_mp3.setAlbum(testCatalogWithPath, "album test")
        for newFile in newFilesList:
            newFileWithPath = os.path.join(testCatalogWithPath,newFile)
            self.assertTrue(os.path.isfile(newFileWithPath))
            metatag = EasyID3(newFileWithPath)
            self.assertEqual(metatag['album'][0], "album test")

    
        shutil.rmtree(os.path.join(currentDirectory,testCatalog))
       
class TestSetArtist(TestCase):
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

        newFilesList = metadata_mp3.setArtist(testCatalogWithPath, "artist test")
        for newFile in newFilesList:
            newFileWithPath = os.path.join(testCatalogWithPath,newFile)
            self.assertTrue(os.path.isfile(newFileWithPath))
            metatag = EasyID3(newFileWithPath)
            self.assertEqual(metatag['artist'][0], "artist test")
    
        shutil.rmtree(os.path.join(currentDirectory,testCatalog))
 

if __name__=='__main__':
    unittest.main()
