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


class SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.SecurePasswordKdfAlgo`.

    Details:
        - Layer: ``158``
        - ID: ``BBF2DDA0``

    Parameters:
        salt (``bytes``):
            N/A

    """

    __slots__: List[str] = ["salt"]

    ID = 0xbbf2dda0
    QUALNAME = "types.SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000"

    def __init__(self, *, salt: bytes) -> None:
        self.salt = salt  # bytes

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000":
        # No flags
        
        salt = Bytes.read(b)
        
        return SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000(salt=salt)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.salt))
        
        return b.getvalue()
