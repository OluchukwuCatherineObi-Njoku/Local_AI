# Author: Oluchukwu Obi-Njoku
# Date: 2024-08-12
# Description: This script is a simple implementation of a chatbot using the LocalAI API.


# Import required libraries
import subprocess
import sys
import shlex
import os
import time
import json

# Required packages
required_packages = [
    "requests",
]

# Global variables
init_complete = 0 # Initialization status
chat_history_file = "chat_history.json" # File to persist chat history
chat_history = [] # List to store chat history

def install_lib(package: str) -> None:

    """
    Install a package using pip

    Args: package (str): The name of the package to install
    Returns: None
    """

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package]) # Install the package
    except subprocess.CalledProcessError as e:
        print(f"Error installing {package}: {e}")
    except subprocess.TimeoutExpired:
        print(f"Timeout expired while installing {package}")
    except FileNotFoundError as e:
        print(f"Error installing {package}: {e}")
    except OSError as e:
        print(f"Error installing {package}: {e}")
    except IOError as e:
        print(f"Error installing {package}: {e}")
    except Exception as e:
        print(f"Error installing {package}: {e}")
    except:
        print(f"Error installing {package}")


def install_packages(req_packages: list) -> None:

    """
    Install a list of packages using pip

    Args: req_packages (list): A list of package names to install
    Returns: None
    """
    try:
        for package in req_packages:
            try:
                __import__(package)
            except ImportError:
                print(f"{package} not found. Installing...")
                install_lib(package)
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
    except subprocess.TimeoutExpired:
        print(f"Timeout expired while installing packages")
    except FileNotFoundError as e:
        print(f"Error installing packages: {e}")
    except OSError as e:
        print(f"Error installing packages: {e}")
    except IOError as e:
        print(f"Error installing packages: {e}")
    except Exception as e:
        print(f"Error installing packages: {e}")
    except:
        print(f"Error installing packages")


# Import required packages if installed else install it
try:
    import requests
except ImportError:
    install_packages(required_packages)
    import requests
except Exception as e:
    print(f"Error importing packages: {e}")
except:
    print(f"Error importing packages")


def check_initialization_complete() -> bool:

    """
    Check if the LocalAI repository has been cloned and the required files are present

    Args: None
    Returns: bool: True if initialization is complete, False otherwise
    """

    global init_complete # Initialize global variable
    repo_path = os.path.join(os.getcwd(), "LocalAI") # Path to LocalAI repository
    model_path = os.path.join(repo_path, "models", "luna-ai-llama2") # Path to model file
    tmpl_path = os.path.join(repo_path, "models", "luna-ai-llama2.tmpl") # Path to template file
    
    try:
        if os.path.isdir(repo_path) and os.path.isfile(model_path) and os.path.isfile(tmpl_path):
            print("Initialization is complete.")
            init_complete = 1
            return True
        else:
            print("Initialization is not complete.")
            return False
    except FileNotFoundError as e:
        print(f"Error checking initialization: {e}")
        return False
    except OSError as e:
        print(f"Error checking initialization: {e}")
        return False
    except IOError as e:
        print(f"Error checking initialization: {e}")
        return False
    except Exception as e:
        print(f"Error checking initialization: {e}")
        return False
    except:
        print("Error checking initialization.")
        return False

def init_setup() -> None:

    # global init_complete
    # init_complete = 1

    """
    Initialize the LocalAI repository and required files

    Args: None
    Returns: None
    """

    try:
        run_command("git clone https://github.com/go-skynet/LocalAI")
        os.chdir("LocalAI")
        run_command("wget https://huggingface.co/TheBloke/Luna-AI-Llama2-Uncensored-GGUF/resolve/main/luna-ai-llama2-uncensored.Q4_0.gguf -O models/luna-ai-llama2")
        run_command("cp -rf prompt-templates/getting_started.tmpl models/luna-ai-llama2.tmpl")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing LocalAI: {e}")
    except subprocess.TimeoutExpired:
        print("Timeout expired.")
    except FileNotFoundError as e:
        print(f"Error initializing LocalAI: {e}")
    except OSError as e:
        print(f"Error initializing LocalAI: {e}")
    except IOError as e:
        print(f"Error initializing LocalAI: {e}")
    except Exception as e:
        print(f"Error initializing LocalAI: {e}")
    except:
        print("Error initializing LocalAI")

def localai_start() -> None:

    try:
        if (check_docker() == True) and (init_complete == 1):
            if not check_containers_running():
        
                current_directory = os.getcwd()
                path_parts = current_directory.split(os.sep)

                if len(path_parts) < 2 or path_parts[-2:] != ['Local_AI', 'LocalAI']:
                    os.chdir("LocalAI")

                #os.chdir("LocalAI")
                run_command("docker compose up -d --pull always", retries=3, timeout=360)
    except subprocess.CalledProcessError as e:
        print(f"Error starting LocalAI: {e}")
    except subprocess.TimeoutExpired:
        print("Timeout expired.")
    except FileNotFoundError as e:
        print(f"Error starting LocalAI: {e}")
    except OSError as e:
        print(f"Error starting LocalAI: {e}")
    except IOError as e:
        print(f"Error starting LocalAI: {e}")
    except Exception as e:
        print(f"Error starting LocalAI: {e}")
    except:
        print("Error starting LocalAI")


def run_command(command_str:str, retries:int = 3, timeout: int =120) -> bool:

    """
    Run a command in the shell

    Args: 
        command_str (str): The command to run
        retries (int): The number of times to retry the command
        timeout (int): The timeout for the command

    Returns: bool: True if the command was successful, False otherwise
    """

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
            return False

        except subprocess.CalledProcessError as e:
            print(f"Command failed with error: {e}")
            init_complete = init_complete & 0
            return False

        except FileNotFoundError as e:
            print(f"Command failed with error: {e}")
            init_complete = init_complete & 0
            return False

        except OSError as e:
            print(f"Command failed with error: {e}")
            init_complete = init_complete & 0
            return False

        except IOError as e:
            print(f"Command failed with error: {e}")
            init_complete = init_complete & 0
            return False

        except Exception as e:
            print(f"Command failed with error: {e}")
            init_complete = init_complete & 0
            return False

        except:
            print(f"Command failed.")
            init_complete = init_complete & 0
            return False

        time.sleep(5)  # Wait before retrying
    return False


def check_docker() -> bool:
    
    """
    Check if docker is installed

    Args: None
    Returns: bool: True if docker is installed, False otherwise
    """

    try:
        output = run_command("docker --version")
        if output != True:
            print("You need to install docker to commmense with LocalAI")
            return False
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error checking Docker: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("Timeout expired.")
        return False
    except FileNotFoundError as e:
        print(f"Error checking Docker: {e}")
        return False
    except OSError as e:
        print(f"Error checking Docker: {e}")
        return False
    except IOError as e:
        print(f"Error checking Docker: {e}")
        return False
    except Exception as e:
        print(f"Error checking Docker: {e}")
        return False
    except:
        print("Error checking Docker.")
        return False

def load_chat_history() -> None:

    """
    Load chat history from a file

    Args: None
    Returns: None
    """

    try:
        global chat_history
        if os.path.exists(chat_history_file):
            with open(chat_history_file, "r") as file:
                chat_history = json.load(file)
                print("Chat history loaded.")
    except FileNotFoundError as e:
        print(f"Error loading chat history: {e}")
    except OSError as e:
        print(f"Error loading chat history: {e}")
    except IOError as e:
        print(f"Error loading chat history: {e}")
    except Exception as e:
        print(f"Error loading chat history: {e}")
    except:
        print("Error loading chat history.")

def save_chat_history() -> None:

    """
    Save chat history to a file

    Args: None
    Returns: None
    """

    try:
        with open(chat_history_file, "w") as file:
            json.dump(chat_history, file)
            print("Chat history saved.")
    except FileNotFoundError as e:
        print(f"Error saving chat history: {e}")
    except OSError as e:
        print(f"Error saving chat history: {e}")
    except IOError as e:
        print(f"Error saving chat history: {e}")
    except Exception as e:
        print(f"Error saving chat history: {e}")
    except:
        print("Error saving chat history.")


def check_containers_running() -> bool:

    """
    Check if the required docker containers are running

    Args: None
    Returns: bool: True if the containers are running, False otherwise
    """

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
    except FileNotFoundError as e:
        print(f"Error checking running containers: {e}")
        return False
    except OSError as e:
        print(f"Error checking running containers: {e}")
        return False
    except IOError as e:
        print(f"Error checking running containers: {e}")
        return False
    except Exception as e:
        print(f"Error checking running containers: {e}")
        return False
    except:
        print("Error checking running containers.")
        return False

def handle_chat() -> None:

    """
    Handle the chat between the user and the assistant

    Args: None
    Returns: None
    """

    try:
        global chat_history
        while True:
            user_input = input("You: ")
            if user_input.lower() == "end chat":
                print("Ending chat. Goodbye!")
                break
            response = chat(user_input,chat_history)
            print(f"Assistant: {response['choices'][0]['message']['content']}")
    except KeyboardInterrupt:
        print("Chat ended.")
    except FileNotFoundError as e:
        print(f"Error handling chat: {e}")
    except OSError as e:
        print(f"Error handling chat: {e}")
    except IOError as e:
        print(f"Error handling chat: {e}")
    except Exception as e:
        print(f"Error handling chat: {e}")
    except:
        print("Error handling chat.")


def chat(chat_question: str,chat_history: list) -> dict:

    """
    Chat with the LocalAI assistant

    Args: 
        chat_question (str): The question to ask the assistant
        chat_history (list): The chat history
    Returns: dict: The response from the assistant
    """

    try:

        url = "http://localhost:8080/v1/chat/completions"
        headers = {"Content-Type": "application/json"}

        chat_history.append({"role": "user", "content": chat_question})

        data = {
        "model": "luna-ai-llama2",
        #"messages": [{"role": "user", "content": chat_question}],
        "messages": chat_history,
        "temperature": 0.9
        }

        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        chat_history.append({"role": "assistant", "content": response_data['choices'][0]['message']['content']})

        save_chat_history()

        return response_data
    except requests.exceptions.RequestException as e:
        print(f"Error chatting with assistant: {e}")
        return {"error": f"Error chatting with assistant: {e}"}
    except FileNotFoundError as e:
        print(f"Error chatting with assistant: {e}")
        return {"error": f"Error chatting with assistant: {e}"}
    except OSError as e:
        print(f"Error chatting with assistant: {e}")
        return {"error": f"Error chatting with assistant: {e}"}
    except IOError as e:
        print(f"Error chatting with assistant: {e}")
        return {"error": f"Error chatting with assistant: {e}"}
    except Exception as e:
        print(f"Error chatting with assistant: {e}")
        return {"error": f"Error chatting with assistant: {e}"}
    except:
        print("Error chatting with assistant.")
        return {"error": "Error chatting with assistant."}
    

def main():
    global init_complete
    if not check_initialization_complete():
        init_setup()
    localai_start()
    load_chat_history()
    handle_chat()

if __name__ == "__main__":
    main()