import unittest


class ClassTest(unittest.TestCase):

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



class SubclassTest(unittest.TestCase):


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
    ClassTest.init()
    SubclassTest.init()
    unittest.main()
