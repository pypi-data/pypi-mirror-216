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


class InstallWallPaper(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``FEED5769``

    Parameters:
        wallpaper (:obj:`InputWallPaper <pyrography.raw.base.InputWallPaper>`):
            N/A

        settings (:obj:`WallPaperSettings <pyrography.raw.base.WallPaperSettings>`):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["wallpaper", "settings"]

    ID = 0xfeed5769
    QUALNAME = "functions.account.InstallWallPaper"

    def __init__(self, *, wallpaper: "raw.base.InputWallPaper", settings: "raw.base.WallPaperSettings") -> None:
        self.wallpaper = wallpaper  # InputWallPaper
        self.settings = settings  # WallPaperSettings

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InstallWallPaper":
        # No flags
        
        wallpaper = TLObject.read(b)
        
        settings = TLObject.read(b)
        
        return InstallWallPaper(wallpaper=wallpaper, settings=settings)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.wallpaper.write())
        
        b.write(self.settings.write())
        
        return b.getvalue()
