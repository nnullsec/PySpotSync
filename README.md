

<h1 align="center">PySpotSync</h1>

<p align="center">Sync local music and text files to Spotify playlists</p>

## Features

- 🎵 **Sync Local Directories** - Compare and sync local music folders
- 📋 **Create Spotify Playlists** - Create playlists and populate with tracks
- 🔄 **Sync to Existing Playlists** - Add tracks to existing playlists
- 📝 **Text File Integration** - Sync tracks from text files to Spotify

## Quick Start

### Requirements

- Python 3.8+
- Spotify Developer Account
- `spotipy` and `python-dotenv` libraries

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd PySpotSync
   ```

2. Install dependencies:

   ```bash
   uv pip install spotipy python-dotenv
   ```

3. **Set up Spotify API Credentials:**

   - Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new application
   - Copy your **Client ID** and **Client Secret**
   - Set redirect URI to `http://127.0.0.1:80`

4. **Add credentials to `.env` file:**
   ```
   CLIENT_ID=your_client_id_here
   CLIENT_SECRET=your_client_secret_here
   ```

### Usage

```bash
python main.py
```

Select from the menu:

1. Sync local directories
2. Create Spotify playlist and sync tracks
3. Sync tracks to existing Spotify playlist
4. Sync tracks from text file to Spotify

## File Formats

### Local Audio Files

Naming convention: `Artist Name - Track Name.mp3`

Supported: `.mp3`, `.flac`, `.wav`, `.m4a`, `.ogg`, `.aac`, `.aiff`, `.ape`, `.wma`, `.webm`, etc.

### Text File Format

One track per line: `Artist Name - Track Name`

```
The Beatles - Let It Be
Pink Floyd - Wish You Were Here
David Bowie - Space Oddity

# Lines starting with # are ignored
# Blank lines are skipped
```

## Project Structure

```
PySpotSync/
├── main.py                 # Application entry point
├── auth.py                 # Spotify authentication
├── playlist.py             # Playlist operations
├── txt2spotify.py          # Text file syncing
├── local_sync.py           # Directory syncing
├── .env                    # API credentials (fill with your values)
├── README.md               # This file
├── successful_tracks.log   # Success log
└── failed_tracks.log       # Failure log
```

## Logging

The app creates log files for tracking results:

- `successful_tracks.log` - Successfully added tracks
- `failed_tracks.log` - Tracks not found on Spotify
- `fails.txt` - Local files that couldn't be parsed

## Troubleshooting

| Issue                    | Solution                                                        |
| ------------------------ | --------------------------------------------------------------- |
| **Auth fails**           | Verify `.env` has correct CLIENT_ID and CLIENT_SECRET           |
| **Tracks not found**     | Check filename format: `Artist - Track` with dash and space     |
| **Redirect URI error**   | Ensure URI is set to `http://127.0.0.1:80` in Spotify Dashboard |
| **Permission denied**    | Verify you have playlist modification permissions               |
| **Directory sync fails** | Check source/destination paths exist and are accessible         |

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.


**⚠️ Disclaimer:** This documentation was generated with AI assistance. While it has been reviewed and examined, it may contain inaccuracies or outdated information. Please verify critical information independently and report any issues.
