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
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# $Id$

__author__ = "Julien Anguenot <ja@nuxeo.com>"

""" Simple Question class declaration

Used within a CPSChat content type.
"""

import DateTime

from Globals import Persistent
from AccessControl import ClassSecurityInfo

class Question(Persistent):
    """A question, including possibly its answers
    """

    security = ClassSecurityInfo()

    _id = _question = _answer = _pseudo = _answer_time = _submit_time = ''

    status = 'PENDING'

    def __init__(self, id, question='', pseudo=''):
        """Constructor
        """
        self._id = id
        self._question = question
        self._pseudo = pseudo
        self._submit_time = DateTime.DateTime()

    security.declarePublic('id', 'question', 'answer', 'pseudo',
                           'submit_time', 'answer_time', 'setQuestion',
                           'setStatus', 'setAnswer')

    #
    # Accessors
    #

    def id(self):
        return self._id

    def question(self):
        return self._question

    def answer(self):
        return self._answer

    def pseudo(self):
        if not self._pseudo:
            return '(pas de pseudo)'
        return self._pseudo

    def answer_time(self):
        return self._answer_time

    def submit_time(self):
        return self._submit_time

    #
    # Mutators
    #

    def setQuestion(self, question):
        self._question = question

    def setAnswer(self, answer):
        self._answer = answer

    def setStatus(self, status):
        self.status = status

    def addAnswer(self, answer):
        self._answer = answer
        self.setStatus('ANSWERED')
        self._answer_time = DateTime.DateTime()
