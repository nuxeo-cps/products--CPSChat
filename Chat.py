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

"""Chat module for CPS.
"""

from zLOG import LOG, DEBUG

import time

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from AccessControl.SecurityManagement import newSecurityManager

from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2Base

from Products.CMFCore.permissions import View

from Products.CPSCore.CPSBase import CPSBaseFolder, CPSBase_adder
from Products.CPSCore.CPSMembershipTool import CPSUnrestrictedUser

from CPSChatPermissions import chatModerate, chatReply, chatPost

factory_type_information = (
    { 'id': 'Chat',
      'meta_type': 'Chat',
      'description': 'portal_type_CPSChat_description',
      'icon': 'chat_icon.gif',
      'title': "portal_type_CPSChat_title",
      'product': 'CPSChat',
      'factory': 'addChat',
      'immediate_view': 'cps_chat_edit_form',
      'filter_content_types': 0,
      'allowed_content_types': (),
      'allow_discussion': 0,
      'actions': ({'id': 'view',
                   'name': 'action_view',
                   'action': 'cps_chat_view',
                   'permissions': (View,),
                   },
                  {'id': 'edit',
                   'name': 'action_edit',
                   'action': 'cps_chat_edit_form',
                   'permissions': (chatModerate,),
                   },
                  {'id': 'moderate_chat',
                   'name': 'action_moderate_chat',
                   'action': 'cps_chat_moderate_form',
                   'permissions': (chatModerate,),
                   },
                  {'id': 'action_chat_reply_to_questions',
                   'name': 'action_chat_reply_to_questions',
                   'action': 'cps_chat_answer_form',
                   'permissions': (chatReply,),
                   },
                  {'id': 'localroles',
                   'name': 'action_local_roles',
                   'action': 'cps_chat_localrole_form',
                   'permissions': (chatModerate,)
                   },
                  ),
      'cps_display_as_document_in_listing' : 1,
      },
    )

class Chat(BTreeFolder2Base, CPSBaseFolder):
    """Chat class
    """

    meta_type = "Chat"
    portal_type = meta_type

    security = ClassSecurityInfo()

    _properties = CPSBaseFolder._properties + (
        {'id': 'cps_chat_guest', 'type': 'string'},
        {'id': 'is_moderated', 'type': 'boolean'},
        {'id': 'cps_chat_refresh_rate', 'type': 'int'},
        {'id': 'effective_date', 'type': 'date'},
        {'id': 'expiration_date', 'type': 'date'},
        )

    cps_chat_guest = ''
    is_moderated = 0
    cps_chat_refresh_rate = 10

    def __init__(self, id, **kw):
        """ Constructor
        """
        BTreeFolder2Base.__init__(self, id)
        CPSBaseFolder.__init__(self, id, **kw)
        self.chat_users = []

    security.declareProtected(chatModerate, 'editProps')
    def editProps(self, **kw):
        """ Edit
        """
        self.manage_changeProperties(**kw)

    security.declareProtected(View, 'isModerated')
    def isModerated(self):
        """Is the Chat moderated
        """
        return self.is_moderated

    ##############################################
    ##############################################

    security.declareProtected(View, 'getPublicMessages')
    def getPublicMessages(self, include_pending=0):
        """Returns the whole chat items
        """
        wftool = self.portal_workflow
        list = []
        for post in self.values():
            rstate = wftool.getInfoFor(post, 'review_state')
            if rstate == 'published' or include_pending and rstate == 'pending':
                list.append(post)
        return list

    security.declareProtected(chatModerate, 'getPendingMessages')
    def getPendingMessages(self):
        """Returns the messages that need to be moderated
        """
        wftool = self.portal_workflow
        list = []
        for post in self.values():
            if wftool.getInfoFor(post, 'review_state') == 'waiting':
                list.append(post)
        return list

    security.declareProtected(chatModerate, 'getPendingAnswerMessages')
    def getPendingAnswerMessages(self):
        """Returns the messages that need to be moderated
        """
        wftool = self.portal_workflow
        list = []
        for main_post in self.values():
            for post in main_post.objectValues():
                if wftool.getInfoFor(post, 'review_state') == 'waiting':
                    list.append(post)
        return list

    ##############################################
    ##############################################

    security.declareProtected(chatModerate, 'moderateMessages')
    def moderateMessages(self, messages={}):
        """Moderate messages

        If accepted then publish them else drop.
        """
        wftool = self.portal_workflow
        for post_id, published in messages.items():
            action = int(published)
            message = self.get(post_id)
            if action == 2:
                wftool.doActionFor(message,
                                   'submit_question',
                                   comment='Submit question to guest',
                                   workflow_id='chat_item_wf')
            elif action == 1:
                wftool.doActionFor(message,
                                   'publish_post',
                                   comment='Message Acceptance',
                                   workflow_id='chat_item_wf')
            else:
                self.manage_delObjects([post_id])

    security.declareProtected(chatModerate, 'moderateAnswers')
    def moderateAnswers(self, messages={}):
        """Moderate Answers

        If accepted then publish them else drop.
        """
        wftool = self.portal_workflow
        for post_id, published in messages.items():
            parent = None
            message = None
            for post in self.values():
                if post_id in post.objectIds():
                    parent = post
                    message = getattr(post, post_id)
                    continue
            if int(published):
                wftool.doActionFor(message,
                                   'publish_post',
                                   comment='Message Acceptance',
                                   workflow_id='chat_item_wf')
            else:
                parent.manage_delObjects([post_id])
                # if the answer to a pending question was deleted
                # we change back the status of the question to "waiting"
                # so that the moderator can re-submit, accept or reject it
                if wftool.getInfoFor(parent, 'review_state') == 'pending':
                    wftool.doActionFor(parent,
                                   'unsubmit',
                                   comment='Unsubmit question',
                                   workflow_id='chat_item_wf')

    security.declarePublic('isClosed')
    def isClosed(self):
        """Is the chat closed
        """
        wftool = self.portal_workflow
        return wftool.getInfoFor(self, 'review_state') == 'closed'

    ##############################################
    ##############################################

    security.declareProtected(chatPost, 'addChatItem')
    def addChatItem(self, message='', pseudo=''):
        """Add a Chat Item
        """
        if self.isClosed():
            return 0

        # Injecting the post within the chat
        new_id = self.computeId() # skins
        self.invokeFactory('ChatItem', new_id)
        ob = self.get(new_id)

        # Chat item properties
        kw = {}
        kw['message'] = message
        kw['pseudo'] = pseudo
        ob.editProps(**kw)

        mtool = self.portal_membership
        isAno = mtool.isAnonymousUser()

        # Moderation business
        if not self.isModerated():
            wftool = self.portal_workflow
            if not isAno:
                user = mtool.getAuthenticatedMember()
                member_id = user.getMemberId()
            else:
                member_id = 'pseudo'

            #
            # Create a tmp_user to create the post
            # The method is protected with
            # chatPost permissions which is given at least to the role
            # ChatPoster.  But, I don't want all the chatPoster to have the
            # modifyPortalContent permission to do whatever they want within
            # the chat.  So I'm just opening here permissions with a tmp
            # SecutiryManager just the time to create the post.  As well,
            # only the moderator is able to change the workflow state of the
            # chat item for security purpose when the moderation is off
            #

            tmp_user = CPSUnrestrictedUser(member_id, '',
                                           ['ChatModerator'], '')
            tmp_user = tmp_user.__of__(self.acl_users)
            newSecurityManager(None, tmp_user)

            wftool.doActionFor(ob,
                               'publish_post',
                               comment='Not moderated post',
                               workflow_id='chat_item_wf')

            # Revert to original user if not anonymous
            if not isAno:
                newSecurityManager(None, user)

    security.declareProtected(chatModerate, 'delChatItems')
    def delChatItems(self, chat_item_ids=[]):
        """Remove given chat items
        """
        self.manage_delObjects(chat_item_ids)

    ####################################################
    ####################################################

    security.declareProtected(View, 'getModeratorMemberIds')
    def getModeratorMemberIds(self):
        """Get the members who are chat moderators
        """
        moderator_role = 'ChatModerator'
        member_ids = []
        for member_id, roles in self.get_local_roles():
            if moderator_role in roles and \
                   member_id not in member_ids:
                member_ids.append(member_id)
        return member_ids

    security.declareProtected(View, 'getModeratorGroupIds')
    def getModeratorGroupIds(self):
        """Get the groups which are chat moderators
        """
        moderator_role = 'ChatModerator'
        group_ids = []
        for group_id, roles in self.get_local_group_roles():
            if moderator_role in roles and \
                   group_id not in group_ids:
                group_ids.append(group_id)
        return group_ids

    #####################################################
    #####################################################

    def _getTimeToLeave(self):
        """Return the time to leave for a user
        """
        return self.cps_chat_refresh_rate * 2

    security.declareProtected(View, 'getChatUsers')
    def getChatUsers(self):
        """Returns a list containing the users currently
        connected to the chat
        """
        return [x[0] for x in self.chat_users]

    security.declareProtected(View, 'trackChatUser')
    def trackChatUser(self, pseudo='', REQUEST=None):
        """Track the current user
        """
        mtool = self.portal_membership
        isAno = mtool.isAnonymousUser()
        nyt = int(time.time())

        if isAno:
            # Don't handle the anonymous connection right now
            # should keep track of the pseudo within cookies
            to_append = pseudo
            return
        else:
            to_append = mtool.getAuthenticatedMember().getMemberId()
            new = [x for x in self.chat_users if x[0] != to_append]
            self.chat_users = new + [(to_append, nyt)]

            # Update according to the time to leave
            new = [x for x in self.chat_users if (x[1] + self._getTimeToLeave()
                                                  > nyt)]
            self.chat_users = new

InitializeClass(Chat)

def addChat(container, id, REQUEST=None, **kw):
    """Add a Chat.
    """
    ob = Chat(id, **kw)
    return CPSBase_adder(container, ob, REQUEST=REQUEST)
