# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Union
from abc import abstractmethod

# Local
from .core import BaseObject, SportType
from .sport import Sport
from .country import Country

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------ class: BaseCompetingObject ------------------------------------------------------ #

class BaseCompetingObject(BaseObject):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        d: dict,
        sport_or_sport_dict: Union[Sport, dict],
        country_or_country_dict: Union[Country, dict]
    ):
        super().__init__(d)

        self.sport = sport_or_sport_dict if isinstance(sport_or_sport_dict, Sport) else Sport(sport_or_sport_dict)
        self.country = country_or_country_dict if isinstance(country_or_country_dict, Country) else Country(country_or_country_dict)

        self.popularity_rank = d['popularityRank']

        self.image_url = self.get_image_url(round=False)
        self.image_url_round = self.get_image_url(round=True)

        self.long_name = self._d_val(d, 'longName')
        self.short_name = self._d_val(d, 'shortName')


    # ------------------------------------------------------- Abstract methods ------------------------------------------------------- #

    @abstractmethod
    def _image_url_key(self) -> str:
        pass


    # ------------------------------------------------------- Public properties ------------------------------------------------------ #

    @property
    def sport_id(self) -> int:
        return self.sport.id

    @property
    def sport_type(self) -> SportType:
        return SportType(self.sport_id)

    @property
    def country_id(self) -> int:
        return self.country.id


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def get_name(self) -> str:
        return self.long_name or self.name

    def get_image_url(
        self,
        round: bool = False
    ) -> str:
        return 'https://imagecache.365scores.com/image/upload/d_Countries{}:{}.png/{}/{}'.format(
            ':Round' if round else '',
            self.country_id,
            self._image_url_key(),
            self.id
        )


# ---------------------------------------------------------------------------------------------------------------------------------------- #