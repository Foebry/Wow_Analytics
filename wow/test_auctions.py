import unittest


class AuctionTest(unittest.TestCase):

    @staticmethod
    def init():
        auction = None
        return auction


    @unittest.skip
    def test_init(self):

        # testing rebuilding auction
        self.assertEqual(id, auction.id)
        self.assertEqual(realm, auction.realm)
        self.assertEqual(item_id, auction.item_id)
        self.assertEqual(pet_id, auction.pet_id)
        self.assertEqual(quantity, auction.quantity)
        self.assertEqual(unit_price, auction.unit_price)
        self.assertEqual(time_left, auction.time_left)
        self.assertEqual(bid, auction.bid)
        self.assertEqual(buyout, auction.buyout)
        self.assertEqual(time_posted, auction.time_posted)
        self.assertEqual(last_updated, auction.last_updated)
        self.assertEqual(item, auction.Item)

        # testing existing item
        pass

        # testing new_item
        pass

        # testing existing_pet
        pass

        # testing new_pet
        pass

        # testing first_pet
        pass


        # testing new_auction
        pass


        # testing existing_auction
        pass




    @unittest.skip
    def test_insert(self):


        self.assertEqual(1, len(insert_data["auctions"][auction.realm.id]))
        self.assertEqual(True, auction in insert_data["auctions"][auction.realm.id])

    @unittest.skip
    def test_update(self):
        pass



class SoldAuctionTest(unittest.TestCase):

    @staticmethod
    def init():
        soldauction = None
        return soldauction


    @unittest.skip
    def test_init(self):
        pass


    @unittest.skip
    def test_insert(self):
        pass


    @unittest.skip
    def test_isValidSoldAuction(self):
        pass



if __name__ == "__main__":
    auction = AuctionTest.init()
    soldauction = SoldAuctionTest.init()
    unittest.main()
