import unittest


class ItemTest(unittest.TestCase):


    @staticmethod
    def init():
        pass


    @unittest.skip
    def test_init(self):
        pass


    @unittest.skip
    def test_setData(self):
        pass


    @unittest.skip
    def test_insert(self):
        pass


    @unittest.skip
    def test_update(self):
        pass


    @unittest.skip
    def test_updateMean(self):
        pass



if __name__ == "__main__":
    ItemTest.init()
    unittest.main()
