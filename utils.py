#!/usr/bin/env python3
"""
MLTB Utilities - Consolidated utility script for common tasks
Usage: python3 utils.py <command> [options]
"""

import argparse
import os
import sys
import subprocess
import time
import signal
from pathlib import Path

def setup_logging():
    """Setup basic logging for utilities"""
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def setup_logging():
    """Setup basic logging for utilities"""
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def generate_session_string():
    """Generate Pyrogram session string for user account"""
    try:
        from pyrogram import Client
    except ImportError as e:
        print(f"Error: {e}")
        print("Install pyrogram: pip3 install pyrogram")
        return

    print("Required pyrogram V2 or greater.")
    try:
        API_KEY = int(input("Enter API KEY: "))
        API_HASH = input("Enter API HASH: ")
        with Client(name="USS", api_id=API_KEY, api_hash=API_HASH, in_memory=True) as app:
            session_string = app.export_session_string()
            print("\nYour session string:")
            print(session_string)
            print("\nAdd this to your config.py as USER_SESSION_STRING")
    except ValueError:
        print("Invalid API KEY. Must be a number.")
    except Exception as e:
        print(f"Error generating session string: {e}")

def run_application():
    """Run the MLTB application (equivalent to ./run.sh)"""
    print("🚀 Starting MLTB Telegram Bot...")

    # Check if already running
    if check_application_status()["bot"]:
        print("❌ Application is already running!")
        print("Use 'python3 utils.py stop' to stop it first.")
        return False

    try:
        # Run the complete startup process
        return run_application_complete()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return False

def run_application_complete():
    """Complete application startup process (replaces run.sh functionality)"""
    try:
        # Step 1: Check configuration
        if not check_config_for_run():
            return False

        # Step 2: Check system dependencies
        if not check_system_dependencies():
            return False

        # Step 3: Setup  environment and install dependencies
        if not setup_python_environment():
            return False

        # Step 4: Start services
        if not start_download_services():
            return False

        # Step 5: Start the bot
        if not start_bot_process():
            return False

        print("✅ Application started successfully!")
        print("Use 'python3 utils.py status' to check status.")
        return True

    except Exception as e:
        print(f"❌ Startup failed: {e}")
        return False

def check_config_for_run():
    """Check if config.py is properly configured for running"""
    print("📋 Checking configuration...")

    if not os.path.exists("config.py"):
        print("❌ config.py not found!")
        print("Run: cp config_sample.py config.py")
        return False

    config_path = Path("config.py")
    content = config_path.read_text()

    checks = [
        ("BOT_TOKEN", lambda x: x.strip() == '""' or len(x.strip()) < 20, "Bot token not configured or too short"),
        ("OWNER_ID", lambda x: x.strip() == "0" or x.strip() == "", "Owner ID not configured"),
        ("TELEGRAM_API", lambda x: x.strip() == "0" or x.strip() == "", "Telegram API ID not configured"),
        ("TELEGRAM_HASH", lambda x: x.strip() == '""' or len(x.strip()) < 10, "Telegram API hash not configured or too short"),
    ]

    all_good = True
    for field, validator, message in checks:
        # Extract the value for this field
        import re
        pattern = rf'{field}\s*=\s*(.+?)(?:\s*#|$)'
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            value = match.group(1).strip()
            if validator(value):
                print(f"❌ {message}")
                all_good = False
        else:
            print(f"❌ {field} not found in config.py")
            all_good = False

    if all_good:
        print("✅ Configuration looks good!")
        return True
    else:
        print("\nEdit config.py to configure the missing fields.")
        return False

def check_system_dependencies():
    """Check if all required system dependencies are installed"""
    print("🔧 Checking system dependencies...")

    required_deps = ["aria2c", "qbittorrent-nox", "sabnzbdplus", "ffmpeg", "curl"]
    missing_deps = []

    for dep in required_deps:
        try:
            result = subprocess.run(["which", dep], capture_output=True, text=True)
            if result.returncode != 0:
                missing_deps.append(dep)
        except Exception:
            missing_deps.append(dep)

    if missing_deps:
        print(f"❌ Missing system dependencies: {', '.join(missing_deps)}")
        print("Install them using your package manager:")
        print("  Ubuntu/Debian: sudo apt install aria2 qbittorrent-nox sabnzbdplus ffmpeg curl")
        print("  Arch Linux: sudo pacman -S aria2 qbittorrent-nox sabnzbd ffmpeg curl")
        return False

    print("✅ All system dependencies found!")
    return True

def setup_python_environment():
    """Setup Python  environment and install dependencies"""
    print("🐍 Setting up Python  environment...")

    # venv_dir = "mltbenv"

    # Create  environment if it doesn't exist
    # if not os.path.exists(venv_dir):
    #     print("📦 Creating  environment...")
    #     try:
    #         result = subprocess.run(["python3", "-m", "venv", venv_dir],
    #                               capture_output=True, text=True)
    #         if result.returncode != 0:
    #             print(f"❌ Failed to create  environment: {result.stderr}")
    #             return False
    #     except Exception as e:
    #         print(f"❌ Error creating  environment: {e}")
    #         return False
    # else:
    #     print("📦  environment already exists.")

    # Activate environment and install dependencies
    pip_cmd = "pip"

    try:
        # Upgrade pip
        result = subprocess.run([pip_cmd, "install", "--upgrade", "pip"],
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️  Warning: Failed to upgrade pip: {result.stderr}")

        # Install requirements
        print("📥 Installing/updating dependencies...")
        if os.path.exists("requirements.txt"):
            result = subprocess.run(["sudo apt", "install", "-r", "requirements.txt"],
                                  capture_output=True, text=True)
        else:
            print("⚠️  requirements.txt not found, installing basic dependencies...")
            result = subprocess.run([pip_cmd, "install", "pyrogram", "TgCrypto", "aiohttp", "requests"],
                                  capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False

        print("✅  environment ready!")
        return True

    except Exception as e:
        print(f"❌ Error setting up environment: {e}")
        return False

def start_download_services():
    """Start all download services (aria2c, qbittorrent, sabnzbd)"""
    print("🔄 Starting download services...")

    # Check if services are already running and stop them first
    status = check_application_status()
    if status["services"]:
        print("⚠️  Services appear to be already running. Stopping them first...")
        stop_application()
        time.sleep(2)

    # Remove any existing PID file
    services_pid_file = ".services.pid"
    if os.path.exists(services_pid_file):
        os.remove(services_pid_file)

    pids = []

    try:
        # Create SABnzbd config directory
        os.makedirs(".sabnzbd", exist_ok=True)

        # Start aria2c
        print("📥 Starting aria2c...")
        try:
            # Get tracker list
            result = subprocess.run(["curl", "-Ns", "https://ngosang.github.io/trackerslist/trackers_all_http.txt"],
                                  capture_output=True, text=True, timeout=10)
            tracker_list = result.stdout.replace('\n\n', ',') if result.returncode == 0 else ""

            aria2c_cmd = [
                "aria2c",
                "--allow-overwrite=true", "--auto-file-renaming=true", "--bt-enable-lpd=true",
                "--bt-detach-seed-only=true", "--bt-remove-unselected-file=true",
                f"--bt-tracker=[{tracker_list}]", "--bt-max-peers=0", "--enable-rpc=true",
                "--rpc-max-request-size=1024M", "--max-connection-per-server=10",
                "--max-concurrent-downloads=1000", "--split=10", "--seed-ratio=0",
                "--check-integrity=true", "--continue=true", "--daemon=true",
                "--disk-cache=40M", "--force-save=true", "--min-split-size=10M",
                "--follow-torrent=mem", "--check-certificate=false",
                "--optimize-concurrent-downloads=true", "--http-accept-gzip=true",
                "--max-file-not-found=0", "--max-tries=20", "--peer-id-prefix=-qB4520-",
                "--reuse-uri=true", "--content-disposition-default-utf8=true",
                "--user-agent=Wget/1.12", "--peer-agent=qBittorrent/4.5.2",
                "--quiet=true", "--summary-interval=0", "--max-upload-limit=1K"
            ]

            process = subprocess.Popen(aria2c_cmd)
            pids.append(process.pid)

        except Exception as e:
            print(f"⚠️  Warning: Failed to start aria2c: {e}")

        # Start qbittorrent-nox
        print("🧲 Starting qBittorrent...")
        try:
            os.makedirs(".qbittorrent/config", exist_ok=True)
            qb_cmd = ["qbittorrent-nox", "-d", f"--profile={os.getcwd()}/.qbittorrent"]
            process = subprocess.Popen(qb_cmd)
            pids.append(process.pid)
        except Exception as e:
            print(f"⚠️  Warning: Failed to start qBittorrent: {e}")

        # Start SABnzbd
        print("📰 Starting SABnzbd...")
        try:
            sab_cmd = ["sabnzbdplus", "-f", ".sabnzbd/SABnzbd.ini", "-s", ":::8070",
                      "-b", "0", "-d", "-c", "-l", "0", "--console"]
            process = subprocess.Popen(sab_cmd)
            pids.append(process.pid)
        except Exception as e:
            print(f"⚠️  Warning: Failed to start SABnzbd: {e}")

        # Save PIDs to file
        with open(services_pid_file, "w") as f:
            for pid in pids:
                f.write(f"{pid}\n")

        # Wait a moment for services to start
        time.sleep(3)

        print("✅ All services started!")
        return True

    except Exception as e:
        print(f"❌ Error starting services: {e}")
        return False

def start_bot_process():
    """Start the Telegram bot in background"""
    print("🤖 Starting Telegram bot...")

    try:
        # Check if  environment exists
        venv_python = os.path.join("mltbenv", "bin", "python3")
        if not os.path.exists(venv_python):
            print("❌  environment not found!")
            return False

        # Optional update
        if "--update" in sys.argv:
            print("🔄 Running update.py...")
            try:
                result = subprocess.run([venv_python, "update.py"],
                                      capture_output=True, text=True, timeout=60)
                if result.returncode != 0:
                    print(f"⚠️  Warning: Update failed: {result.stderr}")
            except Exception as e:
                print(f"⚠️  Warning: Update error: {e}")

        # Start bot in background
        print("🚀 Bot is starting... Running in background.")
        with open(".bot.log", "a") as log_file:
            process = subprocess.Popen(
                [venv_python, "-m", "bot"],
                stdout=log_file,
                stderr=log_file,
                preexec_fn=os.setsid
            )

        bot_pid = process.pid

        # Save bot PID
        with open(".bot.pid", "w") as f:
            f.write(str(bot_pid))

        print(f"✅ Bot started with PID: {bot_pid}")
        return True

    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        return False

def stop_application():
    """Stop the MLTB application"""
    print("🛑 Stopping MLTB Telegram Bot...")

    try:
        # Run the stop command
        result = subprocess.run(["./run.sh", "--stop"], capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            print("✅ Application stopped successfully!")
            return True
        else:
            print("❌ Failed to stop application!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("⚠️  Stop command timed out.")
        return False
    except FileNotFoundError:
        print("❌ run.sh script not found!")
        return False
    except Exception as e:
        print(f"❌ Error stopping application: {e}")
        return False

def check_application_status():
    """Check if the MLTB application is running"""
    status = {"bot": False, "services": False, "bot_pid": None, "services_count": 0}

    # First check for PID files (indicates processes started by this session)
    if os.path.exists(".bot.pid"):
        try:
            with open(".bot.pid", "r") as f:
                bot_pid = int(f.read().strip())
            # Verify the process is still running and owned by current user
            result = subprocess.run(["ps", "-p", str(bot_pid), "-o", "pid,user"],
                                  capture_output=True, text=True)
            if result.returncode == 0 and str(bot_pid) in result.stdout:
                status["bot"] = True
                status["bot_pid"] = bot_pid
        except (ValueError, FileNotFoundError):
            # PID file exists but process is not running
            os.remove(".bot.pid")

    if os.path.exists(".services.pid"):
        try:
            with open(".services.pid", "r") as f:
                service_pids = [int(pid.strip()) for pid in f.readlines() if pid.strip()]
            running_services = 0
            for pid in service_pids:
                result = subprocess.run(["ps", "-p", str(pid), "-o", "pid"],
                                      capture_output=True, text=True)
                if result.returncode == 0 and str(pid) in result.stdout:
                    running_services += 1
            status["services"] = running_services > 0
            status["services_count"] = running_services
        except (ValueError, FileNotFoundError):
            # Services PID file exists but processes are not running
            os.remove(".services.pid")

    # If no PID files found, check for any running processes (fallback)
    if not status["bot"]:
        try:
            # Check for bot processes owned by current user
            result = subprocess.run(["pgrep", "-u", str(os.getuid()), "-f", "python3 -m bot"],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                status["bot"] = True
                status["bot_pid"] = int(result.stdout.strip().split('\n')[0])
        except Exception:
            pass

    if not status["services"]:
        # Check for services owned by current user
        services_running = 0
        services = ["aria2c", "qbittorrent-nox", "sabnzbdplus"]

        for service in services:
            try:
                result = subprocess.run(["pgrep", "-u", str(os.getuid()), "-f", service],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    services_running += 1
            except Exception:
                pass

        status["services"] = services_running > 0
        status["services_count"] = services_running

    return status

def show_application_status():
    """Display detailed application status"""
    print("📊 MLTB Application Status")
    print("=" * 40)

    status = check_application_status()

    # Bot status
    if status["bot"]:
        print(f"🤖 Bot:      ✅ Running (PID: {status.get('bot_pid', 'Unknown')})")
    else:
        print("🤖 Bot:      ❌ Not running")

    # Services status
    if status["services"]:
        print(f"🔧 Services: ✅ {status['services_count']} running")
    else:
        print("🔧 Services: ❌ None running")

    # Overall status
    if status["bot"] and status["services"]:
        print("\n🎉 Overall:  ✅ All systems operational")
        return True
    elif status["bot"] or status["services"]:
        print("\n⚠️  Overall:  ⚠️  Partial operation")
        return True
    else:
        print("\n❌ Overall:  ❌ Application not running")
        return False

def restart_application():
    """Restart the MLTB application"""
    print("🔄 Restarting MLTB Telegram Bot...")

    # Stop first
    if not stop_application():
        print("❌ Failed to stop application for restart")
        return False

    # Wait a moment
    print("⏳ Waiting for clean shutdown...")
    time.sleep(3)

    # Start again
    if run_application():
        print("✅ Application restarted successfully!")
        return True
    else:
        print("❌ Failed to restart application")
        return False

def monitor_application(duration=60):
    """Monitor application health for specified duration (seconds)"""
    print(f"📈 Monitoring application for {duration} seconds...")
    print("Press Ctrl+C to stop monitoring")

    start_time = time.time()
    checks = 0

    try:
        while time.time() - start_time < duration:
            checks += 1
            status = check_application_status()

            if not status["bot"]:
                print(f"⚠️  WARNING: Bot not running at check #{checks}")
            if not status["services"]:
                print(f"⚠️  WARNING: No services running at check #{checks}")

            time.sleep(5)  # Check every 5 seconds

        print(f"✅ Monitoring complete after {checks} checks")

    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")
    except Exception as e:
        print(f"❌ Monitoring error: {e}")

def cleanup_application():
    """Clean up application files and temporary data"""
    print("🧹 Cleaning up application...")

    cleanup_files = [
        ".services.pid",
        ".bot.pid",
        ".bot.log",
        "nohup.out",
        "*.pyc",
        "__pycache__",
        ".qbittorrent/logs",
        ".sabnzbd/logs"
    ]

    cleaned = 0

    for pattern in cleanup_files:
        try:
            if "*" in pattern:
                # Use find for patterns
                result = subprocess.run(["find", ".", "-name", pattern, "-type", "f", "-delete"],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    cleaned += 1
            else:
                # Direct file removal
                if os.path.exists(pattern):
                    if os.path.isdir(pattern):
                        import shutil
                        shutil.rmtree(pattern)
                    else:
                        os.remove(pattern)
                    cleaned += 1
        except Exception as e:
            print(f"⚠️  Could not clean {pattern}: {e}")

    # Clean empty directories
    try:
        result = subprocess.run(["find", ".", "-type", "d", "-empty", "-delete"],
                              capture_output=True, text=True)
    except Exception:
        pass

    print(f"✅ Cleanup complete! Removed {cleaned} items")

def generate_drive_token():
    """Generate Google Drive token for authentication"""
    try:
        import pickle
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError as e:
        print(f"Error: {e}")
        print("Install required packages: pip3 install google-auth google-auth-oauthlib")
        return

    credentials = None
    token_file = "token.pickle"
    scopes = ["https://www.googleapis.com/auth/drive"]

    if os.path.exists(token_file):
        with open(token_file, "rb") as f:
            credentials = pickle.load(f)
            if (credentials and not credentials.valid and credentials.expired
                and credentials.refresh_token):
                credentials.refresh(Request())

    if not credentials or not credentials.valid:
        if not os.path.exists("credentials.json"):
            print("Error: credentials.json not found!")
            print("Download credentials from Google Cloud Console and place in project root.")
            return

        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes)
        credentials = flow.run_local_server(port=0)

    with open(token_file, "wb") as f:
        pickle.dump(credentials, f)

    print("✅ Google Drive token generated successfully!")
    print(f"Token saved to: {token_file}")

def generate_sa_accounts():
    """Generate Service Account credentials"""
    print("Service Account generation requires specific setup.")
    print("This feature requires the gen_sa_accounts.py file which is not included.")
    print("Please obtain it from the original repository if needed.")

def check_config():
    """Check if config.py is properly configured"""
    if not os.path.exists("config.py"):
        print("❌ config.py not found!")
        print("Run: cp config_sample.py config.py")
        return False

    config_path = Path("config.py")
    content = config_path.read_text()

    checks = [
        ("BOT_TOKEN", '"', "Bot token not configured"),
        ("OWNER_ID", "0", "Owner ID not configured"),
        ("TELEGRAM_API", "0", "Telegram API ID not configured"),
        ("TELEGRAM_HASH", '""', "Telegram API hash not configured"),
    ]

    all_good = True
    for field, default_value, message in checks:
        if f'{field} = {default_value}' in content:
            print(f"❌ {message}")
            all_good = False

    if all_good:
        print("✅ Configuration looks good!")
        return True
    else:
        print("\nEdit config.py to configure the missing fields.")
        return False

def show_help():
    """Show help information"""
    print("MLTB Utilities - Complete application management")
    print()
    print("Usage: python3 utils.py <command>")
    print()
    print("Application Management:")
    print("  run/start   Start the complete MLTB application (replaces ./run.sh)")
    print("  stop        Stop the MLTB application")
    print("  status      Show application status")
    print("  restart     Restart the MLTB application")
    print("  monitor     Monitor application health")
    print("  cleanup     Clean up temporary files")
    print()
    print("Configuration & Setup:")
    print("  session     Generate Pyrogram session string")
    print("  drive-token Generate Google Drive authentication token")
    print("  sa-accounts Generate Service Account credentials")
    print("  check-config Check if config.py is properly configured")
    print("  help        Show this help message")
    print()
    print("Examples:")
    print("  python3 utils.py run         # Start everything")
    print("  python3 utils.py status      # Check status")
    print("  python3 utils.py restart     # Restart application")
    print("  python3 utils.py session     # Generate session string")
    print("  python3 utils.py drive-token # Setup Google Drive")
    print("  python3 utils.py check-config # Validate config")

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    commands = {
        'session': generate_session_string,
        'drive-token': generate_drive_token,
        'sa-accounts': generate_sa_accounts,
        'check-config': check_config_for_run,
        'run': run_application,
        'start': run_application,
        'stop': stop_application,
        'status': show_application_status,
        'restart': restart_application,
        'monitor': monitor_application,
        'cleanup': cleanup_application,
        'help': show_help,
    }

    if command in commands:
        commands[command]()
    else:
        print(f"Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main()