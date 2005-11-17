import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
from Testing import ZopeTestCase

import DateTime

class TestChat(ZopeTestCase.ZopeTestCase):
    def afterSetUp(self):
        self.app.manage_addProduct['CPSChat'].manage_addCPSChat('chat')
        self.chat = self.app.chat

        #self.ws.invokeFactory(doc_type, doc_id)

    def beforeTearDown(self):
        self.logout()

    # Old tests that were meant to be inside a CPSChatTestCase (ie CPSTestCase)
    # instance and already commented out.   

    #def testZMI(self):
    #    "Test ZMI methods"
    #    assert self.portal.manage_addProduct['CPSChat'].Chat_addForm
    #
    #def testSkin(self):
    #    "Test presentation (skin) methods"
    #    assert self.chat.Chat_index
    #    assert self.chat.Chat_questions
    #    assert self.chat.Chat_addQuestionForm
    #    assert self.chat.Chat_addAnswerForm
    #    assert self.chat.Chat_moderateForm
    #    assert self.chat.Chat_history
    #
    #def testProps(self):
    #    "Test default properties"
    #    self.assertEquals(self.chat.meta_type, 'CPSChat')
    #    self.assertEquals(self.chat.id, 'chat')
    #    self.assertEquals(self.chat.title, '')
    #    self.assertEquals(self.chat.description, '')
    #    self.assertEquals(self.chat.num_replies, 5)
    #    self.assertEquals(len(self.chat.questions), 0)
    #
    #def testAddQuestion(self):
    #    "Test question addition"
    #    self.chat.addQuestion(question='q1', pseudo='p1')
    #    self.chat.addQuestion(question='q2', pseudo='p2')
    #    l = self.chat.selectQuestions()
    #    self.assertEquals(len(l), 2)
    #    self.assertEquals(l[0].question(), 'q1')
    #    self.assertEquals(l[1].question(), 'q2')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestChat))
    return suite

