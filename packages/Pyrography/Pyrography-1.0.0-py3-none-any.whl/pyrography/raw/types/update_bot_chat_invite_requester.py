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


class UpdateBotChatInviteRequester(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.Update`.

    Details:
        - Layer: ``158``
        - ID: ``11DFA986``

    Parameters:
        peer (:obj:`Peer <pyrography.raw.base.Peer>`):
            N/A

        date (``int`` ``32-bit``):
            N/A

        user_id (``int`` ``64-bit``):
            N/A

        about (``str``):
            N/A

        invite (:obj:`ExportedChatInvite <pyrography.raw.base.ExportedChatInvite>`):
            N/A

        qts (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["peer", "date", "user_id", "about", "invite", "qts"]

    ID = 0x11dfa986
    QUALNAME = "types.UpdateBotChatInviteRequester"

    def __init__(self, *, peer: "raw.base.Peer", date: int, user_id: int, about: str, invite: "raw.base.ExportedChatInvite", qts: int) -> None:
        self.peer = peer  # Peer
        self.date = date  # int
        self.user_id = user_id  # long
        self.about = about  # string
        self.invite = invite  # ExportedChatInvite
        self.qts = qts  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateBotChatInviteRequester":
        # No flags
        
        peer = TLObject.read(b)
        
        date = Int.read(b)
        
        user_id = Long.read(b)
        
        about = String.read(b)
        
        invite = TLObject.read(b)
        
        qts = Int.read(b)
        
        return UpdateBotChatInviteRequester(peer=peer, date=date, user_id=user_id, about=about, invite=invite, qts=qts)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.date))
        
        b.write(Long(self.user_id))
        
        b.write(String(self.about))
        
        b.write(self.invite.write())
        
        b.write(Int(self.qts))
        
        return b.getvalue()
