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


class UpdateChatDefaultBannedRights(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.Update`.

    Details:
        - Layer: ``158``
        - ID: ``54C01850``

    Parameters:
        peer (:obj:`Peer <pyrography.raw.base.Peer>`):
            N/A

        default_banned_rights (:obj:`ChatBannedRights <pyrography.raw.base.ChatBannedRights>`):
            N/A

        version (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["peer", "default_banned_rights", "version"]

    ID = 0x54c01850
    QUALNAME = "types.UpdateChatDefaultBannedRights"

    def __init__(self, *, peer: "raw.base.Peer", default_banned_rights: "raw.base.ChatBannedRights", version: int) -> None:
        self.peer = peer  # Peer
        self.default_banned_rights = default_banned_rights  # ChatBannedRights
        self.version = version  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateChatDefaultBannedRights":
        # No flags
        
        peer = TLObject.read(b)
        
        default_banned_rights = TLObject.read(b)
        
        version = Int.read(b)
        
        return UpdateChatDefaultBannedRights(peer=peer, default_banned_rights=default_banned_rights, version=version)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.default_banned_rights.write())
        
        b.write(Int(self.version))
        
        return b.getvalue()
