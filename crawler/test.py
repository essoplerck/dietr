import multiprocessing

import AH_allergenen_crawler
import Jumbo_allergenen_crawler
import database_opschonen
import Pictures

if __name__ == '__main__':


    #Jumbo_allergenen_crawler.start(500)  # De Jumbo crawler kan niet sneller omdat de toegang anders wordt geweigerd

    for i in range(210):  # De Albertheijn crawler wordt opgesplits in 20 processen zodat het proces sneller gaat
        p = multiprocessing.Process(target=Pictures.start, args=(i,))
        p.start()

    #database_opschonen.opschonen()
