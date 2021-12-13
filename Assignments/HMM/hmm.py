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
        try:
            O = input().split(' ')[1:]
            self.O = [int(element) for element in O]
        except EOFError:
            return
    
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

    def forward(self):
        T = len(self.O)
        N = len(self.A)

        # compute initial alpha
        alpha = [[0 for x in range(N)] for y in range(T)]
        for i in range(N):
            alpha[0][i] = self.pi[0][i]*self.B[i][self.O[0]]

        # compute remaining alpha recursively
        for t in range(1, T):
            for i in range(N):
                for j in range(N):
                    alpha[t][i] = alpha[t][i] + alpha[t-1][j]*self.A[j][i]
                alpha[t][i] = alpha[t][i]*self.B[i][self.O[t]]
        res=0
        for i in range(N):
            res=sum(alpha[T-1])
        return res

        
