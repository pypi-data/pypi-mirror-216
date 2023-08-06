### Usage
```python
from promptSDK import prompts
print(prompts.my_folder.myprompt)
```

### Setup
Information on how to generate a token can be found [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

If your prompt repo is public just leave the token empty.
Required env variables (see env.sample) are

BASE_URL=https://github.com/username/repo
TOKEN=your_github_personal_access_token
BRANCH=main
