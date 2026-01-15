from auth import get_spotify_client
from playlist import (
    create_playlist,
    add_track_to_playlist,
    discover_local,
    parse_local,
    search_spotify_track,
)
from txt2spotify import sync_text_to_spotify
from datetime import datetime

import sys
import local_sync


def display_menu():
    """Display the main menu options to the user."""
    print("\n" + "=" * 50)
    print("Spotify Integration Tool")
    print("=" * 50)
    print("1. Sync local directories")
    print("2. Create Spotify playlist and sync tracks")
    print("3. Sync tracks to existing Spotify playlist")
    print("4. Sync tracks from text file to Spotify")
    print("=" * 50)


def get_user_choice():
    """Get and validate user's menu choice."""
    while True:
        try:
            choice = input("\nEnter your choice (1, 2, 3, or 4): ").strip()
            if choice in ["1", "2", "3", "4"]:
                return choice
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)


def sync_directories_flow():
    """Handle directory syncing."""
    print("\n--- Sync Local Directories ---")
    source = input("Enter source directory path: ").strip()
    destination = input("Enter destination directory path: ").strip()

    if not source or not destination:
        print("Error: Both paths are required.")
        return

    try:
        local_sync.sync_directories(source, destination)
        print("✓ Directories synced successfully!")
    except Exception as e:
        print(f"✗ Error during sync: {e}")


def create_playlist_flow(sp):
    """Handle new playlist creation and track sync."""
    print("\n--- Create Playlist & Sync Tracks ---")
    playlist_name = input("Enter playlist name (or press Enter for default): ").strip()

    if not playlist_name:
        playlist_name = "MyBackup" + datetime.now().strftime("%Y%m%d_%H%M")

    try:
        playlist_id = create_playlist(sp, playlist_name, description="")
        print(f"✓ Playlist created: {playlist_name}")
    except Exception as e:
        print(f"✗ Error creating playlist: {e}")
        return

    sync_tracks_to_playlist(sp, playlist_id)


def sync_existing_playlist_flow(sp):
    """Handle syncing to an existing playlist."""
    print("\n--- Sync Tracks to Existing Playlist ---")
    playlist_id = input("Enter Spotify playlist ID: ").strip()

    if not playlist_id:
        print("Error: Playlist ID is required.")
        return

    sync_tracks_to_playlist(sp, playlist_id)


def sync_tracks_to_playlist(sp, playlist_id):
    """Search for and add local tracks to a Spotify playlist."""
    directory = input("Enter directory path containing local tracks: ").strip()

    if not directory:
        print("Error: Directory path is required.")
        return

    try:
        # Discover and parse local tracks
        local_files = discover_local(directory)
        parsed_tracks = parse_local(local_files)
        print(f"\n✓ Parsed {len(parsed_tracks)} tracks from local directory.")

        # Search for each track on Spotify and add to playlist
        print("\nSearching for tracks on Spotify...")
        added_count = 0
        for artist_name, track_name in parsed_tracks:
            track_uri = search_spotify_track(sp, track_name, artist_name)
            if track_uri:
                add_track_to_playlist(sp, track_uri, playlist_id)
                print(f"✓ Added: {artist_name} - {track_name}")
                added_count += 1
            else:
                print(f"✗ Failed: {artist_name} - {track_name}")

        print(f"\n✓ Sync complete! Added {added_count}/{len(parsed_tracks)} tracks.")
        print("Check failed_tracks.log for any missing tracks.")
    except Exception as e:
        print(f"✗ Error during sync: {e}")


def sync_text_file_flow(sp):
    """Handle syncing tracks from a text file to Spotify."""
    print("\n--- Sync Tracks from Text File to Spotify ---")
    file_path = input("Enter text file path: ").strip()

    if not file_path:
        print("Error: File path is required.")
        return

    playlist_id = input("Enter Spotify playlist ID: ").strip()

    if not playlist_id:
        print("Error: Playlist ID is required.")
        return

    try:
        # Sync tracks from the specified text file to Spotify
        sync_text_to_spotify(sp, file_path, playlist_id)
        print("✓ Tracks synced from text file successfully!")
    except Exception as e:
        print(f"✗ Error during sync: {e}")


def main():
    """Main application entry point."""
    display_menu()
    choice = get_user_choice()

    if choice == "1":
        sync_directories_flow()

    elif choice in ["2", "3"]:
        # Authenticate with Spotify
        try:
            sp = get_spotify_client()
            print("✓ Spotify authentication successful.")
        except Exception as e:
            print(f"✗ Error during Spotify authentication: {e}")
            return

        if choice == "2":
            create_playlist_flow(sp)
        else:  # choice == "3"
            sync_existing_playlist_flow(sp)
    elif choice == "4":
        # Authenticate with Spotify
        try:
            sp = get_spotify_client()
            print("✓ Spotify authentication successful.")
        except Exception as e:
            print(f"✗ Error during Spotify authentication: {e}")
            return

        sync_text_file_flow(sp)


if __name__ == "__main__":
    main()
