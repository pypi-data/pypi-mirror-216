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


class PromoData(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.help.PromoData`.

    Details:
        - Layer: ``158``
        - ID: ``8C39793F``

    Parameters:
        expires (``int`` ``32-bit``):
            N/A

        peer (:obj:`Peer <pyrography.raw.base.Peer>`):
            N/A

        chats (List of :obj:`Chat <pyrography.raw.base.Chat>`):
            N/A

        users (List of :obj:`User <pyrography.raw.base.User>`):
            N/A

        proxy (``bool``, *optional*):
            N/A

        psa_type (``str``, *optional*):
            N/A

        psa_message (``str``, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrography.raw.functions

        .. autosummary::
            :nosignatures:

            help.GetPromoData
    """

    __slots__: List[str] = ["expires", "peer", "chats", "users", "proxy", "psa_type", "psa_message"]

    ID = 0x8c39793f
    QUALNAME = "types.help.PromoData"

    def __init__(self, *, expires: int, peer: "raw.base.Peer", chats: List["raw.base.Chat"], users: List["raw.base.User"], proxy: Optional[bool] = None, psa_type: Optional[str] = None, psa_message: Optional[str] = None) -> None:
        self.expires = expires  # int
        self.peer = peer  # Peer
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.proxy = proxy  # flags.0?true
        self.psa_type = psa_type  # flags.1?string
        self.psa_message = psa_message  # flags.2?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PromoData":
        
        flags = Int.read(b)
        
        proxy = True if flags & (1 << 0) else False
        expires = Int.read(b)
        
        peer = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        psa_type = String.read(b) if flags & (1 << 1) else None
        psa_message = String.read(b) if flags & (1 << 2) else None
        return PromoData(expires=expires, peer=peer, chats=chats, users=users, proxy=proxy, psa_type=psa_type, psa_message=psa_message)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.proxy else 0
        flags |= (1 << 1) if self.psa_type is not None else 0
        flags |= (1 << 2) if self.psa_message is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.expires))
        
        b.write(self.peer.write())
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        if self.psa_type is not None:
            b.write(String(self.psa_type))
        
        if self.psa_message is not None:
            b.write(String(self.psa_message))
        
        return b.getvalue()
