from __future__ import annotations
import logging

from mweb.orm.fields import IntegerField
from mweb.utils.id.snowflakeid import SnowflakeGenerator

logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class SnowflakeField(IntegerField):
    generator = SnowflakeGenerator.get_instance()

    def default(self):
        return self.generator.__next__()
