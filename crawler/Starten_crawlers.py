import multiprocessing

import AH_allergenen_crawler
import Jumbo_allergenen_crawler
import database_opschonen
import Pictures
import extra_info_crawler_AH
import extra_info_crawler_Jumbo

if __name__ == '__main__':

    Jumbo_allergenen_crawler.start(500)  # De Jumbo crawler kan niet sneller omdat de toegang anders wordt geweigerd

    for i in range(20):  # De Albertheijn crawler wordt opgesplits in 20 processen zodat het proces sneller gaat
        p = multiprocessing.Process(target=AH_allergenen_crawler.start, args=(i,))
        p.start()

    database_opschonen.start()  # Er zijn recepten zonder ingredienten die worden hier verwijderd

    Pictures.start()  # Hier worden plaatjes bij de recepten gezocht

    extra_info_crawler_AH.start()  # Omdat er veel recepten zijn wordt er hier extra informatie bij gezocht

    extra_info_crawler_Jumbo.start()  # Omdat er veel recepten zijn wordt er hier extra informatie bij gezocht
