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
    num_prounds = 4
    num_rounds = 2*num_brounds+num_prounds  
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
    # 2nd Calibration
    dError          = models.FloatField()
    ValidPts        = models.IntegerField()
    Result          = models.StringField()
    NumCal          = models.IntegerField()
    # Result Variables
    iCandSet        = models.IntegerField()




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
            mTrials = lTrials
            # Random Order Block2
            random.shuffle(lTrials)
            mTrials.extend(lTrials)
            # Save trials as participant variable.
            part.mTrials = mTrials
            # Relevant round numbers for choosing paid rounds
            iR1 = Constants.num_prounds+1
            iR2 = Constants.num_prounds+Constants.num_brounds
            iR3 = Constants.num_prounds+Constants.num_brounds+1
            iR4 = Constants.num_rounds
            # Randomize paid rounds
            part.iRound1     = random.choice(range(iR1,iR2))
            part.iRound2     = random.choice(range(iR3,iR4))
            print('Trials selected for participant {}: {} and {}'.format(part.code,part.iRound1,part.iRound2))
    for player in subsession.get_players():
        ## Load participant's round
        p = player.participant
        if player.round_number<= Constants.num_prounds:
            vPars = p.mTrials[random.randint(Constants.num_brounds)]     # Choose random round for the practice 
        else:
            vPars = p.mTrials[player.round_number-Constants.num_prounds-1] # Choose respective round values
        # Save variables in players database

        pos1,pos2,pos3,pos4,pos5 = list(p.lOrder)
        player.sOrder = "{},{},{},{},{}".format(pos1,pos2,pos3,pos4,pos5)
        player.iCandSet, player.iGender, player.iFirst, player.iGMA, player.iPersonality, player.iInterview = vPars
        
def calibrate():
    # Open Connection with Eye-Tracker
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(Constants.ADDRESS)
    # Start Calibration and Show results
    s.send(str.encode('<SET ID="CALIBRATE_START" STATE="1" />\r\n'))
    s.send(str.encode('<SET ID="CALIBRATE_SHOW" STATE="1" />\r\n'))

    iCal = 1 # Number of calibration attempts
    while True:
            rxdat = s.recv(1024)    
            # print(bytes.decode(rxdat))
            result  = bytes.decode(rxdat)
            if result.find('CALIB_RESULT_PT')!=-1:
                iPts    = int(result.split('PT="')[1].split('"')[0])
            if (result.find('ID="CALIB_RESULT"')!=-1):
                s.send(str.encode('<GET ID="CALIBRATE_RESULT_SUMMARY" />\r\n'))
                rxdat = s.recv(1024)    
                sum = bytes.decode(rxdat)
                dError      = float(sum.split('AVE_ERROR="')[1].split('"')[0])
                dValidPts   = float(sum.split('VALID_POINTS="')[1].split('"')[0])
                print('Valid Points: {}, Avg. Error: {}'.format(dValidPts,dError))
                if dValidPts==iPts and dError<=60: 
                    s.send(str.encode('<SET ID="CALIBRATE_SHOW" STATE="0" />\r\n'))
                    break
                else:
                    s.send(str.encode('<SET ID="CALIBRATE_START" STATE="1" />\r\n'))
                    iCal +=1

    s.close()
    return dict(
        dError = dError,
        ValidPts = dValidPts,
        Result  = result,
        NumCal = iCal,
    )

# PAGES
class Calibration(Page):
    @staticmethod
    def vars_for_template(player):
        print(calibrate)
        Calibration = calibrate()
        player.dError = float(Calibration['dError'])
        player.ValidPts = int(Calibration['ValidPts'])
        player.Result = str(Calibration['Result'])
        player.NumCal = int(Calibration['NumCal'])

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==Constants.num_brounds+Constants.num_prounds+1 or player.round_number==1

class ChangeTask(Page):
    @staticmethod
    def vars_for_template(player: Player):
        msg = [dict(Title='Change in Task',path='Notifications/msgChangeTask.html')]
        return dict(Slides = msg, selfEval = player.participant.BlockOrder==0)

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_brounds+Constants.num_prounds+1


class MsgBeforeTrial(Page):
    @staticmethod
    def vars_for_template(player: Player):
        msg = 'Notifications/msgStartPractice.html'

        return dict(Message = msg, selfEval = player.participant.BlockOrder==0)

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in Constants.lRoundsBefore

class MsgAfterTrial(Page):
    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number == Constants.num_prounds+Constants.num_brounds:
            msg = 'Notifications/msgMiddle.html'
        else:
            msg = 'Notifications/msgEndPractice.html'

        return dict(Message = msg)

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in Constants.lRoundsAfter


class MsgVisual(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(Message = 'Notifications/msgVisual.html')

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in Constants.lRoundsVisual


class VisualTest(Page):
    form_model = 'player'
    form_fields = [ 'sStartVisual','sEndVisual' ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in Constants.lRoundsVisual


class FixCross(Page):
    form_model = 'player'
    form_fields = [ 'sStartCross','sEndCross' ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number!=1

class Info(Page):
    form_model = 'player'
    form_fields = [ 'dRT_info', 'sStartInfo','sEndInfo' ]

    @staticmethod
    def vars_for_template(player: Player):

        lOutcomes   = []
        # Gender
        if (player.iGender==1):
            lOutcomes.append('Female')
        else:
            lOutcomes.append('Male')
        # First
        if (player.iFirst==1):
            lOutcomes.append('Odd')
        else:
            lOutcomes.append('Even')
        # GMA
        if (player.iGMA==1):
            lOutcomes.append('High GMA')
        else:
            lOutcomes.append('Low GMA')
        # Personality
        if (player.iPersonality==1):
            lOutcomes.append('High Consc.')
        else:
            lOutcomes.append('Low Consc.')
        # Interview
        if (player.iInterview==1):
            lOutcomes.append('Good Interview')
        else:
            lOutcomes.append('Bad Interview')
        
        vOutcomes = np.array(lOutcomes)
        vOrder = player.participant.lOrder
        lOutcomes = list(vOutcomes[vOrder])
        return dict(
          Vars = lOutcomes
        )

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number!=1

class Decision(Page):

    form_model = 'player'
    form_fields = [ 'dRT_dec', 'iDec', 'sStartDec','sEndDec' ]
    @staticmethod
    def js_vars(player: Player):
        return dict(
            iMax = Constants.iRatingScale,
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
    def is_displayed(player: Player):
        return player.round_number!=1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        p = player.participant
        if player.round_number==int(p.iRound1):
            p.iAnsValue1 = player.iDec
            iMat = Constants.Results.to_numpy()
            p.iRightValue1 = iMat[player.iCandSet,p.BlockOrder]
            print('Type:{}, Decision: {}, Correct Answer: {}'.format(player.iCandSet,int(p.iAnsValue1),int(p.iRightValue1)))
        if player.round_number==int(p.iRound2):
            p.iAnsValue2 = player.iDec
            iMat = Constants.Results.to_numpy()
            col = 1-p.BlockOrder
            p.iRightValue2 = iMat[player.iCandSet,col]
            print('Type:{}, Decision: {}, Correct Answer: {}'.format(player.iCandSet,int(p.iAnsValue2),int(p.iRightValue2)))

        



page_sequence = [ Calibration, ChangeTask, MsgBeforeTrial, FixCross, Info, Decision, MsgVisual, VisualTest, MsgAfterTrial]
# page_sequence = [  MsgBeforeTrial, FixCross, Info, Decision, MsgVisual, VisualTest, MsgAfterTrial]
