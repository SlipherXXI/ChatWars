'''
Created on Feb 12, 2018

@author: rslip
'''




class KnockKnockProtocol :
    WAITING = 0
    SENTKNOCKKNOCK = 1
    SENTCLUE = 2
    ANOTHER = 3

    NUMJOKES = 5

    #state int = WAITING
    #int currentJoke = 0

    clues = [ "Turnip", "Little Old Lady", "Atch", "Who", "Who" ]
    answers = [ "Turnip the heat, it's cold in here!",
                                 "I didn't know you could yodel!",
                                 "Bless you!",
                                 "Is there an owl in here?",
                                 "Is there an echo in here?" ]

    def __init__(self):
        self.state = KnockKnockProtocol.WAITING
        self.currentJoke = 0
        
    def processInput(self, theInput):
        if self.state == KnockKnockProtocol.WAITING:
            theOutput = "Knock! Knock!"
            self.state = KnockKnockProtocol.SENTKNOCKKNOCK
        elif self.state == KnockKnockProtocol.SENTKNOCKKNOCK:
            print(theInput.lower())
            #print("Who's there?".lower())
            if theInput.lower() == "Who's there?".lower():
                theOutput = KnockKnockProtocol.clues[self.currentJoke]
                self.state = KnockKnockProtocol.SENTCLUE
            else:
                theOutput = "You're supposed to say \"Who's there?\"! " \
                "Try again. Knock! Knock!"
        elif self.state == KnockKnockProtocol.SENTCLUE:
            expResponce = KnockKnockProtocol.clues[self.currentJoke] + " who?"
            if theInput.lower() == expResponce.lower():
                theOutput = KnockKnockProtocol.answers[self.currentJoke] + " Want another? (y/n)"
                self.state = KnockKnockProtocol.ANOTHER
            else:
                theOutput = "You're supposed to say \"" 
                theOutput += KnockKnockProtocol.clues[self.currentJoke] 
                theOutput += " who?\"" 
                theOutput += "! Try again. Knock! Knock!";
                self.state = KnockKnockProtocol.SENTKNOCKKNOCK;
        elif self.state == KnockKnockProtocol.ANOTHER:
            if theInput.lower() == "y":
                theOutput = "Knock! Knock!"
                if self.currentJoke == KnockKnockProtocol.NUMJOKES - 1:
                    self.currentJoke = 0
                else:
                    self.currentJoke += 1
                self.state = KnockKnockProtocol.SENTKNOCKKNOCK
            else:
                theOutput = "Bye."
                self.state = KnockKnockProtocol.WAITING
        
        
        
        print("KKP sending: %s" % theOutput)
        return theOutput
    
