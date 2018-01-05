import unittest
import sys
from os.path import join, abspath, dirname
import json

LOCAL_DIR = abspath(dirname(__file__))
# For package imports
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from libnano.datastructures.seqrecord import SeqRecord, fromGenbankLike
from libnano.datastructures.seqrecord import Feature, locationStr2Feature
from libnano.datastructures.seqrecord import Location
import _setup

class TestSeqRecord(unittest.TestCase):

    def setUp(self):
        self.normal_files = [ 'sample.gb',
                        'mds42_full.gb',
                        'mds42_recode.gb',
                        'failed.gb',
                        'sample.gb.json'

        ]
        self.exception_files = ['sample_complex.gb' # fails for compound location
                                ]
    # end def

    def checkFile(self, fn):
        fn_gb = join(LOCAL_DIR, 'test_data', fn)
        a = fromGenbankLike(fn_gb)
        self.assertIsNotNone(a)
        return a
    # end def

    def test_checkNormalFiles(self):
        for fn in self.normal_files:
            self.checkFile(fn)

    def test_checkExceptionFiles(self):
        def doexc(fn):
            fn_gb = join(LOCAL_DIR, 'test_data', fn)
            self.assertRaises(NotImplementedError, fromGenbankLike, fn_gb)
        # end def

        for fn in self.exception_files:
            doexc(fn)

    def test_addFeature(self):
        sr = self.checkFile(self.normal_files[0])
        feature_name = "myfeature"
        ft = locationStr2Feature(feature_name, "1615..1636")
        sr.addFeature(ft)
        self.assertIn(feature_name, sr)

    def test_removeFeature(self):
        sr = self.checkFile(self.normal_files[0])
        feature_name = "myfeature"
        ft = locationStr2Feature(feature_name, "1615..1636")
        sr.addFeature(ft)
        self.assertIn(feature_name, sr)
        sr.removeFeature(ft)
        self.assertNotIn(feature_name, sr)
# end class


if __name__ == '__main__':
    unittest.main(verbosity=2)