"""auctions functionality"""
from datetime import datetime
from operations import setTimePosted, setTimeSold
from items import Item

import datetime
import random



class Auction():
    """docstring"""
    def __init__(self, realm, operation=None, request=None, test=False, *args, **kwargs):
        """Auction constructor. Takes in 7 args. Always needs 6 arguments, so either args or kwargs need to be given:
            :arg live_data: dict,
            :arg previous_auctions: dict,
            :arg insert_data: dict,
            :arg update_data: dict,
            :arg sold_data: dict,
            :arg *args: list (optional),
            :arg **kwargs: dict (optional)"""

        rebuild_auction = operation is None and kwargs

        if rebuild_auction:
            self.id = kwargs["_id"]
            self.realm = realm
            self.item_id = kwargs["item_id"]
            self.pet_id = kwargs["pet_id"]
            self.quantity = kwargs["quantity"]
            self.unit_price = kwargs["unit_price"]
            self.time_left = kwargs["time_left"]
            self.bid = kwargs["bid"]
            self.buyout = kwargs["buyout"]
            self.time_posted = kwargs["time_posted"]
            self.last_updated = kwargs["last_updated"]
            self.Item = kwargs["Item"]
            return

        self.realm = realm
        self.id = args[0]
        self.item_id = args[1]
        self.pet_id = args[2]["_id"]
        self.quantity = args[3]
        self.unit_price = args[4]
        self.time_left = args[5]
        self.bid = args[6]
        self.buyout = args[7]
        self.time_posted = setTimePosted(test=test)
        self.last_updated = self.time_posted

        first_pet = self.item_id == 82800 and self.item_id not in operation.live_data["items"]
        is_pet = self.item_id == 82800 and self.item_id in operation.live_data["items"]
        existing_pet = is_pet and self.pet_id in operation.live_data["items"][self.item_id]
        new_pet = is_pet and self.pet_id not in operation.live_data["items"][self.item_id]
        new_item = not self.item_id == 82800 and self.item_id not in operation.live_data["items"]
        existing_item = not self.item_id == 82800 and self.item_id in operation.live_data["items"]
        new_auction = operation is not None and self.id not in realm.previous_auctions
        existing_auction = operation is not None and self.id in realm.previous_auctions


        if existing_item:
            self.Item = operation.live_data["items"][self.item_id]

        elif new_item:
            item = Item(operation, request, self.item_id)
            operation.live_data["items"][self.item_id] = item
            self.Item = item

        elif existing_pet:
            self.Item = operation.live_data["items"][self.item_id][self.pet_id]

        elif new_pet:
            item = Item(operation, request, self.item_id, args[2])
            operation.live_data["items"][self.item_id][self.pet_id] = item
            self.Item = item

        elif first_pet:
            item = Item(operation, request, self.item_id, args[2])
            operation.live_data["items"][self.item_id] = {}
            operation.live_data["items"][self.item_id][self.pet_id] = item
            self.Item = item

        else: return

        if new_auction:
            realm.auctions[self.id] = self
            self.insert(operation)

        elif existing_auction:
            self.update(operation, realm, realm.previous_auctions[self.id], test)


    def insert(self, operation):
        unset_insert_data_auctions = "auctions" not in operation.insert_data
        unset_realm_insert_data_auctions = "auctions" in operation.insert_data and self.realm.id not in operation.insert_data["auctions"]
        set_realm_insert_data_auctions = "auctions" in operation.insert_data and self.realm.id in operation.insert_data["auctions"]

        if set_realm_insert_data_auctions:
            operation.insert_data["auctions"][self.realm.id].append(self)

        elif unset_realm_insert_data_auctions:
            operation.insert_data["auctions"][self.realm.id] = [self]

        elif unset_insert_data_auctions:
            operation.insert_data["auctions"] = {}
            operation.insert_data["auctions"][self.realm.id] = [self]


    def update(self, operation, realm, existing, test=False):
        """
            Updating an Auction object.
            If auction is still active at t+1 we need to check if it is partially sold.
            Afterwards we remove the auction with equal id from t so the new one can take its place.
            If auction has fewer quantity, we know the auction got partially sold.
            We then create a Soldauction.
            Finally we add auction to update dictionary to be updated.
        """
        # calculate sold_quantity, new buyout of sold_quantity and bid of sold_quantity
        sold_quantity = existing.quantity - self.quantity
        buyout = existing.unit_price * sold_quantity
        bid = -1
        if existing.bid > -1: bid = existing.bid / existing.quantity * sold_quantity

        set_realm_update_data_auctions = "auctions" in operation.update_data and self.realm.id in operation.update_data["auctions"]
        unset_realm_update_data_auctions = "auctions" in operation.update_data and self.realm.id not in operation.update_data["auctions"]
        unset_auctions_update_data = "auctions" not in operation.update_data

        # new time_posted = existing time_posted
        self.time_posted = existing.time_posted
        self.last_updated = setTimePosted()

        if sold_quantity > 0:
            # create sold_auction
            args = (existing, self.id, self.item_id, self.pet_id, sold_quantity, self.unit_price, self.time_left, bid, buyout, self.time_posted, True)
            sold_auction = SoldAuction(operation, test, *args)

        # remove auction_id from previous_auctions
        if not test:
            del self.realm.previous_auctions[self.id]

        # add to live_data
        realm.auctions[self.id] = self

        # adding auction to be updated
        if set_realm_update_data_auctions:
            operation.update_data["auctions"][self.realm.id].append(self)

        elif unset_realm_update_data_auctions:
            operation.update_data["auctions"][self.realm.id] = [self]

        elif unset_auctions_update_data:
            operation.update_data["auctions"] = {}
            operation.update_data["auctions"][self.realm.id] = [self]



class SoldAuction():
    """docstring"""
    def __init__(self, operation, test=False, *args):
        """Constructor for sold auctions. Takes in 1 argument:
            :arg *args: list"""

        self.Auction = args[0]
        self.realm = self.Auction.realm
        self.id = args[1]
        self.item_id = args[2]
        self.pet_id = args[3]
        self.quantity = args[4]
        self.unit_price = args[5]
        self.time_left = args[6]
        self.bid = args[7]
        self.buyout = args[8]
        self.time_posted = args[9]
        self.time_sold = setTimeSold(posted=self.Auction.last_updated)
        self.partial = args[10]
        if not test: self.insert(operation, test)


    def insert(self, operation, test=False):
        """updates sold_data. Takes in 2 arguments:
            :arg insert_data: dict
            :arg update_data: dict"""

        item = self.Auction.Item

        set_sold_auctions_insert_data = "sold_auctions" in operation.insert_data
        set_realm_insert_data_sold_auctions = set_sold_auctions_insert_data and self.realm.id in operation.insert_data["sold_auctions"]


        if not set_sold_auctions_insert_data:
            operation.insert_data["sold_auctions"] = {}
            operation.insert_data["sold_auctions"][self.realm.id] = []

        elif not set_realm_insert_data_sold_auctions:
            operation.insert_data["sold_auctions"][self.realm.id] = []

        if self.partial:
            # partially sold auctions will always be considered as sold
            operation.insert_data["sold_auctions"][self.realm.id].append(self)
            return item.updateMean(self, operation)

        insert_auctions = operation.insert_data["sold_auctions"][self.realm.id]
        auctions_to_check = [
                                insert_auctions[x] for x in range(len(insert_auctions))
                                if insert_auctions[x].Auction.Item.id == self.Auction.Item.id
                        ]

        if not test and self.isValidSoldAuction(operation, auctions_to_check):
            operation.insert_data["sold_auctions"][self.realm.id].append(self)
            item.updateMean(self, operation)



    def isValidSoldAuction(self, operation, auctions_to_check):

        item = self.Auction.Item
        try: not_overpriced = item.mean_price == 0 or self.unit_price < 5*item.mean_price and self.unit_price < 9999999.9999
        except Exception as e:
            operation.logger.log(True, msg="item = {}".format(self.Auction.Item))
            return
        valid = self.time_left != "SHORT" and not_overpriced

        for soldauction in auctions_to_check:
            cheaper = self.unit_price < soldauction.unit_price
            got_undercut = self.unit_price == soldauction.unit_price and self.Auction.time_posted < soldauction.Auction.time_posted

            if not cheaper or got_undercut: return False

        if valid:
            del self.realm.auctions[self.Auction.id]
            return True

        return False
