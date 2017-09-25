import numpy as np

f = open('three.txt', 'r')
words = f.read().split('\n')

def sixer():
    one = np.random.randint(len(words))
    two = np.random.randint(len(words))
    word = words[one] + words[two]
    word = word[:6]
    return word 


if __name__ == '__main__':
    print(sixer())
