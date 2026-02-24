#!/bin/bash
# Cleanup script for Telegram Bot - removes generated runtime files
# This keeps the app directory clean while preserving configuration

echo "🧹 Cleaning up generated runtime files..."

# Remove session files (will be recreated on next run)
rm -rf .sessions/

# Remove thumbnails (will be recreated as needed)
rm -rf downloads/.thumbnails/

# Remove temp files (safe to remove)
rm -rf downloads/.temp/

# Remove qBittorrent runtime config (preserves main config)
rm -rf .qbittorrent/

# Remove SABnzbd runtime config (preserves main config)
rm -rf .sabnzbd/

# Remove log file (will be recreated)
rm -f .bot.log

echo "✅ Cleanup complete! The app directory is now clean."
echo "📝 Note: Configuration files (config.py) and virtual environment are preserved."