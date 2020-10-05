import pymongo 

class MongoDB: 
    """
    Mongodb Configuration 
    """
    def __init__(self, uri, database_name, collection_name): 
        """
        Init the database configuration
        """
        self.client = pymongo.MongoClient(uri)
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]
        self.database_name = database_name
        self.collection_name = collection_name


    def _insert(self, document): 
        """
        Insert document 
        """
        try :
            self.collection.insert_one(document)
        except : 
            print("ERROR : _insert")

    def _update(self, _filter, update_data, upsert, many): 
        """
        Update document based on _filter with update_date
        upsert : Bool 
        many : Bool
        """
        try : 
            if (many == False) : 
                self.collection.update_one(_filter,update_data,upsert=upsert)
            if (many == True):
                self.collection.update_many(_filter, update_data,upsert=upsert)
        except : 
            print("ERROR : _update")

    def _find(self, _filter): 
        """
        Find documents base on _filter condition 
        """
        try : 
            cursor = self.collection.find(_filter)
            return cursor 
        except : 
            print("ERROR : _find")
            return None   

    def _process_cursor(self, cursor): 
        try : 
            for doc in cursor :
                print(doc)
        except : 
            print("ERROR : _process_cursor")


