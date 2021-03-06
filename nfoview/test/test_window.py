# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
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

import nfoview

from gi.repository import Gtk


class TestWindow(nfoview.TestCase):

    def run_window(self):
        self.window.show()
        self.window.connect("delete-event", Gtk.main_quit)
        Gtk.main()

    def setup_method(self, method):
        self.window = nfoview.Window(self.new_nfo_file())

    def test__on_close_document_activate(self):
        self.window._get_action("close_document").activate()

    def test__on_copy_text_activate(self):
        self.window._get_action("select_all_text").activate()
        self.window._get_action("copy_text").activate()

    def test__on_edit_preferences_activate(self):
        self.window._get_action("edit_preferences").activate()
        self.window._get_action("edit_preferences").activate()
        self.window._preferences_dialog.response(Gtk.ResponseType.CLOSE)
        self.window._get_action("edit_preferences").activate()

    def test__on_escape_pressed(self):
        self.window._on_escape_pressed()

    @nfoview.util.monkey_patch(nfoview, "OpenDialog")
    def test__on_open_file_activate(self):
        nfoview.OpenDialog.run = lambda *args: Gtk.ResponseType.CANCEL
        self.window._get_action("open_file").activate()

    def test__on_quit_activate(self):
        nfoview.main.windows.append(self.window)
        self.window._get_action("quit").activate()

    def test__on_select_all_text_activate(self):
        self.window._get_action("select_all_text").activate()

    def test__on_show_about_dialog_activate(self):
        self.window._get_action("show_about_dialog").activate()
        self.window._get_action("show_about_dialog").activate()
        self.window._about_dialog.response(Gtk.ResponseType.CLOSE)
        self.window._get_action("show_about_dialog").activate()

    def test__on_wrap_lines_activate(self):
        self.window._get_action("wrap_lines").activate()
        self.window._get_action("wrap_lines").activate()
        self.window._get_action("wrap_lines").activate()

    def test_open_file__blank_lines(self):
        path = self.new_nfo_file()
        with open(path, "a") as f:
            f.write("\n\n\n")
        self.window.open_file(path)

    def test_open_file__even_lines(self):
        path = self.new_nfo_file()
        with open(path, "a") as f:
            f.write("\na\n\na\n\n")
        self.window.open_file(path)

    def test_open_file__odd_lines(self):
        path = self.new_nfo_file()
        with open(path, "w") as f:
            f.write("a\n\na\n\n")
        self.window.open_file(path)

    def test_resize_to_text__blank(self):
        self.window = nfoview.Window()
        self.window.resize_to_text()

    def test_resize_to_text__long_file(self):
        path = self.new_nfo_file()
        with open(path, "w") as f:
            f.write("aaa\n" * 100)
        self.window.open_file(path)
        self.window.resize_to_text()

    def test_resize_to_text__long_lines(self):
        path = self.new_nfo_file()
        with open(path, "w") as f:
            f.write("aaa " * 100)
        self.window.open_file(path)
        self.window.resize_to_text()
