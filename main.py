import argparse
import configparser
import os
from difflib import get_close_matches

cp = configparser.ConfigParser()
user = os.environ["ESSENTIA_USERNAME"].split(".")[0].replace("_", ".")
# cp.read(f"/Users/{user}/.aws/config")
cp.read(
    f"/Users/{user}/essentia/machine-build/roles/dev_machine/files/dotfiles/aws/config"
)

profiles = [p.split(" ")[1].lower() for p in cp.sections() if p.startswith("profile")]

profiles = [
    {
        "id": p,
        "admin_id": p + "_admin",
        "type": "firm"
        if "cust" in p
        else "legacy"
        if "legacy" in p
        else "res"
        if "res" in p
        else "app",
    }
    for p in profiles
    if "admin" not in p
]

# keywords in profile names
APP_KEYWORDS = ["app", "shared", "primary", "log", "security"]
RES_KEYWORDS = ["res"]
FIRM_KEYWORDS = ["cust"]
LEGACY_KEYWORDS = ["legacy"]
# keywords in user input
FIRM_SEARCHTERMS = ["cust", "customer", "client", "firm"]

parser = argparse.ArgumentParser(description="Switch AWS profiles like a pro")
parser.add_argument("type", help="Type of profile: app, firm or legacy")
parser.add_argument("keywords", nargs="*", help="Key word(s) in the profile name")
args = parser.parse_args()
if args.type in FIRM_SEARCHTERMS:
    args.type = "firm"
possible_profiles = [p for p in profiles if p["type"] == args.type]
input_keywords = args.keywords
possible_profiles = [
    p for p in possible_profiles if any(k in p["id"] for k in input_keywords)
]

print(possible_profiles[0]["id"])
