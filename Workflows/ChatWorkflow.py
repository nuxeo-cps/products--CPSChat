# Copyright (c) 2004 Nuxeo SARL <http://nuxeo.com>
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

""" Chat Workflfow
"""

__author__ = "Julien Anguenot <ja@nuxeo.com>"

import os, sys
from zLOG import LOG, INFO, DEBUG

from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent

from Products.CPSChat.CPSChatPermissions import chatModerate, \
     chatReply, chatPost

from Products.CPSCore.CPSWorkflow import \
     TRANSITION_INITIAL_CREATE, \
     TRANSITION_ALLOWSUB_CHECKOUT, \
     TRANSITION_ALLOWSUB_CREATE, \
     TRANSITION_ALLOWSUB_DELETE, \
     TRANSITION_ALLOWSUB_MOVE, \
     TRANSITION_ALLOWSUB_COPY

from Products.DCWorkflow.Transitions import \
     TRIGGER_USER_ACTION

def chatWorkflowsInstall(self):
    """Install the workflow for the Chat Type
    """

    portal = self.portal_url.getPortalObject()
    wftool = portal.portal_workflow

    wfids = wftool.objectIds()
    wfid = 'chat_section_wf'

    if wfid in wfids:
        wftool.manage_delObjects([wfid])

    wftool.manage_addWorkflow(id=wfid,
                              workflow_type='cps_workflow (Web-configurable workflow for CPS)')

    wf = wftool[wfid]

    for p in (View,
              ModifyPortalContent,
              chatModerate,
              chatReply,
              chatPost):
        wf.addManagedPermission(p)

    ###########################################################################
    ###########################################################################

    #                                  STATES

    ###########################################################################
    ###########################################################################

    for s in ('work',):
        wf.states.addState(s)

    ##########################################################################
    #                                  WORK
    ##########################################################################

    s = wf.states.get('work')

    s.setPermission(View, 1, ('ChatPoster',))
    s.setPermission(ModifyPortalContent, 1, ('ChatModerator',))
    s.setPermission(chatReply, 1, ('ChatModerator', 'ChatGuest',))
    s.setPermission(chatPost, 1, ('ChatModerator', 'ChatPoster', 'ChatGuest',))
    s.setPermission(chatModerate, 1, ('ChatModerator',))

    s.setInitialState('work')
    s.setProperties(title='Work',
                    description='',
                    transitions=('create_content',
                                 'cut_copy_paste', ),)

    ###########################################################################
    ###########################################################################

    #                               TRANSITIONS

    ###########################################################################
    ###########################################################################

    for t in ('create',
              'create_content',
              'cut_copy_paste',):
        wf.transitions.addTransition(t)


    ###########################################################################
    #                                 CREATE
    ###########################################################################

    t = wf.transitions.get('create')
    t.setProperties(title='Initial creation',
                    description='Intial transition like',
                    new_state_id='work',
                    transition_behavior=(TRANSITION_INITIAL_CREATE, ),
                    clone_allowed_transitions=None,
                    actbox_name='', actbox_category='workflow', actbox_url='',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager; SectionManager',
                           'guard_expr':''},)

    ###########################################################################
    #                                  CREATE CONTENT
    ###########################################################################

    t = wf.transitions.get('create_content')
    t.setProperties(title='Create content',
                    description='Allow sub Object Create',
                    new_state_id='work',
                    transition_behavior=(TRANSITION_ALLOWSUB_CREATE,
                                         TRANSITION_ALLOWSUB_CHECKOUT,),
                    trigger_type=TRIGGER_USER_ACTION,
                    actbox_name='New',
                    actbox_category='',
                    actbox_url='',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager; SectionManager; SectionReviewer; SectionReader; ChatModerator; ChatGuest; ChatPoster',
                           'guard_expr':''},)

    ##########################################################################
    #                                  CUT/COPY/PASTE
    ##########################################################################

    t = wf.transitions.get('cut_copy_paste')
    t.setProperties(title='Cut/Copy/Paste',
                    new_state_id='work',
                    transition_behavior=(TRANSITION_ALLOWSUB_DELETE,
                                         TRANSITION_ALLOWSUB_MOVE,
                                         TRANSITION_ALLOWSUB_COPY),
                    clone_allowed_transitions=None,
                    trigger_type=TRIGGER_USER_ACTION,
                    actbox_name='New',
                    actbox_category='',
                    actbox_url='',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager; SectionManager',
                           'guard_expr':''},)


    wfid = 'chat_workspace_wf'

    if wfid in wfids:
        wftool.manage_delObjects([wfid])

    wftool.manage_addWorkflow(id=wfid,
                              workflow_type='cps_workflow (Web-configurable workflow for CPS)')

    wf = wftool[wfid]

    for p in (View,
              ModifyPortalContent,
              chatModerate,
              chatReply,
              chatPost):
        wf.addManagedPermission(p)

    ###########################################################################
    ###########################################################################

    #                                  STATES

    ###########################################################################
    ###########################################################################

    for s in ('work',):
        wf.states.addState(s)

    ##########################################################################
    #                                  WORK
    ##########################################################################

    s = wf.states.get('work')

    s.setPermission(View, 1, ('ChatPoster',))
    s.setPermission(ModifyPortalContent, 1, ('ChatModerator',))
    s.setPermission(chatReply, 1, ('ChatModerator', 'ChatGuest',))
    s.setPermission(chatPost, 1, ('ChatModerator', 'ChatPoster', 'ChatGuest',))
    s.setPermission(chatModerate, 1, ('ChatModerator',))

    s.setInitialState('work')
    s.setProperties(title='Work',
                    description='',
                    transitions=('create_content',
                                 'cut_copy_paste', ),)

    ###########################################################################
    ###########################################################################

    #                               TRANSITIONS

    ###########################################################################
    ###########################################################################

    for t in ('create',
              'create_content',
              'cut_copy_paste',):
        wf.transitions.addTransition(t)


    ###########################################################################
    #                                 CREATE
    ###########################################################################

    t = wf.transitions.get('create')
    t.setProperties(title='Initial creation',
                    description='Intial transition like',
                    new_state_id='work',
                    transition_behavior=(TRANSITION_INITIAL_CREATE, ),
                    clone_allowed_transitions=None,
                    actbox_name='', actbox_category='workflow', actbox_url='',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager; WorkspaceManager',
                           'guard_expr':''},)

    ###########################################################################
    #                                  CREATE CONTENT
    ###########################################################################

    t = wf.transitions.get('create_content')
    t.setProperties(title='Create content',
                    description='Allow sub Object Create',
                    new_state_id='work',
                    transition_behavior=(TRANSITION_ALLOWSUB_CREATE,
                                         TRANSITION_ALLOWSUB_CHECKOUT,),
                    trigger_type=TRIGGER_USER_ACTION,
                    actbox_name='New',
                    actbox_category='',
                    actbox_url='',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager; WorkspaceManager; WorkspaceMember; WorkspaceReader; ChatModerator; ChatGuest; ChatPoster',
                           'guard_expr':''},)

    ##########################################################################
    #                                  CUT/COPY/PASTE
    ##########################################################################

    t = wf.transitions.get('cut_copy_paste')
    t.setProperties(title='Cut/Copy/Paste',
                    new_state_id='work',
                    transition_behavior=(TRANSITION_ALLOWSUB_DELETE,
                                         TRANSITION_ALLOWSUB_MOVE,
                                         TRANSITION_ALLOWSUB_COPY),
                    clone_allowed_transitions=None,
                    trigger_type=TRIGGER_USER_ACTION,
                    actbox_name='New',
                    actbox_category='',
                    actbox_url='',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager; WorkspaceManager; WorkspaceMember',
                           'guard_expr':''},)

