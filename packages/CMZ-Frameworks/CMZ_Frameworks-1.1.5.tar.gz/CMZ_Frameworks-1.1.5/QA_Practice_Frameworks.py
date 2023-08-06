import requests
import json
import subprocess

def callAPI():
    url = 'https://slb-it.visualstudio.com/it-commercialization/_apis/git/repositories?api-version=7.0'

    # Basic Authentication credentials
    username = ''
    password = str(input("Enter your PAT: "))

    # Make the API call with basic authentication
    response = requests.get(url, auth=(username, password))

    # Check the response status code
    if response.status_code == 200:
        # Request was successful
        data = response.json()
        pretty_data = json.dumps(data, indent=4)
    else:
        # Request failed
        print('API request failed with status code:', response.status_code)



    Repos = data['count']
    RepoName_URL_Map = {}
    # print('API response:', len(Repos))

    for i in range(Repos) :
        repoName = data['value'][i]['name']
        RepoURL  = data['value'][i]['remoteUrl']

        
        RepoName_URL_Map[repoName] = RepoURL

    print("Available options:")
    for index, key in enumerate(RepoName_URL_Map.keys()):
        print(f"{index + 1}. {key}")

    selected_index = int(input("Enter the number of the option you want to select: ")) - 1

    keys_list = list(RepoName_URL_Map.keys())
    if 0 <= selected_index < len(keys_list):
        selected_key = keys_list[selected_index]
        process_selected_option(selected_key, RepoName_URL_Map)
    else:
        print("Invalid selection. Exiting...")

def git_clone(url, destination_path):
    try:
        print(url)
        subprocess.run(["git", "clone", url, destination_path], check=True)
        print(f"Cloned repository from {url} to {destination_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {str(e)}")


def process_selected_option(selected_key, dictionary):
    selected_value = dictionary.get(selected_key)
    if selected_value is not None:
        repository_url = selected_value + "/"
        destination_path = input("Enter the destination path where you want to clone the repository: ")
        git_clone(repository_url, destination_path)
    else:
                print("Invalid selection.")


