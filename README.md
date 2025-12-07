WhatsApp Lead Bot (WLB) 🤖

The WhatsApp Lead Bot (WLB) is an intelligent AI agent designed for Indosat Ooredoo Hutchison B2B. It automates the qualification of inbound leads via WhatsApp, ensuring that only high-quality, Sales Qualified Leads (SQLs) are handed off to human agents.

Built with Google Agent Development Kit (ADK), Gemini 2.5 Flash, and Firebase Firestore.

🚀 Key Features

BANT Qualification: Automatically collects Budget, Authority (implied), Need, and Timeline data.

Smart Persistence: Stores conversation state and final lead data in Google Cloud Firestore.

Secure: Fetches API keys securely from Google Cloud Secret Manager (no hardcoded keys).

Guardrails:

Strictly avoids discussing pricing or specific contracts.

Automatically disqualifies "just browsing" or "no budget" leads.

Validates data completeness before handoff.

🛠️ Prerequisites

Python 3.10+ installed.

Google Cloud Project with the following APIs enabled:

Secret Manager API

Firestore API

Vertex AI API (optional, if not using Studio keys)

Google Cloud CLI (gcloud) installed and authenticated.

⚙️ Setup & Configuration

1. Google Cloud Setup

A. Firestore

Go to the Firebase Console or GCP Console.

Create a Firestore database (in Native mode).

Ensure your local environment has permission to write to it (Owner/Editor role is fine for dev).

B. Secret Manager

Go to Secret Manager.

Create a new secret named gemini-api-key.

Add a new version containing your actual Google AI Studio API Key.

2. Local Environment

Clone this repository and navigate to the project folder:

cd wlb_project


Install dependencies:

pip install -r requirements.txt


Authenticate your local machine (Application Default Credentials):

gcloud auth application-default login


Set your Project ID:

# Replace with your actual Project ID
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"


▶️ Running the Agent

We use the ADK web interface for testing and interaction.

Launch the ADK Server:

adk web


Open Browser:
Navigate to http://localhost:8000 (or the port shown in your terminal).

Select Agent:
Choose whatsapp_lead_bot from the dropdown menu.

📂 Project Structure

wlb_project/
├── requirements.txt          # Python dependencies
├── README.md                 # This documentation
└── wlb_agent/                # Main Package
    ├── __init__.py           # Enforces config loading before agent init
    ├── agent.py              # Logic: Persona, System Instructions, Guardrails
    ├── config.py             # Infra: Secret Manager & Firestore setup
    └── tools.py              # Capabilities: BANT logic & DB writes


🧠 How it Works

The Logic Flow (tools.py)

update_lead_profile: This tool runs repeatedly. It fills slots in the session state (full_name, budget, etc.) as the user speaks. It calculates missing fields and instructs the LLM what to ask next.

disqualify_lead: If the user signals low intent, this tool flags the session as disqualified and ends the flow.

finalize_handoff:

Validates that all 5 required fields are present.

Writes the structured JSON payload to the Firestore leads collection.

Returns the success signal to the Agent to send the final closing message.

The Persona (agent.py)

The agent is instructed to act like a human specialist. It acknowledges the ad source immediately ("Thanks for clicking our ad on Instagram") and maintains a professional, concise tone suitable for WhatsApp.

📝 Database Schema

The agent writes to the leads collection in Firestore with the following structure:

{
  "Lead_Status": "Qualified - Hot Lead",
  "Source": "Meta_WA_Ad",
  "Full_Name": "String",
  "Company_Name": "String",
  "Specific_Need": "String",
  "Budget_Range": "String",
  "Timeline_Urgency": "String",
  "Conversation_Summary": "String",
  "Hand_Off_Timestamp": "ISO8601 Date"
}
