
# Dual-Agent AI Chat Application


---
This project features a web-based chat interface with two distinct AI agents: a rule-based **FAQ Agent** for specific company queries and an LLM-powered **Genetic Wellness Agent** for general knowledge questions. The application is built with a Python Flask backend and a dynamic HTML, CSS, and JavaScript frontend.

## Key Features

  * **Dual-Agent System**: Seamlessly toggle between a highly specific FAQ bot and a generalist LLM agent.
  * **Conversational Logic**: Both agents are designed to handle common conversational phrases (greetings, thanks, identity queries) for a more natural user experience.
  * **Persistent Chat History**: The conversation state for each agent is saved using `localStorage`, allowing users to refresh the page or switch between agents without losing their chat history.
  * **Dynamic UI**: A clean, responsive user interface with features like a dark mode toggle and a "New Chat" button for clearing conversations.
  * **Robust Backend**: The FAQ agent uses a combination of exact and fuzzy matching for accuracy, while the Wellness agent integrates with the Google Gemini Pro model for powerful generative responses.

-----

## My Development Process and Role

My approach for this project was to act as the architect and integrator, using modern AI assistance tools to accelerate development while retaining full control over the design, logic, and final implementation.

### My Role as Architect and Integrator

My primary responsibilities included:

  * **System Design**: I designed the overall architecture, choosing to use a Python Flask backend with a Blueprint structure to ensure the FAQ and Wellness agents were modular and scalable.
  * **Logic Definition**: I defined the core logic for both agents. This included designing the rule-based system for the FAQ agent and architecting the stateful, memory-enabled chat flow for the LLM-based Wellness Agent.
  * **Code Integration and Refinement**: A significant part of my work was integrating code snippets, debugging the interactions between the frontend and backend, and refactoring the final code to be clean, efficient, and robust.

### How I Leveraged AI Assistance

I used several AI tools strategically to enhance productivity and resolve complex issues:

  * **ChatGPT:** I leveraged ChatGPT to accelerate the initial development of the UI and server boilerplate, providing a solid foundation that I then customized.
  * **Gemini & Perplexity:** For complex technical challenges, such as debugging Python logic or implementing new features like `localStorage` persistence, I used these tools as advanced technical sounding boards. By providing them with specific code and error contexts, I could quickly validate solutions and overcome development roadblocks efficiently.
  * **GitHub:** I researched open-source projects on GitHub to analyze established design patterns for agent architecture, ensuring my solution was robust and well-designed.

-----

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-link>
    cd <your-repository-folder>
    ```
2.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Credentials:**
      * Create a file named `.env` in the root directory.
      * Add your Google Cloud credentials path to it:
        ```
        GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credential.json"
        ```

-----

## How to Run the Application

With the setup complete, run the Flask application from the root directory:

```bash
python app.py
```

Open your web browser and navigate to `http://127.0.0.1:5000` to interact with the chat agents.