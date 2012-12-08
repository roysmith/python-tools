#!/usr/bin/env python

import unittest
import logging
from fio import TextRecordFile

class Basic(unittest.TestCase):
    def setUp(self):
        self.f = TextRecordFile("testdata/basic.log")

    def tearDown(self):
        self.f.close()
        
    def test_read_first_line(self):
        line = self.f.readline()
        self.assertEquals(line, "2012-07-07t00:00:01+00:00 line 1\n")

    def test_seek_back_to_beginning(self):
        line1 = self.f.readline()
        self.f.seek(0)
        line2 = self.f.readline()
        self.assertEquals(line1, "2012-07-07t00:00:01+00:00 line 1\n")
        self.assertEquals(line2, "2012-07-07t00:00:01+00:00 line 1\n")

    def test_eof(self):
        for i in range(20):
            line = self.f.readline()
        self.assertEquals(line, "2012-07-07t00:00:20+00:00 line 20\n")
        line = self.f.readline()
        self.assertEqual(line, "")

class File60(unittest.TestCase):
    def setUp(self):
        test_file = "testdata/file60"
        self.f = TextRecordFile(test_file)

        # Get the first two lines of the file
        f = open(test_file)
        self.line1 = f.readline()
        self.line2 = f.readline()
        assert self.line1.endswith('\n')
        assert self.line2.endswith('\n')
        self.len1 = len(self.line1.rstrip('\n'))
        self.len2 = len(self.line2.rstrip('\n'))
        f.close()

    def tearDown(self):
        self.f.close()

    def test_seek_end_of_first_line(self):
        self.f.seek(self.len1 - 1)
        line = self.f.readline()
        self.assertEqual(line, self.line1)

    def test_seek_newline_of_first_line(self):
        self.f.seek(self.len1)
        line = self.f.readline()
        self.assertEqual(line, self.line1)

    def test_seek_start_of_second_line(self):
        self.f.seek(self.len1 + 1)
        line = self.f.readline()
        self.assertEqual(line, self.line2)

    def test_seek_second_character_of_second_line(self):
        self.f.seek(self.len1 + 2)
        line = self.f.readline()
        self.assertEqual(line, self.line2)
        
if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger("fio").setLevel(logging.DEBUG)
    unittest.main()
