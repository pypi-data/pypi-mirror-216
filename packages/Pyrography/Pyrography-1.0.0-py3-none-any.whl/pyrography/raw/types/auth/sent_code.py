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


class SentCode(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.auth.SentCode`.

    Details:
        - Layer: ``158``
        - ID: ``5E002502``

    Parameters:
        type (:obj:`auth.SentCodeType <pyrography.raw.base.auth.SentCodeType>`):
            N/A

        phone_code_hash (``str``):
            N/A

        next_type (:obj:`auth.CodeType <pyrography.raw.base.auth.CodeType>`, *optional*):
            N/A

        timeout (``int`` ``32-bit``, *optional*):
            N/A

    Functions:
        This object can be returned by 6 functions.

        .. currentmodule:: pyrography.raw.functions

        .. autosummary::
            :nosignatures:

            auth.SendCode
            auth.ResendCode
            auth.ResetLoginEmail
            account.SendChangePhoneCode
            account.SendConfirmPhoneCode
            account.SendVerifyPhoneCode
    """

    __slots__: List[str] = ["type", "phone_code_hash", "next_type", "timeout"]

    ID = 0x5e002502
    QUALNAME = "types.auth.SentCode"

    def __init__(self, *, type: "raw.base.auth.SentCodeType", phone_code_hash: str, next_type: "raw.base.auth.CodeType" = None, timeout: Optional[int] = None) -> None:
        self.type = type  # auth.SentCodeType
        self.phone_code_hash = phone_code_hash  # string
        self.next_type = next_type  # flags.1?auth.CodeType
        self.timeout = timeout  # flags.2?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SentCode":
        
        flags = Int.read(b)
        
        type = TLObject.read(b)
        
        phone_code_hash = String.read(b)
        
        next_type = TLObject.read(b) if flags & (1 << 1) else None
        
        timeout = Int.read(b) if flags & (1 << 2) else None
        return SentCode(type=type, phone_code_hash=phone_code_hash, next_type=next_type, timeout=timeout)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.next_type is not None else 0
        flags |= (1 << 2) if self.timeout is not None else 0
        b.write(Int(flags))
        
        b.write(self.type.write())
        
        b.write(String(self.phone_code_hash))
        
        if self.next_type is not None:
            b.write(self.next_type.write())
        
        if self.timeout is not None:
            b.write(Int(self.timeout))
        
        return b.getvalue()
