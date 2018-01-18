import multiprocessing

import AH_allergenen_crawler
import Jumbo_allergenen_crawler


if __name__ == '__main__':
    for i in range(20):
        p = multiprocessing.Process(target=AH_allergenen_crawler.start, args=(i,))
        p.start()

    Jumbo_allergenen_crawler.start(500)

