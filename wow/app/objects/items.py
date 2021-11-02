"""Item functionality"""
import random
import datetime
from Requests import Request
from pets import Pet
from classes import Class, Subclass
from mounts import Mount
from objects import Object
from math import inf



class Item(Object):
    """Item"""
    def __init__(self, operation=None, request=None, id_=None, test=False, **kwargs):
        """
            Initialization of Item object.
        """
        super().__init__(operation, request, id_, test, **kwargs)

        self.open = None
        self.low = inf
        self.high = -inf
        self.close = 0
        self.amount = 0


    def prepareData(self, operation, request=None, data=None, dummy: bool=False, **kwargs):

        if dummy:
            operation.logger(True, msg="Encountered an item without data from api")

            data["id"] = self.id
            data["pet_id"] = 0
            data["mount_id"] = 0
            data["level"] = 0

            return data

        is_pet = self.id == 82800
        is_mount = data["item_subclass"]["name"] == "Mount"

        data["item_class"] = data["item_class"]["id"]
        data["item_subclass"] = data["item_subclass"]["id"]
        data["type"] = data["inventory_type"]["type"]
        data["subtype"] = data["inventory_type"]["name"]
        data["sold"] = 0.0
        data["price"] = 0.0
        data["mean_price"] = 0.0
        data["quality"] = data["quality"]["name"]

        live_pets = operation.live_data["pets"]
        live_mounts = operation.live_data["mounts"]
        live_classes = operation.live_data["classes"]

        if is_pet:
            new_pet = self.id == 82800 and self.pet_id not in live_pets
            existing_pet = self.id == 82800 and self.pet_id in live_pets

            qualities = {0: "Poor", 1:"Common", 2:"Uncommon", 3:"Rare", 4:"Epic", 5:"Legendary"}
            data["mount_id"] = 0
            data["pet_id"] = kwargs["id_"]
            data["quality"] = qualities[pet_data["quality"]]
            data["level"] = pet_data["level"]

            if new_pet:
                pet = Pet(operation, request, data["pet_id"])
                data["Pet"] = pet
                operation.live_data["pets"][pet.id] = pet

            elif existing_pet:
                pet_id = data["pet_id"]
                data["Pet"] = live_pets[pet_id]

        elif is_mount:
            mount_id = request.getMount_id_by_name(data["name"])

            new_mount = mount_id not in live_mounts
            existing_mount = mount_id in live_mounts

            data["mount_id"] = mount_id
            data["pet_id"] = 0

            if new_mount:
                mount = Mount(operation, request, mount_id)
                data["Mount"] = mount
                live_mounts[mount_id] = mount

            elif existing_mount:
                data["Mount"] = live_mounts[mount_id]

        else:
            data["mount_id"] = 0
            data["pet_id"] = 0

        item_class = data["item_class"]
        item_subclass = data["item_subclass"]
        new_class = item_class not in live_classes
        existing_class = item_class in live_classes
        new_subclass = item_class not in live_classes or item_subclass not in live_classes[item_class].subclasses
        existing_subclass = item_class in live_classes and item_subclass in live_classes[item_class].subclasses

        if new_class:
            data["Class"] = Class(operation, request, item_class)
            live_classes[item_class] = data["Class"]

        elif existing_class:
            data["Class"] = live_classes[item_class]

        if new_subclass:
            data["Subclass"] = Subclass(operation, request, item_class, False, *(item_subclass,))
            live_classes[item_class].subclasses[item_subclass] = data["Subclass"]

        elif existing_subclass:
            data["Subclass"] = live_classes[item_class].subclasses[item_subclass]

        return data


    def updateMean(self, soldauction, operation):
        try: self.sold += soldauction.quantity
        except:
            operation.logger.log(True, "item {} has not attribute sold".format(self.id))
        self.price += soldauction.buyout
        temp_mean = self.price / self.sold
        new_mean = temp_mean != self.mean_price
        if new_mean:
            self.mean_price = temp_mean
            self.update(operation, soldauction)

        if self.open is None:
            self.open = soldauction.unit_price
            self.low = soldauction.unit_price
            self.high = soldauction.unit_price
            self.close = soldauction.unit_price

        elif self.low > soldauction.unit_price:
            self.low = soldauction.unit_price

        elif self.high < soldauction.unit_price:
            self.high = soldauction.unit_price

        self.close = soldauction.unit_price
        self.amount += soldauction.quantity

        if self not in operation.export_items:
            operation.export_items.append(self)


    def reset(self):
        self.open = None
        self.low = inf
        self.high = -inf
        self.close = 0
        self.amount = 0
