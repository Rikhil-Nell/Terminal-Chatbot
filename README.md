# TARS Terminal Chatbot

TARS is a terminal-based chatbot inspired by the character TARS from *Interstellar*. It leverages modern LLMs, tool integrations, and persistent memory to deliver engaging and context-aware interactions.

## Features

- **Interactive Chat:** Chat with TARS in your terminal, complete with wit and useful responses.
- **Tool Integration:** Includes search capabilities using APIs (e.g., Tavily).
- **Persistent Memory:** Maintains context between interactions using a memory module.
- **Configurable Personality:** Modify the system prompt to fine-tune TARS's personality and behavior.

## Prerequisites

- Python 3.8 or higher
- `pip` for installing dependencies
- API keys for Tavily and Groq (or other LLM APIs)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Rikhil-Nell/Terminal-Chatbot.git
   cd tars-terminal-chatbot
   ```

2. Set up a virtual environment (optional but recommended):

   ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a .env file in the project root with your API keys:

    ```bash
    GROQ_API_KEY=your_groq_api_key
    TAVILY_API_KEY=your_tavily_api_key
    ```

5. Modify the system prompt if desired:
    - Update the `prompt.txt` file to define TARS's personality and tone.

## Usage

Run the chatbot using:

```bash
    python app.py
```

Once running, you'll see a terminal interface where you can chat with TARS. Enter your messages, and TARS will respond with contextually aware and detailed answers.

## File Structure

core.py: Main logic of the chatbot.
app.py: Sets up the terminal interface for inference.
prompt.txt: Defines the system prompt for TARS's personality.
requirements.txt: List of dependencies.
.env: Configuration file for storing API keys (not included in the repository).

## Configuration

- System Prompt: Customize `prompt.txt` to adjust TARS's behavior.
- Memory Management: Persistent memory ensures TARS remembers previous interactions. Adjust the memory settings in
tars_chatbot.py as needed.

## Contributions

Contributions are welcome! If you'd like to improve TARS or add features, please submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
