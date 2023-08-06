#!/usr/bin/env python3
#                        _                    _ _   _
#  _ __ ___   __ _  __ _(_) _____      ____ _| | | (_) ___
# | '_ ` _ \ / _` |/ _` | |/ __\ \ /\ / / _` | | | | |/ _ \
# | | | | | | (_| | (_| | | (__ \ V  V / (_| | | |_| | (_) |
# |_| |_| |_|\__,_|\__, |_|\___| \_/\_/ \__,_|_|_(_)_|\___/
#                  |___/
#
# magicwall.io - a magic wall
# Copyright (C) 2022 - Frans Fürst
#
# magicwall.io is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# magicwall.io is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details at
# <http://www.gnu.org/licenses/>.
#


"""This module implements a Python API around REST calls to a magicwall.io web server currently
just used for testing.
"""


class MagicWall:
    """Connects to and interfaces a magicwall.io site"""

    def __init__(self, hostname: str, port: int) -> None:
        """Not yet implemented"""
        print(f"does not yet connect to {hostname}:{port}")

    def handle_dragdrop_data(self, data: object) -> None:
        """Not yet implemented"""
        print(f"does not yet handle {self}:{data}")
