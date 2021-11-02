"""main program functionality"""
from datetime import datetime, timedelta

import concurrent.futures
import os
import argparse
import json



def setup(test=False):
    from realms import Realm

    app.logger = Logger(os.getcwd(), "d")

    app.logger.log(msg="\n"*3, timestamped=False, level_display=False)
    app.logger.log(msg="*"*150, timestamped=False, level_display=False)
    app.logger.log(msg="*"*65+"Started new session!"+"*"*65, timestamped=False, level_display=False)
    app.logger.log(msg="*"*150, timestamped=False, level_display=False)

    for realm_id in REALMS:
        realm = Realm(realm_id, db, logger, request)
        operation.realms.append(realm)

    app.setLiveData()

    return app



def wait(duration):
    import time
    end = time.time() + duration

    while not time.time() >= end:
        remaining = round(end - time.time())

        print(" "*100, end="\r")
        print("sleeping {} seconds".format(remaining), end='\r')
        time.sleep(1)



def main():
    open_time = datetime.now()

    while True:
        round = True
        close_time = datetime.now()
        for realm in operation.realms:
            response = request.getAuctionData(realm, operation)

            if response:
                if round: operation.logger.log(msg="\n\n"+"*"*100, timestamped=False, level_display=False)
                operation.logger.log(msg=f"New data of {len(response)} auctions for {realm.name}")
                round = False

                realm.setAuctionData(response, operation, request)

                operation.insertData(realm)
                operation.updateData(realm)
                operation.exportData([1096,], open_time, close_time)
                operation.update(realm)

                open_time = datetime.now()

        wait(600)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", dest="test", action="store_true")
    args = parser.parse_args()
    app = setup(args.test)

    main()
