# Copyright (C) 2003  Nuxeo <http://www.nuxeo.com/>
# Author: Stefane Fermigier <sf@nuxeo.com>
#         Julien Anguenot <ja@nuxeo.com>

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

"""
Chat module for CPS.
This is *NOT* a real time chat. It's moderated and designed to
be used as a kind of FAQ where you can filter the anwsers.
"""

# Zope
from zLOG import LOG, DEBUG
import DateTime
from Globals import InitializeClass, DTMLFile
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from BTrees import IOBTree

# CMF
from Products.CMFCore.CMFCorePermissions import View, \
     ManageProperties, ModifyPortalContent

# CPS
from Products.CPSCore.CPSBase import CPSBaseDocument

# This product
from Question import Question

factory_type_information = (
    { 'id': 'Chat',
      'meta_type': 'CPSChat',
      'description': "CPSChat is a chat Product used within CPS",
      'icon': 'chat_icon.gif',
      'title': "portal_type_chat",
      'product': 'CPSChat',
      'factory': 'manage_addCPSChat',
      'immediate_view': 'Chat_edit_form',
      'filter_content_types': 0,
      'allowed_content_types': (),
      'allow_discussion': 0,
      'actions': ({'id': 'view',
                   'name': 'action_view',
                   'action': 'Chat_history',
                   'permissions': (View,),
                   },
                  {'id': 'edit',
                   'name': 'action_edit',
                   'action': 'Chat_edit_form',
                   'permissions': (ManageProperties,),
                   },
                  {'id': 'moderate_chat',
                   'name': 'action_moderate_chat',
                   'action': 'Chat_moderateForm',
                   'permissions': (ManageProperties,),
                   },
                  {'id': 'action_access_chat_room',
                   'name': 'action_access_chat_room',
                   'action': 'string:javascript:open_external_window()',
                   'permissions': (View,),
                   },
                  {'id': 'action_reply_question',
                   'name': 'action_reply_question',
                   'action': 'Chat_addAnswerForm',
                   'permissions': (ManageProperties,),
                   },
                  {'id': 'action_post_question',
                   'name': 'action_post_question',
                   'action': 'Chat_quickPostForm',
                   'permissions': (ManageProperties,),
                   },
                  {'id': 'metadata',
                   'name': 'action_metadata',
                   'action': 'metadata_edit_form',
                   'permissions': (ModifyPortalContent,)},
                  {'id': 'localroles',
                   'name': 'action_local_roles',
                   'action': 'folder_localrole_form',
                   'permissions': ('Change permissions',)
                   },
                  ),
      },
    )

class CPSChat(SimpleItem, PropertyManager, CPSBaseDocument):
    """CPSChat object"""

    # Zope stuff
    meta_type = 'CPSChat'
    portal_type = meta_type

    security = ClassSecurityInfo()

    # XXX
    manage_options = (
        PropertyManager.manage_options + SimpleItem.manage_options
    )

    # Properties (ZMI)
    _properties = (
        {'id': 'title', 'type': 'string'},
        {'id': 'description', 'type': 'text'},
        {'id': 'num_replies', 'type': 'int'},
        {'id': 'question_max_length', 'type': 'int'},
        {'id': 'pseudo_max_length', 'type': 'int'},
        {'id': 'chat_host', 'type': 'string'},
    )

    # Sensible default values
    num_replies = 5
    question_max_length = 500
    pseudo_max_length = 100

    def __init__(self, id, title='', description='', host=''):
        """
        Default constructor
        """
        self.id = id
        self.title = title
        self.description = description
        self.host = host

        # Content
        self.questions = IOBTree.IOBTree()
        self.counter = 0

    #
    # Publicly available methods
    #
    def index_html(self, REQUEST=None):
        """
        Default view -> redirect to Chat_history
        """
        if REQUEST:
            REQUEST.RESPONSE.redirect(self.absolute_url() + '/Chat_history')

    security.declareProtected('Moderate Chat', 'editProperties')
    def editProperties(self, title='', description='', host='',
                       REQUEST=None):
        """
        Edit chat object properties.
        """
        self.title = title
        self.description = description
        self.host = host

    security.declareProtected('View', 'addQuestion')
    def addQuestion(self, question, pseudo='', REQUEST=None):
        """
        Add a new (hence unmoderated) question
        """
        question = question[0:self.question_max_length]
        pseudo = pseudo[0:self.pseudo_max_length]
        self.questions[self.counter] = Question(
            self.counter, question, pseudo=pseudo)
        self.counter += 1

        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(
                self.absolute_url() )

    #
    # Moderation methods
    #
    security.declareProtected('Moderate Chat', 'addAnswer')
    def addAnswer(self, question_id, answer, REQUEST=None):
        """
        Add an answer to a question
        """
        question = self.getQuestion(int(question_id))
        question.addAnswer(answer)

        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(
                self.absolute_url() + '/Chat_addAnswerForm')

    def getQuestion(self, question_id):
        """
        Return the question
        """
        return self.questions[question_id]

    def delQuestion(self, question_id):
        """
        Delete the question
        """
        del self.questions[question_id]


    def selectQuestions(self, status=None, num=None, reverse=0,
                        sort_by_answer_time=0):
        """
        Return list of questions
        """
        l = self.questions.values()
        if status is not None:
            l = [ q for q in l if q.status == status ]
        if sort_by_answer_time:
            l.sort(lambda x, y: cmp(x.answer_time(), y.answer_time()))
        if num is not None:
            l = l[-num:]
        if reverse:
            l.reverse()
        return l


    security.declareProtected('Moderate Chat', 'moderate')
    def moderate(self, REQUEST):
        """
        Moderate a batch of questions
        """
        form = REQUEST.form
        for k, v in form.items():
            k = int(k)
            if v == 'go':
                try:
                    q = self.getQuestion(k)
                    q.setStatus('WAITING')
                except:
                    pass
            elif v == 'nogo':
                try:
                    self.delQuestion(k)
                except:
                    pass
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(
                self.absolute_url() + '/Chat_moderateForm')

    security.declareProtected('Moderate Chat', 'publish')
    def publish(self, REQUEST):
        """
        Publish a batch of questions
        """
        form = REQUEST.form
        for k, v in form.items():
            k = int(k)
            if v == 'go':
                try:
                    q = self.getQuestion(k)
                    q.setStatus('PUBLISHED')
                except:
                    pass

        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(
                self.absolute_url() + '/Chat_moderateForm')


    security.declareProtected('Moderate Chat', 'answerQuestion')
    def answerQuestion(self, question_id, answer, REQUEST=None):
        """
        Answer a question
        """
        question = self.questions[id(question_id)]
        question.addAnswer(answer)

        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(
                self.absolute_url() + '/Chat_moderateForm')


def manage_addCPSChat(self, id, title='', description='', host='', 
                      REQUEST=None):
    """
    Constructor method for the type CPSChat.
    """
    self._setObject(id, CPSChat(id, title, description, host))
    if REQUEST is not None:
        REQUEST.RESPONSE.redirect(self.absolute_url() + '/manage_main')

manage_addCPSChatForm = DTMLFile('skins/Chat_addForm', globals())

InitializeClass(CPSChat)
