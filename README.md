Multi-Agent AI Chat Application (Powered by Google ADK)
This project is a sophisticated, multi-agent chat application built using the Google Agent Development Kit (ADK). It features a central Manager Agent that intelligently routes user queries to one of two specialized agents: a Customer Support Agent with a dynamic, file-based knowledge base, and a Genetic Wellness Agent for handling general knowledge questions.

The application is built with a Python Flask backend and demonstrates a modern approach to creating complex, tool-using AI systems.

Key Features
Advanced Multi-Agent Architecture: A central Manager Agent acts as a smart router, analyzing user intent to delegate tasks to the appropriate specialist agent.

Google ADK Integration: Leverages Google's official Agent Development Kit (google-adk) to structure the agents, manage conversation state, and handle tool execution, ensuring a robust and scalable design.

Dynamic Prompt Engineering:

The Customer Support Agent's knowledge base is dynamically injected into its prompt at runtime by reading a scraped_faqs.json file.

The Manager Agent's routing instructions are also dynamically built using the questions from the FAQ file, enabling it to make highly accurate routing decisions based on concrete examples.

Tool-Using Agents: The Manager Agent uses ADK's FunctionTool to call the other agents, showcasing a powerful pattern for building complex, interconnected AI systems.

Stateful Conversations: The application uses InMemorySessionService from the ADK to maintain distinct, coherent conversation histories for each agent.

My Development Process and Role
My approach for this project was to act as the architect and orchestrator, using the powerful framework provided by the Google Agent Development Kit to build a complex, multi-agent system.

My Role as Architect and Orchestrator
My primary responsibilities included:

System Design: I designed the overall multi-agent architecture, defining the roles and responsibilities of the Manager, Customer Support, and Genetic Wellness agents. I chose to use the Google ADK to provide a structured and scalable foundation.

Agent and Tool Implementation: I implemented the core logic for each agent using the Agent class and created the FunctionTools that allow the Manager Agent to call the specialist agents.

Prompt Engineering and Logic Refinement: A critical part of my work was iteratively refining the instruction prompts for each agent. I engineered the prompts to be highly explicit and, in the case of the Manager Agent, dynamically generated them from our knowledge base to solve complex routing challenges and ensure the correct agent was called every time.

Integration and Debugging: I integrated all the ADK components (Agent, Runner, SessionService, LiteLlm) and debugged the asynchronous interactions between the Flask frontend and the agent backend to create a seamless user experience.

How I Leveraged AI Assistance
I used several AI tools strategically to enhance productivity and resolve complex issues:

GitHub Copilot: I used GitHub Copilot directly in my editor for real-time code completion, generating boilerplate for Flask routes, and quickly implementing standard functions. It was invaluable for accelerating the core coding process.

Codebase-Aware AI (e.g., Codebase, Cursor): For more complex, multi-file challenges like debugging the agent routing logic, I leveraged an AI tool that could analyze the entire codebase. This allowed me to get context-aware suggestions for refactoring and to identify the root cause of issues that spanned multiple modules.

ChatGPT, Perplexity, & Gemini: For complex technical challenges, such as debugging Python logic or implementing new features, I used these tools as advanced technical sounding boards. By providing them with specific code and error contexts, I could quickly validate solutions and overcome development roadblocks efficiently.

Setup and Installation
Clone the Repository:

git clone <your-repository-link>
cd <your-repository-folder>

Create and Activate a Virtual Environment:

python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

Install Dependencies:
Create a requirements.txt file with the following content:

flask
flask_cors
python-dotenv
google-generativeai
google-adk
litellm

Then, install the dependencies:

pip install -r requirements.txt

Configure Credentials:

Create a file named .env in the root directory.

Add your Google API Key to it:

GOOGLE_API_KEY="YOUR_API_KEY_HERE"

Create Knowledge Base:

Ensure you have a scraped_faqs.json file in the root directory with your question-and-answer pairs.

How to Run the Application
With the setup complete, run the Flask application from the root directory:

python app.py
