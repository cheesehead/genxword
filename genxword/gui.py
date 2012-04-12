# -*- coding: utf-8 -*-

# Authors: David Whitlock <alovedalongthe@gmail.com>, Bryan Helmig
# Crossword generator that outputs the grid and clues as a pdf file and/or
# the grid in png/svg format with a text file containing the words and clues.
# Copyright (C) 2010-2011 Bryan Helmig
# Copyright (C) 2011-2012 David Whitlock
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, tempfile
from gi.repository import Gtk, Pango
from . import control

help_text = """genxword-gtk
Genxword-gtk is a crossword generator, which produces pdf (A4 or letter size) versions of the grid and clues, \
or png / svg versions of the crossword grid, together with a text file containing the words and clues.\n
New - create a new word list
If you click on the New button, the screen will be cleared and you will be able to create a new word list. \
The word list can be just a list of words, like this:\n
history
spam
vikings\n
or it can be a list or words and clues, like this:\n
excalibur A sword that a moistened bint lobbed at Arthur.
duck An animal that weighs the same as a witch.
coconut A fruit that possibly migrates.\n
As you can see, each word needs to be on a separate line, and there should be a space between each word and its clue. \
The clue is everything after the first space.\n
Open - open a word list
The Open button lets you open, and edit, a word list, which needs to be formatted as written above. \
The word list can be thousands of words long. If you use a large word list, the crossword will be created \
with a set amount of words randomly selected from it. The default number of words is 50.\n
Calculate - create the crossword
Click on Calculate to create the crossword. If you click on it a second time, the crossword will be recalculated.\n
Inc grid size - increase the grid size and recalculate
This button gives you the option of increasing the grid size before recalculating the crossword.\n
Save - save the crossword
This button lets you choose where you save the crossword files.\n
Further options
In the entry box below, you can write the name of the crossword.\nYou can save the crossword in pdf, png \
and / or svg format. Just toggle the appropriate buttons below.
"""
save_recalc = """\nIf you want to save this crossword, press the Save button.
If you want to recalculate the crossword, press the Calculate button.
To increase the grid size and then recalculate the crossword, 
press the Inc grid size button.
"""

class Genxinterface(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='genxword-gtk')

        self.set_default_size(-1, 500)
        self.saveformat = ''

        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.grid.set_border_width(6)
        self.grid.set_row_spacing(6)
        self.grid.set_column_spacing(12)

        self.textview_win()
        self.check_buttons()
        self.tool_buttons()

    def textview_win(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 1, 7, 1)

        self.textview = Gtk.TextView()
        self.textview.set_border_width(6)
        fontdesc = Pango.FontDescription('serif')
        self.textview.modify_font(fontdesc)
        self.textbuffer = self.textview.get_buffer()
        self.tag_title = self.textbuffer.create_tag('title', font='sans bold 12')
        self.tag_subtitle = self.textbuffer.create_tag('subtitle', font='sans bold')
        self.tag_mono = self.textbuffer.create_tag('mono', font='monospace')
        self.help_message()
        scrolledwindow.add(self.textview)

    def check_buttons(self):
        self.enter_name = Gtk.Entry()
        self.enter_name.set_text('Name of crossword')
        self.enter_name.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, Gtk.STOCK_CLEAR)
        self.enter_name.connect('icon-press', self.entry_cleared)
        self.grid.attach(self.enter_name, 0, 2, 2, 1)

        save_A4pdf = Gtk.CheckButton('_A4 pdf', use_underline=True)
        save_A4pdf.set_active(False)
        save_A4pdf.connect('toggled', self.save_options, 'p')
        self.grid.attach(save_A4pdf, 2, 2, 1, 1)

        save_letterpdf = Gtk.CheckButton('_letter pdf', use_underline=True)
        save_letterpdf.set_active(False)
        save_letterpdf.connect('toggled', self.save_options, 'l')
        self.grid.attach(save_letterpdf, 3, 2, 1, 1)

        save_png = Gtk.CheckButton('pn_g', use_underline=True)
        save_png.set_active(False)
        save_png.connect('toggled', self.save_options, 'n')
        self.grid.attach(save_png, 4, 2, 1, 1)

        save_svg = Gtk.CheckButton('s_vg', use_underline=True)
        save_svg.set_active(False)
        save_svg.connect('toggled', self.save_options, 's')
        self.grid.attach(save_svg, 5, 2, 1, 1)

    def entry_cleared(self, entry, position, event):
        self.enter_name.set_text('')
        self.enter_name.grab_focus()

    def save_options(self, button, name):
        if button.get_active():
            self.saveformat += name
        else:
            self.saveformat = self.saveformat.replace(name, '')

    def tool_buttons(self):
        button_new = Gtk.Button(stock=Gtk.STOCK_NEW)
        button_new.connect('clicked', self.new_wlist)
        self.grid.attach(button_new, 0, 0, 1, 1)

        button_open = Gtk.Button(stock=Gtk.STOCK_OPEN)
        button_open.connect('clicked', self.open_wlist)
        self.grid.attach(button_open, 1, 0, 1, 1)

        button_calc = Gtk.Button(stock=Gtk.STOCK_EXECUTE)
        self.button_name(button_calc, '_Create')
        button_calc.connect('clicked', self.calc_xword)
        self.grid.attach(button_calc, 2, 0, 1, 1)

        button_incgsize = Gtk.Button(stock=Gtk.STOCK_REDO)
        self.button_name(button_incgsize, '_Inc size')
        button_incgsize.connect('clicked', self.incgsize)
        self.grid.attach(button_incgsize, 3, 0, 1, 1)

        button_save = Gtk.Button(stock=Gtk.STOCK_SAVE)
        button_save.connect('clicked', self.save_xword)
        self.grid.attach(button_save, 4, 0, 1, 1)

        button_help = Gtk.Button(stock=Gtk.STOCK_HELP)
        button_help.connect('clicked', self.help_page)
        self.grid.attach(button_help, 5, 0, 1, 1)

        button_quit = Gtk.Button(stock=Gtk.STOCK_QUIT)
        button_quit.connect('clicked', Gtk.main_quit)
        self.grid.attach(button_quit, 6, 0, 1, 1)

    def button_name(self, name, display):
        label = name.get_children()[0]
        label = label.get_children()[0].get_children()[1]
        label = label.set_label(display)

    def new_wlist(self, button):
        self.textview.set_editable(True)
        self.textview.set_cursor_visible(True)
        self.textview.set_wrap_mode(Gtk.WrapMode.NONE)
        self.textbuffer.set_text('')

    def open_wlist(self, button):
        dialog = Gtk.FileChooserDialog('Please choose a file', self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            with open(dialog.get_filename()) as infile:
                data = infile.read()
            self.textview.set_editable(True)
            self.textview.set_cursor_visible(True)
            self.textview.set_wrap_mode(Gtk.WrapMode.NONE)
            self.textbuffer.set_text(data)
        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name('Text files')
        filter_text.add_mime_type('text/plain')
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name('Any files')
        filter_any.add_pattern('*')
        dialog.add_filter(filter_any)

    def calc_xword(self, button):
        self.textview.set_wrap_mode(Gtk.WrapMode.NONE)
        buff = self.textview.get_buffer()
        rawtext = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), False)
        if save_recalc in rawtext:
            self.textbuffer.set_text(self.gen.calcgrid())
            self.add_tag(self.tag_mono, 0, -1)
            self.textbuffer.insert_at_cursor(save_recalc)
        else:
            fd, wordlist = tempfile.mkstemp()
            with open(wordlist, 'w') as wlist_file:
                wlist_file.write(rawtext)
            self.textview.set_editable(False)
            self.textview.set_cursor_visible(False)
            self.gen = control.Genxword()
            with open(wordlist) as infile:
                self.gen.wlist(infile)
            self.gen.grid_size(True)
            self.textbuffer.set_text(self.gen.calcgrid())
            self.add_tag(self.tag_mono, 0, -1)
            self.textbuffer.insert_at_cursor(save_recalc)
            os.close(fd)
            os.remove(wordlist)

    def incgsize(self, button):
        self.textview.set_wrap_mode(Gtk.WrapMode.NONE)
        self.textbuffer.set_text(self.gen.calcgrid(True))
        self.add_tag(self.tag_mono, 0, -1)
        self.textbuffer.insert_at_cursor(save_recalc)

    def save_xword(self, button):
        self.xwordname = self.enter_name.get_text()
        if self.saveformat and self.xwordname != 'Name of crossword':
            dialog = Gtk.FileChooserDialog('Please choose a folder', self,
                Gtk.FileChooserAction.SELECT_FOLDER,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 'Select', Gtk.ResponseType.OK))

            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                os.chdir(dialog.get_filename())
            dialog.destroy()

            self.gen.savefiles(self.saveformat, self.xwordname, True)
            saved_message = 'Your crossword files have been saved in ' + os.getcwd()
            self.textbuffer.set_text(saved_message)
            self.enter_name.set_text('Name of crossword')
        else:
            self.textbuffer.set_text('Please fill in the name of the crossword and how you want it saved.')
            self.textbuffer.insert_at_cursor('\nThen click on the Save button again.')

    def help_page(self, button):
        self.help_message()

    def help_message(self):
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.textbuffer.set_text(help_text)
        self.add_tag(self.tag_title, 0, 1)
        self.add_tag(self.tag_subtitle, 3, 4)
        self.add_tag(self.tag_subtitle, 18, 19)
        self.add_tag(self.tag_subtitle, 21, 22)
        self.add_tag(self.tag_subtitle, 24, 25)
        self.add_tag(self.tag_subtitle, 27, 28)
        self.add_tag(self.tag_subtitle, 30, 31)

    def add_tag(self, tag_name, startline, endline):
        start = self.textbuffer.get_iter_at_line(startline)
        end = self.textbuffer.get_iter_at_line(endline)
        self.textbuffer.apply_tag(tag_name, start, end)

def main():
    win = Genxinterface()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
