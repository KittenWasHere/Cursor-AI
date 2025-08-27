#!/usr/bin/env python3
"""
Simple Python script to open Google in the default browser.
Designed for use in Termux on Android.
"""

import webbrowser
import sys

def open_google():
    """Open Google in the default browser."""
    url = "https://www.google.com"
    
    try:
        print(f"Opening {url} in your default browser...")
        webbrowser.open(url)
        print("Success! Google should now be opening in your browser.")
    except Exception as e:
        print(f"Error opening browser: {e}")
        print("Make sure you have a browser installed on your device.")
        sys.exit(1)

if __name__ == "__main__":
    open_google()