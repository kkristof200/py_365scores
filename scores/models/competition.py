# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Union

# Local
from .base import BaseCompetingObject, Country, Sport

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: Competition ---------------------------------------------------------- #

class Competition(BaseCompetingObject):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        d: dict,
        sport_or_sport_dict: Union[Sport, dict],
        country_or_country_dict: Union[Country, dict]
    ):
        super().__init__(d, sport_or_sport_dict=sport_or_sport_dict, country_or_country_dict=country_or_country_dict)

        self.has_standings = self._d_val(d, 'hasStandings', False)
        self.has_standings_groups = self._d_val(d, 'hasStandingsGroups', False)
        self.has_active_games = self._d_val(d, 'hasActiveGames', False)
        self.is_top = self._d_val(d, 'isTop', False)

        self.total_games = self._d_val(d, 'totalGames', 0)
        self.live_games = self._d_val(d, 'liveGames', 0)


    # ----------------------------------------------------------- Overrides ---------------------------------------------------------- #

    def _image_url_key(self) -> str:
        return 'Competitions'

# ---------------------------------------------------------------------------------------------------------------------------------------- #