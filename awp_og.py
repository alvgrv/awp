#!/usr/bin/env python3

import argparse
import configparser
import os
import sys
from difflib import get_close_matches


def activate_profile(profile):
    sys.stdout.write(f'export AWS_PROFILE="{profile}"')
    sys.stdout.flush()
    sys.exit()


firm_key_map = {
    "t000001": "testres1",
    "t000002": "testres2",
    "t100580": "essentiademo",
    "f000000": "testres0",
    "f100030": "artemis",
    "f100060": "brown",
    "f100340": "nnip",
    "f100360": "bellrock",
    "f100420": "morganst",
    "f100440": "trs",
    "f100470": "amiral",
    "f100530": "ab",
    "f100560": "aperture",
    "f100570": "carmignac",
    "f100580": "essentiademo",
    "f100590": "iridian",
    "f100600": "janush",
    "f100630": "voya",
    "f100640": "invesco",
    "f100670": "cdpq2020",
    "f100680": "artisan",
    "f100690": "pzena",
    "f100700": "baird",
    "f100720": "deka",
    "f100730": "thunderbird",
    "f100740": "hca",
    "f100750": "adams",
    "f100760": "hermes2021",
    "f100770": "dws",
    "f100780": "blacksheep",
    "f100790": "kadensa",
    "f100800": "odey",
    "f100810": "wheb",
    "f100820": "g2",
    "f100830": "viewforth2021",
    "f100840": "evergreen",
    "f100850": "pm",
    "f100860": "amundi",
    "f100870": "brookfield",
    "f100880": "massave",
    "f100890": "2xideas",
    "f100900": "fam",
}
key_firm_map = {v: k for k, v in firm_key_map.items()}
firm_keys = list(key_firm_map.keys())
firm_ids = list(firm_key_map.keys())

cp = configparser.ConfigParser()
user = os.environ["ESSENTIA_USERNAME"].split(".")[0].replace("_", ".")
# cp.read(f"/Users/{user}/.aws/config")
cp.read(
    os.path.expanduser(
        "~/essentia/machine-build/roles/dev_machine/files/dotfiles/aws/config"
    )
)

profiles = [p.split(" ")[1].lower() for p in cp.sections() if p.startswith("profile")]
admin_profiles = [p for p in profiles if "admin" in p]
profiles = [p for p in profiles if "admin" not in p]

FIRM_SEARCHTERMS = ["cust", "customer", "client", "firm"]
FIRM_KEYS_AND_NAMES = firm_keys + firm_ids
ONE_WORD_SEARCHES = [
    "shared",
    "primary",
    "legacy",
    "log",
    "security",
] + FIRM_KEYS_AND_NAMES

parser = argparse.ArgumentParser(description="Switch AWS profiles like a pro")
parser.add_argument("keywords", nargs="*", help="Key word(s) in the profile name")
args = parser.parse_args()
keywords = [k.lower() for k in args.keywords]

if "admin" in keywords:
    keywords.remove("admin")
    profiles = admin_profiles

# if "web" in keywords:
#     keywords.remove("admin")
#     # TODO print web login

if len(keywords) == 1:
    keyword = keywords[0]

    if keyword in firm_keys:
        keyword = key_firm_map[keyword]

    if keyword in ONE_WORD_SEARCHES:
        activate_profile([p for p in profiles if keyword in p][0])
    else:
        print(f"echo 'Error - Too few keywords used'")
        sys.exit()  # todo parser.exit


# if firm search
if any(k in FIRM_SEARCHTERMS for k in keywords):
    keywords = [k for k in keywords if k not in FIRM_SEARCHTERMS]
    activate_profile([p for p in profiles if any(k in p for k in keywords)][0])


# if app search
elif "app" in keywords:
    keywords.remove("app")
    activate_profile([p for p in profiles if any(k in p for k in keywords)][0])
elif "res" in keywords:
    keywords.remove("res")
    activate_profile([p for p in profiles if any(k in p for k in keywords)][0])
else:
    print("echo 'Error - No result found for your keywords'")
