""" Module for non CPSTestCase based tests. """


import unittest
from DateTime import DateTime
from Products.CPSChat.Chat import Chat

class FakeWfTool:
    def getInfoFor(self, ob, info):
        return getattr(ob, info)

class FakeChatItem:

    def __init__(self, msg, date=None, review_state=''):
        self.msg = msg
        if date is not None:
            self.creation_date = date
        self.review_state = review_state or 'published'

    def CreationDate(self):
        return self.creation_date


def values(self):
    return self.fake_values

# Workflow tool is found by acquisition in the code
Chat.portal_workflow = FakeWfTool() 


class CPSChatLightTestCase(unittest.TestCase):
    def setUp(self):
        self.old_values_method = Chat.values
        Chat.values = values
        self.chat = Chat('test_chat')

    def tearDown(self):
        Chat.values = self.old_values_method

    def test_sorting(self):
        item1 = FakeChatItem('item 1', date=DateTime('2000/01/01 00:00:00'))
        item2 = FakeChatItem('item 2', date=DateTime('2005/01/01 00:00:00'))
        self.chat.fake_values = [item2, item1]
        # msg below is for readability of failure        
        result = [item.msg for item in self.chat.getPublicMessages()]
        self.assertEquals(result, ['item 1', 'item 2']) 

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CPSChatLightTestCase))
    return suite
