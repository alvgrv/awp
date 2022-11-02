#!/usr/bin/env python3

import argparse
import os
import sys


class AwsProfiles:
    def __init__(self):
        self.username = os.environ["ESSENTIA_USERNAME"].split(".")[0].replace("_", ".")
        self.firm_key_map = {
            "testres1": "t000001",
            "testres2": "t000002",
            "essentiademo": "f100580",
            "testres0": "f000000",
            "artemis": "f100030",
            "brown": "f100060",
            "nnip": "f100340",
            "bellrock": "f100360",
            "morganst": "f100420",
            "trs": "f100440",
            "amiral": "f100470",
            "ab": "f100530",
            "aperture": "f100560",
            "carmignac": "f100570",
            "iridian": "f100590",
            "janush": "f100600",
            "voya": "f100630",
            "invesco": "f100640",
            "cdpq2020": "f100670",
            "artisan": "f100680",
            "pzena": "f100690",
            "baird": "f100700",
            "deka": "f100720",
            "thunderbird": "f100730",
            "hca": "f100740",
            "adams": "f100750",
            "hermes2021": "f100760",
            "dws": "f100770",
            "blacksheep": "f100780",
            "kadensa": "f100790",
            "odey": "f100800",
            "wheb": "f100810",
            "g2": "f100820",
            "viewforth2021": "f100830",
            "evergreen": "f100840",
            "pm": "f100850",
            "amundi": "f100860",
            "brookfield": "f100870",
            "massave": "f100880",
            "2xideas": "f100890",
            "fam": "f100900",
        }
        self.firm_ids = list(self.firm_key_map.values())
        self.firm_keys = list(self.firm_key_map.keys())
        self.all_profiles = [
            "es_legacy",
            "es_legacy_admin",
            "es_lz_main-primary",
            "es_lz_main-primary_admin",
            "es_lz_main-shared-services",
            "es_lz_main-shared-services_admin",
            "es_lz_main-security",
            "es_lz_main-security_admin",
            "es_lz_main-log-archive",
            "es_lz_main-log-archive_admin",
            "es_lz_main-euwest1-live-app",
            "es_lz_main-euwest1-live-app_admin",
            "es_lz_main-euwest1-stag-app",
            "es_lz_main-euwest1-stag-app_admin",
            "es_lz_main-euwest1-test-app",
            "es_lz_main-euwest1-test-app_admin",
            "es_lz_main-euwest1-live-res",
            "es_lz_main-euwest1-live-res_admin",
            "es_lz_main-euwest1-stag-res",
            "es_lz_main-euwest1-stag-res_admin",
            "es_lz_main-euwest1-test-res",
            "es_lz_main-euwest1-test-res_admin",
            "es_lz_main-euwest1-cust-t000001",
            "es_lz_main-euwest1-cust-t000001_admin",
            "es_lz_main-euwest1-cust-t000002",
            "es_lz_main-euwest1-cust-t000002_admin",
            "es_lz_main-euwest1-cust-t100580",
            "es_lz_main-euwest1-cust-t100580_admin",
            "es_lz_main-euwest1-cust-f100060",
            "es_lz_main-euwest1-cust-f100060_admin",
            "es_lz_main-euwest1-cust-f100340",
            "es_lz_main-euwest1-cust-f100340_admin",
            "es_lz_main-euwest1-cust-f100440",
            "es_lz_main-euwest1-cust-f100440_admin",
            "es_lz_main-euwest1-cust-f100560",
            "es_lz_main-euwest1-cust-f100560_admin",
            "es_lz_main-euwest1-cust-f100580",
            "es_lz_main-euwest1-cust-f100580_admin",
            "es_lz_main-euwest1-cust-f100700",
            "es_lz_main-euwest1-cust-f100700_admin",
            "es_lz_main-euwest1-cust-f100720",
            "es_lz_main-euwest1-cust-f100720_admin",
            "es_lz_main-euwest1-cust-f100800",
            "es_lz_main-euwest1-cust-f100800_admin",
            "es_lz_main-euwest1-cust-f100830",
            "es_lz_main-euwest1-cust-f100830_admin",
            "es_lz_main-euwest1-cust-f100730",
            "es_lz_main-euwest1-cust-f100730_admin",
            "es_lz_main-euwest1-cust-f100630",
            "es_lz_main-euwest1-cust-f100630_admin",
            "es_lz_main-euwest1-cust-f100760",
            "es_lz_main-euwest1-cust-f100760_admin",
            "es_lz_main-euwest1-cust-f100590",
            "es_lz_main-euwest1-cust-f100590_admin",
            "es_lz_main-euwest1-cust-f100690",
            "es_lz_main-euwest1-cust-f100690_admin",
            "es_lz_main-euwest1-cust-f100790",
            "es_lz_main-euwest1-cust-f100790_admin",
            "es_lz_main-euwest1-cust-f100820",
            "es_lz_main-euwest1-cust-f100820_admin",
            "es_lz_main-euwest1-cust-f100360",
            "es_lz_main-euwest1-cust-f100360_admin",
            "es_lz_main-euwest1-cust-f100780",
            "es_lz_main-euwest1-cust-f100780_admin",
            "es_lz_main-euwest1-cust-f100740",
            "es_lz_main-euwest1-cust-f100740_admin",
            "es_lz_main-euwest1-cust-f100640",
            "es_lz_main-euwest1-cust-f100640_admin",
            "es_lz_main-euwest1-cust-f100670",
            "es_lz_main-euwest1-cust-f100670_admin",
            "es_lz_main-euwest1-cust-f100840",
            "es_lz_main-euwest1-cust-f100840_admin",
            "es_lz_main-euwest1-cust-f100680",
            "es_lz_main-euwest1-cust-f100680_admin",
            "es_lz_main-euwest1-cust-f100530",
            "es_lz_main-euwest1-cust-f100530_admin",
            "es_lz_main-euwest1-cust-f100570",
            "es_lz_main-euwest1-cust-f100570_admin",
            "es_lz_main-euwest1-cust-f100750",
            "es_lz_main-euwest1-cust-f100750_admin",
            "es_lz_main-euwest1-cust-f100810",
            "es_lz_main-euwest1-cust-f100810_admin",
            "es_lz_main-euwest1-cust-f100770",
            "es_lz_main-euwest1-cust-f100770_admin",
            "es_lz_main-euwest1-cust-f100870",
            "es_lz_main-euwest1-cust-f100870_admin",
        ]
        self.admin_profiles = [p for p in self.all_profiles if "admin" in p]
        self.profiles = [p for p in self.all_profiles if "admin" not in p]


class ProfileSwitcher:
    def __init__(self, aws_profiles: AwsProfiles):
        self.aws_profiles = aws_profiles
        self.one_word_searches = (
            [
                "shared",
                "primary",
                "legacy",
                "log",
                "security",
            ]
            + self.aws_profiles.firm_ids
            + self.aws_profiles.firm_keys
        )
        self.parser = argparse.ArgumentParser(
            description="Switch AWS profiles like a pro"
        )
        self.parser.add_argument(
            "keywords", nargs="*", help="Key word(s) in the profile name"
        )
        self.keywords = [k.lower() for k in self.parser.parse_args().keywords]

    def retrieve_profile(self, keywords):
        if len(keywords) == 1:
            return [n for n in self.aws_profiles.profiles if keywords[0] in n][0]
        else:
            return [
                n for n in self.aws_profiles.profiles if any(k in n for k in keywords)
            ][0]

    @staticmethod
    def activate_profile(profile):
        sys.stdout.write(f'export AWS_PROFILE="{profile}"')
        sys.stdout.flush()
        sys.exit()

    def run(self):
        # if admin given as a keyword
        if "admin" in self.keywords:
            self.keywords.remove("admin")
            self.aws_profiles.profiles = self.aws_profiles.admin_profiles

        # if one keyword given e.g. shared or voya
        if len(self.keywords) == 1:
            keyword = self.keywords[0]

            # if keywords is a key e.g. voya, convert to id e.g. f100630
            if keyword in self.aws_profiles.firm_keys:
                keyword = self.aws_profiles.firm_key_map[keyword]

            if keyword in self.one_word_searches:
                self.activate_profile(self.retrieve_profile([keyword]))
            else:
                print(f"echo 'Error - too few keywords used'")
                sys.exit()

        # else multiple keywords given e.g. live app or test res
        if "app" in self.keywords:
            self.keywords.remove("app")
            self.activate_profile(self.retrieve_profile(self.keywords))
        elif "res" in self.keywords:
            self.keywords.remove("res")
            self.activate_profile(self.retrieve_profile(self.keywords))
        else:
            print("echo 'Error - no result found for your keywords'")


if __name__ == "__main__":
    profile_switcher = ProfileSwitcher(AwsProfiles())
    profile_switcher.run()
