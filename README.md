# 🚀 WhatsApp Lead Bot (WLB)

**WhatsApp Lead Bot (WLB)** is an AI-powered qualification agent built.

It automates inbound WhatsApp conversations, performs full **BANT qualification**, and hands off only **high-intent SQL leads** to human sales teams.

Powered by:

- **Google Agent Development Kit (ADK)**
- **Gemini 2.5 Flash**
- **Firebase Firestore**
- **Google Cloud Secret Manager**

---

## ✨ Features

- **🔎 BANT Qualification**
    
    Automatically captures Budget, Authority (inferred), Need, and Timeline.
    
- **💾 Persistent State**
    
    Conversation progress and final lead data are securely saved in **Firestore**.
    
- **🔐 Secure Secrets**
    
    API keys and credentials retrieved on-demand from **Secret Manager**.
    
- **🛡 Guardrails & Validation**
    - Rejects pricing or contract discussions.
    - Identifies and disqualifies unqualified leads (e.g., “just looking”, “no budget”).
    - Ensures all required fields are collected before handoff.

---

## 📦 Tech Stack

| Component | Usage |
| --- | --- |
| **Python 3.10+** | Primary runtime |
| **Google ADK** | Agent orchestration |
| **Gemini 2.5 Flash** | LLM reasoning & dialog |
| **Firestore** | Lead persistence |
| **Secret Manager** | API key storage |
| **Google Cloud CLI** | Local auth |

---

## 🛠 Prerequisites

Before you begin, ensure you have:

- ✔ Python **3.10+**
- ✔ A **Google Cloud Project**
- ✔ **Firestore**, **Secret Manager**, and (optionally) **Vertex AI** enabled
- ✔ Installed & authenticated **Google Cloud CLI**
    
    ```bash
    gcloud auth application-default login
    
    ```
    

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourname/wlb.git
cd wlb_project

```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt

```

### 3️⃣ Configure Google Cloud

### **A. Firestore**

1. Open Firebase or GCP Console
2. Create a Firestore **Native mode** database
3. Ensure your local ADC user has write permissions

### **B. Secret Manager**

Create a secret named:

```
gemini-api-key

```

Add a new version with your actual **Google AI Studio** key.

### **C. Environment Variable**

```bash
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"

```

---

## ▶️ Running the Agent

Use the ADK web interface for local development and testing.

1. **Start ADK:**
    
    ```bash
    adk web
    
    ```
    
2. **Open browser:**
    
    [http://localhost:8000](http://localhost:8000/)
    
3. **Select the agent:**
    
    Choose `whatsapp_lead_bot`
    

---

## 📂 Project Structure

```
wlb_project/
├── requirements.txt         # Python dependencies
├── README.md                # This documentation
└── wlb_agent/
    ├── __init__.py          # Ensures config loads first
    ├── agent.py             # Persona, guardrails, LLM config
    ├── config.py            # Firestore + Secret Manager setup
    └── tools.py             # BANT logic & DB interactions

```

---

## 🧠 How It Works

### **1. update_lead_profile (tools.py)**

Continuously fills in the session profile (name, need, budget, timeline).

Identifies gaps and instructs the LLM to ask only what is missing.

### **2. disqualify_lead**

Triggered when:

- User expresses low/no intent
- Budget = 0
- Browsing only

Marks lead as *Disqualified* and gracefully ends the flow.

### **3. finalize_handoff**

Validates all required fields, then:

- Writes the structured lead JSON to Firestore
- Generates a final confirmation message
- Returns success metadata to ADK

---

## 🧱 Firestore Schema

A document is stored in the `leads` collection with the structure:

```json
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

```

---

## 🧪 Example Conversation Flow

1. User clicks a Meta ad
2. Bot greets with ad-aware acknowledgement
3. Bot captures Need → Budget → Timeline
4. If qualified → saved to Firestore → forwarded to human sales
5. If not → politely disqualified

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
