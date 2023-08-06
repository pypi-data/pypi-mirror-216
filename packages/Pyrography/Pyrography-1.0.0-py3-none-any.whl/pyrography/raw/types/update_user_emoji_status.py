#  Pyrography - A wonderful Pyrogram fork inspired by Pyromod & AmanoTeam/Pyrogram.
#  Copyright (C) 2023-present Lelzin λ <https://github.com/d3cryptofc>
#
#  Forked from Pyrogram <https://github.com/pyrogram/pyrogram>,
#  originally copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrography.
#
#  Pyrography is is free software: you can redistribute it and/or modify it under
#  the terms of the GNU Lesser General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Pyrography is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
#  for more details.
#
#  You should have received a copy of the GNU Lesser General Public License along
#  with Pyrography. If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrography.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrography.raw.core import TLObject
from pyrography import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class UpdateUserEmojiStatus(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.Update`.

    Details:
        - Layer: ``158``
        - ID: ``28373599``

    Parameters:
        user_id (``int`` ``64-bit``):
            N/A

        emoji_status (:obj:`EmojiStatus <pyrography.raw.base.EmojiStatus>`):
            N/A

    """

    __slots__: List[str] = ["user_id", "emoji_status"]

    ID = 0x28373599
    QUALNAME = "types.UpdateUserEmojiStatus"

    def __init__(self, *, user_id: int, emoji_status: "raw.base.EmojiStatus") -> None:
        self.user_id = user_id  # long
        self.emoji_status = emoji_status  # EmojiStatus

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateUserEmojiStatus":
        # No flags
        
        user_id = Long.read(b)
        
        emoji_status = TLObject.read(b)
        
        return UpdateUserEmojiStatus(user_id=user_id, emoji_status=emoji_status)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.user_id))
        
        b.write(self.emoji_status.write())
        
        return b.getvalue()
