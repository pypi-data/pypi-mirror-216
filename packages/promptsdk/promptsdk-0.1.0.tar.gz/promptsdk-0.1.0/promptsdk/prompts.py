import requests
import configparser
import time
import os
from typing import Dict, Optional

import webbrowser


class Prompt:
    """
    Prompt class for fetching file content from a GitHub repository.

    Attributes:
        base_url (str): Base URL for the prompts.
        token (str): GitHub personal access token.
        branch (str): Branch to load prompts from.
        cache (Dict[str, tuple]): Cache for storing fetched prompt content.
    """

    def __init__(self, path: str = "") -> None:
        """
        Initializes a Prompt object.

        Args:
            path (str): Path for the prompt file.
        """
        self.path = path
        self.config = configparser.ConfigParser()

        # Create a new directory named .promptSDK in the current directory
        if not os.path.exists('.promptSDK'):
            os.makedirs('.promptSDK')

        # Specify the new path
        config_path = os.path.join('.promptSDK', 'config.ini')
        self.config.read(config_path)

        # Read configuration from config.ini or prompt user for input
        self.base_url: str = self.config['DEFAULT'].get('base_url') if 'DEFAULT' in self.config else ''
        self.token: str = self.config['DEFAULT'].get('token') if 'DEFAULT' in self.config else ''
        self.branch: str = self.config['DEFAULT'].get('branch') if 'DEFAULT' in self.config else ''

        if not self.base_url:
            self.base_url = input("Please enter the base URL for the prompts: ")
            self.config['DEFAULT']['base_url'] = self.base_url

        if not self.token:
            self.token = input(
                "Information on how to generate a token can be found here:\n"
                "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens\n"
                "enter your personal access token - or leave empty if youre prompt repo is public: ")
            self.config['DEFAULT']['token'] = self.token

        if not self.branch:
            self.branch = input("Please enter the branch to load from (press Enter for 'main'): ")
            if not self.branch:
                self.branch = "main"
            self.config['DEFAULT']['branch'] = self.branch

        with open(config_path, 'w') as configfile:
            self.config.write(configfile)

        self.cache: Dict[str, tuple] = {}

    # The rest of your class remains unchanged...

prompts = Prompt()
