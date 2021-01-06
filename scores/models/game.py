# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
import datetime

# Pip
from jsoncodable import JSONCodable

# Local
from .enums import Sport
from .competitor import Competitor

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: Game -------------------------------------------------------------- #

class Game(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        d: dict
    ):
        self.id = d['id']
        self.sport_id = d['sportId']
        self.sport = Sport(self.sport_id)
        self.competition_id = d['competitionId']
        self.competition_display_name = d['competitionDisplayName'] if 'competitionDisplayName' in d else None
        self.status_group = d['statusGroup']
        self.status_text = d['statusText']
        self.short_status_text = d['shortStatusText']
        self.start_time_str = d['startTime']
        self.start_time_date = datetime.datetime.strptime(self.start_time_str.split('+')[0], '%Y-%m-%dT%H:%M:%S')
        self.start_time_ts = self.start_time_date.timestamp()
        self.just_ended = d['justEnded']
        self.postponed = self.status_group == 4 and self.status_text.lower() == 'postponed'
        self.cancelled = self.status_group == 4 and not self.postponed and self.status_text.lower() == 'cancelled'
        self.game_time = d['gameTime']

        self.home_competitor = Competitor(d['homeCompetitor'])
        self.away_competitor = Competitor(d['awayCompetitor'])

        self.score = (self.home_competitor.score, self.away_competitor.score)
        self.aggregated_score = (self.home_competitor.aggregated_score, self.away_competitor.aggregated_score)


# ---------------------------------------------------------------------------------------------------------------------------------------- #