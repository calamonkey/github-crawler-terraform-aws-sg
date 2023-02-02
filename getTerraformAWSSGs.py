from github import Github
import hcl2
import os
import sys, getopt
#import certifi

def main(argv):
    github_access_token = os.environ.get('GITHUB_ACCESS_TOKEN')
    repo_names = []
    is_enterprise = False
    enterprise_hostname = ""
    branch_name = ""
    try:
        opts, args = getopt.getopt(argv,"hr:t:e:b:",["repo=","token=","enterprise_hostname=","branch_name="])
    except getopt.GetoptError:
        print ('getTerraformAWSSGs.py -r <repo/path> [-t <github_access_token> -b <branch_name>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('''
            getTerraformAWSSGs.py -r <repo/path> [-r <repo/path2> -r <repo/pathn> -t <github_access_token> -b <branch_name>]

            github_access_token can also be set as an environment variable
            github_access_token set on command line takes precidence

            Multiple repos can be submitted with additional -r <repo/path>
            ''')
            sys.exit()
        elif opt in ("-r", "--repo"):
            repo_names.append(arg)
        elif opt in ("-b", "--branch_name"):
            branch_name = arg
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
    for repo_name in repo_names:
        terraform_files = []
        print(repo_name)
        repo = g.get_repo(repo_name)
        try:
            contents = repo.get_contents("",ref=branch_name)
        except:
            print(f"No {branch_name} branch found for {repo_name}")
            continue
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path,ref=branch_name))
            else:
                if file_content.path[-3:] == ".tf":
                    terraform_files.append(file_content)
        if not os.path.isdir(repo_name[:repo_name.find("/")]):
            os.makedirs(repo_name[:repo_name.find("/")])
        with open(f"{repo_name}.txt", 'w') as f:
            for tf in terraform_files:
                f.write(tf.name + "\n")
                try:
                    file_content = hcl2.loads(tf.decoded_content.decode())
                except:
                    print(f"Issue interpreting {tf.name}, skipping")
                    continue
                try:
                    for resource in file_content['resource']:
                        if 'aws_security_group_rule' in resource:
                            sgrulename = list(resource['aws_security_group_rule'].keys())[0]
                            sgrules = resource['aws_security_group_rule'][sgrulename]
                            f.write(f"SG Rule Name: {sgrulename}\n")
                            for key in sgrules:
                                f.write(str(key) + ' = ' + str(sgrules[key]) + "\n")
                            f.write("\n")
                except KeyError:
                    f.write(f"No aws_security_group resources found in {tf.name}\n")
                except ValueError: 
                    continue

if __name__ == "__main__":
    main(sys.argv[1:])
