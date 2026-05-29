"""
Homey Configuration - TEMPLATE

Copy this file to config.py and fill in your values:

    cp config.example.py config.py        # macOS / Linux
    copy config.example.py config.py      # Windows

config.py is git-ignored so your secrets never get committed.

You can also leave HOMEY_API_KEY empty here and provide it via the
HOMEY_API_KEY environment variable instead (see the fallback below).
"""
import os

# Local IP address of your Homey (find it in the Homey app -> Settings -> General,
# or in your router's DHCP client list).
HOMEY_IP = "192.168.1.x"

# Generate from: https://my.homey.app -> Settings -> API Keys -> New API Key
# Leave as "" to use the HOMEY_API_KEY environment variable instead.
HOMEY_API_KEY = ""

# Fallback: read the key from an environment variable if not set above.
if not HOMEY_API_KEY:
    HOMEY_API_KEY = os.environ.get("HOMEY_API_KEY", "")
