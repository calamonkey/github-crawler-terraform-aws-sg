# github-crawler-terraform-aws-sg
 Crawl the given repositories for terraform files containing `aws_security_group` resources.

# Dependencies
```
pip install PyGithub
pip install python-hcl2
```
# Usage 
```
getTerraformAWSSGs.py -r <repo/path> [-t <github_access_token> -b <branch_name> -r <repo/path2> -r <repo/pathn> ]
```

`github_access_token` can also be set as an environment variable

`github_access_token` set on command line takes precidence

Multiple repos can be submitted with additional `-r <repo/path>`
