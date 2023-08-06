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


class GetParticipant(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``A0AB6CC6``

    Parameters:
        channel (:obj:`InputChannel <pyrography.raw.base.InputChannel>`):
            N/A

        participant (:obj:`InputPeer <pyrography.raw.base.InputPeer>`):
            N/A

    Returns:
        :obj:`channels.ChannelParticipant <pyrography.raw.base.channels.ChannelParticipant>`
    """

    __slots__: List[str] = ["channel", "participant"]

    ID = 0xa0ab6cc6
    QUALNAME = "functions.channels.GetParticipant"

    def __init__(self, *, channel: "raw.base.InputChannel", participant: "raw.base.InputPeer") -> None:
        self.channel = channel  # InputChannel
        self.participant = participant  # InputPeer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetParticipant":
        # No flags
        
        channel = TLObject.read(b)
        
        participant = TLObject.read(b)
        
        return GetParticipant(channel=channel, participant=participant)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(self.participant.write())
        
        return b.getvalue()
