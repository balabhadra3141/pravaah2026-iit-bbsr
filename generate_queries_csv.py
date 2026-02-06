# generate_queries_csv.py

import csv
from pipeline import CausalPipeline

# Initialize the pipeline
pipeline = CausalPipeline()

# Define queries across multiple domains
queries = [
    # Healthcare domain
    {"id": 1, "query": "Why are customers escalating in healthcare calls?", "category": "Healthcare", "remarks": "Initial query"},
    {"id": 2, "query": "Which healthcare issues lead to the most customer complaints?", "category": "Healthcare", "remarks": "Initial query"},
    {"id": 3, "query": "How often do appointment scheduling errors cause escalations?", "category": "Healthcare", "remarks": "Initial query"},
    {"id": 4, "query": "What are the main reasons for patient dissatisfaction?", "category": "Healthcare", "remarks": "Initial query"},
    {"id": 5, "query": "Are escalations more frequent in billing or service quality?", "category": "Healthcare", "remarks": "Follow-up analysis"},

    # Telecom domain
    {"id": 6, "query": "Why do telecom customers cancel subscriptions?", "category": "Telecom", "remarks": "Initial query"},
    {"id": 7, "query": "Which factors cause repeated billing disputes in telecom?", "category": "Telecom", "remarks": "Initial query"},
    {"id": 8, "query": "Why do customers escalate when facing service outages?", "category": "Telecom", "remarks": "Follow-up analysis"},
    {"id": 9, "query": "How frequently are technical issues the reason for complaints?", "category": "Telecom", "remarks": "Initial query"},
    {"id": 10, "query": "Which telecom plans have the most escalations?", "category": "Telecom", "remarks": "Follow-up analysis"},

    # Banking domain
    {"id": 11, "query": "Why are banking customers requesting manager intervention?", "category": "Banking", "remarks": "Initial query"},
    {"id": 12, "query": "Which banking complaints result in dispute escalation?", "category": "Banking", "remarks": "Initial query"},
    {"id": 13, "query": "Do delays in transaction resolution cause more escalations?", "category": "Banking", "remarks": "Follow-up analysis"},
    {"id": 14, "query": "How often do account issues lead to customer dissatisfaction?", "category": "Banking", "remarks": "Initial query"},
    {"id": 15, "query": "Are customer support delays a major reason for escalation?", "category": "Banking", "remarks": "Follow-up analysis"},

    # Retail domain
    {"id": 16, "query": "Why do retail customers escalate regarding delivery issues?", "category": "Retail", "remarks": "Initial query"},
    {"id": 17, "query": "Which product categories generate the most complaints?", "category": "Retail", "remarks": "Initial query"},
    {"id": 18, "query": "Are refund delays the primary cause of escalations?", "category": "Retail", "remarks": "Follow-up analysis"},
    {"id": 19, "query": "Do repeated order mistakes increase escalation rates?", "category": "Retail", "remarks": "Initial query"},
    {"id": 20, "query": "Which customer service practices reduce escalations effectively?", "category": "Retail", "remarks": "Follow-up analysis"},
]

# Output CSV file
output_file = "hackathon_queries.csv"

# Open CSV file and write results
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Query Id", "Query", "Query Category", "System Output", "Remarks"])
    writer.writeheader()

    for q in queries:
        print(f"Processing Query ID {q['id']}: {q['query']} ...")
        try:
            # Run query through your pipeline
            system_output = pipeline.run_query(q["query"])
        except Exception as e:
            system_output = f"Error: {str(e)}"

        # Convert output to string for CSV
        if isinstance(system_output, dict):
            # Optional: summarize JSON output to keep CSV readable
            system_output = str(system_output)

        # Write row to CSV
        writer.writerow({
            "Query Id": q["id"],
            "Query": q["query"],
            "Query Category": q["category"],
            "System Output": system_output,
            "Remarks": q["remarks"]
        })

print(f"✅ Queries processed and saved to {output_file}")
