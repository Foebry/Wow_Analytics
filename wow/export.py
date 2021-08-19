"""
This is the program to to create a snapshot of a database,
exporting all schemas unto seperate csv files.
"""

from databases.Database import Database
from logger.Logger import Logger
from config import DATABASE

import datetime
import os

logger = Logger(os.getcwd())
db = Database(DATABASE, logger)

get_tables_query = """SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='wow' """
tables = db.get(get_tables_query, all=True)

for table in tables:
    name = table[0]
    if name in ("auctionhouses", "item_prices", "items", "soldauctions"): continue

    if name == "soldauctions":
        limit = datetime.datetime.now() - datetime.timedelta(hours=50)
        data = db.get("select * from {} where time_sold > '{}'".format(name, limit), all=True)

        for row in data:
            file = open("C://Users//Rain_//Desktop//{}.txt".format(name), "a")
            file.write(str(row))
            file.write("\n")
            file.close()

    count = "id"
    if name == "responses": count = "realm_id"
    elif name == "pets": count = "ID"
    rows = db.get("select count({}) from {}".format(count, name))[0]
    offset = 0
    limit = 10000

    from math import ceil
    times = ceil(rows/limit)
    print("{} times for {}".format(times, name))
    for _ in range(times):
        data = db.get("select * from {}".format(name, offset, limit), all=True)
        rows = len(data)
        print("{} rows for {}".format(rows, name))
        for row in data:
            file = open("C://Users//Rain_//Desktop//{}.txt".format(name), "a")
            file.write(str(row))
            file.write("\n")
            file.close()
        offset += limit
