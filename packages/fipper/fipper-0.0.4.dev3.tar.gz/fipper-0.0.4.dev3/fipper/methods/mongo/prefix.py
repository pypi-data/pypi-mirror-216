# Ayiin - Ubot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinUbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinUbot/blob/main/LICENSE/>.
#
# FROM AyiinUbot <https://github.com/AyiinXd/AyiinUbot>
# t.me/AyiinChats & t.me/AyiinChannel


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import fipper

from .core import db


hndlrdb = db['prefix']


class Prefix:
    def set_prefix(self: "fipper.Client", handler):
        user_id = self.me.id
        cek = hndlrdb.find_one({"user_id": user_id})
        if cek:
            hndlrdb.update_one({"user_id": user_id}, {"$set": {"hndlr": handler.split(' ')}})
        else:
            hndlrdb.insert_one(
                {
                    "user_id": user_id,
                    "hndlr": handler
                }
            )

    def del_prefix(self: "fipper.Client"):
        hndlrdb.update_one({"user_id": self.me.id}, {"$set": {"hndlr": [".", "!", "*", "^", "-", "?"]}})

    def get_prefix(self: "fipper.Client"):
        x = hndlrdb.find_one({'user_id': self.me.id})
        return x['hndlr']
        #if x:
        #    return x['hndlr']
        #else:
        #    return [".", "!", "*", "^", "-", "?"]
