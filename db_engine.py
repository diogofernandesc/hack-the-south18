import logging
import os

from pymongo import MongoClient, bulk
from pymongo.errors import DuplicateKeyError

from cons import DB

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


class DBConnection(object):
    def __init__(self):
        self.client = MongoClient("mongodb://%s:%s@%s:27017" % (
            os.getenv("USER_MONGO"),
            os.getenv("PASS_MONGO"),
            os.getenv("ADDRESS_MONGO")
            ))

        # Testing:
        # self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client.spock
        self.bulkWrite = []
        self.logger = logging.getLogger(__name__)


    def start_bulk_upsert(self, collection):
        bulk = self.db[collection].initialize_ordered_bulk_op()
        return bulk

    def add_to_bulk_upsert(self, query, data, bulk_op):
        result = bulk_op.find(query).upsert().update({"$set": data})
        return result

    def add_to_bulk_upsert_push(self, query, field, value, bulk_op):
        result = bulk_op.find(query).upsert().update({"$push": {field: value}})
        return result

    def add_to_bulk_upsert_addtoset(self, query, field, value, bulk_op):
        result = bulk_op.find(query).upsert().update({"$addToSet": {field: value}})
        return result

    def end_bulk_upsert(self, bulk_op):
        results = bulk_op.execute()
        return results

    def insert_news_article(self, article):
        news_collection = self.db.news_articles
        try:
            result = news_collection.update_one(filter={"url": article["url"]}, update={"$set": article}, upsert=True)
        except DuplicateKeyError as e:
            pass

    def apply_field_to_all(self, field, value, collection):
        result = self.db[collection].update_many({}, {'$set': {field: value}}, upsert=True)
        self.logger.info(result.matched_count)

    def insert(self, document):
        self.db[DB.SPOILERS].insert_one(document)

    def start_bulk_write(self):
        self.bulkWrite = []

    def end_bulk_write(self, collection, ordered=False):
        try:
            self.db[collection].bulk_write(self.bulkWrite, ordered=ordered)
            self.bulkWrite = []
        except self.client.BulkWriteError as bwe:
            self.logger.warning(bwe.details)

    def find_document(self, collection, filter=None, projection=None, limit=0, sort=False, sort_field=None):
        if sort:
            return self.db[collection].find(filter=filter, projection=projection, no_cursor_timeout=True,
                                            limit=limit).sort(sort_field, -1)
        else:
            return self.db[collection].find(filter=filter, projection=projection, no_cursor_timeout=True,  limit=limit)

    def find_and_update(self, collection, query=None, update=None, multi=False):
        result = self.db[collection].update_one(query, update, upsert=True)
        return result

    def increment_field(self, collection, query, field):
        result = self.db[collection].update_one(query, update={"$inc": {field: 1}}, upsert=True)
        return result

    def close(self):
        self.client.close()