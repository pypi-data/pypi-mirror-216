Manage prompts via github


### Usage
```python
from promptSDK import prompts
print(prompts.my_folder.myprompt)
# this expects a repo with repo/my_folder/myprompt.md
```

When your code accesses a prompt it fetches that file from your prompt repo. This allows iterating on prompts while your server is running. 
Prompts are cached, so the SDK does not fetch from the web everytime you accesss a prompt. The default cache lifetime is 10 seconds for dev and 300 for production

### Install
```bash
pip install promptSDK
```

### Setup
Information on how to generate a token can be found [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

If your prompt repo is public just leave the token empty.
Required env variables (see env.sample) are
```bash
BASE_URL=https://github.com/username/repo
TOKEN=your_github_personal_access_token
```

### Limitations
Currently only supports reading .md files in the prompt repo

### Example Prompt Repo
https://github.com/ottozastrow/sample-prompts