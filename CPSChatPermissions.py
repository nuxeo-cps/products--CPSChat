# (C) Copyright 2004 Nuxeo SARL <http://nuxeo.com>
# Author: Julien Anguenot <ja@nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
# $Id$

__author__ = "Julien Anguenot <ja@nuxeo.com>"

"""CPS Chat Permissions

  - 'Chat Moderate' : Permission you need to moderate the chat

  - 'Chat Reply'    : Permission you need to answer question

  - 'Chat Post'     : Permission you need to post question
"""

from Products.CMFCore.permissions import setDefaultRoles

chatModerate = 'Chat Moderate'
setDefaultRoles(chatModerate, ('Manager', 'Owner'))

chatReply = 'Chat Reply'
setDefaultRoles(chatReply, ('Manager', 'Owner'))

chatPost = 'Chat Post'
setDefaultRoles(chatPost, ('Manager', 'Owner'))
