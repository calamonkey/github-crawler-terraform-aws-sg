# github-crawler-terraform-aws-sg
 Crawl the given repositories for terraform files containing `aws_security_group` resources.

# Dependencies
```
pip install PyGithub
pip install pyhcl
```
# Usage 
```
getTerraformAWSSGs.py -r <repo/path> [-t <github_access_token> -e <enterprise_hostname>]
```

`github_access_token` can also be set as an environment variable

`github_access_token` set on command line takes precidence

Multiple repos can be submitted with additional `-r <repo/path>`