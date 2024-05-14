#!/usr/bin/env python3
"""returns the list of school having a specific topic"""


from pymongo import MongoClient
list_all = __import__('8-all').list_all
insert_school = __import__('9-insert_school').insert_school
schools_by_topic = __import__('11-schools_by_topic').schools_by_topic

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_db = client.logs.nginx

    print("{} logs".format(logs_db.estimated_document_count()))
    print("Methods:")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = logs_db.count_documents({'method': method})
        print("\tmethod {}: {}".format(method, count))

    documents_get = logs_db.count_documents(
        {'method': 'GET', 'path': "/status"})
    print("{} status check".format(documents_get))

    print("IPs:")
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = list(logs_db.aggregate(pipeline))
    for ip in top_ips:
        print("\t{}: {}".format(ip["_id"], ip["count"]))
