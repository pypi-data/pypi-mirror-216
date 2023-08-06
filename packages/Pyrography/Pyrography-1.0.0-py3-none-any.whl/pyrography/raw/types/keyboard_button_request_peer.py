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


class KeyboardButtonRequestPeer(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.KeyboardButton`.

    Details:
        - Layer: ``158``
        - ID: ``D0B468C``

    Parameters:
        text (``str``):
            N/A

        button_id (``int`` ``32-bit``):
            N/A

        peer_type (:obj:`RequestPeerType <pyrography.raw.base.RequestPeerType>`):
            N/A

    """

    __slots__: List[str] = ["text", "button_id", "peer_type"]

    ID = 0xd0b468c
    QUALNAME = "types.KeyboardButtonRequestPeer"

    def __init__(self, *, text: str, button_id: int, peer_type: "raw.base.RequestPeerType") -> None:
        self.text = text  # string
        self.button_id = button_id  # int
        self.peer_type = peer_type  # RequestPeerType

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "KeyboardButtonRequestPeer":
        # No flags
        
        text = String.read(b)
        
        button_id = Int.read(b)
        
        peer_type = TLObject.read(b)
        
        return KeyboardButtonRequestPeer(text=text, button_id=button_id, peer_type=peer_type)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.text))
        
        b.write(Int(self.button_id))
        
        b.write(self.peer_type.write())
        
        return b.getvalue()
