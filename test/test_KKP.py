'''
Created on Apr 5, 2018

@author: rslip
'''

import unittest
from KnockKnockProtocol import KnockKnockProtocol


class CoreMethodsTest(unittest.TestCase):
    def test_initial_state_waiting(self):
        kkp = KnockKnockProtocol()
        #self.assertEqual(-1, KnockKnockProtocol.WAITING)
        self.assertEqual(kkp.state, 
                         KnockKnockProtocol.WAITING, 
                         "initial state not Waiting")
        
    def test_kkp_correct_msg_after_waiting(self):
        kkp = KnockKnockProtocol()
        msg = kkp.processInput('')
        
        self.assertEqual(msg, 
                         "Knock! Knock!", 
                         "Incorrect Message From state")
        
    def test_kkp_correct_state_after_waiting(self):
        kkp = KnockKnockProtocol()
        msg = kkp.processInput('')
        
        self.assertEqual(kkp.state, 
                         KnockKnockProtocol.SENTKNOCKKNOCK, 
                         "initial state not SENTKNOCKKNOCK")
        
    def test_kkp_correct_state_after_SentKnockKnock(self):
        kkp = KnockKnockProtocol()
        kkp.state = KnockKnockProtocol.SENTKNOCKKNOCK
        msg = kkp.processInput("Who's There?")
        
        self.assertEqual(kkp.state, 
                         KnockKnockProtocol.SENTCLUE, "New State not SentClue")
       
    def test_kkp_correct_state_after_SentKnockKnock_lower_case(self):
        kkp = KnockKnockProtocol()
        kkp.state = KnockKnockProtocol.SENTKNOCKKNOCK
        msg = kkp.processInput("who's there?")
        
        self.assertEqual(kkp.state, 
                         KnockKnockProtocol.SENTCLUE, "New State not SentClue")   
        
    def test_kkp_same_state_after_incorrect_SentKnockKnock(self):
        kkp = KnockKnockProtocol()
        kkp.state = KnockKnockProtocol.SENTKNOCKKNOCK
        msg = kkp.processInput("Whos There")
        
        self.assertEqual(kkp.state, 
                         KnockKnockProtocol.SENTKNOCKKNOCK, "state not SentClue")
    
if __name__ == '__main__':
    suit = unittest.TestLoader().loadTestsFromTestCase(CoreMethodsTest)
    unittest.TextTestRunner(verbosity=2).run(suit)
    
    
    
    
    
    