import unittest
import os

print("test_mounts")


class MountTest(unittest.TestCase):

    @staticmethod
    def init():
        from mounts import Mount
        from operations import Operation
        from logger.Logger import Logger
        from databases.Database import Database
        from Requests import Request
        from config import DATABASE, CREDENTIALS

        logger = Logger(os.getcwd())
        db = Database(DATABASE, logger, test=True, testcase=True)
        operation = Operation(db, logger)
        request = Request(CREDENTIALS, db, logger)

        new_mount = Mount(operation, request, _id=69)
        rebuild_mount = Mount(_id=85, **{"name":"Swift Mistsaber", "source":"Vendor", "faction":"Alliance"})

        return new_mount, rebuild_mount, operation, request


    def test_init(self):

        # testing new mount
        mount = new_mount
        self.assertEqual(69, mount.id)
        self.assertEqual("Rivendare's Deathcharger", mount.name)
        self.assertEqual("Drop", mount.source)
        self.assertEqual("Factionless", mount.faction)

        # testing rebuild mount
        mount = rebuild_mount
        self.assertEqual(85, mount.id)
        self.assertEqual("Swift Mistsaber", mount.name)
        self.assertEqual("Vendor", mount.source)
        self.assertEqual("Alliance", mount.faction)


    def test_setData(self):
        data = new_mount.setData(operation, request, True)
        self.assertEqual(4, len(data.keys()))
        self.assertEqual(True, "_id" in data)
        self.assertEqual(True, "source" in data)
        self.assertEqual(True, "faction" in data)
        self.assertEqual(True, "name" in data)
        self.assertEqual(69, data["_id"])
        self.assertEqual("Rivendare's Deathcharger", data["name"])
        self.assertEqual("Drop", data["source"])
        self.assertEqual("Factionless", data["faction"])

        data = rebuild_mount.setData(operation, request, True)
        self.assertEqual(4, len(data.keys()))
        self.assertEqual(True, "_id" in data)
        self.assertEqual(True, "source" in data)
        self.assertEqual(True, "faction" in data)
        self.assertEqual(True, "name" in data)
        self.assertEqual(85, data["_id"])
        self.assertEqual("Swift Mistsaber", data["name"])
        self.assertEqual("Vendor", data["source"])
        self.assertEqual("Alliance", data["faction"])


    def test_insert(self):
        operation.insert_data["mounts"] = []
        insert_mounts = operation.insert_data["mounts"]
        new_mount.insert(operation)
        rebuild_mount.insert(operation)

        self.assertEqual(2, len(insert_mounts))
        self.assertEqual(new_mount, insert_mounts[0])
        self.assertEqual(rebuild_mount, insert_mounts[1])



if __name__ == "__main__":
    new_mount, rebuild_mount, operation, request = MountTest.init()
    unittest.main()
