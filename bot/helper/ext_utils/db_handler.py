from aiofiles import open as aiopen
from aiofiles.os import path as aiopath

from ... import LOGGER, user_data, rss_dict, qbit_options
from ...core.telegram_manager import TgClient
from ...core.config_manager import Config


class DbManager:
    def __init__(self):
        self._return = True
        self._conn = None
        self.db = None

    async def connect(self):
        # Database functionality removed
        self._return = True
        pass

    async def disconnect(self):
        # Database functionality removed
        pass

    async def update_deploy_config(self):
        # Database functionality removed
        pass

    async def update_config(self, dict_):
        # Database functionality removed
        pass

    async def load_config(self):
        # Database functionality removed
        pass

    async def trunc_table(self, name):
        # Database functionality removed
        pass

    async def update_user_data(self, user_id):
        # Database functionality removed
        pass

    async def update_user_doc(self, user_id, key, path=None):
        # Database functionality removed
        pass

    async def get_user_data(self, user_id):
        # Database functionality removed
        return {}

    async def get_user_property(self, user_id, property_):
        # Database functionality removed
        return None

    async def update_thumb(self, user_id, path):
        # Database functionality removed
        pass

    async def get_thumb(self, user_id):
        # Database functionality removed
        return None

    async def update_rss_data(self, _id, data):
        # Database functionality removed
        pass

    async def get_rss_data(self, _id):
        # Database functionality removed
        return {}

    async def rss_update_all(self):
        # Database functionality removed
        pass

    async def del_rss_data(self, _id):
        # Database functionality removed
        pass

    async def add_incomplete_task(self, cid, msg_id, _id):
        # Database functionality removed
        pass

    async def get_incomplete_task(self, _id):
        # Database functionality removed
        return []

    async def del_incomplete_task(self, _id):
        # Database functionality removed
        pass

    async def is_sudo(self, user_id):
        # Database functionality removed - check config instead
        return str(user_id) in Config.SUDO_USERS.split()

    async def auth_user(self, user_id):
        # Database functionality removed - check config instead
        return str(user_id) in Config.AUTHORIZED_CHATS.split()

    async def add_private_file(self, _id, link, tag=None):
        # Database functionality removed
        pass

    async def get_private_file(self, _id):
        # Database functionality removed
        return {}

    async def get_private_files(self, _id, tag=None):
        # Database functionality removed
        return {}

    async def rename_private_file(self, _id, link, name):
        # Database functionality removed
        pass

    async def delete_private_file(self, _id, link):
        # Database functionality removed
        pass

    async def delete_all_private_files(self, _id):
        # Database functionality removed
        pass

    async def count_private_files(self, _id):
        # Database functionality removed
        return 0

    async def update_qbit_options(self, _id, key, value):
        # Database functionality removed
        pass

    async def get_qbit_options(self, _id):
        # Database functionality removed
        return {}

    async def update_limits(self, _id, key, value):
        # Database functionality removed
        pass

    async def get_limits(self, _id):
        # Database functionality removed
        return {}

    async def update_jdownloader(self, _id, key, value):
        # Database functionality removed
        pass

    async def get_jdownloader(self, _id):
        # Database functionality removed
        return {}

    async def update_private_file(self, _id, link, key, value):
        # Database functionality removed
        pass


database = DbManager()
