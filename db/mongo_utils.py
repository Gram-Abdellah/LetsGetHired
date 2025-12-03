from pymongo import MongoClient
from datetime import datetime, timedelta 
import os
# -------------------------------
# 1️⃣ Connect to MongoDB
def get_db(uri="mongodb+srv://abdellahgram01_db_user:G3qStRgzhFZajEco@cluster0.yo1fmrw.mongodb.net/?appName=Cluster0",
            db_name="job_bank"):
    client = MongoClient(uri)
    db = client[db_name]
    return db

def load_all_docs(collection_name, db):
    """
    Load all documents from a MongoDB collection
    """
    collection = db[collection_name]
    return list(collection.find())

def store_doc_if_not_exists(collection_name, db, docs):
    """
    Store a document if no document exists with the same ID or URL.
    """
    collection = db[collection_name]

    for doc in docs:
        # Ensure doc has both ID and URL
        if "ID" not in doc or "URL" not in doc:
            print("Error: Document must have both 'ID' and 'URL'.")
            pass

        # Check if a document with same ID or URL exists
        query = {"$or": [{"ID": doc.get("ID")}, {"URL": doc.get("URL")}]}
        existing = collection.find_one(query)

        if existing:
            print(f"Document with ID={doc.get('ID')} or URL={doc.get('URL')} already exists. Skipping.")
            
        else:
            collection.insert_one(doc)
            print(f"Document with ID={doc.get('ID')} inserted successfully.")
            
def get_not_sent_today(db ,collection_name):

    # Connect
    col = db[collection_name]

    # Today in MM/DD/YYYY format
    today = f"{datetime.now().month}/{datetime.now().day}/{datetime.now().year}"
    

    # MongoDB query
    query = {
        "Is_sent": "Not Sent",
        "Sending_date": today
    }

    docs = list(col.find(query))
    return docs

def get_not_sent_ready_today(db ,collection_name):

    # Connect
    col = db[collection_name]

    # Today in MM/DD/YYYY format
    today = f"{datetime.now().month}/{datetime.now().day}/{datetime.now().year}"
    

    # MongoDB query
    query = {
        "Is_sent": "Not Sent",
        "Sending_date": today,
        "Status": "ready",
    }

    
    docs = list(col.find(query).limit(19))
    return docs
 
def update_status_based_on_fields(db, collection_name, docs):
    col = db[collection_name]

    # List of required properties
    required_fields = [
        "Email",
        "Subject",
        "Resume_path",
        "Cover_letter",
        "Email_template",
    ]

    for doc in docs:
        # Check if all required fields exist and not empty
        is_ready = True
        for field in required_fields:
            if field not in doc or doc[field] is None or doc[field] == "":
                is_ready = False
                break

        new_status = "ready" if is_ready else "not ready"

        # Update the document in MongoDB
        col.update_one(
            {"_id": doc["_id"]},
            {"$set": {"Status": new_status}}
        )

        print(f"Updated ID={doc.get('ID', 'UNKNOWN')} → Status = {new_status}")

def get_and_reschedule_not_sent_today(db, collection_name):
    col = db[collection_name]

    # Format today and tomorrow in MM/DD/YYYY
    today = datetime.now()
    today_str = today.strftime("%m/%d/%Y")
    tomorrow_str = (today + timedelta(days=1)).strftime("%m/%d/%Y")

    # Query for documents not sent today
    query = {
        "Status": "ready",
        "Sending_date": today_str
    }

    # Find and reschedule
    docs = list(col.find(query).limit(19))
    for doc in docs:
        col.update_one({"_id": doc["_id"]}, {"$set": {"Sending_date": tomorrow_str}})

    return docs

def delete_today_sent_cover_letters(db, collection_name):
    """
    Find all documents where Is_sent = 'Sent' and Sending_date = today,
    then delete the file located at doc['Cover_letter'].
    """
    col = db[collection_name]

    # Today format MM/DD/YYYY — same format used in your DB
    today = f"{datetime.now().month}/{datetime.now().day}/{datetime.now().year}"

    # Query sent documents for today
    query = {
        "Is_sent": "Sent",
        "Sending_date": today
    }

    docs = list(col.find(query))

    if not docs:
        print("No sent documents for today found.")
        return

    for d in docs:
        file_path_cl = d.get("Cover_letter")
        file_path_cv = d.get("Cover_letter")

        if not file_path_cl:
            print(f"Document {d.get('ID')} has no Cover_letter field.")
            continue
        if not file_path_cv:
            print(f"Document {d.get('ID')} has no Resume field.")
            continue

        # Ensure correct path (strip spaces)
        file_path_cl = file_path_cl.strip()
        # Ensure correct path (strip spaces)
        file_path_cv = file_path_cv.strip()

        # Delete file if exists
        if os.path.exists(file_path_cl):
            try:
                os.remove(file_path_cl)
                print(f"Deleted cover letter: {file_path_cl}")
            except Exception as e:
                print(f"Error deleting {file_path_cl}: {e}")
        else:
            print(f"File not found: {file_path_cl}")
        
        # Delete file if exists
        if os.path.exists(file_path_cv):
            try:
                os.remove(file_path_cv)
                print(f"Deleted Resume: {file_path_cv}")
            except Exception as e:
                print(f"Error deleting {file_path_cv}: {e}")
        else:
            print(f"File not found: {file_path_cv}")
