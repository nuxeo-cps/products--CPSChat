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

""" Chat Item Workflfow
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
     TRANSITION_ALLOWSUB_CREATE

from Products.DCWorkflow.Transitions import \
     TRIGGER_USER_ACTION

def chatItemWorkflowsInstall(self):
    """Installs the workflow for the ChatItem Type
    """

    portal = self.portal_url.getPortalObject()
    wftool = portal.portal_workflow

    wfids = wftool.objectIds()
    wfid = 'chat_item_workspace_wf'

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

    for s in ('waiting',
              'published',):
        wf.states.addState(s)


    ##########################################################################
    #                                  WAITING
    ##########################################################################

    s = wf.states.get('waiting')

    s.setPermission(View, 1, ('ChatModerator',))
    s.setPermission(ModifyPortalContent, 1, ('ChatModerator',))
    s.setPermission(chatReply, 1, ('ChatModerator',))
    s.setPermission(chatPost, 1, ('ChatModerator',))
    s.setPermission(chatModerate, 1, ('ChatModerator',))

    s.setInitialState('waiting')
    s.setProperties(title='Waiting',
                    description='',
                    transitions=('create_content',
                                 'publish_post',))

    ###########################################################################
    #                               PUBLISHED
    ###########################################################################

    s = wf.states.get('published')

    s.setPermission(View, 1, ('ChatPoster', 'ChatModerator', 'ChatGuest'))
    s.setPermission(ModifyPortalContent, 1, ('ChatModerator',))
    s.setPermission(chatReply, 1, ('ChatModerator', 'ChatGuest'))
    s.setPermission(chatPost, 1, ('ChatModerator', 'ChatGuest'))
    s.setPermission(chatModerate, 1, ('ChatModerator',))

    s.setProperties(title='published',
                    description='Published',
                    transitions=('create_content',
                                 'unpublish_post',))

    ###########################################################################
    ###########################################################################

    #                               TRANSITIONS

    ###########################################################################
    ###########################################################################

    for t in ('create',
              'create_content',
              'publish_post',
              'unpublish_post'):
        wf.transitions.addTransition(t)

    ###########################################################################
    #                                 CREATE
    ###########################################################################

    t = wf.transitions.get('create')
    t.setProperties(title='Initial creation',
                    description='Intial transition like',
                    new_state_id='waiting',
                    transition_behavior=(TRANSITION_INITIAL_CREATE, ),
                    clone_allowed_transitions=None,
                    actbox_name='', actbox_category='workflow', actbox_url='',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager;WorkspaceManager; WorkspaceMember; WorkspaceReader; ChatModerator; ChatPoster; ChatGuest',
                           'guard_expr':''},)

    ###########################################################################
    #                                  CREATE CONTENT
    ###########################################################################

    t = wf.transitions.get('create_content')
    t.setProperties(title='Create content',
                    description='Allow sub Object Create',
                    new_state_id='',
                    transition_behavior=(TRANSITION_ALLOWSUB_CREATE,
                                         TRANSITION_ALLOWSUB_CHECKOUT,),
                    trigger_type=TRIGGER_USER_ACTION,
                    actbox_name='New',
                    actbox_category='',
                    actbox_url='',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager;WorkspaceManager; WorkspaceMember; WorkspaceReader; ChatModerator;ChatGuest',
                           'guard_expr':''},)

    ###########################################################################
    #                                  PUBLISH_POST
    ###########################################################################

    t = wf.transitions.get('publish_post')
    t.setProperties(title='Publish_post',
                    description='Publish_post',
                    new_state_id='published',
                    transition_behavior=(),
                    trigger_type=TRIGGER_USER_ACTION,
                    actbox_name='New',
                    actbox_category='',
                    actbox_url='',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager;WorkspaceManager;ChatModerator',
                           'guard_expr':''},)

    ###########################################################################
    #                                  UNPUBLISH_POST
    ###########################################################################

    t = wf.transitions.get('unpublish_post')
    t.setProperties(title='unPublish post',
                    description='unPublish',
                    new_state_id='waiting',
                    transition_behavior=(),
                    trigger_type=TRIGGER_USER_ACTION,
                    actbox_name='New',
                    actbox_category='',
                    actbox_url='',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager;WorkspaceManager;ChatModerator',
                           'guard_expr':''},)

    ###########################################################################
    ###########################################################################

    #                                     VARIABLES

    ###########################################################################
    ###########################################################################

    for v in ('action',
              'actor',
              'comments',
              'review_history',
              'time',
              'dest_container',
              ):
        wf.variables.addVariable(v)


    wf.variables.setStateVar('review_state')
    vdef = wf.variables['action']
    vdef.setProperties(description='The last transition',
                       default_expr='transition/getId|nothing',
                       for_status=1, update_always=1)

    vdef = wf.variables['actor']
    vdef.setProperties(description='The ID of the user who performed '
                       'the last transition',
                       default_expr='user/getId',
                       for_status=1, update_always=1)

    vdef = wf.variables['comments']
    vdef.setProperties(description='Comments about the last transition',
                       default_expr="python:state_change.kwargs.get('comment',\
                       '')",
                       for_status=1, update_always=1)

    vdef = wf.variables['review_history']
    vdef.setProperties(description='Provides access to workflow history',
                       default_expr="state_change/getHistory",
                       props={'guard_permissions':'',
                              'guard_roles':'Manager; WorkspaceManager; \
                              WorkspaceMember; WorkspaceReader; Member',
                              'guard_expr':''})

    vdef = wf.variables['time']
    vdef.setProperties(description='Time of the last transition',
                       default_expr="state_change/getDateTime",
                       for_status=1, update_always=1)

    ###########################################################################
    ###########################################################################

    wfid = 'chat_item_section_wf'

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

    for s in ('waiting',
              'published',):
        wf.states.addState(s)


    ##########################################################################
    #                                  WAITING
    ##########################################################################

    s = wf.states.get('waiting')

    s.setPermission(View, 1, ('ChatModerator',))
    s.setPermission(ModifyPortalContent, 1, ('ChatModerator',))
    s.setPermission(chatReply, 1, ('ChatModerator',))
    s.setPermission(chatPost, 1, ('ChatModerator',))
    s.setPermission(chatModerate, 1, ('ChatModerator',))

    s.setInitialState('waiting')
    s.setProperties(title='Waiting',
                    description='',
                    transitions=('create_content',
                                 'publish_post',))

    ###########################################################################
    #                               PUBLISHED
    ###########################################################################

    s = wf.states.get('published')

    s.setPermission(View, 1, ('ChatPoster', 'ChatModerator', 'ChatGuest'))
    s.setPermission(ModifyPortalContent, 1, ('ChatModerator',))
    s.setPermission(chatReply, 1, ('ChatModerator', 'ChatGuest'))
    s.setPermission(chatPost, 1, ('ChatModerator', 'ChatGuest'))
    s.setPermission(chatModerate, 1, ('ChatModerator',))

    s.setProperties(title='published',
                    description='Published',
                    transitions=('create_content',
                                 'unpublish_post',))

    ###########################################################################
    ###########################################################################

    #                               TRANSITIONS

    ###########################################################################
    ###########################################################################

    for t in ('create',
              'create_content',
              'publish_post',
              'unpublish_post'):
        wf.transitions.addTransition(t)

    ###########################################################################
    #                                 CREATE
    ###########################################################################

    t = wf.transitions.get('create')
    t.setProperties(title='Initial creation',
                    description='Intial transition like',
                    new_state_id='waiting',
                    transition_behavior=(TRANSITION_INITIAL_CREATE, ),
                    clone_allowed_transitions=None,
                    actbox_name='', actbox_category='workflow', actbox_url='',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager;SectionManager; SectionReviewer; SectionReader; ChatModerator; ChatPoster; ChatGuest',
                           'guard_expr':''},)

    ###########################################################################
    #                                  CREATE CONTENT
    ###########################################################################

    t = wf.transitions.get('create_content')
    t.setProperties(title='Create content',
                    description='Allow sub Object Create',
                    new_state_id='',
                    transition_behavior=(TRANSITION_ALLOWSUB_CREATE,
                                         TRANSITION_ALLOWSUB_CHECKOUT,),
                    trigger_type=TRIGGER_USER_ACTION,
                    actbox_name='New',
                    actbox_category='',
                    actbox_url='',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager;SectionManager; SectionReviewer; SectionReader; ChatModerator;ChatGuest',
                           'guard_expr':''},)

    ###########################################################################
    #                                  PUBLISH_POST
    ###########################################################################

    t = wf.transitions.get('publish_post')
    t.setProperties(title='Publish_post',
                    description='Publish_post',
                    new_state_id='published',
                    transition_behavior=(),
                    trigger_type=TRIGGER_USER_ACTION,
                    actbox_name='New',
                    actbox_category='',
                    actbox_url='',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager;SectionManager;ChatModerator',
                           'guard_expr':''},)

    ###########################################################################
    #                                  UNPUBLISH_POST
    ###########################################################################

    t = wf.transitions.get('unpublish_post')
    t.setProperties(title='unPublish post',
                    description='unPublish',
                    new_state_id='waiting',
                    transition_behavior=(),
                    trigger_type=TRIGGER_USER_ACTION,
                    actbox_name='New',
                    actbox_category='',
                    actbox_url='',
                    props={'guard_permissions':'',
                           'guard_roles':'Manager;SectionManager;ChatModerator',
                           'guard_expr':''},)

    ###########################################################################
    ###########################################################################

    #                                     VARIABLES

    ###########################################################################
    ###########################################################################

    for v in ('action',
              'actor',
              'comments',
              'review_history',
              'time',
              'dest_container',
              ):
        wf.variables.addVariable(v)


    wf.variables.setStateVar('review_state')
    vdef = wf.variables['action']
    vdef.setProperties(description='The last transition',
                       default_expr='transition/getId|nothing',
                       for_status=1, update_always=1)

    vdef = wf.variables['actor']
    vdef.setProperties(description='The ID of the user who performed '
                       'the last transition',
                       default_expr='user/getId',
                       for_status=1, update_always=1)

    vdef = wf.variables['comments']
    vdef.setProperties(description='Comments about the last transition',
                       default_expr="python:state_change.kwargs.get('comment',\
                       '')",
                       for_status=1, update_always=1)

    vdef = wf.variables['review_history']
    vdef.setProperties(description='Provides access to workflow history',
                       default_expr="state_change/getHistory",
                       props={'guard_permissions':'',
                              'guard_roles':'Manager; WorkspaceManager; \
                              WorkspaceMember; WorkspaceReader; Member',
                              'guard_expr':''})

    vdef = wf.variables['time']
    vdef.setProperties(description='Time of the last transition',
                       default_expr="state_change/getDateTime",
                       for_status=1, update_always=1)
