# 🚀 WhatsApp Lead Bot (WLB)

**WhatsApp Lead Bot (WLB)** is an AI-powered qualification agent built for **Indosat Ooredoo Hutchison B2B**.

It automates inbound WhatsApp conversations, performs full **BANT qualification**, and hands off only **high-intent Sales Qualified Leads (SQLs)** to human sales teams.

The bot stores data in:

- **Firestore** → tracks conversation & state
- **BigQuery** → stores structured SQL leads
- **Google Sheets** → provides a clean, real-time dashboard for sales teams

Powered by:

- Google Agent Development Kit (ADK)
- Gemini 2.5 Flash
- Firebase Firestore
- BigQuery
- Google Cloud Secret Manager

---

## ✨ Features

### 🔍 Automated BANT Qualification

Captures Budget, Authority (inferred), Need, and Timeline through natural WhatsApp conversation.

### 💾 Hybrid Storage Architecture

- **Firestore**: conversational state & incremental lead data
- **BigQuery**: clean, normalized SQL lead records
- **Google Sheets**: human-friendly reporting layer for sales agents

### 🔐 Secure by Design

Secrets (API keys, service credentials) are retrieved from **Google Cloud Secret Manager** — never hardcoded.

### 🛡 Guardrails

- Prevents bot from discussing pricing or contracts
- Disqualifies low-intent / no-budget leads
- Ensures required fields are collected before saving to BigQuery
- Maintains a polite, concise, human-like persona appropriate for WhatsApp

---

## 📦 Tech Stack Overview

| Component | Role |
| --- | --- |
| **Google ADK** | Agent orchestration |
| **Gemini 2.5 Flash** | Dialog reasoning |
| **Firestore** | State persistence |
| **BigQuery** | Lead warehouse |
| **Google Sheets** | Sales dashboards |
| **Secret Manager** | Secure API key storage |
| **Python 3.10+** | Runtime |

---

## 🛠 Prerequisites

Before setup, ensure you have:

- A Google Cloud Project
- Firestore, BigQuery, Secret Manager, and (optional) Vertex AI APIs enabled
- Google Cloud CLI installed and authenticated
- Python 3.10 or higher

You will also need to configure the following:

- A Firestore database in **Native mode**
- A Secret in **Secret Manager** to store your Gemini API key
- A BigQuery dataset and table for SQL leads (`lead_data.sql_leads`)
- Google Sheets access connected to BigQuery for your sales team

---

## ⚙️ Setup Steps

### 1️⃣ Repository Setup

Clone the project and install dependencies.

### 2️⃣ Google Cloud Configuration

- Set up Firestore
- Create your Secret Manager entry
- Configure BigQuery dataset & table
- Set up service account permissions if running outside Cloud Shell or ADC

### 3️⃣ Running the Agent

Use the ADK web interface:

1. Start the ADK server
2. Open the local UI
3. Select **whatsapp_lead_bot**
4. Start testing conversations

---

## 📂 Project Structure

```
wlb_project/
├── README.md                # Documentation (this file)
├── requirements.txt         # Python dependencies
├── create_resources.py      # BigQuery setup script (no code shown here)
└── wlb_agent/
    ├── agent.py             # Persona, system prompts, guardrails
    ├── config.py            # Firestore, BigQuery & Secret Manager config
    ├── tools.py             # BANT logic + DB write tools
    └── __init__.py          # Ensures config loads before agent startup

```

---

## 🧠 How It Works

### Step 1: Intake & Slot Filling

The agent gathers user information in a structured way (name, company, need, budget, timeline). Missing fields trigger follow-up questions.

### Step 2: Qualification

Guardrails determine whether the lead is:

- **Qualified – Hot Lead**
- **Medium Intent**
- **Disqualified**

### Step 3: Data Persistence

When ready:

- Firestore stores the conversation context
- BigQuery receives a clean SQL lead row (via the `lead_data.sql_leads` table)
- Google Sheets gives the sales team a live, filterable view of leads via BigQuery → Sheets connector

### Step 4: Handoff

The bot notifies the user that a sales agent will contact them and finalizes the lead record.

---

## 🧱 Data Models

### Firestore (Lead Documents)

Used for incremental lead capture and conversation state tracking.

### BigQuery (Sales Qualified Leads)

The BigQuery table acts as a warehouse for human sales teams and analytics.

It contains fields such as:

- Lead status
- Name, phone number
- Company & industry
- Specific need
- Budget range
- Timeline urgency
- Conversation summary
- Timestamp

### Google Sheets (Sales Dashboard)

Designed for daily use by sales teams:

- Pulls data directly from BigQuery
- Provides real-time filtering, sorting, notes, and follow-up tracking
- Can be extended with Looker Studio dashboards for management

---

## 📊 Sales Team Workflow

1. Lead arrives through WhatsApp
2. WLB qualifies and stores data in BigQuery
3. Sales agents open the connected Google Sheets
4. They use filters such as:
    - Industry
    - Timeline urgency
    - Budget range
    - Lead source
5. Agents update follow-up status directly in Sheets

This removes manual data entry and ensures marketing → sales alignment.

---

---

## 🤝 Contributing

Pull requests are welcome!

If you’d like to improve logic, add tools, or expand qualification methods:

1. Fork the repo
2. Create a feature branch
3. Submit a PR

---

## 📄 License

MIT License — feel free to use and adapt for your own projects.

---

## 📬 Contact

For questions, support, or collaboration opportunities:

**muhammad@borobudur.ai**
