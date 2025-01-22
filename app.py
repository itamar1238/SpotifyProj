# Imports
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import os

from dotenv import load_dotenv
load_dotenv()

# Spotify API credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8080/callback"

# Spotify API scope
SCOPE = "user-top-read"

def display_top_items(items, item_type, filter_explicit=False):
    """
    Displays the top items (artists or tracks) with optional filtering for explicit content.
    items: List of items (artists or tracks).
    item_type: Type of item ("artists" or "tracks").
    filter_explicit: Whether to filter out explicit tracks (default: False).
    """
    print(f"Top {item_type}:")
    count = 1
    # Loop throught the items
    for item in items:
        if item_type == "tracks":
            name = item["name"]
            artist = item["artists"][0]["name"]
            # Check if the track is explicit
            is_explicit = item.get("explicit", False)
            # Skip explicit tracks if filter_explicit is True
            if filter_explicit and is_explicit:
                continue
            print(f"{count}. {name} by {artist} {'(Explicit)' if is_explicit else ''}")
        # Display the artist name
        elif item_type == "artists":
            print(f"{count}. {item['name']}")
        count += 1

def main():
    # Waits for user input to start the program and log in to Spotify
    print("Press ENTER to log in to Spotify")
    input()

    # Log in to Spotify
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )

    sp = spotipy.Spotify(auth_manager=sp_oauth)

    # Display the current user
    print("Logged in as", sp.current_user()["display_name"])
    time.sleep(0.5)

    # Retrieve and display top artists
    top_artists = sp.current_user_top_artists(limit=5)["items"]
    display_top_items(top_artists, "artists")

    time.sleep(0.5)

    # Retrieve and display top tracks with explicit filtering
    top_tracks = sp.current_user_top_tracks(limit=5)["items"]
    explicitChoice = input("Would you like to filter out explicit tracks? (y/n): ")
    if explicitChoice == "y":
        display_top_items(top_tracks, "tracks", filter_explicit=True)
    else:
        display_top_items(top_tracks, "tracks")

if __name__ == "__main__":
    main()