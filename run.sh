#!/bin/bash
# MLTB Bot Start Script - Single command deployment
# This script handles everything needed to run the Telegram bot

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VENV_DIR="mltbenv"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICES_PID_FILE=".services.pid"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if config is valid
check_config() {
    print_step "Checking configuration..."

    if [ ! -f "config.py" ]; then
        print_error "config.py not found! Please copy config_sample.py to config.py and fill in the required fields."
        exit 1
    fi

    # Check for required BOT_TOKEN
    if ! grep -q "BOT_TOKEN = \".*\"" config.py || grep -q "BOT_TOKEN = \"\"" config.py; then
        print_error "BOT_TOKEN is not set in config.py! Please configure your bot token."
        exit 1
    fi

    # Check for required OWNER_ID
    if ! grep -q "OWNER_ID = [0-9]" config.py || grep -q "OWNER_ID = 0" config.py; then
        print_error "OWNER_ID is not set in config.py! Please configure your Telegram user ID."
        exit 1
    fi

    print_status "Configuration looks good!"
}

# Function to setup virtual environment
setup_venv() {
    print_step "Setting up Python virtual environment..."

    if [ ! -d "$VENV_DIR" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv "$VENV_DIR"
    else
        print_status "Virtual environment already exists."
    fi

    # Activate virtual environment
    source "$VENV_DIR/bin/activate"

    # Upgrade pip
    pip install --upgrade pip

    # Install/update requirements
    print_status "Installing/updating dependencies..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        print_warning "requirements.txt not found, installing basic dependencies..."
        pip install pyrogram TgCrypto aiohttp requests python-dotenv
    fi

    print_status "Virtual environment ready!"
}

# Function to check system dependencies
check_system_deps() {
    print_step "Checking system dependencies..."

    local missing_deps=()

    # Check for required commands
    for cmd in aria2c qbittorrent-nox sabnzbdplus ffmpeg curl; do
        if ! command_exists "$cmd"; then
            missing_deps+=("$cmd")
        fi
    done

    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing system dependencies: ${missing_deps[*]}"
        echo "Please install them using your package manager:"
        echo "  Ubuntu/Debian: sudo apt install aria2 qbittorrent-nox sabnzbdplus ffmpeg curl"
        echo "  Arch Linux: sudo pacman -S aria2 qbittorrent-nox sabnzbd ffmpeg curl"
        exit 1
    fi

    print_status "All system dependencies found!"
}

# Function to start services
start_services() {
    print_step "Starting download services..."

    # Check if services are already running and stop them first
    if pgrep -f aria2c >/dev/null || pgrep -f qbittorrent-nox >/dev/null || pgrep -f sabnzbdplus >/dev/null; then
        print_warning "Services appear to be already running. Stopping them first..."
        stop_services
        sleep 2
    fi

    # Remove any existing PID file
    rm -f "$SERVICES_PID_FILE"

    # Create SABnzbd config directory if it doesn't exist
    mkdir -p .sabnzbd

    # Start aria2c
    print_status "Starting aria2c..."
    tracker_list=$(curl -Ns https://ngosang.github.io/trackerslist/trackers_all_http.txt | awk '$0' | tr '\n\n' ',')
    aria2c --allow-overwrite=true --auto-file-renaming=true --bt-enable-lpd=true --bt-detach-seed-only=true \
           --bt-remove-unselected-file=true --bt-tracker="[$tracker_list]" --bt-max-peers=0 --enable-rpc=true \
           --rpc-max-request-size=1024M --max-connection-per-server=10 --max-concurrent-downloads=1000 --split=10 \
           --seed-ratio=0 --check-integrity=true --continue=true --daemon=true --disk-cache=40M --force-save=true \
           --min-split-size=10M --follow-torrent=mem --check-certificate=false --optimize-concurrent-downloads=true \
           --http-accept-gzip=true --max-file-not-found=0 --max-tries=20 --peer-id-prefix=-qB4520- --reuse-uri=true \
           --content-disposition-default-utf8=true --user-agent=Wget/1.12 --peer-agent=qBittorrent/4.5.2 --quiet=true \
           --summary-interval=0 --max-upload-limit=1K &
    echo $! >> "$SERVICES_PID_FILE"

    # Start qbittorrent-nox
    print_status "Starting qBittorrent..."
    mkdir -p .qbittorrent/config
    qbittorrent-nox -d --profile="$(pwd)/.qbittorrent" &
    echo $! >> "$SERVICES_PID_FILE"

    # Start SABnzbd
    print_status "Starting SABnzbd..."
    sabnzbdplus -f .sabnzbd/SABnzbd.ini -s :::8070 -b 0 -d -c -l 0 --console &
    echo $! >> "$SERVICES_PID_FILE"

    # Wait a moment for services to start
    sleep 3

    print_status "All services started!"
}

# Function to stop services
stop_services() {
    print_step "Stopping download services..."

    # Stop the bot first
    if [ -f ".bot.pid" ]; then
        BOT_PID=$(cat .bot.pid)
        if kill -0 "$BOT_PID" 2>/dev/null; then
            print_status "Stopping bot (PID: $BOT_PID)..."
            kill "$BOT_PID" 2>/dev/null || true
        fi
        rm -f .bot.pid
    fi

    # Stop services tracked in PID file
    if [ -f "$SERVICES_PID_FILE" ]; then
        while read -r pid; do
            if kill -0 "$pid" 2>/dev/null; then
                print_status "Stopping process $pid..."
                kill "$pid" 2>/dev/null || true
            fi
        done < "$SERVICES_PID_FILE"
        rm -f "$SERVICES_PID_FILE"
    fi

    # Force kill any remaining processes with sudo
    print_status "Force stopping any remaining services..."
    sudo killall -9 aria2c qbittorrent-nox sabnzbdplus python3 2>/dev/null || true
    sudo pkill -9 -f "python3 -m bot" 2>/dev/null || true

    print_status "Services stopped!"
}

# Function to run the bot
run_bot() {
    print_step "Starting Telegram bot..."

    # Activate virtual environment
    source "$VENV_DIR/bin/activate"

    # Optional update
    if [ "$UPDATE_FIRST" = true ]; then
        print_status "Running update.py..."
        python3 update.py || print_warning "Update failed, continuing..."
    fi

    # Run the bot in background
    print_status "Bot is starting... Running in background."
    nohup python3 -m bot > .bot.log 2>&1 &
    BOT_PID=$!
    echo $BOT_PID > .bot.pid
    print_status "Bot started with PID: $BOT_PID"
}

# Function to cleanup on exit
cleanup() {
    print_status "Shutting down..."
    stop_services
    print_status "Goodbye!"
    exit 0
}

# Function to show usage
show_usage() {
    echo "MLTB Bot Start Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --start          Start the bot (default)"
    echo "  --stop           Stop running services"
    echo "  --restart        Restart the bot and services"
    echo "  --update         Run update.py before starting bot"
    echo "  --clean          Clean generated files before starting"
    echo "  --help           Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0              # Start the bot"
    echo "  $0 --update     # Update and start the bot"
    echo "  $0 --clean      # Clean files and start the bot"
    echo "  $0 --stop       # Stop all services"
}

# Parse command line arguments
UPDATE_FIRST=false
CLEAN_FIRST=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --start)
            ACTION="start"
            shift
            ;;
        --stop)
            ACTION="stop"
            shift
            ;;
        --restart)
            ACTION="restart"
            shift
            ;;
        --update)
            UPDATE_FIRST=true
            shift
            ;;
        --clean)
            CLEAN_FIRST=true
            shift
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Default action is start
ACTION=${ACTION:-start}

# Change to script directory
cd "$SCRIPT_DIR"

# Handle different actions
case $ACTION in
    start)
        print_status "🚀 Starting MLTB Telegram Bot..."

        # Set up cleanup on exit
        trap cleanup SIGINT SIGTERM

        # Run pre-start checks
        check_config
        check_system_deps

        if [ "$CLEAN_FIRST" = true ]; then
            print_step "Cleaning generated files..."
            ./cleanup.sh || print_warning "Cleanup failed, continuing..."
        fi

        setup_venv
        start_services
        run_bot
        ;;

    stop)
        stop_services
        ;;

    restart)
        print_status "🔄 Restarting MLTB Telegram Bot..."
        stop_services
        sleep 2
        exec "$0" --start
        ;;
esac