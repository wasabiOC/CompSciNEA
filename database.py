import requests
import pprint

MUSICBRAINZ_API_URL = "https://musicbrainz.org/ws/2"

def search_artist_from_song(work_name):
    response = requests.get(f"{MUSICBRAINZ_API_URL}/work",
                            params={"query": work_name,
                                    "inc": "recordings",
                                    "fmt": "json"
                                    })
    data = response.json()
    if data["recordings"]:
        print("artist:")
        pprint.pp(data["recordings"]["artist"]["name"])
        return data["recordings"]["artist"]["name"]

def search_requested_release(artist_title):
    response = requests.get(f"{MUSICBRAINZ_API_URL}/artist",
                            params={"query": artist_title,
                                    "fmt": "json"
                                    })
    data = response.json()
    if data["artists"]:
        print("artist id:")
        pprint.pp(data["artists"][0]["id"])
        return data["artists"][0]["id"]
    return None


def search_genres_of_artist(artist_id__):
    response = requests.get(f"{MUSICBRAINZ_API_URL}/artist/{artist_id__}",
                            params={"fmt": "json"
                                    })
    data = response.json()
    tags = data.get("tags", [])
    print("artist tags:")
    pprint.pp([tag["name"] for tag in tags])
    return [tag["name"] for tag in tags]

def search_artists_by_genre_tag(artist_tag):
    response = requests.get(f"{MUSICBRAINZ_API_URL}/artist",
                            params={"query": f"tag:{artist_tag}",
                                    "fmt": "json",
                                    "limit": 10})
    data = response.json()
    print("other artist:")
    pprint.pp(data.get("artists", []))
    return data.get("artists", [])


def get_artist_releases(artist_id_):
    response = requests.get(f"{MUSICBRAINZ_API_URL}/release",
                            params={"artist": artist_id_,
                                    "status": "official",
                                    "type": "single",
                                    "limit": 2,
                                    "fmt": "json"
                                    })
    data = response.json()
    if data["releases"]:
        keyword_list = ["(remix)", "(radio edit)", "edit)", "(freemix)", "remix", "freemix", "mix)"]
        return {x["title"] for x in data["releases"]
                if not any(keyword in x["title"].lower() for keyword in keyword_list)}
    return data


song_title = "white noise"
artist_name = search_artist_from_song(song_title)
artist_id = search_requested_release(artist_name)
if artist_id:
    artist_genres = search_genres_of_artist(artist_id)
    for genre in artist_genres:
        other_artists = search_artists_by_genre_tag(genre)
        for artist in other_artists:
            artist_releases = get_artist_releases(artist["id"])
            pprint.pp(artist_releases)
else:
    print(f"No artist found for the song: {song_title}")
