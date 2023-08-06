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


class MessageEmpty(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.Message`.

    Details:
        - Layer: ``158``
        - ID: ``90A6CA84``

    Parameters:
        id (``int`` ``32-bit``):
            N/A

        peer_id (:obj:`Peer <pyrography.raw.base.Peer>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["id", "peer_id"]

    ID = 0x90a6ca84
    QUALNAME = "types.MessageEmpty"

    def __init__(self, *, id: int, peer_id: "raw.base.Peer" = None) -> None:
        self.id = id  # int
        self.peer_id = peer_id  # flags.0?Peer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageEmpty":
        
        flags = Int.read(b)
        
        id = Int.read(b)
        
        peer_id = TLObject.read(b) if flags & (1 << 0) else None
        
        return MessageEmpty(id=id, peer_id=peer_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.peer_id is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.id))
        
        if self.peer_id is not None:
            b.write(self.peer_id.write())
        
        return b.getvalue()
