import numpy as np

def matrix_pow(A,n) :

    B = np.eye(len(A))
    while n > 0 :
        if n % 2 == 1 :
            B = np.matmul(B,A)
        A = np.matmul(A,A)
        n = n / 2
    return B

def random_select_page(pages, distribution) :

    total = np.sum(distribution)
    winner = np.random.random(1)[0] * total

    cumulative_sum = 0
    for i,p in enumerate(pages) :
        # print(i)
        cumulative_sum += distribution[i]
        if winner < cumulative_sum :
            return p

    return pages[-1]


if __name__ == "__main__" :

    pages =     [   1,  2,  3,4]
    dist =      [   10, 70, 15, 5]

    p = random_select_page(pages, dist)
    print(p)
