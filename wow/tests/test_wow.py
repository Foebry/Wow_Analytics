import unittest
import time
import os

from wow import setup, wait
from operations import Operation
from Requests import Request
from logger.Logger import Logger



def testcases():
    os.system("py test_requests.py")
    os.system("py test_operations.py")
    os.system("py test_realms.py")
    os.system("py test_pets.py")
    os.system("py test_mounts.py")
    os.system("py test_classes.py")
    os.system("py test_items.py")
    os.system("py test_auctions.py")
    print("test_wow")



class Testcase(unittest.TestCase):


    @staticmethod
    def init():
        pass


    def test_setup(self):
        operation, request = setup(test=True)
        logger = operation.logger
        items = operation.database.getAmountItems()
        pets = operation.database.getAmountPets()
        classes = operation.database.getAmountClasses()
        mounts = operation.database.getAmountMounts()

        # testing types of operation and request
        self.assertEqual(True, isinstance(operation, Operation))
        self.assertEqual(True, isinstance(request, Request))
        self.assertEqual(True, isinstance(logger, Logger))
        self.assertEqual(True, logger == request.logger)

        # testing types of operation attributes
        self.assertEqual(dict, type(operation.live_data))
        self.assertEqual(dict, type(operation.insert_data))
        self.assertEqual(dict, type(operation.update_data))

        # testing live_data
        self.assertEqual(4, len(operation.live_data.keys()))
        self.assertEqual(True, "items" in operation.live_data.keys())
        self.assertEqual(True, "classes" in operation.live_data.keys())
        self.assertEqual(True, "pets" in operation.live_data.keys())
        self.assertEqual(True, "mounts" in operation.live_data.keys())
        self.assertEqual(False, 82800 in operation.live_data["items"])
        self.assertEqual(dict, type(operation.live_data["items"]))
        self.assertEqual(dict, type(operation.live_data["classes"]))
        self.assertEqual(dict, type(operation.live_data["pets"]))
        self.assertEqual(dict, type(operation.live_data["mounts"]))
        self.assertEqual(items, len(operation.live_data["items"].keys()))
        self.assertEqual(classes, len(operation.live_data["classes"].keys()))
        self.assertEqual(pets, len(operation.live_data["pets"].keys()))
        self.assertEqual(mounts, len(operation.live_data["mounts"].keys()))

        # testing insert_data
        self.assertEqual(6, len(operation.insert_data.keys()))
        self.assertEqual(True, "items" in operation.insert_data.keys())
        self.assertEqual(True, "classes" in operation.insert_data.keys())
        self.assertEqual(True, "subclasses" in operation.insert_data.keys())
        self.assertEqual(True, "pets" in operation.insert_data.keys())
        self.assertEqual(True, "mounts" in operation.insert_data.keys())
        self.assertEqual(True, "item_prices" in operation.insert_data.keys())
        self.assertEqual(list, type(operation.insert_data["items"]))
        self.assertEqual(list, type(operation.insert_data["classes"]))
        self.assertEqual(list, type(operation.insert_data["subclasses"]))
        self.assertEqual(list, type(operation.insert_data["pets"]))
        self.assertEqual(list, type(operation.insert_data["mounts"]))
        self.assertEqual(list, type(operation.insert_data["item_prices"]))
        self.assertEqual(0, len(operation.insert_data["items"]))
        self.assertEqual(0, len(operation.insert_data["classes"]))
        self.assertEqual(0, len(operation.insert_data["subclasses"]))
        self.assertEqual(0, len(operation.insert_data["pets"]))
        self.assertEqual(0, len(operation.insert_data["mounts"]))
        self.assertEqual(0, len(operation.insert_data["item_prices"]))

        # testing update_data
        self.assertEqual(0, len(operation.update_data.keys()))
        self.assertEqual(dict, type(operation.update_data))


    def test_wait(self):
        start = time.time()
        sleep_duration = 5

        wait(sleep_duration)

        end = time.time()

        self.assertEqual(5, int(end-start))



if __name__ == "__main__":
    testcases()
    unittest.main()
