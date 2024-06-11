import logging
import requests

from typing import List, Dict


class WX:
    logger = logging.getLogger(__name__)

    def send(self, to_users: List[str], template_id: str, data: Dict):
        self.logger.debug(f"{to_users=}, {template_id=}, {data=}")
        if data and to_users and template_id:
            url = "http://47.109.110.64:51127/notify_dialtest"
            _data = {
                "users": to_users,
                "template_id": template_id,
                "data": data
            }
            ret = requests.post(url, json=_data)
            self.logger.debug(ret.json())

    def notify_devoloper(self, msg: str="", user=None):
        if msg:
            url = "http://47.109.110.64:51127/notify_developer"
            ret = requests.post(url, json={"msg": msg, "user": user})
            self.logger.debug(ret.json())