import sys
"""
Estimate sequence of hidden states given observation sequence
"""
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
        O = input().split(' ')
        O = [x for x in O if x.strip()]
        O = O[1:]
        self.O = [int(element) for element in O]
    
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

    """
    Finds the hidden states in time steps 1:T given observation sequence O in 1:T and model lambda
    """
    def viterbi(self):
        T = len(self.O)
        N = len(self.A)

        
        delta = [[0 for x in range(N)] for y in range(T)]
        index = [[0 for x in range(N)] for y in range(T-1)]

        # compute base case delta
        for i in range(N):
            delta[0][i] = self.pi[0][i]*self.B[i][self.O[0]]
        
        # compute remaining delta and store indeces
        for t in range(1, T):
            for i in range(N):
                temp = []
                for j in range(N):
                    temp.append(delta[t-1][j]*self.A[j][i]*self.B[i][self.O[t]])
                # store probability of most likely current state, and index for most likely previous state
                max_value = max(temp)
                delta[t][i] = max_value
                index[t-1][i] = temp.index(max_value)
        
        # backtrack from most likely ending state at time step T to time step 0 to find the path of most likely hidden states
        result = []
        back_track = delta[T-1].index(max(delta[T-1]))
        result.append(back_track)
        for t in range(T-2, -1, -1):
            back_track = index[t][back_track]
            result.append(back_track)
        result.reverse()
        return result

                

if __name__ == '__main__':
    hmm = HMM()
    hmm.init()
    result = hmm.viterbi()
    print(' '.join(map(str, result)))