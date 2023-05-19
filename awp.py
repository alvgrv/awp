import argparse
import sys
import configparser
import dataclasses
import os
import re
from typing import Optional

cp = configparser.ConfigParser()

user = os.environ["ESSENTIA_USERNAME"].split(".")[0].replace("_", ".")
# cp.read(f"/Users/{user}/.aws/config")
cp.read(f"/Users/{user}/.aws/config")


unique_profile_names = {
    p.split(" ")[1].replace("_admin", "")
    for p in cp.sections()
    if p.startswith("profile")
}


class AwsConfig:
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
        self.profiles = [
            self.AwsProfile(
                profile_name=profile,
                admin_profile_name=f"{profile}_admin",
                account_name=cp.get(f"profile {profile}", "name"),
                firm_id=re.search(r"([TSFtsf]\d{6})", profile).group(0)
                if "cust" in profile
                else None,
            )
            for profile in unique_profile_names
        ]


class ProfileSwitcher:
    def __init__(self):
        self.config = AwsConfig()
        self.profiles = self.config.profiles
        self.profile_account_names = [p.account_name for p in self.profiles]
        self.profile_account_name_map = {p.account_name: p for p in self.profiles}
        self.profile_firm_ids = [p.firm_id for p in self.profiles]
        self.profile_firm_id_name_map = {p.firm_id: p for p in self.profiles}
        self.parser = argparse.ArgumentParser(
            description="Switch AWS profiles like a pro. Enter a short form of the profile name and "
        )
        self.parser.add_argument(
            "profile_name",
            nargs="?",
            help="A short profile name e.g. brown, f100060, testres1, live-app, shared",
        )
        # TODO add admin arg
        # TODO add console arg
        # TODO add login arg
        self.user_entry = self.parser.parse_args().profile_name

    @staticmethod
    def activate_profile(profile):
        sys.stdout.write(f'export AWS_PROFILE="{profile.profile_name}"')
        sys.stdout.flush()
        sys.exit()

    def return_fail_message(self):
        print(
            f"echo 'Your entered profile name {self.user_entry} did not match a profile.'"
        )
        sys.exit()

    def run(self):
        matched_profile = None

        try:
            if re.match(r"([TSFtsf]\d{6})", self.user_entry):
                matched_firm_id = [
                    id for id in self.profile_firm_ids if self.user_entry.upper() == id
                ][0]
                matched_profile = self.profile_firm_id_name_map.get(matched_firm_id)
            else:
                matched_account_name = [
                    name
                    for name in self.profile_account_names
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
    profile_switcher = ProfileSwitcher()
    profile_switcher.run()
