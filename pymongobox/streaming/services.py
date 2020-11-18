import pymongo 
import json 
from bson.json_util import dumps 
import multiprocessing as mp 
from multiprocessing import Pool 
import types
import json
from datetime import datetime

class Stream:
    """
    a Stream is listening on a mongoDB collection. 
    When receiving a log, the stream executes a custom process on the log. 
    """

    def __init__(self, uri , database_name , collection_name , custom_method):
        """
        Init the stream configuration 
        """
        self.client = pymongo.MongoClient(uri)
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]
        self.database_name = database_name
        self.collection_name = collection_name
        self.custom_method = custom_method

    def stream(self): 
        """
        Init the stream 
        """
        self.change_stream = self.collection.watch()
        for self.change_stream_document in self.change_stream : 
            self.documentKey = str( self.change_stream_document["documentKey"]["_id"])
            self.operationType  = self.change_stream_document["operationType"]
            self.cs_db = self.change_stream_document["ns"]["db"]
            self.cs_coll = self.change_stream_document["ns"]["coll"]

            self.process()

    def process(self): 
        """
        Process the output of the stream
        """
        oplog = {
                "documentKey":self.documentKey,
                "operationType":self.operationType,
                "database":self.cs_db,
                "collection":self.cs_coll
                }

        if (self.custom_method == None):
            self.log("info", json.dumps(oplog, indent=2))
            print('')
        else :
            if isinstance(self.custom_method, types.FunctionType):
                self.custom_method(**oplog)

    def log(self, level, message):

        """
        Method to generate & display logs
        """

        level = level.upper()
        now = datetime.now()
        log_date = now.strftime("%d/%m/%Y %H:%M:%S")

        log = "{} : {} : {}".format(log_date, level, message)
        print(log)


class Worker:
    """
    Worker init a pool of stream, and run each stream in parallel. 
    """

    def __init__(self,cpu_count, stream_config) : 
        """
        Init Worker configuration
        """
        self.cpu_count = cpu_count
        self.stream_config = stream_config

    def pool_worker(self,config): 
        """
        pool_worker is the task called in each thread 
        """
        if ( len(config)== 4): 
            self.input_stream = Stream(config[0], config[1], config[2], config[3])
        else : 
            self.input_stream = Stream(config[0], config[1], config[2], None)
        print("Worker.pool_worker : start stream on collection :", self.input_stream.collection_name)
        self.input_stream.stream()

    def pool_handler(self): 
        """
        Init and run the pool of tasks 
        """
        print("worker.pool_handler : Init and start of a pool ... ")
        p = Pool(self.cpu_count)
        p.map(self.pool_worker, self.stream_config)


