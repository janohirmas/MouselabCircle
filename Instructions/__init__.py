import numpy as np
from otree.api import *
import socket

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url         = 'Instructions'
    players_per_group   = None
    num_rounds          = 1
    figUvA_logo         = 'global/figures/UvA_logo.png'
    figExample1         = 'global/figures/example1.jpg'
    figExample2         = 'global/figures/example2.jpg'
    iEvalTime           = 45
    AvgDur              = '30'
    iMaxScale           = '7'
    iBonus              = 3
    iPracticeRounds     = 3
    NumTrials           = 30
    SlidesIntro         = [
        dict(
            Title = 'General Information',
            path='Introduction/slide0.html',
            ),
        dict(
            Title = 'Informed Consent',
            path='Introduction/slide1.html',
            ),        
    ]
    SlidesInstructions = [
        dict(
            Title = 'The experiment',
            path='Instructions/slide0.html',
            ),
        dict(
            Title = 'The job and the applications',
            path='Instructions/slide1.html',
            ),           
        dict(
            Title = 'Information Screen',
            path='Instructions/slide2.html',
            ),        
        dict(
            Title = 'Information Screen',
            path='Instructions/slide3.html',
            ),        
        dict(
            Title = 'Your Decision',
            path='Instructions/slide4.html',
            ),        
        dict(
            Title = 'Payment',
            path='Instructions/slide5.html',
            ),          
        dict(
            Title = 'Review',
            path='Instructions/slide6.html',
            ),    
        dict(
            Title = 'Review',
            path='Instructions/slide7.html',
            ),        
    
    ]
    ## EYE-TRACKER CONSTANTS
    # Host machine IP
    HOST = '127.0.0.1'
    PORT = 4242
    ADDRESS = (HOST, PORT)



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Controls    = models.StringField()
    dError       = models.FloatField()
    ValidPts    = models.IntegerField()
    Result      = models.StringField()
    NumCal      = models.IntegerField()
    iBlockOrder = models.IntegerField()

# FUNCTIONS

def creating_session(subsession):
    if subsession.round_number == 1:
        for player in subsession.get_players():
            part            = player.participant
            block = np.random.choice([0,1])
            part.BlockOrder = block
            player.iBlockOrder = int(block)
   
    
# PAGES
     
                
    
        


class Introduction(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(
            UvA_logo = Constants.figUvA_logo,
            Slides = Constants.SlidesIntro,
        )

class Instructions(Page):
    @staticmethod
    def vars_for_template(player):
        selfEval = player.participant.BlockOrder==0
        return dict(
            Example1        = Constants.figExample1,
            Example2        = Constants.figExample2,
            Slides          = Constants.SlidesInstructions,
            SelfEval        = selfEval ,
        )

class MessageBeforeCal(Page):
    
    @staticmethod
    def vars_for_template(player):
        return dict(
            Message         = 'Notifications/msgBeforeCal.html',
        )


page_sequence = [Introduction, Instructions, MessageBeforeCal]
