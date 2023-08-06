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


class CancelCode(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``1F040578``

    Parameters:
        phone_number (``str``):
            N/A

        phone_code_hash (``str``):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["phone_number", "phone_code_hash"]

    ID = 0x1f040578
    QUALNAME = "functions.auth.CancelCode"

    def __init__(self, *, phone_number: str, phone_code_hash: str) -> None:
        self.phone_number = phone_number  # string
        self.phone_code_hash = phone_code_hash  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CancelCode":
        # No flags
        
        phone_number = String.read(b)
        
        phone_code_hash = String.read(b)
        
        return CancelCode(phone_number=phone_number, phone_code_hash=phone_code_hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.phone_number))
        
        b.write(String(self.phone_code_hash))
        
        return b.getvalue()
