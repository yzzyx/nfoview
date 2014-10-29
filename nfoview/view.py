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

"""Text view widget for NFO text with support for clickable hyperlinks."""

import nfoview
import re

from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Pango

__all__ = ("TextView",)


class TextView(Gtk.TextView):

    """Text view widget for NFO text with support for clickable hyperlinks."""

    def __init__(self):
        """Initialize a :class:`TextView` instance."""
        GObject.GObject.__init__(self)
        self._link_tags = []
        self._visited_link_tags = []
        self._init_properties()
        self.update_colors()

    def get_text(self):
        """Return the text in the text view."""
        text_buffer = self.get_buffer()
        start, end = text_buffer.get_bounds()
        return text_buffer.get_text(start, end, False)

    def _init_properties(self):
        """Initliaze text view widget properties."""
        pixels_above = nfoview.conf.pixels_above_lines
        pixels_below = nfoview.conf.pixels_below_lines
        font_desc = nfoview.util.get_font_description()
        self.set_cursor_visible(False)
        self.set_editable(False)
        self.set_wrap_mode(Gtk.WrapMode.NONE)
        self.set_pixels_above_lines(pixels_above)
        self.set_pixels_below_lines(pixels_below)
        self.set_left_margin(6)
        self.set_right_margin(6)
        self.override_font(font_desc)
        nfoview.util.connect(self, self, "motion-notify-event")

    def _insert_href(self, url, start_pos, end_pos):
        text_buffer = self.get_buffer()
        tag = text_buffer.create_tag(None)
        tag.props.underline = Pango.Underline.SINGLE
        tag.connect("event", self._on_link_tag_event)
        tag.nfoview_url = url
        start_itr = text_buffer.get_iter_at_offset(start_pos)
        end_itr = text_buffer.get_iter_at_offset(end_pos)
        text_buffer.apply_tag(tag, start_itr, end_itr)
        self._link_tags.append(tag)

    def _insert_url(self, url):
        """Insert `url` into the text view as a hyperlink."""
        text_buffer = self.get_buffer()
        start_itr = text_buffer.get_end_iter()
        text_buffer.insert(url)
        end_itr = text_buffer.get_end_iter()
        self._insert_href(url, start_itr.get_offset(), end_itr.get_offset())


    def _insert_word(self, word, tags = None):
        """Insert `word` into the text view."""
        text_buffer = self.get_buffer()
        itr = text_buffer.get_end_iter()
        if tags:
            text_buffer.insert_with_tags(itr, word, *tags)
        else:
            text_buffer.insert(itr, word)

        """
        tag_str = ""
        for tag in tags:
            tag_str += tag.props.name
            text_buffer.apply_tag(tag, itr, text_buffer.get_end_iter())
        print("Adding text %s with tags: %s" % (word, tag_str))
        """

    def _on_link_tag_event(self, tag, text_view, event, itr):
        """Open clicked hyperlink in web browser."""
        if event.type != Gdk.EventType.BUTTON_RELEASE: return
        text_buffer = self.get_buffer()
        if text_buffer.get_selection_bounds(): return
        nfoview.util.show_uri(tag.nfoview_url)
        if tag in self._link_tags:
            self._link_tags.remove(tag)
            self._visited_link_tags.append(tag)
            self.update_colors()

    def _on_motion_notify_event(self, text_view, event):
        """Change the mouse pointer when hovering over a hyperlink."""
        window = Gtk.TextWindowType.WIDGET
        x, y = self.window_to_buffer_coords(window, int(event.x), int(event.y))
        window = self.get_window(Gtk.TextWindowType.TEXT)
        for tag in self.get_iter_at_location(x, y).get_tags():
            if hasattr(tag, "nfoview_url"):
                window.set_cursor(Gdk.Cursor(cursor_type=Gdk.CursorType.HAND2))
                return True # to not call the default handler.
        window.set_cursor(Gdk.Cursor(cursor_type=Gdk.CursorType.XTERM))

    def set_text(self, text, text_type = 'ASCII', screen_width = 0):
        """Set the text displayed in the text view."""
        re_url = re.compile(r"(([0-9a-zA-Z]+://\S+?\.\S+)|(www\.\S+?\.\S+))")
        self._link_tags = []
        self._visited_link_tags = []
        text_buffer = self.get_buffer()
        bounds = text_buffer.get_bounds()
        text_buffer.remove_all_tags(*bounds)
        text_buffer.delete(*bounds)

        lines = text.splitlines()

        if text_type == 'ANSI':
            if screen_width == 0:
                screen_width = 80

            # Create colors
            fg_color_tags_normal =  {
                    30: text_buffer.create_tag("color_30", foreground_rgba=Gdk.RGBA(0.0,0,0,1.0)),
                    31: text_buffer.create_tag("color_31", foreground_rgba=Gdk.RGBA(0.66,0,0,1.0)),
                    32: text_buffer.create_tag("color_32", foreground_rgba=Gdk.RGBA(0,0.66,0,1.0)),
                    33: text_buffer.create_tag("color_33", foreground_rgba=Gdk.RGBA(0.66,0.33,1.0)),
                    34: text_buffer.create_tag("color_34", foreground_rgba=Gdk.RGBA(0,0,0.66,1.0)),
                    35: text_buffer.create_tag("color_35", foreground_rgba=Gdk.RGBA(0.66,0,0.66,1.0)),
                    36: text_buffer.create_tag("color_36", foreground_rgba=Gdk.RGBA(0,0.66,0.66,1.0)),
                    37: text_buffer.create_tag("color_37", foreground_rgba=Gdk.RGBA(0.66,0.66,0.66,1.0)),
                    }
            fg_color_tags_high =  {
                    30: text_buffer.create_tag("color_30_hi", foreground_rgba=Gdk.RGBA(0.33,0.33,0.33,1.00)),
                    31: text_buffer.create_tag("color_31_hi", foreground_rgba=Gdk.RGBA(1.00,0.33,0.33,1.00)),
                    32: text_buffer.create_tag("color_32_hi", foreground_rgba=Gdk.RGBA(0.33,1.00,0.33,1.00)),
                    33: text_buffer.create_tag("color_33_hi", foreground_rgba=Gdk.RGBA(1.00,1.00,0.33,1.00)),
                    34: text_buffer.create_tag("color_34_hi", foreground_rgba=Gdk.RGBA(0.33,0.33,1.00,1.00)),
                    35: text_buffer.create_tag("color_35_hi", foreground_rgba=Gdk.RGBA(1.00,0.33,1.00,1.00)),
                    36: text_buffer.create_tag("color_36_hi", foreground_rgba=Gdk.RGBA(0.33,1.00,1.00,1.00)),
                    37: text_buffer.create_tag("color_37_hi", foreground_rgba=Gdk.RGBA(1.00,1.00,1.00,1.00)),
                    }

            bg_color_tags_normal =  {
                    40: text_buffer.create_tag("color_40", background_rgba=Gdk.RGBA(0.00,0.00,0.00,1.00)),
                    41: text_buffer.create_tag("color_41", background_rgba=Gdk.RGBA(0.66,0.00,0.00,1.00)),
                    42: text_buffer.create_tag("color_42", background_rgba=Gdk.RGBA(0.00,0.66,0.00,1.00)),
                    43: text_buffer.create_tag("color_43", background_rgba=Gdk.RGBA(0.66,0.33,0.00,1.00)),
                    44: text_buffer.create_tag("color_44", background_rgba=Gdk.RGBA(0.00,0.00,0.66,1.00)),
                    45: text_buffer.create_tag("color_45", background_rgba=Gdk.RGBA(0.66,0.00,0.66,1.00)),
                    46: text_buffer.create_tag("color_46", background_rgba=Gdk.RGBA(0.00,0.66,0.66,1.00)),
                    47: text_buffer.create_tag("color_47", background_rgba=Gdk.RGBA(0.66,0.66,0.66,1.00)),
                    }

            bold_tag = text_buffer.create_tag("bold", weight=Pango.Weight.BOLD)
            underline_tag = text_buffer.create_tag("underline", underline=Pango.Underline.SINGLE)
            # Blink, slow <150/m
            # Blink, rapid >150/m
            # Inverse video
            # 22 - Normal color
            # 25 - Blink off

            active_fg_color = 37
            active_bg_color = 40
            active_fg_color_tag = fg_color_tags_normal[active_fg_color]
            active_bg_color_tag = bg_color_tags_normal[active_bg_color]

            active_tags = [ active_fg_color_tag, active_bg_color_tag, ]
            use_high = False
            use_inverse = False

            re_ansi = re.compile(r"\033\[(.*?)([A-Za-z])")

            for i, line in enumerate(lines):
                line_length = 0
                matches = re_ansi.finditer(line)
                last_match = 0
                for m in matches:
                    # Add text before ANSI escape code
                    text_to_add = line[last_match:m.start(0)]
                    if screen_width:
                        while (line_length + len(text_to_add)) > screen_width:
                            self._insert_word(text_to_add[:screen_width - line_length] + '\n', active_tags)
                            text_to_add = text_to_add[screen_width - line_length:]
                            line_length = 0

                    self._insert_word(text_to_add, active_tags)
                    line_length += len(text_to_add)
                    last_match = m.end(0)

                    # Handle escape code
                    code = m.group(2)
                    modifier = m.group(1)

                    if code == "m":
                        modifiers = modifier.split(";")
                        for modifier in modifiers:
                            modifier = int(modifier)
                            # SGR parameters
                            if modifier == 0:
                                active_fg_color = 37
                                active_bg_color = 40
                                use_high = False
                                use_inverse = False

                            elif modifier == 1:
                                use_high = True

                            elif modifier == 7: # Inverse, swap fg and bg
                                use_inverse = True

                            elif modifier == 21: # Bold: off or Underline: double
                                use_high = False

                            elif modifier == 22: # Normal color or intesity
                                use_high = False

                            elif modifier == 27: # Normal color or intesity
                                use_inverse = False

                            elif modifier >= 30 and modifier <= 37: # fg colors
                                active_fg_color = modifier

                            elif modifier >= 40 and modifier <= 47: # fg colors
                                active_bg_color = modifier
                            else:
                                print("Unhandled SGR flag %d" % modifier)

                        if use_high:
                            active_fg_color_tag = fg_color_tags_high[active_fg_color]
                        else:
                            active_fg_color_tag = fg_color_tags_normal[active_fg_color]
                        active_bg_color_tag = bg_color_tags_normal[active_bg_color]

                        active_tags = [ active_fg_color_tag, active_bg_color_tag, ]

                    elif code == "C": # Move cursor n steps to the right
                        if screen_width:
                            while (line_length + int(modifier)) > screen_width:
                                self._insert_word(" " * (screen_width - line_length) + '\n', active_tags)
                                modifier = int(modifier) - (screen_width - line_length)
                                line_length = 0
                        self._insert_word(" " * int(modifier), active_tags)
                        line_length += int(modifier)
                    elif code == "A": # Cursor UP
                        print("ANSI Cursor up not handled!")
                    else:
                        print("Unhandled ANSI escape code %s" % code)

                # Add text after last escape-code
                text_to_add = line[last_match:]
                if screen_width:
                    while (line_length + len(text_to_add)) > screen_width:
                        self._insert_word(text_to_add[:screen_width - line_length] + '\n', active_tags)
                        text_to_add = text_to_add[screen_width - line_length:]
                        line_length = 0

                self._insert_word(text_to_add, active_tags)
                line_length += len(text_to_add)

                suffix = ""
                if line_length < 80:
                    suffix = " " * (80 - line_length)
                self._insert_word(suffix + "\n", active_tags)

        else:
            for i, line in enumerate(lines):
                self._insert_word(line+"\n")

        # Get all text from our textview, and find any/all urls
        text = self.get_text()
        matches = re_url.finditer(text)
        for m in matches:
            print("add href %s @ %d,%d" % (m.group(0), m.start(0),
                m.end(0)))
            self._insert_href(m.group(0),m.start(0),m.end(0))

        self.update_colors()
        """

            words = line.split(" ")
            for j, word in enumerate(words):
                match = re_url.search(word)
                if match is not None:
                    a, z = match.span()
                    word_queue.append(word[:a])
                    self._insert_word("".join(word_queue))
                    word_queue = []
                    self._insert_url(word[a:z])
                    word_queue.append(word[z:])
                else: # Normal text.
                    word_queue.append(word)
                word_queue.append(" ")
            word_queue.pop(-1)
            word_queue.append("\n")
            if len(word_queue) > 100:
                self._insert_word("".join(word_queue))
                word_queue = []
        self._insert_word("".join(word_queue))
        """

    def update_colors(self):
        """Update colors to match the current color scheme."""
        name = nfoview.conf.color_scheme
        scheme = nfoview.util.get_color_scheme(name, "default")
        state = Gtk.StateFlags.NORMAL
        self.override_color(state, scheme.foreground)
        self.override_background_color(state, scheme.background)
        entry = Gtk.Entry()
        entry.show()
        style = entry.get_style_context()
        state = Gtk.StateFlags.SELECTED
        foreground = style.get_color(state)
        background = style.get_background_color(state)
        self.override_color(state, foreground)
        self.override_background_color(state, background)
        for tag in self._link_tags:
            tag.props.foreground_rgba = scheme.link
        for tag in self._visited_link_tags:
            tag.props.foreground_rgba = scheme.visited_link
