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


class ViewSponsoredMessage(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``BEAEDB94``

    Parameters:
        channel (:obj:`InputChannel <pyrography.raw.base.InputChannel>`):
            N/A

        random_id (``bytes``):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["channel", "random_id"]

    ID = 0xbeaedb94
    QUALNAME = "functions.channels.ViewSponsoredMessage"

    def __init__(self, *, channel: "raw.base.InputChannel", random_id: bytes) -> None:
        self.channel = channel  # InputChannel
        self.random_id = random_id  # bytes

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ViewSponsoredMessage":
        # No flags
        
        channel = TLObject.read(b)
        
        random_id = Bytes.read(b)
        
        return ViewSponsoredMessage(channel=channel, random_id=random_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(Bytes(self.random_id))
        
        return b.getvalue()
