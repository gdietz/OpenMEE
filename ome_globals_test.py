import ome_globals

import unittest
import urllib2


class Test_HelpURL(unittest.TestCase):
    def test_isValid(self):
        # errors out if ome_globals.HELP_URL is invalid
        urllib2.urlopen(ome_globals.HELP_URL)