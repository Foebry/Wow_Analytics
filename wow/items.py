"""Item functionality"""
import random
import datetime
from Requests import Request
from pets import Pet
from classes import Class, Subclass
from mounts import Mount



class Item:
    """Item"""
    def __init__(self, operation=None, request=None, _id=None, pet_data=None, test=False, **kwargs):
        """constructor for Item class"""

        insert_new_item = operation is not None and not kwargs
        insert_item = operation is not None and kwargs
        test_item = test
        rebuild_item = operation is None and kwargs

        if test_item:
            self.id = _id
            self.kwargs = self.setData(operation, request, None, test=True)

        elif rebuild_item or insert_item:
            self.pet_id = kwargs["pet"]["_id"]
            self.mount_id = kwargs["mount"]["_id"]
            self.name = kwargs["name"]
            self.level = kwargs["level"]
            self.quality = kwargs["quality"]
            self.class_id = kwargs["item_class"]
            self.subclass_id = kwargs["item_subclass"]
            self.type = kwargs["type"]
            self.subtype = kwargs["subtype"]
            self.sold = kwargs["sold"]
            self.price = kwargs["price"]
            self.mean_price = kwargs["mean_price"]

            if rebuild_item:
                self.id = _id
                self.Pet = kwargs["Pet"]
                self.Mount = kwargs["Mount"]
                self.Class = kwargs["Class"]
                self.Subclass = kwargs["Subclass"]

        elif insert_new_item:
            self.id = _id
            self.Pet = None
            self.Mount = None
            status, data = self.setData(operation, request, pet_data)
            if status:
                new_pet = self.id == 82800 and self.pet_id not in operation.live_data["pets"]
                existing_pet = self.id == 82800 and self.pet_id in operation.live_data["pets"]
                new_class = self.class_id not in operation.live_data["classes"]
                existing_class = self.class_id in operation.live_data["classes"]
                new_subclass = self.class_id not in operation.live_data["classes"] or self.subclass_id not in operation.live_data["classes"][self.class_id].subclasses
                existing_subclass = self.class_id in operation.live_data["classes"] and self.subclass_id in operation.live_data["classes"][self.class_id].subclasses
                new_mount = not self.mount_id == 0 and self.mount_id not in operation.live_data["mounts"]
                existing_mount = not self.mount_id == 0 and self.mount_id in operation.live_data["mounts"]

                if new_pet:
                    self.Pet = Pet(operation, request, self.pet_id)
                    operation.live_data["pets"][self.pet_id] = self.Pet

                elif existing_pet:
                    self.Pet = operation.live_data["pets"][self.pet_id]

                elif new_mount:
                    self.Mount = Mount(operation, request, self.mount_id)
                    operation.live_data["mounts"][self.mount_id] = self.Mount

                elif existing_mount: self.Mount = operation.live_data["mounts"][self.mount_id]

                if new_class:
                    self.Class = Class(operation, request, self.class_id)
                    operation.live_data["classes"][self.class_id] = self.Class

                elif existing_class: self.Class = operation.live_data["classes"][self.class_id]

                if new_subclass:
                    self.Subclass = Subclass(operation, request, self.class_id, self.subclass_id)
                    operation.live_data["classes"][self.class_id].subclasses[self.subclass_id] = self.Subclass

                elif existing_subclass: self.Subclass = operation.live_data["classes"][self.class_id].subclasses[self.subclass_id]

                self.insert(operation)
                return


            if status == False:
                operation.logger.log(True, msg="Encountered an item without data from api")
                self.id = data["id"]
                self.pet_id = data["pet_id"]
                self.mount_id = data["mount_id"]
                self.name = ""
                self.level = data["level"]
                self.quality = ""
                self.class_id = 0
                self.subclass_id = 0
                self.type = ""
                self.subtype = ""
                self.sold = 0.0
                self.price = 0.0
                self.mean_price = 0.0

                self.insert(operation)
                return


    def setData(self, operation, request, pet_data, test=False):
        data = request.getItemData(self.id)
        is_pet = self.id == 82800

        if data:
            is_mount = data["item_subclass"]["name"] == "Mount"

            data["item_class"] = data["item_class"]["id"]
            data["item_subclass"] = data["item_subclass"]["id"]
            data["type"] = data["inventory_type"]["type"]
            data["subtype"] = data["inventory_type"]["name"]
            data["sold"] = 0.0
            data["price"] = 0.0
            data["mean_price"] = 0.0
            data["_id"] = data["id"]
            data["quality"] = data["quality"]["name"]

            if is_pet:
                qualities = {0: "Poor", 1:"Common", 2:"Uncommon", 3:"Rare", 4:"Epic", 5:"Legendary"}
                data["mount"] = {"_id":0}
                data["pet"] = {"_id":pet_data["_id"]}
                data["quality"] = qualities[pet_data["quality"]]
                data["level"] = pet_data["level"]

            elif is_mount:
                data["mount"] = {"_id":request.getMount_id_by_name(data["name"])}
                data["pet"] = {"_id":0}

            else:
                data["mount"] = {"_id":0}
                data["pet"] = {"_id":0}

            delete = [key for key in data.keys() if key not in ["pet", "mount", "name", "level", "quality", "item_class", "item_subclass", "type", "subtype", "sold", "price", "mean_price", "_id"]]

            for key in delete:
                del(data[key])

            if test: return data

            self.__init__(operation, request, **data)
            return True, data

        data = {"id":self.id, "pet_id":0, "mount_id":0, "level":0}
        return False, data


    def insert(self, operation):
        """adding Item to be inserted"""
        set_items_insert_data = "items" in operation.insert_data
        unset_items_insert_data = "items" not in operation.insert_data

        if set_items_insert_data: operation.insert_data["items"].append(self)

        elif unset_items_insert_data: operation.insert_data["items"] = [self]


    def update(self, operation):
        """update data for item if mean_price changes"""
        unset_items_update_data = "items" not in operation.update_data
        new_item_to_update = not unset_items_update_data and self not in operation.update_data["items"]

        # add items to be updated
        if unset_items_update_data:
            operation.update_data["items"] = [self]

        elif new_item_to_update:
            operation.update_data["items"].append(self)


    def updateMean(self, soldauction, operation):
        try: self.sold += soldauction.quantity
        except:
            operation.logger.log(True, "item {} has not attribute sold".format(self.id))
        self.price += soldauction.buyout
        temp_mean = self.price / self.sold
        new_mean = temp_mean != self.mean_price
        if new_mean:
            self.mean_price = temp_mean
            self.update(operation)
