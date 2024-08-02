<p align="center">
  <img src="https://i.ibb.co/7gNqBFY/9.jpg" alt="Detective 9 Cover Art" width="600"/>
</p>

# Detective 9 Text Based Game

## Overview
Detective Game is an interactive text-based game where you play the role of a detective. This sample is meant to show off Llama 3 from Meta running locally. The AI bot that is running on Llama 3 via Ollama assumes a random role related to a crime scenario. Your goal is to determine whether the AI bot is innocent or guilty through a series of questions.

## Info
- **Llama 3**: Open source Large Language Model from Meta for generating AI responses.
- **Ollama**: Platform for running Llama 3 locally.
- **Rich**: Library for creating beautiful terminal outputs.

## Requirements
- Llama 3 model files (from Ollama)
- `python-dotenv` for environment variable management
- `rich` for terminal UI
- `langchain_community` for Llama 3 integration

## Ollama Download
Download: https://ollama.com/download  
Tutorial: https://www.youtube.com/watch?v=Asleok-Snfs

## Startup

### Method 1: Running the Source Code

1. **Initialize Llama 3**:
   - Run the command `ollama run llama3` to initialize and run the Llama 3 model locally using the Ollama platform. This is required for generating AI responses.

2. **Install Dependencies**:
   - Install the required Python packages by running:
     ```bash
     pip install -r requirements.txt
     ```

3. **Start the Game**:
   - Run the following command to start the game:
     ```bash
     python startGame.py
     ```

### Method 2: Running the Executable

1. **Initialize Llama 3**:
   - Just like with the source code method, you need to run the Llama 3 model:
     ```bash
     ollama run llama3
     ```

2. **Run the Game**:
   - Navigate to the `dist` folder where the executable is located.
   - Double-click on `startGame.exe` to launch the game.

   Alternatively, you can run the executable via the command line:
   ```bash
   ./dist/startGame.exe
