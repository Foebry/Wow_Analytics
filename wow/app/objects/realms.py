"""Realms functionality"""

import os


class Realm:
    """ """

    def __init__(self, _id, db, logger, request, store=True, region=False):
        """
            Realm constructor. Takes in 4 argument
                :arg: _id -> int
                :arg: name -> string
                :arg: db -> obj<Database>
                :arg: logger -> obj<Logger>
        """
        self.id = _id
        self.store = store
        self.name = request.getRealmData(condition=("id", self.id))["name"]
        self.output = self.setOutputFile(request, region)
        self.database = db
        self.logger = logger
        self.auctions = {}
        self.previous_auctions = {}

        query = "select * from responses where realm_id = {}".format(self.id)
        not_set = db.get(query) is None

        if not_set:
            self.insert()
            self.last_modified = None
            return
        self.last_modified = db.get(query)[1]



    def update(self):
        query = """
                    update responses
                        set previous_response = "{}"
                        where realm_id = {}
                """.format(self.last_modified, self.id)
        self.database.update(query)


    def insert(self):
        query = """
                    insert into responses(realm_id)
                        values({})
                """.format(self.id)

        self.database.write(query)


    def exportData(self, operation, open_time, close_time):
        from datetime import datetime

        now = datetime.now()
        now = round(datetime.timestamp(now))
        open_time = round(datetime.timestamp(open_time))
        close_time = round(datetime.timestamp(close_time))

        space = " "
        data = ""

        with open(self.output, 'r') as file:
            data = file.read()[:-1]
            data += "\n {} {} \n{}".format(now, '{\n', space*3)
            data += "{}\n{}".format(open_time, space*3)
            data += "{}\n{}".format(close_time, space*3)
            for item in operation.export_items:
                data += "{} {}\n{}".format(item.id, '{', space*6)
                data += "open = {},\n{}".format(item.open, space*6)
                data += "low = {},\n{}".format(item.low, space*6)
                data += "high = {},\n{}".format(item.high, space*6)
                data += "close = {},\n{}".format(item.close, space*6)
                data += "amount = {},\n{}".format(item.amount, space*3)
            data += "}\n}"

        with open(self.output, 'w') as file:
            file.write(data)


    def setOutputFile(self, request, region):
        """

        """
        if self.store is False: return None

        slug = request.getRealmData(("id", self.id))["slug"]
        location = "D://Games//World of Warcraft//_retail_//Interface//AddOns//wow_analytics//"
        extension = ".lua"

        outputfile = location + slug + extension

        if not os.path.exists(outputfile):
            with open(outputfile, 'a') as file:
                file.write("{}")

        return outputfile



    def setAuctionData(self, response, operation, request, test=False):
        """
            Setting auction data from getAuctionData response. Takes in 3 arguments:
            :arg response,
            :arg operation: <Operation>,
            :arg live_data: dict,
            :arg previous_auctions: dict
        """

        from operations import setTimeSold, setTimePosted
        from auctions import Auction

        auction_data = []

        for auction in response:
            auction_id = auction["id"]
            item_id = auction["item"]["id"]
            pet = {"id_":0}

            if item_id == 82800:
                pet = {"id_":auction["item"]["pet_species_id"], "quality":auction["item"]["pet_quality_id"], "level":auction["item"]["pet_level"], "breed_id":auction["item"]["pet_breed_id"]}

            quantity = auction["quantity"]
            time_left = auction["time_left"]

            # all are given
            if "unit_price" in auction and "bid" in auction and "buyout" in auction:
                unit_price = auction["unit_price"] / 10000
                bid = auction["bid"] / 10000
                buyout = auction["buyout"] / 10000

            # bid is missing -> bid = -1
            elif "unit_price" in auction and "buyout" in auction and "bid" not in auctions:
                unit_price = auction["unit_price"] / 10000
                buyout = auction["buyout"] / 10000
                bid = -1

            # unit_price is missing -> unit_price = buyout / quantity
            elif "buyout" in auction and "bid" in auction and "unit_price" not in auction:
                buyout = auction["buyout"] / 10000
                bid = auction["bid"] / 10000
                unit_price = buyout / quantity

            # buyout is missing -> buyout = -1
            elif "unit_price" in auction and "bid" in auction and "buyout" not in auction:
                unit_price = auction["unit_price"] / 10000
                bid = auction["bid"] / 10000
                buyout = -1

            # buyout AND bid are missing -> buyout = unit_price*quantity, bid = -1
            elif "unit_price" in auction and "bid" not in auction and "buyout" not in auction:
                unit_price = auction["unit_price"] / 10000
                bid = -1
                buyout = unit_price * quantity

            # bid and unit_price are missing -> unit_price = buyout / quantity, bid = -1
            elif "buyout" in auction and "unit_price" not in auction and "bid" not in auction:
                buyout = auction["buyout"] / 10000
                unit_price = buyout / quantity
                bid = -1

            # buyout AND unit_price are missing -> buyout = -1, unit_price = bid / quantity
            elif "bid" in auction and "unit_price" not in auction and "buyout" not in auction:
                bid = auction["bid"] / 10000
                unit_price = bid / quantity
                buyout = -1

            args = (auction_id, item_id, pet, quantity, unit_price, time_left, bid, buyout)
            auction = Auction(self, operation, request, test, *args)

            print("{}/{} auctions handled".format(len(auction_data), len(response)), end='\r')
            # for testing purposes
            auction_data.append(auction)
        # for testing purposes
        return auction_data
