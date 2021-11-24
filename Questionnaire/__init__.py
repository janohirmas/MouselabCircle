from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Questionnaire'
    players_per_group = None
    num_rounds = 1
    iBonusRight = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Variables for Demographics
    D1 = models.StringField()
    D2 = models.StringField()
    D3 = models.StringField()
    D4 = models.StringField(blank=True)
    D5 = models.StringField(blank=True)
    D6 = models.StringField(blank=True)
    ET1 = models.StringField()
    ET2 = models.StringField()
    ET3 = models.StringField(blank=True)
    EQ1 = models.StringField()
    EQ2 = models.IntegerField()
    EQ3 = models.IntegerField()
    EQ4 = models.IntegerField()
    EQ5 = models.IntegerField()
    # Result Variables
    round1      = models.IntegerField()
    round2      = models.IntegerField()
    RightValue1 = models.IntegerField()
    AnsValue1   = models.IntegerField()         
    RightValue2 = models.IntegerField()
    AnsValue2   = models.IntegerField()


# PAGES
class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 
                    'ET1','ET2','ET3',
                    'EQ1','EQ2','EQ3','EQ4','EQ5']

class ResultPage(Page):
    @staticmethod
    def vars_for_template(player: Player):
        p = player.participant
        # dPayoff = min(5 - 0.5*(p.iRightValue1 - p.iAnsValue1)^2,0) + min(5 - 0.5*(p.iRightValue2 - p.iAnsValue2)^2,0)
        dPayoff =( (p.iRightValue1 == p.iAnsValue1) + (p.iRightValue2 == p.iAnsValue2))*Constants.iBonusRight
        player.round1      = int(p.iRound1)
        player.round2      = int(p.iRound2)
        player.RightValue1 = int(p.iRightValue1)
        player.AnsValue1   = int(p.iAnsValue1)    
        player.RightValue2 = int(p.iRightValue2)
        player.AnsValue2   = int(p.iAnsValue2)
        player.payoff      = dPayoff

        return dict(
            round1      = p.iRound1,
            round2      = p.iRound2,
            RightValue1 = p.iRightValue1,
            AnsValue1   = p.iAnsValue1,            
            RightValue2 = p.iRightValue2,
            AnsValue2   = p.iAnsValue2,
            payoff      = dPayoff,
        )  

page_sequence = [Questionnaire, ResultPage]
