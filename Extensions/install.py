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

import os, sys

from Products.CPSChat.CPSChatPermissions import chatModerate, chatPost, chatReply

from zLOG import LOG, INFO, DEBUG

def cps_chat_i18n_update(self):
    """
    Importation of the po files for internationalization.
    For CPS itself and compulsory products.
    """
    _log = []
    def pr(bla, _log=_log):
        if bla == 'flush':
            return '\n'.join(_log)
        _log.append(bla)
        if (bla):
            LOG('cps_i18n_update:', INFO, bla)

    def primp(pr=pr):
        pr(" !!! Cannot migrate that component !!!")

    def prok(pr=pr):
        pr(" Already correctly installed")

    portal = self.portal_url.getPortalObject()
    def portalhas(id, portal=portal):
        return id in portal.objectIds()

    pr(" Updating i18n support")


    Localizer = portal['Localizer']
    languages = Localizer.get_supported_languages()
    catalog_id = 'cpschat'
    # Message Catalog
    if catalog_id in Localizer.objectIds():
        Localizer.manage_delObjects([catalog_id])
        pr(" Previous default MessageCatalog deleted for CPSChat")

    # Adding the new message Catalog
    Localizer.manage_addProduct['Localizer'].manage_addMessageCatalog(
        id=catalog_id,
        title='CPSChat messages',
        languages=languages,
        )

    defaultCatalog = Localizer.cpschat

    # computing po files' system directory
    CPSChat_path = sys.modules['Products.CPSChat'].__path__[0]
    i18n_path = os.path.join(CPSChat_path, 'i18n')
    pr("   po files are searched in %s" % i18n_path)
    pr("   po files for %s are expected" % str(languages))

    # loading po files
    for lang in languages:
        po_filename = lang + '.po'
        pr("   importing %s file" % po_filename)
        po_path = os.path.join(i18n_path, po_filename)
        try:
            po_file = open(po_path)
        except (IOError, NameError):
            pr("    %s file not found" % po_path)
        else:
            defaultCatalog.manage_import(lang, po_file)
            pr("    %s file imported" % po_path)

    # Translation Service Tool
    if portalhas('translation_service'):
        translation_service = portal.translation_service
        pr (" Translation Sevice Tool found in here ")
        try:
            if getattr(portal['translation_service'], 'cpschat', None) == None:
                # translation domains
                translation_service.manage_addDomainInfo('cpschat','Localizer/'+'cpschat')
                pr(" cpschat domain set to Localizer/cpschat")
        except:
            pass
    else:
        raise str('DependanceError'), 'translation_service'

    return pr('flush')

def install(self):
    """
    Statring point !
    """
    _log = []
    def pr(bla, zlog=1, _log=_log):
        if bla == 'flush':
            return '<html><head><title>CPSChat Installer</title></head><body><pre>'+ \
                   '\n'.join(_log) + \
                   '</pre></body></html>'

        _log.append(bla)
        if bla and zlog:
            LOG('CPSChat Install:', INFO, bla)

    def prok(pr=pr):
        pr(" Already correctly installed")

    pr("Starting CPSChat Install")

    portal = self.portal_url.getPortalObject()

    def portalhas(id, portal=portal):
        return id in portal.objectIds()

    #################################################
    # PORTAL TYPES
    #################################################

    pr("Verifying portal types")
    ttool = portal.portal_types
    ptypes = {
        'CPSChat' : ('CPSChat',
                                  ),
    }

    #################################################
    # AUTHORIZATING PORTAL TYPES (ws and sections)
    #################################################

    # Workspaces
    if 'Workspace' in ttool.objectIds():
        workspaceACT = list(ttool['Workspace'].allowed_content_types)
    else:
        workspaceACT = []

    if 'CPSChat' not in  workspaceACT:
        workspaceACT.append('CPSChat')

    # Sections
    if 'Section' in ttool.objectIds():
        sectionACT = list(ttool['Section'].allowed_content_types)
    else:
        sectionACT = []

    if 'CPSChat' not in sectionACT:
        sectionACT.append('CPSChat')

    allowed_content_type = {
        'Workspace' : workspaceACT,
        'Section'   : sectionACT,
        }

    ptypes_installed = ttool.objectIds()

    for prod in ptypes.keys():
        for ptype in ptypes[prod]:
            pr("  Type '%s'" % ptype)
            if ptype in ptypes_installed:
                ttool.manage_delObjects([ptype])
                pr("   Deleted  ")

            ttool.manage_addTypeInformation(
                id=ptype,
                add_meta_type='Factory-based Type Information',
                typeinfo_name=prod+': '+ptype
                )
            pr("   Installation   ")


    for ptype in allowed_content_type.keys():
        ttool[ptype].allowed_content_types = allowed_content_type[ptype]

    ########################################
    #   WORKFLOW ASSOCIATIONS
    ########################################

    workspaces_id = 'workspaces'
    sections_id = 'sections'

    pr("Verifying local workflow association")

    if not '.cps_workflow_configuration' in portal[workspaces_id].objectIds():
        pr("  Adding workflow configuration to %s" % workspaces_id)
        portal[workspaces_id].manage_addProduct['CPSCore'].addCPSWorkflowConfiguration()

    pr("  Add %s chain to portal type %s in %s of %s" %('workspace_content_wf',
                                                        'CPSChat',
                                                        '.cps_workflow_configuration',
                                                        workspaces_id))
    wfc = getattr(portal[workspaces_id], '.cps_workflow_configuration')
    wfc.manage_addChain(portal_type='CPSChat', chain='workspace_content_wf')

    if not '.cps_workflow_configuration' in portal[sections_id].objectIds():
        pr("  Adding workflow configuration to %s" % sections_id)
        portal[sections_id].manage_addProduct['CPSCore'].addCPSWorkflowConfiguration()

    pr("  Add %s chain to portal type %s in %s of %s" %('section_folder_wf',
                                                        'CPSChat',
                                                        '.cps_workflow_configuration',
                                                        sections_id))
    wfc = getattr(portal[sections_id], '.cps_workflow_configuration')
    wfc.manage_addChain(portal_type='CPSChat', chain='section_folder_wf')

    ##########################################
    # SKINS
    ##########################################

    skins = ('cps_chat',)
    paths = {'cps_chat': 'Products/CPSChat/skins/cps_chat'}

    for skin in skins:
        path = paths[skin]
        path = path.replace('/', os.sep)
        pr(" FS Directory View '%s'" % skin)
        if skin in portal.portal_skins.objectIds():
            dv = portal.portal_skins[skin]
            oldpath = dv.getDirPath()
            if oldpath == path:
                prok()
            else:
                pr("  Correctly installed, correcting path")
                dv.manage_properties(dirpath=path)
        else:
            portal.portal_skins.manage_addProduct['CMFCore'].manage_addDirectoryView(\
                filepath=path, id=skin)
            pr("  Creating skin")
    allskins = portal.portal_skins.getSkinPaths()
    for skin_name, skin_path in allskins:
        if skin_name != 'Basic':
            continue
        path = [x.strip() for x in skin_path.split(',')]
        path = [x for x in path if x not in skins] # strip all
        if path and path[0] == 'custom':
            path = path[:1] + list(skins) + path[1:]
        else:
            path = list(skins) + path
        npath = ', '.join(path)
        portal.portal_skins.addSkinSelection(skin_name, npath)
        pr(" Fixup of skin %s" % skin_name)


    ##############################################
    # i18n support
    ##############################################

    pr(cps_chat_i18n_update(self))

    ##############################################
    # New roles
    ##############################################

    new_roles = ['ChatModerator',
                 'ChatPoster',
                 'ChatGuest',
                 ]

    already = portal.valid_roles()

    for new_role in new_roles:
        if new_role not in already:
            portal._addRole(new_role)
            pr(" Add role for mail manager %s" % new_role)

    ##############################################
    # Permissions
    ##############################################


    chat_perms = {
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
        }

    for perm, roles in chat_perms.items():
        portal.manage_permission(perm, roles, 0)
        pr("  Permission %s" % perm)


    #############################################
    # Action
    #############################################

    def getActionIndex(action_id, action_provider):
        action_index = 0
        for action in action_provider.listActions():
            if action.id == action_id:
                return action_index
            action_index += 1
        return -1

    p_actions = portal['portal_actions']
    action_index = getActionIndex('status_history', p_actions)
    if action_index > -1:
        p_actions.deleteActions((action_index,))
        p_actions.addAction(
            id='status_history',
            name='action_status_history',
            action='string: ${object/absolute_url}/content_status_history',
            # XXX: this is as messy as what is done in cpsinstall
            condition="python:getattr(object, 'portal_type', None) not in ('Section', 'Workspace', 'Portal', 'Calendar', 'Event', 'CPSForum', 'CPSChat',)",
            permission='View',
            category='workflow')

    pr("End of CPSChat install")
    return pr('flush')
