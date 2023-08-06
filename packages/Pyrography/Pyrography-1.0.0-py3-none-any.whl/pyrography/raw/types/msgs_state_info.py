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


class MsgsStateInfo(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.MsgsStateInfo`.

    Details:
        - Layer: ``158``
        - ID: ``04DEB57D``

    Parameters:
        req_msg_id (``int`` ``64-bit``):
            N/A

        info (``str``):
            N/A

    """

    __slots__: List[str] = ["req_msg_id", "info"]

    ID = 0x04deb57d
    QUALNAME = "types.MsgsStateInfo"

    def __init__(self, *, req_msg_id: int, info: str) -> None:
        self.req_msg_id = req_msg_id  # long
        self.info = info  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MsgsStateInfo":
        # No flags
        
        req_msg_id = Long.read(b)
        
        info = String.read(b)
        
        return MsgsStateInfo(req_msg_id=req_msg_id, info=info)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.req_msg_id))
        
        b.write(String(self.info))
        
        return b.getvalue()
