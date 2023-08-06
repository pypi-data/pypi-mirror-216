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
        self.base_url: str = os.getenv('BASE_URL')
        self.token: str = os.getenv('TOKEN')
        self.production_branch: str = os.getenv('PRODUCTION_PROMPTS_BRANCH')
        self.dev_branch: str = os.getenv('DEV_PROMPTS_BRANCH')

        # Determine the current environment and set the appropriate branch
        env: str = os.getenv('ENV')
        if env == "production":
            self.current_branch = self.production_branch
        elif env == "development":
            self.current_branch = self.dev_branch
        else:
            raise Exception("Invalid environment. Please set ENV environment variable to 'production' or 'development'.")

        if not self.base_url:
            raise Exception("Please set BASE_URL environment variable")

        if not self.token or self.token == "your_github_personal_access_token":
            print("Warning: No token provided. This only works for public repositories.")

        if not self.production_branch:
            raise Exception("Please set PRODUCTION_PROMPTS_BRANCH environment variable")

        if not self.dev_branch:
            self.dev_branch = "dev"  # or any sensible default you want

        self.cache: Dict[str, tuple] = {}

    def __getattr__(self, name: str) -> str:
        """
        Retrieves the file content based on the attribute name.

        Args:
            name (str): Attribute name representing the file path.

        Returns:
            str: File content.

        Raises:
            Exception: If unable to fetch the file content.
        """
        path = name.replace(".", "/") + ".md"
        
        if path in self.cache:
            content, timestamp = self.cache[path]
            current_timestamp = int(time.time())
            if current_timestamp - timestamp <= 10:
                print("Fetched prompt from cache")
                return content

        content = self.fetch_file_content(path)
        timestamp = int(time.time())
        self.cache[path] = (content, timestamp)
        return content

    def fetch_file_content(self, path: str) -> str:
        """
        Fetches the file content from the specified path.

        Args:
            path (str): Path of the file.

        Returns:
            str: File content.

        Raises:
            Exception: If unable to fetch the file content.
        """
        url = f"https://raw.githubusercontent.com/{self.base_url.replace('https://github.com', '')}/{self.current_branch}/{path}"
        if self.token:
            headers = {"Authorization": f"token {self.token}"}
        else:
            headers = {}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Fetched prompt from:", url)
            return response.text
        else:
            # Return from cache if available
            if path in self.cache:
                content, timestamp = self.cache[path]
                print("Warning: Returning from cache. Original request failed with status code:", response.status_code)
                return content
            else:
                raise Exception(f"Error: Unable to fetch file from {url}. Status code: {response.status_code}")

prompts = Prompt()
