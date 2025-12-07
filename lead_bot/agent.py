import os
import datetime
from typing import Optional
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.cloud import bigquery

# --- Configuration ---
# TODO: Replace with your actual BigQuery Dataset and Table ID
# Ensure the table schema matches the fields in the tool arguments.
BQ_DATASET_ID = "lead_data" 
BQ_TABLE_ID = "sql_leads"

# Initialize BigQuery Client
# Note: In Cloud Shell, this uses your logged-in credentials automatically.
try:
    bq_client = bigquery.Client()
except Exception as e:
    print(f"Warning: BigQuery client could not be initialized. {e}")
    bq_client = None

# --- Tool Implementation (Option A) ---

def write_lead_to_bigquery(
    full_name: str,
    phone_number: str,
    specific_need: str,
    budget_range: str,
    timeline_urgency: str,
    company_name: str = "NA",
    industry: str = "NA",
    lead_status: str = "Qualified - Hot Lead",
    source: str = "Meta_WA_Ad",
    conversation_summary: str = "",
    tool_context: ToolContext = None
) -> dict:
    """
    Writes a fully qualified sales lead into the BigQuery data warehouse.
    
    This tool should ONLY be called after the user has confirmed all required qualification fields 
    (Name, Need, Budget, Timeline). Do not call this for disqualified leads.

    Args:
        full_name (str): The first and last name of the prospect.
        phone_number (str): The prospect's WhatsApp number.
        specific_need (str): A description of the core problem or pain point (BANT - Need).
        budget_range (str): The estimated budget range (e.g., "$1k-$5k", "Undefined").
        timeline_urgency (str): When they need the solution (e.g., "1 month", "Just browsing").
        company_name (str, optional): Name of the business. Defaults to "NA".
        industry (str, optional): The industry the business belongs to. Defaults to "NA".
        lead_status (str, optional): Status of the lead. Defaults to "Qualified - Hot Lead".
        source (str, optional): The origin of the lead. Defaults to "Meta_WA_Ad".
        conversation_summary (str, optional): A 1-sentence summary of the interaction.
        tool_context (ToolContext, optional): ADK context object (injected automatically).

    Returns:
        dict: A dictionary containing 'status' ('success' or 'error') and a 'message'.
              Example: {"status": "success", "message": "Lead ID 12345 created."}
    """
    
    if not bq_client:
        return {"status": "error", "message": "BigQuery client is not initialized."}

    # Construct table reference
    table_ref = f"{os.environ.get('GOOGLE_CLOUD_PROJECT')}.{BQ_DATASET_ID}.{BQ_TABLE_ID}"
    
    # Prepare the row data
    row_to_insert = [{
        "lead_status": lead_status,
        "source": source,
        "full_name": full_name,
        "phone_number": phone_number,
        "company_name": company_name,
        "industry": industry,
        "specific_need": specific_need,
        "budget_range": budget_range,
        "timeline_urgency": timeline_urgency,
        "conversation_summary": conversation_summary,
        "hand_off_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }]

    try:
        # Insert the row
        # Note: Ideally, check if dataset/table exists first or ensure it is created via Terraform/Console
        errors = bq_client.insert_rows_json(table_ref, row_to_insert)
        
        if errors == []:
            print(f"New lead inserted: {full_name}")
            return {"status": "success", "message": "Lead data successfully saved to BigQuery."}
        else:
            print(f"BigQuery Insert Errors: {errors}")
            return {"status": "error", "message": f"Failed to insert rows: {errors}"}
            
    except Exception as e:
        print(f"Exception during BigQuery insert: {e}")
        return {"status": "error", "message": f"System error during save: {str(e)}"}

# --- System Instructions ---

system_instruction_string = """
You are the **WhatsApp Lead Bot (WLB)**, a Lead Qualification Specialist for **Indosat Ooredoo Hutchison B2B**.

**CONTEXT & TRIGGER**
Your interaction starts when a user sends an inbound WhatsApp message, typically triggered by clicking a "Meta Ad" on Instagram or Facebook.

**YOUR OBJECTIVE**
Convert this inbound message into a **Sales Qualified Lead (SQL)** by collecting specific data points. Once collected, you must hand off the data to the backend system.

**PERSONA & TONE**
- **Tone:** Highly professional, efficient, friendly, and conversational.
- **Style:** Keep messages short (WhatsApp style). Use numbered lists for questions. Avoid excessive emojis.
- **Greeting:** Immediately acknowledge the ad source. Example: "Hi! Thanks for clicking on our ad. My name is [Name], I can get you connected to a specialist. I just need a few details."

**REQUIRED DATA (QUALIFICATION FIELDS)**
You must collect the following. Do not ask for everything at once; make it a conversation.
1. **Full_Name**: First and Last Name.
2. **Company_Name / Industry**: To check ICP fit.
3. **Specific_Need**: The core problem they are solving.
4. **Budget_Range**: A specific or estimated range.
5. **Timeline_Urgency**: When they need the solution.
*(Note: Phone Number is captured automatically by WhatsApp).*

**OPERATIONAL GUARDRAILS**
1. **DO NOT** discuss specific pricing, contract terms, or guaranteed delivery dates. Deflect these questions to the human specialist.
2. **DO NOT** attempt to close the sale yourself.
3. **DISQUALIFICATION:** If the user says they are "just browsing", "not interested", or "have no budget", politely thank them and mark the interaction as ended. Do NOT call the write_lead_to_bigquery tool.

**EXECUTION & HANDOFF**
1. Ask questions one by one or in pairs.
2. Once you have all 5 required fields, summarize them for the user to confirm.
3. **CRITICAL:** Upon confirmation, call the `write_lead_to_bigquery` tool immediately.
4. Only AFTER the tool returns "success", tell the user: "Great! I have securely saved your details. A human agent will reach out within the next business hour."
"""

# --- Agent Definition ---

root_agent = Agent(
    name="whatsapp_lead_bot",
    model="gemini-2.5-flash",
    description="Lead Qualification Specialist for Indosat Ooredoo Hutchison B2B",
    instruction=system_instruction_string,
    tools=[write_lead_to_bigquery]
)
