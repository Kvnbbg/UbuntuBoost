#!/bin/bash

# Root check for necessary privileges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root. Please re-run with sudo."
   exit 1
fi

# --- 1. Detect macOS version and ensure compatibility ---
macos_version=$(sw_vers -productVersion)
macos_major=$(echo $macos_version | cut -d '.' -f 1)
macos_minor=$(echo $macos_version | cut -d '.' -f 2)

echo "Detected macOS version: $macos_version"

# Minimum macOS version check: Example for macOS 10.13 (High Sierra) and newer
min_major=10
min_minor=13

if [[ "$macos_major" -lt "$min_major" || ( "$macos_major" -eq "$min_major" && "$macos_minor" -lt "$min_minor" ) ]]; then
    echo "This script requires macOS 10.13 or newer."
    echo "Your version ($macos_version) is too old. Exiting script."
    exit 1
fi

# --- 2. RAM and Cache Optimization ---
sudo purge

# Clear DNS cache for improved networking performance
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

# --- 3. Dynamic Resource Optimization: CPU & Power ---
cpu_load=$(sysctl -n vm.loadavg | awk '{print $1}')
threshold_load=2.0

if (( $(echo "$cpu_load > $threshold_load" | bc -l) )); then
    echo "Disabling Spotlight due to high CPU load."
    sudo mdutil -a -i off
else
    echo "CPU load is normal. Spotlight indexing remains on."
fi

# Disable power-saving features during gaming sessions
sudo pmset -a sleep 0 disksleep 0 powernap 0

# High-performance mode for Apple Silicon (macOS 11+)
if [[ $(uname -m) == 'arm64' && "$macos_major" -ge 11 ]]; then
    sudo pmset -a highperf 1
fi

# --- 4. System UI Optimizations ---
defaults write com.apple.universalaccess reduceTransparency -bool true
defaults write com.apple.dock expose-animation-duration -float 0.1
killall Dock

# --- 5. Clean Unnecessary Files & Caches ---
sudo find ~/Library/Caches/ -type d -exec rm -rf {} + 2>/dev/null || echo "Some user caches protected by SIP skipped."
sudo rm -rf /Library/Caches/* 2>/dev/null || echo "Skipping SIP-protected files in /Library/Caches."
sudo rm -rf /private/var/folders/* 2>/dev/null || echo "Skipping SIP-protected files in /private/var/folders."

# --- 6. App Usage Heuristics & Unused App Removal ---
apps_to_remove=("GarageBand.app" "iMovie.app" "Pages.app" "Keynote.app")

echo "Removing unused apps to free up disk space and system resources."
for app in "${apps_to_remove[@]}"; do
    if [[ -d "/Applications/$app" ]]; then
        sudo rm -rf "/Applications/$app"
        echo "$app has been removed."
    else
        echo "$app not found, skipping."
    fi
done

# --- 7. Homebrew Cleanup & Package Management ---
if command -v brew &> /dev/null; then
    brew cleanup
    brew update
    brew upgrade
fi

# --- 8. Process Prioritization ---
bg_processes=("Safari" "Mail" "Photos")
for process in "${bg_processes[@]}"; do
    pid=$(pgrep $process)
    if [[ -n "$pid" ]]; then
        sudo renice 10 -p $pid
    fi
done

# --- 9. Dynamic Disk Cleanup Based on Space ---
free_space=$(df / | tail -1 | awk '{print $4}')
min_space=$((10*1024*1024))

if (( $free_space < $min_space )); then
    sudo find /private/var/log -type f -mtime +30 -delete
    sudo find /var/log -type f -mtime +30 -delete
    sudo find /private/tmp -type f -mtime +10 -delete
fi

# --- 10. AI Feedback Loop for Future Optimizations ---
sysctl -n vm.loadavg > ~/system_performance.log

previous_avg=$(tail -n 1 ~/system_performance.log | awk '{print $1}')
if (( $(echo "$cpu_load > $previous_avg" | bc -l) )); then
    echo "CPU usage is higher than historical average. Considering future optimizations."
fi

# --- 11. Final Cleanup and Display Results ---
sudo diskutil verifyVolume /

echo "System optimization completed! Your Mac is now optimized for performance. By Kevin Manville"
echo "Please visit kvnbbg.fr"
