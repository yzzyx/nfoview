# -*- coding: utf-8 -*-

# Copyright (C) 2008 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
Viewer for NFO files.

:var __version__: Version number as string in format ``MAJOR.MINOR[.PATCH]``
:var CONFIG_HOME_DIR: Path to user's local configuration directory
:var DATA_DIR: Path to the global data directory
:var LOCALE_DIR: Path to the global locale directory
:var conf: Instance of :class:`ConfigurationStore` used
"""

__version__ = "1.15"

import os

from nfoview.paths import *

from gi.repository import Gtk
Gtk.IconTheme.get_default().append_search_path(
    os.path.abspath(os.path.join(DATA_DIR, "icons")))

from nfoview import i18n
from nfoview import util
from nfoview import sauce
from nfoview import file
from nfoview.errors import *
from nfoview.config import *

conf = ConfigurationStore()
conf.read_from_file()

from nfoview.schemes import *
from nfoview.builder import *
from nfoview.about import *
from nfoview.open import *
from nfoview.preferences import *
from nfoview.export import *
from nfoview.view import *
from nfoview import actions
from nfoview.window import *
from nfoview import main
from nfoview.unittest import *
