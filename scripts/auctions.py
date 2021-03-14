"""auctions functionality"""
from datetime import datetime
from Wow_Analytics.scripts.functions import setTimePosted, setTimeSold
from Wow_Analytics.scripts.items import Item
import datetime
import random



class Auction():
    """docstring"""
    def __init__(self, live_data, previous_auctions, insert_data, update_data, *args, **kwargs):
        """Auction constructor. Takes in 7 args. Always needs 6 arguments, so either args or kwargs need to be given:
            :arg live_data: dict,
            :arg previous_auctions: dict,
            :arg insert_data: dict,
            :arg update_data: dict,
            :arg sold_data: dict,
            :arg *args: list (optional),
            :arg **kwargs: dict (optional)"""

        if kwargs:
            self.id = kwargs["id"]
            self.realm_id = kwargs["realm_id"]
            self.item_id = kwargs["item_id"]
            self.pet_id = kwargs["pet_id"]
            self.quantity = kwargs["quantity"]
            self.unit_price = kwargs["unit_price"]
            self.time_left = kwargs["time_left"]
            self.bid = kwargs["bid"]
            self.buyout = kwargs["buyout"]
            self.time_posted = kwargs["time_posted"]
            self.last_updated = kwargs["last_updated"]
            # self.Item = kwargs["Item"]
        else:
            self.realm_id = args[0]
            self.id = args[1]
            self.item_id = args[2]
            self.pet_id = args[3]
            self.quantity = args[4]
            self.unit_price = args[5]
            self.time_left = args[6]
            self.bid = args[7]
            self.buyout = args[8]
            self.time_posted = setTimePosted()
            self.last_updated = self.time_posted

            # very 1st new pet
            if self.item_id == 82800 and self.id not in live_data["items"]:
                item = Item(request, self.id, self.pet_id)
                live_data["items"][self.item_id] = {}
                live_Data["items"][self.item_id][self.pet_id]["id"] = item
                self.Item = item
            # pet
            elif self.item_id == 82800 and self.id in live_data["items"]:
                # existing pet
                if self.pet_id["id"] in live_data["items"][self.id]:
                    self.Item = live_data["items"][self.id][self.pet_id["id"]]
                # new pet
                else:
                    item = Item(request, self.id, self.pet_id)
                    live_data["items"][self.id][self.pet_id["id"]] = item
                    self.Item = item
            # new item
            elif not self.item_id == 82800 and self.id not in live_data["items"]:
                item = Item(request, self.item_id)
                live_data["items"] = item
                self.Item = item
            # existing item
            else: self.Item = live_data["items"][self.item_id]


        # If auction_id is not yet in previous_auctions -> add it to live_auctions
        if self.id not in previous_auctions[self.realm_id]:
            live_data["auctions"][self.realm_id][self.id] = self

            # setting auction to be inserted
            if "auctions" in insert_data:
                if self.realm_id in insert_data["auctions"]:
                    insert_data["auctions"][self.realm_id].append(self)
                else:
                    insert_data["auctions"][self.realm_id] = [self]
            else:
                insert_data["auctions"] = {}
                insert_data["auctions"][self.realm_id] = [self]

        # if auction_id is already in previous_auctions -> insert into live_auctions
        else: self.update(live_data, previous_auctions, update_data, insert_data, live_data["auctions"][self.realm_id][self.id], self)


    @staticmethod
    def update(live_data, previous_auctions, update_data, insert_data, existing, new):
        """Updating live_data, update_data dictionaries and possibly insert_data"""

        # calculate sold_quantity, new buyout of sold_quantity and bid of sold_quantity
        sold_quantity = existing.quantity - new.quantity
        buyout = existing.unit_price * sold_quantity
        bid = existing.bid * sold_quantity

        # new time_posted = existing time_posted
        new.time_posted = existing.time_posted
        new.last_updated = setTimePosted(posted=new.time_posted)

        if sold_quantity > 0:
            # create sold_auction
            args = (new.realm_id, new.id, existing.item_id, new.pet_id, sold_quantity, new.unit_price, new.time_left, bid, buyout, new.time_posted, True)
            sold_auction = SoldAuction(insert_data, *args)

        # remove auction_id from previous_auctions
        del previous_auctions[new.realm_id][new.id]

        # add to live_data
        live_data["auctions"][new.realm_id][new.id] = new

        # adding auction to be updated
        if "auctions" in update_data:
            if new.realm_id in update_data["auctions"]: update_data["auctions"][new.realm_id].append(new)
            else:
                update_data["auctions"][new.realm_id] = [new]
        else:
            update_data["auctions"] = {}
            update_data["auctions"][new.realm_id] = [new]



class SoldAuction():
    """docstring"""
    def __init__(self, insert_data, *args):
        """Constructor for sold auctions. Takes in 1 argument:
            :arg *args: list"""
        self.id = args[1]
        self.realm_id = args[0]
        self.item_id = args[2]
        self.pet_id = args[3]
        self.quantity = args[4]
        self.unit_price = args[5]
        self.time_left = args[6]
        self.bid = args[7]
        self.buyout = args[8]
        self.time_posted = args[9]
        self.time_sold = setTimeSold(posted=self.time_posted)
        self.partial = args[10]
        self.insert(insert_data)


    def insert(self, insert_data, update_data):
        """updates sold_data. Takes in 1 argument:
            :arg sold_data: dict"""

        if self.partial:
            # Of partial auctions we know 100% they were sold
            if "sold_auctions" in insert_data:
                if self.realm_id in insert_data["sold_auctions"]:
                    insert_data["sold_auctions"][self.realm_id].append(self)
                else: insert_data["sold_auctions"][self.realm_id] = [self]
            else:
                insert_data["sold_auctions"] = {}
                insert_data["sold_auctions"][self.realm_id] = [self]
        else:
            valid = self.time_left != "SHORT" and self.unit_price < 9999999.9999 and self.unit_price < 5*self.Item.mean_price
            if valid:
                if "sold_auctions" in insert_data:
                    if self.realm_id in insert_data["sold_auctions"]:
                        insert_data["sold_auctions"][self.realm_id].append(self)
                    else: insert_data["sold_auctions"][self.realm_id] = [self]
                else:
                    insert_data["sold_auctions"] = {}
                    insert_data["sold_auctions"][self.realm_id] = [self]

        self.Item.sold += self.quantity
        self.Item.price = self.quantity * self.unit_price
        temp_mean = self.price / self.quantity
        if not temp_mean == self.Item.mean_price:
            self.mean_price = temp_mean
            self.Item.update(update_data)
