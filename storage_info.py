#!/usr/bin/env python3
"""
Android Termux Storage Information Script
Shows total storage size, used space, and available space in GB
"""

import os
import shutil
import subprocess
import sys

def bytes_to_gb(bytes_value):
    """Convert bytes to GB with 2 decimal places"""
    return round(bytes_value / (1024**3), 2)

def get_storage_info():
    """Get storage information for the current filesystem"""
    try:
        # Get storage info for the current directory (usually /data/data/com.termux/files/home)
        statvfs = os.statvfs('.')
        
        # Calculate storage values
        total_bytes = statvfs.f_frsize * statvfs.f_blocks
        available_bytes = statvfs.f_frsize * statvfs.f_bavail
        used_bytes = total_bytes - available_bytes
        
        return {
            'total': bytes_to_gb(total_bytes),
            'used': bytes_to_gb(used_bytes),
            'available': bytes_to_gb(available_bytes),
            'used_percent': round((used_bytes / total_bytes) * 100, 1) if total_bytes > 0 else 0
        }
    except Exception as e:
        print(f"Error getting storage info: {e}")
        return None

def get_termux_storage_info():
    """Get Termux-specific storage information"""
    try:
        # Try to get info about Termux's data directory
        termux_home = os.path.expanduser('~')
        statvfs = os.statvfs(termux_home)
        
        total_bytes = statvfs.f_frsize * statvfs.f_blocks
        available_bytes = statvfs.f_frsize * statvfs.f_bavail
        used_bytes = total_bytes - available_bytes
        
        return {
            'total': bytes_to_gb(total_bytes),
            'used': bytes_to_gb(used_bytes),
            'available': bytes_to_gb(available_bytes),
            'used_percent': round((used_bytes / total_bytes) * 100, 1) if total_bytes > 0 else 0
        }
    except Exception as e:
        print(f"Error getting Termux storage info: {e}")
        return None

def get_external_storage_info():
    """Get external storage information if available"""
    external_paths = [
        '/sdcard',
        '/storage/emulated/0',
        '/storage/self/primary'
    ]
    
    for path in external_paths:
        if os.path.exists(path) and os.access(path, os.R_OK):
            try:
                statvfs = os.statvfs(path)
                total_bytes = statvfs.f_frsize * statvfs.f_blocks
                available_bytes = statvfs.f_frsize * statvfs.f_bavail
                used_bytes = total_bytes - available_bytes
                
                return {
                    'path': path,
                    'total': bytes_to_gb(total_bytes),
                    'used': bytes_to_gb(used_bytes),
                    'available': bytes_to_gb(available_bytes),
                    'used_percent': round((used_bytes / total_bytes) * 100, 1) if total_bytes > 0 else 0
                }
            except Exception:
                continue
    
    return None

def print_storage_bar(used_percent, width=30):
    """Print a visual storage usage bar"""
    filled = int(width * used_percent / 100)
    bar = '█' * filled + '░' * (width - filled)
    return f"[{bar}] {used_percent}%"

def main():
    print("=" * 50)
    print("📱 Android Termux Storage Information")
    print("=" * 50)
    
    # Get Termux internal storage info
    print("\n🏠 Termux Internal Storage:")
    termux_info = get_termux_storage_info()
    if termux_info:
        print(f"  Total Size:    {termux_info['total']:>8.2f} GB")
        print(f"  Used Space:    {termux_info['used']:>8.2f} GB")
        print(f"  Available:     {termux_info['available']:>8.2f} GB")
        print(f"  Usage:         {print_storage_bar(termux_info['used_percent'])}")
    else:
        print("  ❌ Unable to get Termux storage information")
    
    # Get external storage info
    print("\n💾 External Storage (SD Card):")
    external_info = get_external_storage_info()
    if external_info:
        print(f"  Path:          {external_info['path']}")
        print(f"  Total Size:    {external_info['total']:>8.2f} GB")
        print(f"  Used Space:    {external_info['used']:>8.2f} GB")
        print(f"  Available:     {external_info['available']:>8.2f} GB")
        print(f"  Usage:         {print_storage_bar(external_info['used_percent'])}")
    else:
        print("  ❌ External storage not accessible or not found")
    
    # Additional info using df command if available
    print("\n📊 Detailed Filesystem Information:")
    try:
        result = subprocess.run(['df', '-h'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            print("  " + lines[0])  # Header
            for line in lines[1:]:
                if any(path in line for path in ['/data', '/storage', '/sdcard']):
                    print("  " + line)
        else:
            print("  ❌ df command not available")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("  ❌ df command not available or timed out")
    
    print("\n" + "=" * 50)
    print("ℹ️  Note: Storage information may vary depending on Android version and device configuration")
    print("=" * 50)

if __name__ == "__main__":
    main()