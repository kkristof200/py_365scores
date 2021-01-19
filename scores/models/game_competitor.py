# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Union

# Local
from .competitor import Competitor
from .base import Sport, Country

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# -------------------------------------------------------- class: GameCompetitor --------------------------------------------------------- #

class GameCompetitor(Competitor):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        d: dict,
        sport_or_sport_dict: Union[Sport, dict],
        country_or_country_dict: Union[Country, dict]
    ):
        super().__init__(d, sport_or_sport_dict=sport_or_sport_dict, country_or_country_dict=country_or_country_dict)

        self.score = d['score']

        if self.score == int(self.score):
            self.score = int(self.score)

        self.aggregated_score = d['aggregatedScore']

        if self.aggregated_score == int(self.aggregated_score):
            self.aggregated_score = int(self.aggregated_score)


# ---------------------------------------------------------------------------------------------------------------------------------------- #