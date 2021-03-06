#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# Authors: David Whitlock <alovedalongthe@gmail.com>, Bryan Helmig
# Crossword generator that outputs the grid and clues as a pdf file and/or
# the grid in png/svg format with a text file containing the words and clues.
# Copyright (C) 2010-2011 Bryan Helmig
# Copyright (C) 2011-2014 David Whitlock
#
# Genxword is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Genxword is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with genxword.  If not, see <http://www.gnu.org/licenses/gpl.html>.

import os
import subprocess
from distutils.core import setup

lang_files = []
os.mkdir('mo')
for pofile in os.listdir('po'):
    lang = pofile.strip('.po')
    os.mkdir(os.path.join('mo', lang))
    mofile = os.path.join('mo', lang, 'genxword.mo')
    subprocess.call('msgfmt {} -o {}'.format(os.path.join('po', pofile), mofile), shell=True)
    lang_files.append(['share/locale/{}/LC_MESSAGES/'.format(lang), [mofile]])

setup(
    name = 'genxword',
    version = '1.0.1',
    packages = ['genxword'],
    scripts = ['bin/genxword', 'bin/genxword-gtk'],
    data_files = [
        ('share/applications', ['genxword-gtk.desktop']),
        ('share/pixmaps', ['genxword-gtk.png']),
        ('share/genxword', ['gumby.lang', 'help_page']),
        ('share/genxword/word_lists', ['word_lists/2000ENwords', 'word_lists/pythonwords']),
        ] + lang_files,
    author = 'David Whitlock',
    author_email = 'alovedalongthe@gmail.com',
    url = 'https://github.com/riverrun/genxword',
    description = 'A crossword generator',
    license = 'GPLv3',
)
