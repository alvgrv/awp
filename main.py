#!/usr/bin/env python3

import argparse
import sys
import configparser
import dataclasses
import os
import re
from typing import Optional


class AwsConfig:
    USER = os.environ["ESSENTIA_USERNAME"].split(".")[0].replace("_", ".")

    @dataclasses.dataclass
    class AwsProfile:
        """Dataclass representing an AWS Profile stored in ~/.aws/config.

        Args:
            profile_name: e.g. es_lz_main-euwest1-cust-F100060
            admin_profile_name: e.g. es_lz_main-euwest1-cust-F100060_admin
            account_name: e.g. brown
            firm_id: e.g. f100060. Can be None for non-client profiles

        """

        profile_name: str
        admin_profile_name: str
        firm_id: Optional[str]
        account_name: str

    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.parser.read(f"/Users/{self.USER}/.aws/config")
        self.unique_profile_names = {
            p.split(" ")[1].replace("_admin", "")
            for p in self.parser.sections()
            if p.startswith("profile")
        }
        self.profiles = [
            self.AwsProfile(
                profile_name=profile,
                admin_profile_name=f"{profile}_admin",
                account_name=self.parser.get(f"profile {profile}", "name"),
                firm_id=re.search(r"([TSFtsf]\d{6})", profile).group(0)
                if "cust" in profile
                else None,
            )
            for profile in self.unique_profile_names
        ]


class ProfileSwitcher:
    def __init__(self):
        self.config = AwsConfig()
        self.profiles = self.config.profiles
        self.profile_account_name_map = {p.account_name: p for p in self.profiles}
        self.profile_firm_id_name_map = {p.firm_id: p for p in self.profiles}
        self.parser = argparse.ArgumentParser(
            description="Switch AWS profiles like a pro.", add_help=False  # TODO fix
        )
        self.parser.add_argument(
            "profile_name",
            nargs="?",
            help="A short profile name e.g. brown, f100060, testres1, live-app, shared",
        )
        self.parser.add_argument(
            "-a",
            "--admin",
            action="store_true",
            help="Switches to the admin version of the profile",
        )
        self.parser.add_argument(
            "-h",
            "--help",
            action="store_true",
            help="Prints this page",
        )

        # TODO add console arg
        # TODO add login arg
        # todo split parser into own wrapper object
        self.args = self.parser.parse_args()
        self.user_entry = self.args.profile_name
        self.is_admin = self.args.admin

    def activate_profile(self, profile):
        profile = profile.admin_profile_name if self.is_admin else profile.profile_name
        sys.stdout.write(f'export AWS_PROFILE="{profile}"')
        sys.stdout.flush()
        sys.exit()

    def unset_profile(self):
        sys.stdout.write(f"unset AWS_PROFILE")
        sys.stdout.flush()
        sys.exit()

    def return_fail_message(self):
        print(
            f"echo 'Your entered profile name {self.user_entry} did not match a profile.'"
        )
        sys.exit()

    def return_help_message(self):
        pass  # TODO

    def run(self):
        if self.user_entry == "unset":
            self.unset_profile()

        matched_profile = None
        try:
            if re.match(r"([TSFtsf]\d{6})", self.user_entry):
                matched_firm_id = [
                    id
                    for id in self.profile_firm_id_name_map.keys()
                    if self.user_entry.upper() == id
                ][0]
                matched_profile = self.profile_firm_id_name_map.get(matched_firm_id)
            else:
                matched_account_name = [
                    name
                    for name in self.profile_account_name_map.keys()
                    if self.user_entry in name
                ][0]
                matched_profile = self.profile_account_name_map.get(
                    matched_account_name
                )
        except IndexError:
            self.return_fail_message()

        if not matched_profile:
            self.return_fail_message()

        self.activate_profile(matched_profile)


if __name__ == "__main__":
    # todo context mgr for sys exit

    ProfileSwitcher().run()
