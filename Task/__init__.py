from otree.api import *
import numpy as np
from numpy import random
import socket
import pandas as pd

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Task'
    players_per_group = None
    num_brounds = 32
    num_prounds = 3
    # num_rounds = 2*num_brounds+num_prounds+2  # If 2 blocks
    num_rounds = num_brounds+num_prounds+1   # if 1 block
    iRatingScale = 7    
    lRoundsVisual = [1,num_brounds+num_prounds,num_brounds+num_prounds+1,2*num_brounds+num_prounds]
    lRoundsBefore = [2]
    lRoundsAfter  = [num_prounds,num_prounds+num_brounds]
    # Calibration Address
    HOST = '127.0.0.1'
    PORT = 4242
    ADDRESS = (HOST, PORT)
    # Matrix with results
    Results = pd.read_csv("_static/global/results.csv")
    # Friendly Checks
    bRequireFS          = True
    bCheckFocus         = True



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    dRT_info        = models.FloatField()
    dRT_dec         = models.FloatField()
    iDec            = models.IntegerField()
    iGender         = models.IntegerField()
    iFirst          = models.IntegerField()
    iGMA            = models.IntegerField()
    iPersonality    = models.IntegerField()
    iInterview      = models.IntegerField()
    sOrder          = models.StringField()
    # Timestamps
    sStartVisual    = models.StringField()
    sEndVisual      = models.StringField()
    sStartCross     = models.StringField()
    sEndCross       = models.StringField()
    sStartInfo      = models.StringField()
    sEndInfo        = models.StringField()
    sStartDec       = models.StringField()
    sEndDec         = models.StringField()
    # Result Variables
    iCandSet        = models.IntegerField()
    # FriendlyCheck Vars
    iFocusLostInfo          = models.FloatField()
    iFullscreenChangeInfo   = models.FloatField()
    dFocusLostTInfo         = models.FloatField()
    iFocusLostDec           = models.FloatField()
    iFullscreenChangeDec    = models.FloatField()
    dFocusLostTDec          = models.FloatField()



# FUNCTIONS

def creating_session(subsession):
    ## SETUP FOR PARTICIPANT
    if subsession.round_number == 1:
        for player in subsession.get_players():
            # Create participant variables
            part            = player.participant
            lOrder          = list(range(5))
            random.shuffle(lOrder)
            part.lOrder = lOrder
            # Create Trials
            lTrials = []
            vOpts = [0,1]
            iCount = 0
            for g in vOpts:                     # Gender
                for f in vOpts:                 # First
                    for m in vOpts:             # GMA
                        for p in vOpts:         # Personality
                            for i in vOpts:     # Interview
                                iCount +=1
                                lTrials.append([iCount,g,f,m,p,i])
            # Random Order Block1
            random.shuffle(lTrials)
            mTrials = []
            # Random Order Block2
            iHalf = int(np.ceil(Constants.num_brounds/2))
            mTrials.extend(lTrials[0:iHalf])
            mTrials.append([99,99,99,99,99,99])
            mTrials.extend(lTrials[iHalf:])
            random.shuffle(lTrials)
            mTrials.extend(lTrials[0:iHalf])
            mTrials.append([99,99,99,99,99,99])
            mTrials.extend(lTrials[iHalf:])
            # Save trials as participant variable.
            part.mTrials = mTrials
            # Relevant round numbers for choosing paid rounds
            iR1 = Constants.num_prounds+1
            iR2 = Constants.num_prounds+Constants.num_brounds+1
            # iR3 = Constants.num_prounds+Constants.num_brounds+1 # for 2 blocks
            # iR4 = Constants.num_rounds
            # Randomize paid rounds
            iRound1 = random.choice(range(iR1,iR2))
            while iRound1==iHalf:
                iRound1 = random.choice(range(iR1,iR2))
            part.iRound1     = iRound1

            # part.iRound2     = random.choice(range(iR3,iR4)) # for 2 blocks
            # print('Trials selected for participant {}: {} and {}'.format(part.code,part.iRound1,part.iRound2)) ## for 2 blocks
            print('Trial selected for participant {}: {} '.format(part.code,part.iRound1))
    for player in subsession.get_players():
        ## Load participant's round
        p = player.participant
        if player.round_number<= Constants.num_prounds:
            vPars = p.mTrials[random.randint(10)]     # Choose random round for the practice 
        else:
            player.round_number-Constants.num_prounds-1
            vPars = p.mTrials[player.round_number-Constants.num_prounds-1] # Choose respective round values
        # Save variables in players database

        pos1,pos2,pos3,pos4,pos5 = list(p.lOrder)
        player.sOrder = "{},{},{},{},{}".format(pos1,pos2,pos3,pos4,pos5)
        player.iCandSet, player.iGender, player.iFirst, player.iGMA, player.iPersonality, player.iInterview = vPars
        

# PAGES

class ChangeTask(Page):
    @staticmethod
    def vars_for_template(player: Player):
        msg = [dict(Title='Change in Task',path='Notifications/msgChangeTask.html')]
        return dict(Slides = msg, selfEval = player.participant.BlockOrder==0)

    @staticmethod
    def is_displayed(player: Player):
        # return player.round_number == Constants.num_brounds+Constants.num_prounds+1 # in case of 2 blocks
        return False


class Notify(Page):
    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number == Constants.num_prounds+1:
            msg = 'Notifications/msgEndPractice.html'
        else:
            msg = 'Notifications/msgStartPractice.html'

        return dict(Message = msg, selfEval = player.participant.BlockOrder==0)

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in [1,Constants.num_prounds+1]

class FixCross(Page):
    form_model = 'player'
    form_fields = [ 'sStartCross','sEndCross' ]

class Info(Page):
    form_model = 'player'
    form_fields = [ 'dRT_info', 'sStartInfo','sEndInfo', 'iFocusLostInfo', 'iFullscreenChangeInfo', 'dFocusLostTInfo' ]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        # Add Focus variables to total if it's not practice trial
        if (player.round_number > Constants.num_prounds):
            participant.iOutFocus = int(participant.iOutFocus) + player.iFocusLostInfo
            participant.iFullscreenChanges = int(participant.iFullscreenChanges) + player.iFullscreenChangeInfo
            participant.dTimeOutFocus = float(participant.dTimeOutFocus) + player.dFocusLostTInfo


    @staticmethod
    def vars_for_template(player: Player):

        lOutcomes   = []
        # Gender
        if (player.iGender==1):
            lOutcomes.append('Female')
        elif (player.iGender==99): 
            lOutcomes.append('Press 2')
        else:
            lOutcomes.append('Male')
        # First
        if (player.iFirst==1):
            lOutcomes.append('Odd')
        elif (player.iFirst==99): 
            lOutcomes.append('Press 2')
        else:
            lOutcomes.append('Even')
        # GMA
        if (player.iGMA==1):
            lOutcomes.append('High GMA')
        elif (player.iGMA==99): 
            lOutcomes.append('Press 2')
        else:
            lOutcomes.append('Low GMA')
        # Personality
        if (player.iPersonality==1):
            lOutcomes.append('High Consc.')
        elif (player.iPersonality==99): 
            lOutcomes.append('Press 2')
        else:
            lOutcomes.append('Low Consc.')
        # Interview
        if (player.iInterview==1):
            lOutcomes.append('Good Interview')
        elif (player.iInterview==99): 
            lOutcomes.append('Press 2')
        else:
            lOutcomes.append('Bad Interview')
        
        vOutcomes = np.array(lOutcomes)
        vOrder = player.participant.lOrder
        lOutcomes = list(vOutcomes[vOrder])
        return dict(
          Vars = lOutcomes
        )

    def js_vars(player: Player):
        return   dict(      
            bRequireFS    = Constants.bRequireFS,
            bCheckFocus   = Constants.bCheckFocus,
            defaultPixel  = float(player.participant.dPixelRatio),
        )


class Decision(Page):

    form_model = 'player'
    form_fields = [ 'dRT_dec', 'iDec', 'sStartDec','sEndDec', 'iFocusLostDec', 'iFullscreenChangeDec', 'dFocusLostTDec']

    @staticmethod
    def js_vars(player: Player):
        return dict(
            iMax = Constants.iRatingScale,
            bRequireFS    = Constants.bRequireFS,
            bCheckFocus   = Constants.bCheckFocus,
            defaultPixel  = player.participant.dPixelRatio,
        )

    @staticmethod
    def vars_for_template(player: Player):
        lQuestions = [
                'How well do you think the candidate will do?',
                'How well do you think <b> others </b> will rate this candidate?'
        ]
        bOrder = player.participant.BlockOrder == 0
        bFirst = player.round_number <= Constants.num_brounds + Constants.num_prounds
        if  (bOrder and bFirst) or ( (not bOrder) and  (not bFirst) ):
            idx = 0
        else:
            idx = 1

        return dict(
            lRatingScale = list(range(1,Constants.iRatingScale+1)),
            Question = lQuestions[idx]
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        p = player.participant
        # Add Focus variables to total if it's not practice trial 
        if (player.round_number > Constants.num_prounds):
            p.iOutFocus = int(p.iOutFocus) + player.iFocusLostDec
            p.iFullscreenChanges = int(p.iFullscreenChanges) + player.iFullscreenChangeDec
            p.dTimeOutFocus = float(p.dTimeOutFocus) + player.dFocusLostTDec
        # Save results if the round is selected for payments
        if player.round_number==int(p.iRound1):
            p.iAnsValue1 = player.iDec
            iMat = Constants.Results.to_numpy()
            p.iRightValue1 = iMat[player.iCandSet,p.BlockOrder]
            print('Type:{}, Decision: {}, Correct Answer: {}'.format(player.iCandSet,int(p.iAnsValue1),int(p.iRightValue1)))
        # if player.round_number==int(p.iRound2):
        #     p.iAnsValue2 = player.iDec
        #     iMat = Constants.Results.to_numpy()
        #     col = 1-p.BlockOrder
        #     p.iRightValue2 = iMat[player.iCandSet,col]
        #     print('Type:{}, Decision: {}, Correct Answer: {}'.format(player.iCandSet,int(p.iAnsValue2),int(p.iRightValue2)))

page_sequence = [ChangeTask, Notify, FixCross, Info, Decision]
