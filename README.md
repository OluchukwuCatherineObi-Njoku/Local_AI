# LocalAI Chatbot

This project is a simple implementation of a chatbot using the LocalAI API. It initializes the LocalAI environment, starts the necessary Docker containers, and handles chat interactions with the user.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Configuration](#configuration)

## Installation

### Prerequisites

- Python 3.x
- Git

### Steps

1. Clone the repository:
    ```
    git clone https://github.com/yourusername/LocalAI-Chatbot.git
    cd LocalAI-Chatbot
    ```

## Usage

1. Run the script:
    ```
    python localai.py
    ```

2. Follow the prompts to interact with the chatbot.

## Features

- **Automatic Package Installation**: Installs required Python packages if not already installed.
- **Initialization Check**: Verifies if the LocalAI repository and required files are present.
- **Docker Integration**: Starts necessary Docker containers for LocalAI.
- **Chat History**: Loads and saves chat history to a file.
- **Error Handling**: Comprehensive error handling for various operations.

## Configuration

- **Global Variables**:
  - `init_complete`: Tracks initialization status.
  - `chat_history_file`: File to persist chat history.
  - `chat_history`: List to store chat history.
