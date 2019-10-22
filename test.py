import concurrent.futures
import multiprocessing

def f(x):
    return x*x

#
# with concurrent.futures.ProcessPoolExecutor() as p:
#     results = p.map(f, [1, 2, 3, 4, 5])
#     for result in results:
#         print(result)

def func():
    with multiprocessing.Pool(processes=1) as p:
        results = p.map(f, [1, 2, 3, 4, 5])
        for result in results:
            print(result)

if __name__ == '__main__':
    func()
