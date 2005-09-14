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

__author__ = "Julien Anguenot <ja@nuxeo.com>"


from Products.CPSCore.CPSMembershipTool import CPSMembershipTool as mtool

#
# Monkey patch the CPSMemberShipTool.
# I want the ChatModerators to be able to manage
# the local roles within the Chat.
#

ChatModerator = 'ChatModerator'
if ChatModerator not in mtool.roles_managing_local_roles:
    mtool.roles_managing_local_roles += (ChatModerator,)
