from mongo_utils import get_db, store_doc_if_not_exists 
import csv

# Connect to MongoDB
db = get_db()

collection_name = "job_apps"



def csv_to_docs(csv_file_path):

    docs = []

    with open(csv_file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert empty strings to None (optional helper)
            doc = {k: (v if v.strip() != "" else None) for k, v in row.items()}
            docs.append(doc)

    return docs

#---------Storing by CSV file of new job application data
store_doc_if_not_exists(collection_name, db, csv_to_docs("ApprovedLMIAData_Installation_Assembly_Manufacturing.csv"))
