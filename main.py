#!/usr/bin/env python3
"""This command line utility makes it easy to switch between AWS profiles on the command line.

usage: awp [-a] [profile_name]

positional arguments:
  profile_name  A short profile name e.g. ab, f100530, testres2, live-app, shared, legacy

optional arguments:
  -a, --admin   Switches to the admin version of the profile

# TODO add --console/-c flag that prints a link to switch to this profile in the AWS Console
# TODO add --list/-l  flag that prints the list of unique profile names in order
"""


import argparse
import configparser
import dataclasses
import os
import re
import sys
from typing import Optional


class AwsConfig:
    """Object representing the ~/.aws/config file and the profiles it contains."""

    USER = os.environ["ESSENTIA_USERNAME"].split(".")[0].replace("_", ".")

    @dataclasses.dataclass
    class AwsProfile:
        """Dataclass representing an AWS Profile stored in ~/.aws/config.

        Args:
            profile_name: e.g. es_lz_main-euwest1-cust-F100060
            admin_profile_name: e.g. es_lz_main-euwest1-cust-F100060_admin
            account_name: e.g. brown
            firm_id: e.g. F100060. Can be None for non-client profiles
        """

        profile_name: str
        admin_profile_name: str
        firm_id: Optional[str]
        account_name: str

    def __init__(self):
        """Parse the ~/.aws/config file."""
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
                # fmt: off
                firm_id=re.search(r"([TSFtsf]\d{6})", profile).group(0) if "cust" in profile else None,
                # fmt: on
            )
            for profile in self.unique_profile_names
        ]


class ProfileSwitcher:
    """Main class for the command line utility awp."""

    class ArgParser:
        """Wrapper for Python stdlib argparse."""

        def __init__(self):
            self.parser = argparse.ArgumentParser(
                description="Switch AWS profiles like a pro."
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
            self.args = self.parser.parse_args()
            self.user_entry = self.args.profile_name
            self.is_admin = self.args.admin

    def __init__(self, config):
        """Initialise the class with the user's AwsConfig ."""
        self.config = config
        self.profile_account_name_map = {
            p.account_name: p for p in self.config.profiles
        }
        self.profile_firm_id_name_map = {p.firm_id: p for p in self.config.profiles}
        self.argparser = self.ArgParser()

    @staticmethod
    def return_to_stdout(message):
        """Returns a message to stdout which is picked up by the eval function in .zshrc."""
        sys.stdout.write(message)
        sys.exit()

    def activate_profile(self, profile):
        """Given an AwsProfile object, activate that profile in the user's terminal by setting the env var."""
        profile = (
            profile.admin_profile_name
            if self.argparser.is_admin
            else profile.profile_name
        )
        self.return_to_stdout(f'export AWS_PROFILE="{profile}"')

    def unset_profile(self):
        """Unsets the AWS_PROFILE env var which means no profile is active in the user's terminal."""
        self.return_to_stdout("unset AWS_PROFILE")

    def return_fail_message(self):
        """Returns an error message if no AWS profile can be found from the user's input."""
        self.return_to_stdout(
            f"echo 'Your entered profile name `{self.argparser.user_entry}` did not match a profile.'"
        )

    def match_profile(self):
        """Given the user input, attempt to match it to a profile in the ~/.aws/config file."""
        try:
            if re.match(r"([TSFtsf]\d{6})", self.argparser.user_entry):
                matched_firm_id = [
                    firm_id
                    for firm_id in self.profile_firm_id_name_map.keys()
                    if self.argparser.user_entry.upper() == firm_id
                ][0]
                matched_profile = self.profile_firm_id_name_map.get(matched_firm_id)
            else:
                matched_account_name = [
                    name
                    for name in self.profile_account_name_map.keys()
                    if self.argparser.user_entry in name
                ][0]
                matched_profile = self.profile_account_name_map.get(
                    matched_account_name
                )
            return matched_profile
        except IndexError:
            return None

    def run(self):
        """Runs the ProfileSwitcher command line utility."""
        if not self.argparser.user_entry:
            self.unset_profile()

        if matched_profile := self.match_profile():
            self.activate_profile(matched_profile)
        else:
            self.return_fail_message()


if __name__ == "__main__":
    config = AwsConfig()
    ProfileSwitcher(config).run()
