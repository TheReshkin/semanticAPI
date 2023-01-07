import pymongo
from pymongo import MongoClient

# Create the client
client = MongoClient('localhost', 27017)

# Connect to our database
db = client['Users']

# Fetch our series collection
exercises_collection = db['exercises']
users_collection = db['user']


def insert_collection(collection, data):
    """ Function to insert a document into a collection and
    return the document's id.
    """
    return collection.insert_one(data).inserted_id


def find_collection(collection, elements, multiple=False):
    """ Function to retrieve single or multiple documents from a provided
    Collection using a dictionary containing a document's elements.
    """
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)


def update_collection(collection, query_elements, new_values):
    """ Function to update a single document in a collection.
    """
    collection.update_one(query_elements, {'$set': new_values})
