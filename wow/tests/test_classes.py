import unittest
import os

from operations import Operation
from Requests import Request
from logger.Logger import Logger
from databases.Database import Database
from config import DATABASE, CREDENTIALS

print("test_classes")


class ClassTest(unittest.TestCase):

    @staticmethod
    def init():
        from classes import Class

        new_class = Class(operation, request, 0)
        rebuild_class = Class(_id=1, **{"name":"Container", "subclasses":{}})

        return new_class, rebuild_class


    def test_init(self):

        # test new_class
        _class = new_class
        self.assertEqual(0, _class.id)
        self.assertEqual("Consumable", _class.name)
        self.assertEqual({}, _class.subclasses)


        # test rebuild_class
        _class = rebuild_class
        self.assertEqual(1, _class.id)
        self.assertEqual("Container", _class.name)
        self.assertEqual({}, _class.subclasses)


    def test_setData(self):
        data = new_class.setData(operation, request, True)
        self.assertEqual(3, len(data.keys()))
        self.assertEqual(True, "_id" in data)
        self.assertEqual(True, "name" in data)
        self.assertEqual(True, "subclasses" in data)
        self.assertEqual(0, data["_id"])
        self.assertEqual("Consumable", data["name"])
        self.assertEqual({}, data["subclasses"])

        data = rebuild_class.setData(operation, request, True)
        self.assertEqual(3, len(data.keys()))
        self.assertEqual(True, "_id" in data)
        self.assertEqual(True, "name" in data)
        self.assertEqual(True, "subclasses" in data)
        self.assertEqual(1, data["_id"])
        self.assertEqual("Container", data["name"])
        self.assertEqual({}, data["subclasses"])


    def test_insert(self):
        operation.insert_data["classes"] = []
        insert_classes = operation.insert_data["classes"]
        new_class.insert(operation)
        rebuild_class.insert(operation)

        self.assertEqual(2, len(insert_classes))
        self.assertEqual(new_class, insert_classes[0])
        self.assertEqual(rebuild_class, insert_classes[1])



class SubclassTest(unittest.TestCase):


    @staticmethod
    def init():
        from classes import Subclass

        new_subclass = Subclass(operation, request, 0, 0)
        rebuild_subclass = Subclass(**{"name":"Bag", "class_id":1, "subclass_id":0})

        return new_subclass, rebuild_subclass



    def test_init(self):

        # test new subclass
        subclass = new_subclass
        self.assertEqual(0, subclass.class_id)
        self.assertEqual(0, subclass.subclass_id)
        self.assertEqual("Explosives and Devices", subclass.name)


        # test rebuild subclass
        subclass = rebuild_subclass
        self.assertEqual(1, subclass.class_id)
        self.assertEqual(0, subclass.subclass_id)
        self.assertEqual("Bag", subclass.name)


    def test_setData(self):
        data = new_subclass.setData(operation, request, True)
        self.assertEqual(3, len(data.keys()))
        self.assertEqual(True, "class_id" in data)
        self.assertEqual(True, "subclass_id" in data)
        self.assertEqual(True, "name" in data)
        self.assertEqual(0, data["class_id"])
        self.assertEqual(0, data["subclass_id"])
        self.assertEqual("Explosives and Devices", data["name"])

        data = rebuild_subclass.setData(operation, request, True)
        self.assertEqual(3, len(data.keys()))
        self.assertEqual(True, "class_id" in data)
        self.assertEqual(True, "subclass_id" in data)
        self.assertEqual(True, "name" in data)
        self.assertEqual(1, data["class_id"])
        self.assertEqual(0, data["subclass_id"])
        self.assertEqual("Bag", data["name"])


    def test_insert(self):
        operation.insert_data["subclasses"] = []
        insert_subclasses = operation.insert_data["subclasses"]
        new_subclass.insert(operation)
        rebuild_subclass.insert(operation)

        self.assertEqual(2, len(insert_subclasses))
        self.assertEqual(new_subclass, insert_subclasses[0])
        self.assertEqual(rebuild_subclass, insert_subclasses[1])



if __name__ == "__main__":
    logger = Logger(os.getcwd())
    db = Database(DATABASE, logger, test=True, testcase=True)
    operation = Operation(db, logger)
    request = Request(CREDENTIALS, db, logger)
    new_class, rebuild_class = ClassTest.init()
    new_subclass, rebuild_subclass = SubclassTest.init()
    unittest.main()
