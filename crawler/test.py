import multiprocessing
import AH_crawler


def test(i):
    print(i)


if __name__ == '__main__':
    for i in range(20):
        p = multiprocessing.Process(target=test, args=(i,))
        #p = multiprocessing.Process(target=AH_crawler.ah_crawler, args=(i,))
        p.start()
