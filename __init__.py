# Copyright (C) 2004  Nuxeo SARL <http://nuxeo.com>
# Author : Julien Anguenot <ja@nuxeo.com>

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
# $Id$

"""CPSChat is chat product for CPS3.
"""

import permissions

import CPSMemberShipPatch

from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.permissions import AddPortalContent

import Chat
import ChatItem

contentClasses = ( Chat.Chat,
                   ChatItem.ChatItem, )

contentConstructors = ( Chat.addChat,
                        ChatItem.addChatItem, )

fti = (Chat.factory_type_information +
       ChatItem.factory_type_information)

registerDirectory('skins', globals())

def initialize(registrar):
    utils.ContentInit('Chat Content',
                      content_types=contentClasses,
                      permission=AddPortalContent,
                      extra_constructors=contentConstructors,
                      fti=fti
                      ).initialize(registrar)
