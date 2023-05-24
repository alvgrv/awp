#!/usr/bin/env python3
"""This command line utility makes it easy to switch between AWS profiles on the command line.

usage: awp [-a] [profile_name]

positional arguments:
  profile_name  A short profile name e.g. ab, f100530, testres2, live-app, shared, legacy

optional arguments:
  -a, --admin   Switches to the admin version of the profile

example usage:
`awp`  # deactivates any profile that is active
`awp brown`  # activates the brown profile
`awp shared`  # activates the shared-services profile
`awp -a f100530`  # activates the admin version of the ab profile
`aws -c live-app` # prints a link to switch to this profile in the AWS Console
# TODO edit machine build script adding client names to aws config file, for dev, res, frontline
# TODO add --list/-l  flag that prints the list of unique profile names in order
"""

from argparse import ArgumentParser
from configparser import ConfigParser
from dataclasses import dataclass
import os
import re
import sys

USER = os.environ["ESSENTIA_USERNAME"].split(".")[0].replace("_", ".")


class AwsConfig:
    """Object representing the ~/.aws/config file and the profiles it contains."""

    @dataclass
    class AwsProfile:
        """Dataclass representing an AWS Profile stored in ~/.aws/config.

        Args:
            profile_name: e.g. es_lz_main-eueast1-cust-F123456
            admin_profile_name: e.g. es_lz_main-eueast1-cust-F123456_admin
            firm_id: e.g. F123456. Can be None for non-client profiles
            account_name: e.g. ab
            account_id: e.g. 123456789012
            role: e.g. CompanyDeveloper
        """

        profile_name: str
        admin_profile_name: str
        firm_id: str
        account_name: str
        account_id: str
        role: str

    class AwsConfigParser:
        def __init__(self):
            """Initialise the config parser class with stdlib ConfigParser and read user's AWS config file."""
            self._parser = ConfigParser()
            self._parser.read(f"/Users/{USER}/.aws/config")

        def _config_get(self, profile_name, attribute_name):
            """Wraps ConfigParser.get, ensuring that the profile name is prepended with 'profile' as it appears in config."""
            return self._parser.get(f"profile {profile_name}", attribute_name)

        def is_frontline(self):
            """Returns bool if user is a frontline user."""
            return "Frontline" in self._config_get(
                self.unique_profile_names[0], "role_arn"
            )

        def is_research(self):
            """Returns bool is user is a research user."""
            return "Research" in self._config_get(
                self.unique_profile_names[0], "role_arn"
            )

        @property
        def unique_profile_names(self):
            """Returns list of unique AWS profile names, excluding admin profiles."""
            return list(
                {
                    p.split(" ")[1].replace("_admin", "")
                    for p in self._parser.sections()
                    if p.startswith("profile")
                }
            )

        def get_account_id(self, profile_name):
            """Returns the AWS account ID, a 12 digit number in the role_arn config property."""
            role_arn = self._config_get(profile_name, "role_arn")
            pattern = r"\d{12}"
            match = re.search(pattern, role_arn)
            if match:
                account_id = match.group()
                return account_id

        def get_account_name(self, profile_name):
            """Returns the account name config property for a profile."""
            return self._config_get(profile_name, "name")

        def get_profile_role(self, profile_name):
            """Returns the AWS role for a profile, from the role_arn config property."""
            return self._config_get(profile_name, "role_arn").split("/")[-1]

        def get_firm_id(self, profile_name):
            """Returns the Firm ID or an empty string if the profile is non-firm e.g. test-app."""
            if "cust" in profile_name:
                return re.search(r"([TSF]\d{6})", profile_name).group(0)
            else:
                return ""

    def __init__(self):
        """Parse the ~/.aws/config file."""
        self.parser = self.AwsConfigParser()
        self.is_frontline = self.parser.is_frontline()
        self.is_research = self.parser.is_research()

    @property
    def profiles(self):
        """Returns a list of AWS profiles found in the user's ~/.aws/config file."""
        return [
            self.AwsProfile(
                profile_name=profile_name,
                admin_profile_name=f"{profile_name}_admin",
                account_name=self.parser.get_account_name(profile_name),
                account_id=self.parser.get_account_id(profile_name),
                role=self.parser.get_profile_role(profile_name),
                firm_id=self.parser.get_firm_id(profile_name),
            )
            for profile_name in self.parser.unique_profile_names
        ]


class ProfileSwitcher:
    """Main class for the command line utility awp."""

    class ArgParser:
        """Wrapper for Python stdlib argparse."""

        def __init__(self):
            self.parser = ArgumentParser(description="Switch AWS profiles like a pro.")
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
                "-c",
                "--console",
                action="store_true",
                help="Prints a link to switch to this profile in the AWS Console",
            )
            self.args = self.parser.parse_args()
            self.user_entry = self.args.profile_name
            self.is_admin = self.args.admin
            self.is_console = self.args.console

    def __init__(self, config):
        """Initialise the class with the user's AwsConfig."""
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

    @staticmethod
    def is_firm_id(string):
        """Return bool if string contains a firm id e.g. f100060, T100580."""
        if re.match(r"([TSFtsf]\d{6})", string):
            return True
        return False

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
            if self.is_firm_id(self.argparser.user_entry):
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

    def get_console_link(self, matched_profile):
        """Returns a link to switch to the matched profile in the AWS Console."""
        if matched_profile.firm_id:
            return f"https://signin.aws.amazon.com/switchrole?roleName={matched_profile.role}&account={matched_profile.account_id}&displayName={matched_profile.firm_id}-{matched_profile.account_name.capitalize()}"
        else:
            return f"https://signin.aws.amazon.com/switchrole?roleName={matched_profile.role}&account={matched_profile.account_id}&displayName={matched_profile.account_name.capitalize()}"

    def run(self):
        """Runs the ProfileSwitcher command line utility."""
        if not self.argparser.user_entry:
            self.unset_profile()

        if matched_profile := self.match_profile():
            if self.argparser.is_console:
                self.return_to_stdout(
                    f'echo "{self.get_console_link(matched_profile)}"'
                )
            else:
                self.activate_profile(matched_profile)
        else:
            self.return_fail_message()


if __name__ == "__main__":
    ProfileSwitcher(AwsConfig()).run()
