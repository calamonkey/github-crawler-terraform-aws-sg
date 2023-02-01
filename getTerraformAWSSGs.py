from github import Github
import hcl
import os
import sys, getopt

def main(argv):
    github_access_token = os.environ.get('GITHUB_ACCESS_TOKEN')
    repo_names = []
    is_enterprise = False
    enterprise_hostname = ""
    try:
        opts, args = getopt.getopt(argv,"hr:t:e",["repo=","token=","enterprise_hostname="])
    except getopt.GetoptError:
        print ('getTerraformAWSSGs.py -r <repo/path> [-t <github_access_token>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('''
            getTerraformAWSSGs.py -r <repo/path> [-r <repo/path2> -r <repo/pathn> -t <github_access_token>]

            github_access_token can also be set as an environment variable
            github_access_token set on command line takes precidence

            Multiple repos can be submitted with additional -r <repo/path>
            ''')
            sys.exit()
        elif opt in ("-r", "--repo"):
            repo_names.append(arg)
        elif opt in ("-t", "--token"):
            github_access_token = arg
        elif opt in ('-e', "--enterprise_hostname"):
            is_enterprise = True
            enterprise_hostname = arg
    if len(repo_names) == 0:
        print(f"Repo name must be set with the -r option. At least one repo must be set")
        sys.exit()
    if github_access_token == None:
        print(f"Github Access token must be set with the -t option or in ENV")
        sys.exit()
    if(is_enterprise):
        g = Github(base_url="https://{enterprise_hostname}/api/v3", login_or_token=github_access_token)
    else:
        g = Github(github_access_token)
    # Github Enterprise with custom hostname
    # 
    print(f"github token is {github_access_token}")
    terraform_files = []
    for repo_name in repo_names:
        print(repo_name)
        repo = g.get_repo(repo_name)

        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                if file_content.path[-3:] == ".tf":
                    terraform_files.append(file_content)

        for tf in terraform_files:
            file_content = hcl.loads(tf.decoded_content)
            try:
                for group in file_content['resource']['aws_security_group']:
                    print(group)
            except KeyError:
                print(f"No aws_security_group resources found in {tf.name}")

if __name__ == "__main__":
    main(sys.argv[1:])