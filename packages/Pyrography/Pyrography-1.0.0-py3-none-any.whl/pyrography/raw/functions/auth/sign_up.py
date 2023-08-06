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


class SignUp(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``80EEE427``

    Parameters:
        phone_number (``str``):
            N/A

        phone_code_hash (``str``):
            N/A

        first_name (``str``):
            N/A

        last_name (``str``):
            N/A

    Returns:
        :obj:`auth.Authorization <pyrography.raw.base.auth.Authorization>`
    """

    __slots__: List[str] = ["phone_number", "phone_code_hash", "first_name", "last_name"]

    ID = 0x80eee427
    QUALNAME = "functions.auth.SignUp"

    def __init__(self, *, phone_number: str, phone_code_hash: str, first_name: str, last_name: str) -> None:
        self.phone_number = phone_number  # string
        self.phone_code_hash = phone_code_hash  # string
        self.first_name = first_name  # string
        self.last_name = last_name  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SignUp":
        # No flags
        
        phone_number = String.read(b)
        
        phone_code_hash = String.read(b)
        
        first_name = String.read(b)
        
        last_name = String.read(b)
        
        return SignUp(phone_number=phone_number, phone_code_hash=phone_code_hash, first_name=first_name, last_name=last_name)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.phone_number))
        
        b.write(String(self.phone_code_hash))
        
        b.write(String(self.first_name))
        
        b.write(String(self.last_name))
        
        return b.getvalue()
