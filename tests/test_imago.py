import unittest
from unittest import TestCase
import os

from imago import extractor
from imago import helper

class TestImago(unittest.TestCase):
    filename = "./images/solvent.jpg"
    TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'test_1.jpg')
    def setUp(self):
        helper.initialize_sqli()
        pass

    def test_whash(self):
        result = str(extractor.whash(self.TESTDATA_FILENAME))
        self.assertEqual((result), "fcfcf9e060407878")

    def test_phash(self):
        result = str(extractor.phash(self.TESTDATA_FILENAME))
        self.assertEqual((result), "d1dadfd3864620b2")

    def test_dhash(self):
        result = str(extractor.dhash(self.TESTDATA_FILENAME))
        self.assertEqual((result), "fcfcc0e040000000")

    def test_ahash(self):
        result = str(extractor.ahash(self.TESTDATA_FILENAME))
        self.assertEqual((result), "fcfcc0e040000000")

if __name__ == '__main__':
    unittest.main()
