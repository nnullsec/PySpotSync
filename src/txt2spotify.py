import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
success_logger = logging.getLogger("success")
failed_logger = logging.getLogger("failed")

success_handler = logging.FileHandler("successful_tracks.log")
failed_handler = logging.FileHandler("failed_tracks.log")

success_logger.addHandler(success_handler)
failed_logger.addHandler(failed_handler)


def parse_text_file(file_path: str | Path) -> list:
    """Parse a text file to extract artist and track names.

    Expected format: "Artist Name - Track Name" (one per line)
    """
    parsed_tracks = []
    file_path = Path(file_path)

    if not file_path.exists():
        logging.error(f"File does not exist: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                parts = line.split(" - ")
                if len(parts) == 2:
                    artist_name, track_name = parts
                    parsed_tracks.append([artist_name.strip(), track_name.strip()])
                else:
                    failed_logger.info(f" [x] parse_fail | Line {line_num}: {line}")
                    logging.warning(f"Could not parse line {line_num}: {line}")

        print(f"Parsed {len(parsed_tracks)} tracks from {file_path.name}")
        return parsed_tracks
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return []


def sync_text_to_spotify(sp, file_path: str | Path, playlist_id: str):
    """Parse a text file and sync all tracks to a Spotify playlist."""
    from playlist import search_spotify_track, add_track_to_playlist

    parsed_tracks = parse_text_file(file_path)

    if not parsed_tracks:
        print("No tracks to sync.")
        return

    print(f"\nSearching for {len(parsed_tracks)} tracks on Spotify...")
    added = 0
    failed = 0

    for artist_name, track_name in parsed_tracks:
        track_uri = search_spotify_track(sp, track_name, artist_name)
        if track_uri:
            add_track_to_playlist(sp, track_uri, playlist_id)
            success_logger.info(f"Added: {artist_name} - {track_name}")
            print(f"✓ Added: {artist_name} - {track_name}")
            added += 1
        else:
            failed += 1
            print(f"✗ Failed: {artist_name} - {track_name}")

    print(f"\nSync complete!")
    print(f"Successfully added: {added}/{len(parsed_tracks)} tracks")
    print(f"Failed: {failed}")
    print(f"Check failed_tracks.log for details on missing tracks.")
