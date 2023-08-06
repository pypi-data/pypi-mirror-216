import time
import unittest
from mweb.utils.id.snowflakeid import SnowflakeGenerator
import logging

logger = logging.getLogger(__name__)

class TestSnowflake(unittest.TestCase):
    def test_snowflake(self):

        generator = SnowflakeGenerator()
        sf = generator.__next__()

        # check if sf is int
        self.assertIsInstance(sf, int)

        flake = generator.parse(sf)

        age_in_seconds = time.time() - flake.seconds
        self.assertLess(age_in_seconds, 2)

        # self.assertEqual(len(snowflake()), 18
