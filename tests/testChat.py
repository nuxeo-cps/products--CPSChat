import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
from Testing import ZopeTestCase
import CPSChatTestCase

from Products.CPSChat.Question import Question

import DateTime


class TestQuestion(unittest.TestCase):
    qid = 123123

    def testDefaultValue(self):
        self.question = Question(self.qid)
        self.assertEquals(self.question.question(), '')
        self.assertEquals(self.question.answer(), '')
        self.assertEquals(self.question.pseudo(), '(pas de pseudo)')
        self.assertEquals(self.question.id(), self.qid)
        self.assertEquals(self.question.status, 'PENDING')

    def testCreation(self):
        self.question = Question(self.qid, question='toto', pseudo='titi')
        self.assertEquals(self.question.question(), 'toto')
        self.assertEquals(self.question.answer(), '')
        self.assertEquals(self.question.pseudo(), 'titi')
        self.assertEquals(self.question.id(), self.qid)
        self.assertEquals(self.question.status, 'PENDING')

    def testLifeCicle(self):
        start = DateTime.DateTime()

        self.question = Question(self.qid, 'toto')
        self.assertEquals(self.question.question(), 'toto')
        self.assert_(self.question.submit_time() >= start)

        self.question.setQuestion('titi')
        self.assertEquals(self.question.question(), 'titi')

        self.question.setStatus('WAITING')
        self.assertEquals(self.question.status, 'WAITING')

        self.question.addAnswer('tutu')
        self.assertEquals(self.question.answer(), 'tutu')
        self.assertEquals(self.question.status, 'ANSWERED')
        self.assert_(self.question.answer_time() >= start)

        self.question.setAnswer('tata')
        self.assertEquals(self.question.answer(), 'tata')


class TestChat(CPSChatTestCase.CPSChatTestCase):
    def afterSetUp(self):
        self.login('root')
        self.ws = self.portal.workspaces
        self.ws.manage_addProduct['CPSChat'].manage_addCPSChat('chat')
        self.chat = self.ws.chat

        #self.ws.invokeFactory(doc_type, doc_id)

    def beforeTearDown(self):
        self.logout()

    def testZMI(self):
        "Test ZMI methods"
        assert self.portal.manage_addProduct['CPSChat'].Chat_addForm

    def testSkin(self):
        "Test presentation (skin) methods"
        assert self.chat.Chat_index
        assert self.chat.Chat_questions
        assert self.chat.Chat_addQuestionForm
        assert self.chat.Chat_addAnswerForm
        assert self.chat.Chat_moderateForm
        assert self.chat.Chat_history

    def testProps(self):
        "Test default properties"
        self.assertEquals(self.chat.meta_type, 'CPSChat')
        self.assertEquals(self.chat.id, 'chat')
        self.assertEquals(self.chat.title, '')
        self.assertEquals(self.chat.description, '')
        self.assertEquals(self.chat.num_replies, 5)
        self.assertEquals(len(self.chat.questions), 0)

    def testAddQuestion(self):
        "Test question addition"
        self.chat.addQuestion(question='q1', pseudo='p1')
        self.chat.addQuestion(question='q2', pseudo='p2')
        l = self.chat.selectQuestions()
        self.assertEquals(len(l), 2)
        self.assertEquals(l[0].question(), 'q1')
        self.assertEquals(l[1].question(), 'q2')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestQuestion))
    suite.addTest(unittest.makeSuite(TestChat))
    return suite

