import pytest
import requests
from unittest.mock import patch

from src.database import (search_artist_from_song,
                              search_requested_release,
                              search_genres_of_artist,
                              search_artists_by_genre_tag,
                              get_artist_releases)


def test_search_artist_from_song():
    artist_name = search_artist_from_song("white noise")
    assert artist_name == "Disclosure"
    
    artist_name2 = search_artist_from_song("let it be")
    assert artist_name2 == "The Beatles"

    artist_name3 = search_artist_from_song("yesterday")
    assert artist_name3 == "The Beatles"
    
    