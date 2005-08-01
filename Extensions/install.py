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

"""CPSChat Installer

Installer/Updater fot the CPSChat component.
"""

from Products.CPSInstaller.CPSInstaller import CPSInstaller
from Products.CPSChat.CPSChatPermissions import chatModerate, chatPost, \
    chatReply

SECTIONS_ID = 'sections'
WORKSPACES_ID = 'workspaces'
SKINS = {'cps_chat': 'Products/CPSChat/skins/cps_chat',
         }

class CPSChatInstaller(CPSInstaller):
    """CPSChat Installer
    """

    product_name = "CPSChat"

    def install(self):
        """Main func
        """
        self.log("CPSChat Install / Update ........ [ S T A R T ]")
        self.verifySkins(SKINS)
        self.resetSkinCache()
        self.verifyPortalTypes()
        self.installCustomWorkflows()
        self.verifyWorkflowAssociation()
        self.verifyNewRolePermissions()
        self.setupTranslations()
        self.installNewPermissions()
        self.finalize()
        self.reindexCatalog()
        self.log("CPSChat Install / Update .........[ S T O P ]  ")

    def verifyPortalTypes(self):
        """Verify portal types
        """
        ptypes = {
            'Chat': {
                'typeinfo_name': 'CPSChat: Chat (Chat)',
                'add_meta_type': 'Factory-based Type Information',
                'allowed_content_types': ('ChatItem',),
                },
            'ChatItem': {
                'typeinfo_name': 'CPSChat: ChatItem (ChatItem)',
                'add_meta_type': 'Factory-based Type Information',
                'allowed_content_types': (),
                },
            }
        self.verifyContentTypes(ptypes, destructive=1)
        self.allowContentTypes('Chat', ('Workspace', 'Section'))
        self.allowContentTypes('ChatItem', 'Chat')

    def installCustomWorkflows(self):
        """Installs custom workflows
        """
        from Products.CPSChat.Workflows.ChatItemWorkflow import \
             chatItemWorkflowsInstall

        chatItemWorkflowsInstall(self.context)

        from Products.CPSChat.Workflows.ChatWorkflow import \
             chatWorkflowsInstall

        chatWorkflowsInstall(self.context)

    def verifyWorkflowAssociation(self):
        """Verify workflow association
        """
        ws_chains = { 'Chat': 'chat_workspace_wf',
                      'ChatItem' : 'chat_item_workspace_wf',
                      }

        se_chains = { 'Chat': 'chat_section_wf',
                      'ChatItem': 'chat_item_section_wf',
                      }

        self.verifyLocalWorkflowChains(self.portal['workspaces'],
                                       ws_chains,
                                       destructive=1)
        self.verifyLocalWorkflowChains(self.portal['sections'],
                                       se_chains,
                                       destructive=1)

    def verifyNewRolePermissions(self):
        """Verify New Roles

        ChatModerate
        """
        self.verifyRoles(['ChatModerator', 'ChatPoster', 'ChatGuest',])

        # XXX is it really useful ?
        self.setupPortalPermissions({
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
                        'ChatModerator',
                        'ChatGuest',],
            })

    def installNewPermissions(self):
        """Installs new subscriptions dedicated permissions
        """

        # Workspace
        chat_ws_perms = {
            chatPost : ['Manager',
                        'ChatPoster',
                        'ChatGuest',
                        'ChatModerator',
                        'WorkspaceManager',
                        'WorkspaceMember'],

            chatModerate : ['Manager',
                            'ChatModerator',
                            'WorkspaceManager'],

            chatReply : ['Manager',
                         'WorkspaceManager',
                         'ChatGuest',
                         'ChatModerator'],
            }

        for perm, roles in chat_ws_perms.items():
            self.portal[WORKSPACES_ID].manage_permission(perm, roles, 0)

        # Section
        chat_sc_perms = {
            chatPost : ['Manager',
                        'ChatPoster',
                        'ChatModerator',
                        'ChatGuest',
                        'SectionManager',
                        'SectionReviewer'],

            chatModerate : ['Manager',
                            'ChatModerator',
                            'SectionManager',
                            'SectionReviewer'],

            chatReply : ['Manager',
                         'SectionManager',
                         'ChatGuest',
                         'ChatModerator'],
            }

        for perm, roles in chat_sc_perms.items():
            self.portal[SECTIONS_ID].manage_permission(perm, roles, 0)

def install(self):
    installer = CPSChatInstaller(self)
    installer.install()
    return installer.logResult()
