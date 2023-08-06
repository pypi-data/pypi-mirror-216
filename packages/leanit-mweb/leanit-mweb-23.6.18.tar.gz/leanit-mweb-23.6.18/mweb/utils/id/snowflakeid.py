from __future__ import annotations

import hashlib
import logging
import os

from snowflake import SnowflakeGenerator as UpSnowflakeGenerator, Snowflake

logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

class SnowflakeGenerator(UpSnowflakeGenerator):
    _instance = None

    next = UpSnowflakeGenerator.__next__

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        instance_descriptor = os.environ.get("NOMAD_ALLOC_ID")
        if not instance_descriptor:
            # use hostname
            import socket
            instance_descriptor = socket.gethostname()

        hash_value = hashlib.md5(instance_descriptor.encode()).hexdigest()
        # take first 3 hex characters (12 bits), shift right by 2 to get 10 bits
        instance_id = int(hash_value[:3], 16) >> 2

        # ensure instance_id is not larger than 10 bit
        assert instance_id < 2**10

        self.start_epoch = 1687869016000

        super().__init__(instance=instance_id, epoch=self.start_epoch)

    def parse(self, sf: int) -> Snowflake:
        return Snowflake.parse(sf, epoch=self.start_epoch)

if __name__ == '__main__':
    s = SnowflakeGenerator.get_instance()
    print(s.next())
