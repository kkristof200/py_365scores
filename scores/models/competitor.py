# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# Pip
from jsoncodable import JSONCodable

# Local
from .enums import Sport

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: Competitor ----------------------------------------------------------- #

class Competitor(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        d: dict
    ):
        self.id = d['id']
        self.country_id = d['countryId']
        self.sport_id = d['sportId']
        self.sport = Sport(self.sport_id)
        self.name = d['name']
        self.score = d['score']

        if self.score == int(self.score):
            self.score = int(self.score)

        self.aggregated_score = d['aggregatedScore']

        if self.aggregated_score == int(self.aggregated_score):
            self.aggregated_score = int(self.aggregated_score)
        
        self.popularity_rank = d['popularityRank']


# ---------------------------------------------------------------------------------------------------------------------------------------- #