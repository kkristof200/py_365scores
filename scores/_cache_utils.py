# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional
import os

# Pip
from kcu import kpath

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- class: _CacheUtils ---------------------------------------------------------- #

class _CacheUtils:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def images_cache_path(cls) -> str:
        return kpath.new_tempdir(
            path_src=cls.cache_path(),
            appending_subpath='images',
            append_random_subfolder_path=False,
            create_folder_if_not_exists=True
        )

    @staticmethod
    def cache_path() -> str:
        return kpath.new_tempdir(
            appending_subpath='py_365scores_cache',
            append_random_subfolder_path=False,
            create_folder_if_not_exists=True
        )

    @classmethod
    def final_download_image_path_for_url(
        cls,
        image_url: str,
        image_path: Optional[str] = None,
        image_folder_path: Optional[str] = None
    ) -> str:
        if image_path:
            return image_path

        return os.path.join(image_folder_path or cls.images_cache_path(), cls.image_name_for_url(image_url))

    @classmethod
    def temp_download_image_path_for_url(
        cls,
        image_url: str,
        image_path: Optional[str] = None,
        image_folder_path: Optional[str] = None,
        use_cache: bool = True
    ) -> str:
        if image_path:
            return image_path

        return os.path.join(
            image_folder_path if not use_cache and image_folder_path else cls.images_cache_path(),
            cls.image_name_for_url(image_url)
        )

    @classmethod
    def image_name_for_url(
        cls,
        image_url: str
    ) -> str:
        return '{}.png'.format(cls.image_id_for_url(image_url))

    @staticmethod
    def image_id_for_url(image_url: str) -> str:
        # https://imagecache.365scores.com/image/upload/d_Countries:Round:153.png/Competitors/67096
        base = image_url.split('d_Countries:')[-1].replace('.png', '').lower()

        # round:153/competitors/67096
        # 153/competitors/67096
        is_round = 'round' in base

        if is_round:
            base = base.replace('round:', '')

        # 153/competitors/67096
        country_id, type, id = base.split('/')

        return '{}-country_id_{}-id_{}{}'.format(type, country_id, id, '-round' if is_round else '')


# ---------------------------------------------------------------------------------------------------------------------------------------- #