import multiprocessing

import AH_allergenen_crawler
import Jumbo_allergenen_crawler
import database_opschonen

if __name__ == '__main__':


    #Jumbo_allergenen_crawler.start(500)  # De Jumbo crawler kan niet sneller omdat de toegang anders wordt geweigerd

    for i in range(20):  # De Albertheijn crawler wordt opgesplits in 20 processen zodat het proces sneller gaat
        p = multiprocessing.Process(target=AH_allergenen_crawler.start, args=(i,))
        p.start()

    database_opschonen.opschonen()
