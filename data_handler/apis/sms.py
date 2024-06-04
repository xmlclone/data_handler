import logging

from typing import List


class SMS:
    logger = logging.getLogger(__name__)

    def send(self, to_users: List[str]):
        self.logger.debug('stub sms send.')