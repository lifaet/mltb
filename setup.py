#!/usr/bin/env python3
"""
MLTB Setup Script - Easy configuration setup
Usage: python3 setup.py
"""

import os
import shutil
from pathlib import Path

def print_banner():
    print("=" * 50)
    print("🚀 MLTB Telegram Bot Setup")
    print("=" * 50)

def check_existing_config():
    """Check if config.py already exists"""
    if os.path.exists("config.py"):
        response = input("config.py already exists. Overwrite? (y/N): ").lower().strip()
        if response not in ['y', 'yes']:
            print("Setup cancelled.")
            return False
    return True

def get_user_input(prompt, default="", required=False):
    """Get user input with default value"""
    if default:
        value = input(f"{prompt} [{default}]: ").strip()
        return value if value else default
    else:
        while True:
            value = input(f"{prompt}: ").strip()
            if value or not required:
                return value
            print("This field is required.")

def setup_config():
    """Interactive config setup"""
    print("\n📝 Bot Configuration Setup")
    print("Enter your bot details. Press Enter to use defaults for optional fields.")

    # Required fields
    bot_token = get_user_input("Bot Token (from @BotFather)", required=True)
    owner_id = get_user_input("Owner ID (your Telegram user ID)", required=True)
    api_id = get_user_input("Telegram API ID (from my.telegram.org)", required=True)
    api_hash = get_user_input("Telegram API Hash (from my.telegram.org)", required=True)

    # Optional fields with sensible defaults
    print("\n🔧 Optional Configuration:")

    # Upload settings
    default_upload = get_user_input("Default upload destination", "rc")
    status_limit = get_user_input("Status update limit", "4")

    # Drive settings
    gdrive_id = get_user_input("Google Drive folder ID (leave empty to skip)", "")

    # Rclone settings
    rclone_path = get_user_input("Rclone config path", "")
    rclone_flags = get_user_input("Rclone flags", "")

    # Generate config content
    config_content = f'''# REQUIRED CONFIG
BOT_TOKEN = "{bot_token}"
OWNER_ID = {owner_id}
TELEGRAM_API = {api_id}
TELEGRAM_HASH = "{api_hash}"

# OPTIONAL CONFIG
TG_PROXY = {{}}
USER_SESSION_STRING = ""
CMD_SUFFIX = ""
AUTHORIZED_CHATS = ""
SUDO_USERS = ""
STATUS_LIMIT = {status_limit}
DEFAULT_UPLOAD = "{default_upload}"
STATUS_UPDATE_INTERVAL = 15
FILELION_API = ""
STREAMWISH_API = ""
EXCLUDED_EXTENSIONS = ""
INCLUDED_EXTENSIONS = ""
INCOMPLETE_TASK_NOTIFIER = False
YT_DLP_OPTIONS = ""
USE_SERVICE_ACCOUNTS = False
NAME_SUBSTITUTE = r""
FFMPEG_CMDS = {{"merge": ["-f concat -safe 0 -i mltb.txt -c copy mltb.mp4 -del"]}}
UPLOAD_PATHS = {{}}

# GDrive Tools
GDRIVE_ID = "{gdrive_id}"
IS_TEAM_DRIVE = False
STOP_DUPLICATE = False
INDEX_URL = ""

# Rclone
RCLONE_PATH = "{rclone_path}"
RCLONE_FLAGS = "{rclone_flags}"
RCLONE_SERVE_URL = ""
RCLONE_SERVE_PORT = 0
RCLONE_SERVE_USER = ""
RCLONE_SERVE_PASS = ""

# JDownloader
JD_EMAIL = ""
JD_PASS = ""

# Sabnzbd
USENET_SERVERS = [
    {{
        "name": "main",
        "host": "",
        "port": 563,
        "timeout": 60,
        "username": "",
        "password": "",
        "connections": 8,
        "ssl": 1,
        "ssl_verify": 2,
        "ssl_ciphers": "",
        "enable": 1,
        "required": 0,
        "optional": 0,
        "retention": 0,
        "send_group": 0,
        "priority": 0,
    }}
]

# Nzb search
HYDRA_IP = ""
HYDRA_API_KEY = ""

# Update
UPSTREAM_REPO = ""
UPSTREAM_BRANCH = "master"

# Leech
LEECH_SPLIT_SIZE = 0
AS_DOCUMENT = False
EQUAL_SPLITS = False
MEDIA_GROUP = False
USER_TRANSMISSION = False
HYBRID_LEECH = False
LEECH_FILENAME_PREFIX = ""
LEECH_DUMP_CHAT = ""
CLONE_DUMP_CHATS = ""
FILES_LINKS = False
THUMBNAIL_LAYOUT = ""

# qBittorrent/Aria2c
TORRENT_TIMEOUT = 0
BASE_URL = ""
BASE_URL_PORT = 0
WEB_PINCODE = False

# Queueing system
QUEUE_ALL = 0
QUEUE_DOWNLOAD = 0
QUEUE_UPLOAD = 0

# RSS
RSS_DELAY = 600
RSS_CHAT = ""

# Torrent Search
SEARCH_API_LINK = ""
SEARCH_LIMIT = 0
SEARCH_PLUGINS = [
    "https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/piratebay.py",
    "https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/limetorrents.py",
    "https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/torlock.py",
    "https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/torrentscsv.py",
    "https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/eztv.py",
    "https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/torrentproject.py",
    "https://raw.githubusercontent.com/MaurizioRicci/qBittorrent_search_engines/master/kickass_torrent.py",
    "https://raw.githubusercontent.com/MaurizioRicci/qBittorrent_search_engines/master/yts_am.py",
    "https://raw.githubusercontent.com/MadeOfMagicAndWires/qBit-plugins/master/engines/linuxtracker.py",
    "https://raw.githubusercontent.com/MadeOfMagicAndWires/qBit-plugins/master/engines/nyaasi.py",
    "https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/ettv.py",
    "https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/glotorrents.py",
    "https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/thepiratebay.py",
    "https://raw.githubusercontent.com/v1k45/1337x-qBittorrent-search-plugin/master/leetx.py",
    "https://raw.githubusercontent.com/nindogo/qbtSearchScripts/master/magnetdl.py",
    "https://raw.githubusercontent.com/msagca/qbittorrent_plugins/main/uniondht.py",
    "https://raw.githubusercontent.com/khensolomon/leyts/master/yts.py",
]
'''

    # Write config file
    with open("config.py", "w") as f:
        f.write(config_content)

    print("✅ Configuration saved to config.py")

def main():
    print_banner()

    if not check_existing_config():
        return

    setup_config()

    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Run './run.sh' to start the bot")
    print("2. Use 'python3 utils.py session' to generate user session (optional)")
    print("3. Use 'python3 utils.py drive-token' for Google Drive (if needed)")
    print("\nFor help: ./run.sh --help")

if __name__ == "__main__":
    main()