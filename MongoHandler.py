import pymongo


class MongoHandler():

    def __init__(self, mongo_connection: str, database_name: str):
        myclient = pymongo.MongoClient(mongo_connection)
        self.db_client = myclient[database_name]

    def get_client(self):
        """Returns the MongoDB client.

        Parameters
        ----------


        Returns
        -------
        MongoClient
            Return db client.

        """
        return self.db_client
