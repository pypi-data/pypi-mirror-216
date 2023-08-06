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


class StickerSetInstallResultArchive(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrography.raw.base.messages.StickerSetInstallResult`.

    Details:
        - Layer: ``158``
        - ID: ``35E410A8``

    Parameters:
        sets (List of :obj:`StickerSetCovered <pyrography.raw.base.StickerSetCovered>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrography.raw.functions

        .. autosummary::
            :nosignatures:

            messages.InstallStickerSet
    """

    __slots__: List[str] = ["sets"]

    ID = 0x35e410a8
    QUALNAME = "types.messages.StickerSetInstallResultArchive"

    def __init__(self, *, sets: List["raw.base.StickerSetCovered"]) -> None:
        self.sets = sets  # Vector<StickerSetCovered>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StickerSetInstallResultArchive":
        # No flags
        
        sets = TLObject.read(b)
        
        return StickerSetInstallResultArchive(sets=sets)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.sets))
        
        return b.getvalue()
