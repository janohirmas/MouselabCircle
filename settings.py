from os import environ

SESSION_CONFIGS = [
    dict(
        name='Experiment',
        app_sequence=['Instructions','Task','Questionnaire'],
        num_demo_participants=1,
    ),
    dict(
        name='Task',
        app_sequence=['Task'],
        num_demo_participants=1,
    ),
    dict(
        name='Instructions',
        app_sequence=['Instructions'],
        num_demo_participants=1,
    ),
    dict(
        name='Questionnaire',
        app_sequence=['Questionnaire'],
        num_demo_participants=1,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['BlockOrder','mTrials','lOrder','iRound1','iRightValue1','iAnsValue1','iRound2','iRightValue2','iAnsValue2',
                                'startTime','iOutFocus','iFullscreenChanges','dTimeOutFocus','dPixelRatio','bCheckQ' ]
SESSION_FIELDS = []

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='prolific', display_name='Prolific Room (no participant labels)'),
]
# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '4122092790741'
