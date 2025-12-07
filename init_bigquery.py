import os
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

# Configuration
DATASET_NAME = "lead_data"
TABLE_NAME = "sql_leads"

def create_resources():
    # 1. Get Project ID from Environment
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        # Fallback for Cloud Shell if env var isn't set manually yet
        import google.auth
        _, project_id = google.auth.default()
    
    print(f"Initializing BigQuery for Project: {project_id}")
    client = bigquery.Client(project=project_id)

    # 2. Create Dataset
    dataset_id = f"{project_id}.{DATASET_NAME}"
    try:
        client.get_dataset(dataset_id)
        print(f"✅ Dataset {dataset_id} already exists.")
    except NotFound:
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"  # Adjust location if needed (e.g., "asia-southeast2" for Jakarta)
        dataset = client.create_dataset(dataset, timeout=30)
        print(f"🎉 Created dataset {client.project}.{dataset.dataset_id}")

    # 3. Create Table
    table_id = f"{dataset_id}.{TABLE_NAME}"
    
    # Define Schema based on Agent Tool arguments
    schema = [
        bigquery.SchemaField("lead_status", "STRING"),
        bigquery.SchemaField("source", "STRING"),
        bigquery.SchemaField("full_name", "STRING"),
        bigquery.SchemaField("phone_number", "STRING"),
        bigquery.SchemaField("company_name", "STRING"),
        bigquery.SchemaField("industry", "STRING"),
        bigquery.SchemaField("specific_need", "STRING"),
        bigquery.SchemaField("budget_range", "STRING"),
        bigquery.SchemaField("timeline_urgency", "STRING"),
        bigquery.SchemaField("conversation_summary", "STRING"),
        bigquery.SchemaField("hand_off_timestamp", "TIMESTAMP"), # Supports ISO format strings
    ]

    try:
        client.get_table(table_id)
        print(f"✅ Table {table_id} already exists.")
    except NotFound:
        table = bigquery.Table(table_id, schema=schema)
        table = client.create_table(table)
        print(f"🎉 Created table {table.project}.{table.dataset_id}.{table.table_id}")

if __name__ == "__main__":
    create_resources()
