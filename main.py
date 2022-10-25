import argparse


parser = argparse.ArgumentParser(
    description="Switch AWS profiles as easy as we switch prime ministers"
)
parser.add_argument("profile_type", help="Type of profile: legacy, app or firm")
parser.add_argument("profile_id", help="Profile name")
# parser.add_argument("--admin", help="Select admin profile where available")
