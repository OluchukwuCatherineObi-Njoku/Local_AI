# import requests
# import subprocess
# import shlex

import subprocess
import sys
import shlex
import os
import time

try:
    import requests
except ImportError:
    install_packages(required_packages)
    import requests

required_packages = [
    "requests",
]

init_complete = 1

def install_lib(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def install_packages(req_packages):

    for package in req_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} not found. Installing...")
            install_lib(package)


def init_setup():
    global init_complete
    init_complete = 1
    run_command("git clone https://github.com/go-skynet/LocalAI")
    os.chdir("LocalAI")
    run_command("wget https://huggingface.co/TheBloke/Luna-AI-Llama2-Uncensored-GGUF/resolve/main/luna-ai-llama2-uncensored.Q4_0.gguf -O models/luna-ai-llama2")
    run_command("cp -rf prompt-templates/getting_started.tmpl models/luna-ai-llama2.tmpl")

def localai_start():
    if (check_docker() == True) and (init_complete == 1):
        if not check_containers_running():
            run_command("docker compose up -d --pull always", retries=3, timeout=360)


def run_command(command_str, retries=3, timeout=120):
    global init_complete
    command_list = shlex.split(command_str)
    for attempt in range(retries):
        try:
            print(f"Running: {command_str} (Attempt {attempt + 1}/{retries})")
            result = subprocess.run(command_list, capture_output=True, check=True, timeout=timeout, text=True)
            print(f"Completed: {command_str}")
            init_complete = init_complete & 1
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"Timeout expired for: {command_str}")
            init_complete = init_complete & 0
        except subprocess.CalledProcessError as e:
            print(f"Command failed with error: {e}")
            init_complete = init_complete & 0
        time.sleep(5)  # Wait before retrying
    return False


def check_docker():
    output = run_command("docker --version")
    if output != True:
        print("You need to install docker to commmense with LocalAI")
        return False
    return True


def check_containers_running():
    try:
        result = subprocess.run(["docker", "ps"], capture_output=True, check=True, text=True)
        if "localai-api-1" in result.stdout: 
            print("Required containers are already running.")
            return True
        else:
            print("Required containers are not running.")
            return False
    except subprocess.CalledProcessError:
        print("Failed to check running containers.")
        return False

def chat(chat_question):

    url = "http://localhost:8080/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    data = {
    "model": "luna-ai-llama2",
    "messages": [{"role": "user", "content": chat_question}],
    "temperature": 0.9
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()

def main():
    global init_complete
    if init_complete == 0:
        init_setup()
    localai_start()
    response = chat("Hey, how are you doing?")
    print(response)

if __name__ == "__main__":
  main()