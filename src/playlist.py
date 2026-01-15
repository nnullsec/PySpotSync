import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
success_logger = logging.getLogger("success")
failed_logger = logging.getLogger("failed")

formatter = logging.Formatter("%(asctime)s - %(message)s")

success_handler = logging.FileHandler("successful_tracks.log")
success_handler.setFormatter(formatter)

failed_handler = logging.FileHandler("failed_tracks.log")
failed_handler.setFormatter(formatter)

success_logger.addHandler(success_handler)
failed_logger.addHandler(failed_handler)

# Audio file extensions
AUDIO_EXTENSIONS = {
    ".aac",
    ".aiff",
    ".alac",
    ".ape",
    ".awb",
    ".flac",
    ".m4a",
    ".m4b",
    ".mp3",
    ".mpc",
    ".ogg",
    ".opus",
    ".raw",
    ".wav",
    ".wma",
    ".webm",
}


def create_playlist(sp, name, description, public=False):
    """Create a new Spotify playlist."""
    try:
        user_id = sp.current_user()["id"]
        playlist = sp.user_playlist_create(
            user_id, name, public=public, description=description
        )
        print(f"Playlist {playlist['name']} created with ID: {playlist['id']}")
        return playlist["id"]
    except Exception as e:
        logging.error(f"Error creating playlist: {e}")
        return None


def list_playlist_tracks(sp, playlist_id, show_ids=False):
    """List all tracks in a playlist."""
    try:
        results = sp.playlist_tracks(playlist_id)
        items = results["items"]

        while results["next"]:
            results = sp.next(results)
            items.extend(results["items"])

        print("\nPlaylist Tracks:")
        for item in items:
            track = item["track"]
            artists = ", ".join([a["name"] for a in track["artists"]])
            title = track["name"]
            track_id = f" (ID: {track['id']})" if show_ids else ""
            print(f"{artists} - {title}{track_id}")
    except Exception as e:
        logging.error(f"Error listing playlist tracks: {e}")


def search_spotify_track(sp, track_name, artist_name):
    """Search for a track on Spotify by name and artist."""
    try:
        # Primary search with track and artist
        results = sp.search(
            q=f"track:{track_name} artist:{artist_name}", type="track", limit=1
        )

        if results["tracks"]["items"]:
            return results["tracks"]["items"][0]["uri"]

        # Fallback: swap artist and track in case of parsing error
        results = sp.search(
            q=f"track:{artist_name} artist:{track_name}", type="track", limit=1
        )

        if results["tracks"]["items"]:
            return results["tracks"]["items"][0]["uri"]

        # Track not found - log to failed tracks file
        logging.warning(f"No track {artist_name} - {track_name}'")
        failed_logger.info(f" [x] spotify_search fail | {artist_name} - {track_name}")
        return None
    except Exception as e:
        logging.error(
            f"Error searching for track '{track_name}' by '{artist_name}': {e}"
        )
        return None


def add_track_to_playlist(sp, track_uri, playlist_id):
    """Add a track to a playlist."""
    try:
        sp.playlist_add_items(playlist_id, [track_uri])
    except Exception as e:
        logging.error(f"Error adding track to playlist: {e}")


def discover_local(local_directory):
    """Discover audio files in a local directory."""
    dir_path = Path(local_directory)
    print(f"Scanning directory: {dir_path}")

    if not dir_path.exists():
        logging.error(f"Directory does not exist: {dir_path}")
        return []

    local_tracks = [
        f
        for f in dir_path.iterdir()
        if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS
    ]
    print(f"Found {len(local_tracks)} audio files to process.")
    return local_tracks


def parse_local(tracks):
    """Parse local track filenames to extract artist and track name."""
    parsed_tracks = []
    for track in tracks:
        parts = track.stem.split(" - ")
        if len(parts) == 2:
            parsed_tracks.append(parts)
        else:
            with open("fails.txt", "a") as f:
                f.write(f" [x] parse_fail | {track.name}\n")
            logging.warning(f" [x] Could not parse track: {track.name}")
    return parsed_tracks
