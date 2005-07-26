##parameters=mtool=None, base_url=None, context_url=None
# $Id$
"""get Merged Local Roles filtering non CPS Roles.

Returns a tuple dict_roles, editable_users, cps_roles, local_roles_blocked
"""
# XXX AT: This method has to be updated like it's been done in CPSDefault, and
# base_url and context_url are not useful anymore

from Products.CMFcore.utils import getToolByName

if mtool is None:
    mtool = getToolByName(context, 'portal_membership')

# Get the list of Roles from the tool
dict_roles = mtool.getMergedLocalRolesWithPath(context)

utool = getToolByName(context, 'portal_url')
rpath = utool.getRpath(context)

# Filter remove special roles
local_roles_blocked = 0
for user in dict_roles.keys():
    for item in dict_roles[user]:
        roles = item['roles']
        roles = [r for r in roles if r not in ('Owner', 'Member')]
        if user == 'group:role:Anonymous' and '-' in roles:
            roles = [r for r in roles if r != '-']
            if item['url'] == rpath:
                local_roles_blocked = 1
        item['roles'] = roles

    dict_roles[user] = [x for x in dict_roles[user] if x['roles']]

    if not dict_roles[user]:
        del dict_roles[user]

#find editable user with local roles defined in the context
editable_users = []
for user in dict_roles.keys():
    for item in dict_roles[user]:
        if item['url'] == rpath:
            editable_users.append(user)
            continue

# List local roles according to the context
cps_roles = mtool.getCPSCandidateLocalRoles( context )
cps_roles.reverse()

# Filter them for CPS
cps_roles = [x for x in cps_roles if x not in ('Owner',
                                               'Member',
                                               'Reviewer',
                                               'Manager',
                                               'Authenticated')]
# Checking the context (Ws or section)
if context.portal_type == "Section":
    cps_roles = [x for x in cps_roles if x not in ('WorkspaceManager',
                                                   'WorkspaceMember',
                                                   'WorkspaceReader')]
elif context.portal_type == "Workspace":
    cps_roles = [x for x in cps_roles if x not in ('SectionManager',
                                                   'SectionReader',
                                                   'SectionReviewer')]
elif context.portal_type == "Chat":
    cps_roles = [x for x in cps_roles if x in ('ChatModerator',
                                               'ChatPoster',
                                               'ChatGuest')]

else:
    cps_roles = cps_roles

return dict_roles, editable_users, cps_roles, local_roles_blocked
