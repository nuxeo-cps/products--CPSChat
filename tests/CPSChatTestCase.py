from Testing import ZopeTestCase
from Products.CPSDefault.tests import CPSTestCase

ZopeTestCase.installProduct('CPSChat')

CPSTestCase.setupPortal()

CPSChatTestCase = CPSTestCase.CPSTestCase

