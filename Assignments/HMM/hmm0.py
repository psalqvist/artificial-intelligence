import sys

class HMM():
    def __init__(self):
        self.A = []
        self.B = []
        self.pi = []
        self.O = []

    def init(self):
        arrayA = input().split()
        arrayB = input().split()
        arrayPi = input().split()
        self.initMatrix(self.A, arrayA)
        self.initMatrix(self.B, arrayB)
        self.initMatrix(self.pi, arrayPi)
    
    def initMatrix(self, Mat, arr):
        a = int(arr[0])
        b = int(arr[1])
        for i in range(a):
            temp = []
            for j in range(b):
                temp.append(float(arr[j + i * b + 2]))
            Mat.append(temp)

    def matmul(self, A, B):
        res = [[0 for x in range(len(B[0]))] for y in range(len(A))]
        for i in range(len(A)):
            for j in range(len(B[0])):
                res[i][j] = 0
                for x in range(len(A[0])):           
                    res[i][j] += (A[i][x] * B[x][j])

        return res

    def next_emission(self, emm, A, B):
        res = self.matmul(emm, A)
        res = self.matmul(res, B)
        return res

if __name__ == '__main__':
    hmm = HMM()
    hmm.init()
    res = hmm.next_emission(hmm.pi, hmm.A, hmm.B)

    # print solution
    a = len(res)
    b = len(res[0])
    string = str(a) + " " + str(b)
    for i in range(a):
        for j in range(b):
            string = string + " " + str(res[i][j])
    print(string)