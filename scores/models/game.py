# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
import datetime

# Local
from .base import Sport, Country, BaseIdable
from .game_competitor import GameCompetitor
from .competition import Competition

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: Game -------------------------------------------------------------- #

class Game(BaseIdable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        d: dict,
        sport_dict: dict,
        competition_dict: dict,
        competition_country_dict: dict,
        home_competitor_country_dict: dict,
        away_competitor_country_dict: dict
    ):
        super().__init__(d)

        sport = Sport(sport_dict)

        self.competition = Competition(competition_dict, sport_or_sport_dict=sport, country_or_country_dict=competition_country_dict)
        self.home_competitor = GameCompetitor(d['homeCompetitor'], sport_or_sport_dict=sport, country_or_country_dict=home_competitor_country_dict)
        self.away_competitor = GameCompetitor(d['awayCompetitor'], sport_or_sport_dict=sport, country_or_country_dict=away_competitor_country_dict)

        self.season_num = self._d_val(d, 'seasonNum')
        self.stage_num = self._d_val(d, 'stageNum')
        self.group_num = self._d_val(d, 'groupNum')
        self.round_num = self._d_val(d, 'roundNum')

        self.competition_display_name = self._d_val(d, 'competitionDisplayName')
        self.status_group = d['statusGroup']
        self.status_text = d['statusText']
        self.short_status_text = d['shortStatusText']
        self.start_time_str = d['startTime']
        self.start_time_date = datetime.datetime.strptime(self.start_time_str.split('+')[0], '%Y-%m-%dT%H:%M:%S')
        self.start_time_ts = self.start_time_date.timestamp()

        self.just_ended = d['justEnded']
        self.live = self.status_group == 3
        self.postponed = self.status_group == 4 and self.status_text.lower() == 'postponed'
        self.cancelled = self.status_group == 4 and not self.postponed and self.status_text.lower() == 'cancelled'
        self.scheduled = self.status_group == 2 and not self.postponed and not self.cancelled and self.status_text.lower() == 'scheduled'

        self.game_time = d['gameTime']
        self.game_time_display = self._d_val(d, 'gameTimeDisplay', '')
        self.game_time_and_status_display_type = d['gameTimeAndStatusDisplayType']
        self.has_tv_networks = d['hasTVNetworks']

        self.has_lineups = self._d_val(d, 'hasLineups', False)
        self.has_field_positions = self._d_val(d, 'hasFieldPositions', False)
        self.has_missing_players = self._d_val(d, 'hasMissingPlayers', False)

        self.score = (self.home_competitor.score, self.away_competitor.score)
        self.aggregated_score = (self.home_competitor.aggregated_score, self.away_competitor.aggregated_score)

        self.has_score = self.score != (-1, -1)
        self.has_aggregated_score = self.aggregated_score != (-1, -1)


    # ------------------------------------------------------- Public properties ------------------------------------------------------ #

    @property
    def sport(self) -> Sport:
        return self.competition.sport

    @property
    def country(self) -> Country:
        return self.competition.country


# ---------------------------------------------------------------------------------------------------------------------------------------- #