#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
import os

from imago import extractor
from imago import helper

class TestImago(unittest.TestCase):
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

    def test_md5(self):
        result = str(extractor.md5(self.TESTDATA_FILENAME))
        self.assertEqual((result), "35b833f721ed391380a8ddf159852b50")

    def test_sha256(self):
        result = str(extractor.sha256(self.TESTDATA_FILENAME))
        self.assertEqual((result), "14f6453d145c69c96e77c7e901cdbf58f7984c09fe4ab65ca8914c5d0d37e956")

    def test_sha512(self):
        result = str(extractor.sha512(self.TESTDATA_FILENAME))
        self.assertEqual((result), "3db53dc840ccbc85495df537f582f0297d8c4d174df78d9eeab4ce97d071793f8cefb83a7f8a0cf55ce3ec0289bf9e45164f16ca03b70f8d2acf1a3e87fb9636")


    def tearDown(self):
        os.remove('metadata.db')
        pass

if __name__ == '__main__':
    unittest.main()
