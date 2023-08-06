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


class EmojiKeywordsDifference(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.EmojiKeywordsDifference`.

    Details:
        - Layer: ``158``
        - ID: ``5CC761BD``

    Parameters:
        lang_code (``str``):
            N/A

        from_version (``int`` ``32-bit``):
            N/A

        version (``int`` ``32-bit``):
            N/A

        keywords (List of :obj:`EmojiKeyword <pyrography.raw.base.EmojiKeyword>`):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: pyrography.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetEmojiKeywords
            messages.GetEmojiKeywordsDifference
    """

    __slots__: List[str] = ["lang_code", "from_version", "version", "keywords"]

    ID = 0x5cc761bd
    QUALNAME = "types.EmojiKeywordsDifference"

    def __init__(self, *, lang_code: str, from_version: int, version: int, keywords: List["raw.base.EmojiKeyword"]) -> None:
        self.lang_code = lang_code  # string
        self.from_version = from_version  # int
        self.version = version  # int
        self.keywords = keywords  # Vector<EmojiKeyword>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EmojiKeywordsDifference":
        # No flags
        
        lang_code = String.read(b)
        
        from_version = Int.read(b)
        
        version = Int.read(b)
        
        keywords = TLObject.read(b)
        
        return EmojiKeywordsDifference(lang_code=lang_code, from_version=from_version, version=version, keywords=keywords)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.lang_code))
        
        b.write(Int(self.from_version))
        
        b.write(Int(self.version))
        
        b.write(Vector(self.keywords))
        
        return b.getvalue()
