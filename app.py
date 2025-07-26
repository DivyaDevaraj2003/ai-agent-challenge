import json
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import asyncio
import traceback

# --- Local Agent Imports ---
# Make sure you have these files in an 'agents' subfolder
from agents.faq_agent import CustomerSupportAgent
# You would also have your wellness_agent here, e.g.:
# from agents.wellness_agent import GeneticWellnessAgent

# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Debug check
if GOOGLE_API_KEY:
    print(f"Loaded API Key: {GOOGLE_API_KEY[:5]}****")
else:
    print("FATAL: GOOGLE_API_KEY not found in environment variables. Please check your .env file.")
    exit()

# Google ADK + LiteLLM Imports
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import FunctionTool
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.events import Event
from google.genai import types
from google.adk.agents import Agent as BaseAgent # Renaming to avoid conflict

# --- Load FAQs to build dynamic instructions ---
try:
    with open("scraped_faqs.json", "r") as f:
        SCRAPED_FAQS = json.load(f)
        print("Successfully loaded scraped_faqs.json for instruction building.")
except Exception as e:
    print(f"FATAL: Could not load or parse scraped_faqs.json. Error: {e}")
    SCRAPED_FAQS = {}
    exit()

# --- Dynamically create Manager Instructions ---
FAQ_QUESTIONS_SAMPLE = "\n".join([f"- {q}" for q in list(SCRAPED_FAQS.keys())])

MANAGER_AGENT_INSTRUCTION = f"""
You are a highly specialized routing agent. Your only job is to delegate a user's query to the correct tool. You must not answer questions yourself. Follow these rules with absolute precision.

**Rule 1: Greetings**
If the user provides a simple greeting like "hi" or "hello", you MUST respond directly with: "Hello! How can I help you today?"

**Rule 2: Customer Support Tool (`run_customer_support_agent`)**
This tool is for any question related to the NuGenomics program. Use this tool if the user's query is similar to any of the following topics:
{FAQ_QUESTIONS_SAMPLE}
If the user asks about the program, its features, cost, what's included, or anything that sounds like a specific company question, you MUST use this tool. This is your default choice.

**Rule 3: Wellness Tool (`run_genetic_wellness_agent`)**
This tool is ONLY for broad, general, or scientific questions about health and wellness that are NOT about the NuGenomics program.

**CRITICAL RULE:** You must compare the user's query to the list of sample questions. If it is a close match to any of them, you MUST use the `run_customer_support_agent` tool.
"""

CUSTOMER_SUPPORT_AGENT_INSTRUCTION = """You are a helpful customer support agent for a company called NuGenomics.
You MUST answer user questions based *only* on the provided Frequently Asked Questions (FAQs) below.
You MUST find the most relevant question in the FAQ and provide the corresponding answer verbatim, without adding or changing any words.
If the user's query does not match any question in the FAQ, you must clearly state that you do not have that information. Do not make up answers."""

GENETIC_WELLNESS_AGENT_INSTRUCTION = "You are a genetic wellness expert. Provide informative and helpful answers about genetic wellness."
APP_NAME = "MultiAgentApp"
USER_ID = "user_12345"

# --- A placeholder for the wellness agent to make the code runnable ---
class GeneticWellnessAgent(BaseAgent):
    pass

# Initialize Agents with Gemini model and explicit API key
customer_support_adk_agent = CustomerSupportAgent(
    name="CustomerSupportAgent",
    instruction=CUSTOMER_SUPPORT_AGENT_INSTRUCTION,
    faqs=SCRAPED_FAQS,
    model=LiteLlm(
        model="gemini/gemini-1.5-flash-latest",
        api_key=GOOGLE_API_KEY
    )
)

genetic_wellness_adk_agent = GeneticWellnessAgent(
    name="GeneticWellnessInformationAgent",
    instruction=GENETIC_WELLNESS_AGENT_INSTRUCTION,
    model=LiteLlm(
        model="gemini/gemini-1.5-flash-latest",
        api_key=GOOGLE_API_KEY
    )
)

# Initialize Session Service
session_service = InMemorySessionService()

# --- Runner Functions ---
async def run_customer_support_agent(query: str) -> str:
    runner = Runner(
        agent=customer_support_adk_agent,
        session_service=session_service,
        app_name=APP_NAME
    )
    session_id = "cs_session"
    # Reset session for each run to ensure fresh context
    await session_service.delete_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)

    content = types.Content(role="user", parts=[types.Part(text=query)])
    response_text = ""
    async for event in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=content):
        if event.content and hasattr(event.content, "parts"):
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    response_text += str(part.text)
        if hasattr(event, "is_final_response") and event.is_final_response():
            break
    return response_text

async def run_genetic_wellness_agent(query: str) -> str:
    runner = Runner(
        agent=genetic_wellness_adk_agent,
        session_service=session_service,
        app_name=APP_NAME
    )
    session_id = "gw_session"
    # Reset session for each run
    await session_service.delete_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)

    content = types.Content(role="user", parts=[types.Part(text=query)])
    response_text = ""
    async for event in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=content):
        if event.content and hasattr(event.content, "parts"):
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    response_text += str(part.text)
        if hasattr(event, "is_final_response") and event.is_final_response():
            break
    return response_text

# --- Manager Agent ---
customer_support_tool = FunctionTool(func=run_customer_support_agent)
genetic_wellness_tool = FunctionTool(func=run_genetic_wellness_agent)

manager_agent = BaseAgent(
    name="MainAssistantManager",
    instruction=MANAGER_AGENT_INSTRUCTION,
    tools=[customer_support_tool, genetic_wellness_tool],
    model=LiteLlm(
        model="gemini/gemini-1.5-flash-latest",
        api_key=GOOGLE_API_KEY
    )
)

manager_runner = Runner(
    agent=manager_agent,
    session_service=session_service,
    app_name=APP_NAME
)

# --- Flask Web App ---
app = Flask(__name__, static_url_path="/static")
CORS(app)

@app.route("/ask", methods=["POST"])
async def ask_manager():
    data = request.get_json()
    user_query = data.get("query")
    if not user_query:
        return jsonify({"answer": "Please provide a query."}), 400

    session_id = "main_session"
    # Reset manager session each time for stateless routing
    await session_service.delete_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)

    content = types.Content(role="user", parts=[types.Part(text=user_query)])
    full_response = ""
    try:
        async for message_event in manager_runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=content
        ):
            # --- THIS IS THE FIX ---
            # Corrected 'message_content' to 'message_event.content'
            if message_event.content and hasattr(message_event.content, "parts"):
                for part in message_event.content.parts:
                    if hasattr(part, "text") and part.text:
                        full_response += str(part.text)
            if hasattr(message_event, "is_final_response") and message_event.is_final_response():
                break
        return jsonify({"answer": full_response})
    except Exception as e:
        print("An error occurred during agent execution:")
        traceback.print_exc()
        return jsonify(
            {"answer": f"Sorry, the AI service failed to process your request. ({type(e).__name__}: {str(e)})"}
        ), 500

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
