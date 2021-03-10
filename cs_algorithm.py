from datetime import time
from functools import wraps

query_a = 'a new aloirthm '
query_b = 'computer science'
query_a = 'ff'

from bm25_old import BM25


def timer(func):
    """
    calculate function spend time
    :param func:
    :return:
    """

    @wraps(func)
    def timed(*args, **kwargs):
        import time
        begin = time.time()
        func(*args, **kwargs)
        end = time.time()
        print("spend time:{}".format(end - begin))

    return timed


@timer
def funca():
    import time
    time.sleep(2)


if __name__ == '__main__':
    funca()
