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


class DialogFolder(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.Dialog`.

    Details:
        - Layer: ``158``
        - ID: ``71BD134C``

    Parameters:
        folder (:obj:`Folder <pyrography.raw.base.Folder>`):
            N/A

        peer (:obj:`Peer <pyrography.raw.base.Peer>`):
            N/A

        top_message (``int`` ``32-bit``):
            N/A

        unread_muted_peers_count (``int`` ``32-bit``):
            N/A

        unread_unmuted_peers_count (``int`` ``32-bit``):
            N/A

        unread_muted_messages_count (``int`` ``32-bit``):
            N/A

        unread_unmuted_messages_count (``int`` ``32-bit``):
            N/A

        pinned (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["folder", "peer", "top_message", "unread_muted_peers_count", "unread_unmuted_peers_count", "unread_muted_messages_count", "unread_unmuted_messages_count", "pinned"]

    ID = 0x71bd134c
    QUALNAME = "types.DialogFolder"

    def __init__(self, *, folder: "raw.base.Folder", peer: "raw.base.Peer", top_message: int, unread_muted_peers_count: int, unread_unmuted_peers_count: int, unread_muted_messages_count: int, unread_unmuted_messages_count: int, pinned: Optional[bool] = None) -> None:
        self.folder = folder  # Folder
        self.peer = peer  # Peer
        self.top_message = top_message  # int
        self.unread_muted_peers_count = unread_muted_peers_count  # int
        self.unread_unmuted_peers_count = unread_unmuted_peers_count  # int
        self.unread_muted_messages_count = unread_muted_messages_count  # int
        self.unread_unmuted_messages_count = unread_unmuted_messages_count  # int
        self.pinned = pinned  # flags.2?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DialogFolder":
        
        flags = Int.read(b)
        
        pinned = True if flags & (1 << 2) else False
        folder = TLObject.read(b)
        
        peer = TLObject.read(b)
        
        top_message = Int.read(b)
        
        unread_muted_peers_count = Int.read(b)
        
        unread_unmuted_peers_count = Int.read(b)
        
        unread_muted_messages_count = Int.read(b)
        
        unread_unmuted_messages_count = Int.read(b)
        
        return DialogFolder(folder=folder, peer=peer, top_message=top_message, unread_muted_peers_count=unread_muted_peers_count, unread_unmuted_peers_count=unread_unmuted_peers_count, unread_muted_messages_count=unread_muted_messages_count, unread_unmuted_messages_count=unread_unmuted_messages_count, pinned=pinned)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.pinned else 0
        b.write(Int(flags))
        
        b.write(self.folder.write())
        
        b.write(self.peer.write())
        
        b.write(Int(self.top_message))
        
        b.write(Int(self.unread_muted_peers_count))
        
        b.write(Int(self.unread_unmuted_peers_count))
        
        b.write(Int(self.unread_muted_messages_count))
        
        b.write(Int(self.unread_unmuted_messages_count))
        
        return b.getvalue()
