# Copyright (C) 2004  Nuxeo <http://www.nuxeo.com/>
# Author: Julien Anguenot <ja@nuxeo.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License version 2
# as published by the Free Software Foundation; either version 2.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# $Id$

__author__ = "Julien Anguenot <ja@nuxeo.com>"

"""Chat Item

Chat Item is used to store the content of the messages posted within the chat.
This object will follow a given workflow for moderation purposes

It may includes other chat items whish correspond to replies from the chat guest
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from AccessControl.SecurityManagement import newSecurityManager
from Acquisition import aq_inner, aq_parent

from Products.CMFCore.CMFCorePermissions import View

from Products.CPSCore.CPSBase import CPSBase_adder, CPSBaseDocument
from Products.CPSCore.CPSMembershipTool import CPSUnrestrictedUser

from CPSChatPermissions import chatModerate, chatReply

factory_type_information = (
    { 'id': 'ChatItem',
      'meta_type': 'ChatItem',
      'description': 'portal_type_ChatItem_description',
      'icon': 'document_icon.gif',
      'title': "portal_type_ChatItem_title",
      'product': 'CPSChat',
      'factory': 'addChatItem',
      'immediate_view': 'cps_chat_item_edit_form',
      'filter_content_types': 0,
      'allowed_content_types': (),
      'allow_discussion': 0,
      'actions': ({'id': 'edit',
                   'name': 'action_edit',
                   'action': 'cps_chat_item_edit_form',
                   'permissions': (chatModerate,),
                   },
                  {'id': 'reply',
                   'name': 'action_chat_item_reply',
                   'action': 'cps_chat_item_reply_to_form',
                   'permissions': (chatModerate, chatReply),
                   },
                  ),
      },
    )

class ChatItem(CPSBaseDocument):
    """Chat Item

    Chat Item is used to store the content of the messages posted within the chat.
    This object will follow a given workflow for moderation purposes

    It may includes other chat items whish correspond to replies from the chat guest
    """

    meta_type="ChatItem"
    portal_type = meta_type

    security = ClassSecurityInfo()

    _properties = CPSBaseDocument._properties + (
        {'id': 'message', 'type': 'string'},
        {'id': 'pseudo', 'type': 'string'},
        )

    message = ''
    pseudo  = ''

    def __init__(self, id, **kw):
        """Constructor
        """
        CPSBaseDocument.__init__(self, id, **kw)

    security.declareProtected(chatModerate, 'editProps')
    def editProps(self, **kw):
        """Edit properties
        """
        self.manage_changeProperties(**kw)

    security.declareProtected(chatReply, 'hasReply')
    def hasReply(self):
        """Has this message a reply
        """
        return self.objectIds() and 1

    def getCreator(self):
        """Returns the creator of the message
        """
        if self.pseudo:
            return self.pseudo
        else:
            return self.Creator()

    ####################################################
    ####################################################

    security.declareProtected(View, 'getPublicReplies')
    def getPublicReplies(self):
        """Return the eventual published replies to this message
        """
        wftool = self.portal_workflow
        list = []
        for post in self.objectValues():
            if wftool.getInfoFor(post, 'review_state') == 'published':
                list.append(post)
        return list

    security.declareProtected(chatModerate, 'getPendingReplies')
    def getPendingReplies(self):
        """Returns the replies waiting for moderation
        """
        wftool = self.portal_workflow
        list = []
        for post in self.objectValues():
            if wftool.getInfoFor(post, 'review_state') == 'waiting':
                list.append(post)
        return list

    ####################################################
    ####################################################

    security.declareProtected(chatReply, 'addReply')
    def addReply(self, message=''):
        """Add a reply to this message
        """

        # FIXME fix this mess
        mtool = self.portal_membership
        user = mtool.getAuthenticatedMember()
        member_id = user.getMemberId()

        # Create a tmp_user to create the post
        tmp_user = CPSUnrestrictedUser(member_id, '',
                                       ['ChatModerator'], '')
        tmp_user = tmp_user.__of__(self.acl_users)
        newSecurityManager(None, tmp_user)

        new_id = self.computeId() # skins
        self.invokeFactory('ChatItem', new_id)
        ob = getattr(self, new_id)
        # FIXME
        ob.message = message

        if not aq_parent(aq_inner(self)).isModerated():
            wftool = self.portal_workflow
            wftool.doActionFor(ob,
                               'publish_post',
                               comment='Not moderated post',
                               workflow_id='chat_item_wf')

            # Revert to original user.
            newSecurityManager(None, user)
    
    def publishInitialPost(self):
        wftool = self.portal_workflow
        parent = self.aq_inner.aq_parent
        if wftool.getInfoFor(parent, 'review_state') == 'pending':
            wftool.doActionFor(parent,
                       'publish_post',
                       comment='Publish question along with answer',
                       workflow_id='chat_item_wf')

InitializeClass(ChatItem)

def addChatItem(container, id, REQUEST=None, **kw):
    """Add a Chat Item
    """
    ob = ChatItem(id, **kw)
    return CPSBase_adder(container, ob, REQUEST=REQUEST)
