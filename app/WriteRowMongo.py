import pymongo


class WriteRowMongo:
    def open(self, URI, partition_id, epoch_id):
        self.myclient = pymongo.MongoClient(URI)
        self.mydb = self.myclient["electricity_prod"]
        self.mycol = self.mydb["streaming_data"]
        return True

    def process(self, row):
        self.mycol.insert_one(row.asDict())

    def close(self, error):
        self.myclient.close()
        return True
