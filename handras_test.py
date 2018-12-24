import unittest
import handras


class HandrasTest(unittest.TestCase):
    def test_get_url(self):
        for number in range(1, 34):
            self.assertEqual("http://handras.hu/page/" + str(number), handras.get_url(number))
