# Copyright (C) 2002-2003  Nuxeo <http://www.nuxeo.com>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#$Id$

"""
Class used for the project of the Interior Ministry of France.
"""

import string, re

_bad = " ()[]{},'?ÄÅÁÀÂÃäåáàâãÇçÉÈÊËéèêëæÍÌÎÏíìîïÑñÖÓÒÔÕØöóòôõøŠšßÜÚÙÛüúùûİŸıÿ"
_good = '__________AAAAAAaaaaaaCcEEEEeeeeeIIIIiiiiNnOOOOOOooooooSssUUUUuuuuYYyyZz'
_transmap = string.maketrans(_bad, _good)

_with_accents = 'ÄÅÁÀÂÃäåáàâãÇçÉÈÊËéèêëæÍÌÎÏíìîïÑñÖÓÒÔÕØöóòôõøŠšßÜÚÙÛüúùûİŸıÿ'
_without_accents = 'AAAAAAaaaaaaCcEEEEeeeeeIIIIiiiiNnOOOOOOooooooSssUUUUuuuuYYyy'
_remove_accents_map = string.maketrans(_with_accents, _without_accents)


def get_id_from_title(id):
    id = id.split('\\')[-1]
    id = string.strip(id)

    return id.translate(_transmap)


def get_body_from_all3(id):
    # work only with small files
    search = re.search(r'(?is)<body>(.*?)</body>',id)
    if search:
        id = search.group(1)
    return id


def get_body_from_all2(id):
    # idem than get_body_from_all3 but longer
    pat = re.compile(r'(?is)<body>(.*?)</body>')
    found = pat.search(id)
    if found:
        id = found.group(1)
    return id


def get_body_from_all(data):
   # work everytime and using less resources
   body_start_m = re.search(r'<body.*?>(?i)(?s)', data)
   if body_start_m:
     data = data[body_start_m.end():]
   body_end_m = re.search('</body.*?>(?i)(?s)', data)
   if body_end_m:
     data = data[:body_end_m.start()]
   return data

def remove_accents(data):
    return data.translate(_remove_accents_map)

