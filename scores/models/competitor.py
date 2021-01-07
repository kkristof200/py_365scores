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
        self.image_url = 'https://imagecache.365scores.com/image/upload/f_auto,c_limit,q_auto:eco,d_Competitors:default1.png/Competitors/{}'.format(self.id)


# ---------------------------------------------------------------------------------------------------------------------------------------- #