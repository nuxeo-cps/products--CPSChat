# (C) Copyright 2003 Nuxeo SARL <http://nuxeo.com>
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

"""CPSChat Installer

HOWTO USE THAT ?

 - Log into the ZMI as manager
 - Go to your CPS root directory
* - Create an External Method with the following parameters:

     id    : CPSChat Installer (or whatever)
     title : CPSChat Installer (or whatever)
     Module Name   :  CPSChat.install
     Function Name : install

 - save it
 - click now the test tab of this external method.
 - that's it !

"""

from Products.CPSInstaller.CPSInstaller import CPSInstaller
from Products.CPSChat.CPSChatPermissions import chatModerate, chatPost, \
    chatReply

def install(self):
    """
    Starting point !
    """

    ##############################################
    # Create the installer
    ##############################################
    installer = CPSInstaller(self, 'CPSChat')
    installer.log("Starting CPSChat Install")

    #################################################
    # PORTAL TYPES
    #################################################
    installer.allowContentTypes('CPSChat', 'Workspace')
    installer.allowContentTypes('CPSChat', 'Section')
    ptypes = {
        'CPSChat' : {'allowed_content_types': (),
                     'typeinfo_name': 'CPSChat: CPSChat',
                     'add_meta_type': 'Factory-based Type Information',
                    },
    }
    installer.verifyContentTypes(ptypes)

    ########################################
    #   WORKFLOW ASSOCIATIONS
    ########################################
    ws_chains = { 'CPSChat': 'workspace_folder_wf', }
    se_chains = { 'CPSChat': 'section_folder_wf', }
    installer.verifyLocalWorkflowChains(installer.portal['workspaces'],
                                        ws_chains)
    installer.verifyLocalWorkflowChains(installer.portal['sections'],
                                        se_chains)

    ##########################################
    # SKINS
    ##########################################
    skins = {'cps_chat': 'Products/CPSChat/skins/cps_chat'}
    installer.verifySkins(skins)

    ##############################################
    # New roles
    ##############################################
    installer.verifyRoles(['ChatModerator', 'ChatPoster', 'ChatGuest',])

    ##############################################
    # Permissions
    ##############################################
    installer.setupPortalPermissions({
        chatModerate: ['Manager',
                       'WorkspaceManager',
                       'SectionManager',
                       'ChatModerator',
                       ],
        chatPost: ['Manager',
                   'WorkspaceManager',
                   'SectionManager',
                   'ChatPoster',
                   ],
        chatReply: ['Manager',
                    'WorkspaceManager',
                    'SectionManager',
                    'ChatGuest',],
        })

    #############################################
    # Action
    #############################################
    installer.verifyAction('portal_actions',
            id='status_history',
            name='action_status_history',
            action='string: ${object/absolute_url}/content_status_history',
            # XXX: this is as messy as what is done in cpsinstall
            condition="python:getattr(object, 'portal_type', None) not in "
                      "('Section', 'Workspace', 'Portal', 'Calendar', 'Event', "
                      "'CPSForum', 'CPSChat',)",
            permission='View',
            category='workflow')

    ##############################################
    # i18n support
    ##############################################
    installer.verifyMessageCatalog('cpschat', 'CPSChat messages')
    installer.setupTranslations(message_catalog='cpschat')

    ##############################################
    # Finished!
    ##############################################
    installer.finalize()
    installer.log("End of CPSChat install")
    return installer.logResult()
