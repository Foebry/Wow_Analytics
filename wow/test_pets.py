import unittest
import pets


class PetTest(unittest.TestCase):

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




if __name__ == "__main__":
    PetTest.init()
    unittest.main()
