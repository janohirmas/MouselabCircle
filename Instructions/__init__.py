import numpy as np
from otree.api import *
import socket
import time 
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
    # Friendly Checks
    bRequireFS          = True
    bCheckFocus         = True

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
    dError              = models.FloatField()
    ValidPts            = models.IntegerField()
    Result              = models.StringField()
    NumCal              = models.IntegerField()
    iBlockOrder         = models.IntegerField()
    # Friendly Check vars and PixelRatio
    dPixelRatio         = models.FloatField()
    sSlideSequence      = models.StringField(blank=True)
    sSlideTime          = models.StringField(blank=True)


# FUNCTIONS

def creating_session(subsession):
    if subsession.round_number == 1:
        for player in subsession.get_players():
            part            = player.participant
            block = np.random.choice([0,1])
            # part.BlockOrder = block # if two blocks
            part.BlockOrder = 0
            player.iBlockOrder = int(block)
   


# PAGES
     
                
    
        
class Calibration(Page):
    form_model = 'player'
    form_fields = [ 'dPixelRatio' ]

    @staticmethod
    def vars_for_template(player: Player):
        return dict(Message = 'Notifications/msgCal.html')

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        part = player.participant
        part.dPixelRatio = player.dPixelRatio


class Introduction(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(
            UvA_logo = Constants.figUvA_logo,
            Slides = Constants.SlidesIntro,
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        part = player.participant
        # Initialize Focus variables#        
        part.startTime          = time.time()
        part.iOutFocus          = 0
        part.iFullscreenChanges = 0
        part.dTimeOutFocus      = 0


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
    @staticmethod 
    def js_vars(player: Player):
        return   dict(      
            bRequireFS    = Constants.bRequireFS,
            bCheckFocus   = Constants.bCheckFocus,
            defaultPixel  = player.participant.dPixelRatio,
        )

page_sequence = [Introduction, Calibration, Instructions]
