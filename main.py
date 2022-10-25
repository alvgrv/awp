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
        "type": "firm"
        if "cust" in p
        else "legacy"
        if "legacy" in p
        else "res"
        if "res" in p
        else "app",
        "admin": True if "admin" in p else False,
    }
    for p in profiles
]
admin_profiles = [p for p in profiles if p["admin"]]


# keywords in profile names
ONE_WORD_SEARCHES = ["shared", "primary", "legacy", "log", "security"]
# keywords in user input
FIRM_SEARCHTERMS = ["cust", "customer", "client", "firm"]
FIRM_MAP = {}

parser = argparse.ArgumentParser(description="Switch AWS profiles like a pro")
parser.add_argument("keywords", nargs="*", help="Key word(s) in the profile name")
args = parser.parse_args()
keywords = args.keywords

if "admin" in keywords:
    keywords.remove("admin")
    profiles = admin_profiles

if len(keywords) == 1 and keywords[0] in ONE_WORD_SEARCHES:
    print([p["id"] for p in profiles if keywords[0] in p["id"]])


# if firm search
if any(k in FIRM_SEARCHTERMS for k in keywords):
    keywords = [k for k in keywords if k not in FIRM_SEARCHTERMS]
    print([p["id"] for p in profiles if any(k in p["id"] for k in keywords)][0])
# if app search
elif "app" in keywords:
    keywords.remove("app")
    print([p["id"] for p in profiles if any(k in p["id"] for k in keywords)][0])
elif "res" in keywords:
    keywords.remove("res")
    print([p["id"] for p in profiles if any(k in p["id"] for k in keywords)][0])

#
# if args.type in FIRM_SEARCHTERMS:
#     args.type = "firm"
# possible_profiles = [p for p in profiles if p["type"] == args.type]
# input_keywords = args.keywords
# possible_profiles = [
#     p for p in possible_profiles if any(k in p["id"] for k in input_keywords)
# ]
#
# print(possible_profiles[0]["id"])


# next
# add firm key to name map
# add admin stuff
# shared isn't a one word search with admin in there
