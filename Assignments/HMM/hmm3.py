import math

"""
Estimate model parameters using Baum Welch algorithms
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
    Probability of the given observation sequence
    """
    def forward(self):
        T = len(self.O)
        N = len(self.A)
        alpha = [[0 for x in range(N)] for y in range(T)]
        scale = [0 for x in range(T)]

        # compute initial alpha at time step 0
        for i in range(N):
            alpha[0][i] = self.pi[0][i]*self.B[i][self.O[0]]
            scale[0] += alpha[0][i]

        # scale initial alpha
        scale[0] = 1/scale[0]
        for i in range(N):
            alpha[0][i] = alpha[0][i]*scale[0]


        # compute alpha at remaining time steps
        for t in range(1, T):
            for i in range(N):
                for j in range(N):
                    alpha[t][i] += alpha[t-1][j]*self.A[j][i]
                alpha[t][i] = alpha[t][i]*self.B[i][self.O[t]]
                scale[t] += alpha[t][i]
            
            # scale alpha at time step t
            scale[t]=1/scale[t]
            for i in range(N):
                alpha[t][i] = scale[t]*alpha[t][i]

        return [alpha, scale]
    
    def backward(self, scale):
        T = len(self.O)
        N = len(self.A)
        beta = [[0 for x in range(N)] for y in range(T)]

        # compute beta at time step T, scale using same value as for alpha
        for i in range(N):
            beta[T-1][i] = scale[T-1]
        

        # compute beta at remaining time steps
        for t in range(T-2, -1, -1):
            for i in range(N):
                for j in range(N):
                    beta[t][i] += self.A[i][j]*self.B[j][self.O[t+1]]*beta[t+1][j]
                # scale using same values as fopr alpha
                beta[t][i] *= scale[t]
        return beta

    
    """
    Calculates gamma and digamma
    """
    def gamma(self, alpha, beta):
        T = len(self.O)
        N = len(self.A)
        gamma = [[0.0 for x in range(N)] for y in range(T)]
        di_gamma = [[[0.0 for x in range(N)] for y in range(N)] for z in range(T)]
        for t in range(T-1):
            for i in range(N):
                for j in range(N):
                    di_gamma[t][i][j] = alpha[t][i]*self.A[i][j]*self.B[j][self.O[t+1]]*beta[t+1][j]
                    gamma[t][i] += di_gamma[t][i][j]

        for i in range(N):
            gamma[T-1][i] = alpha[T-1][i]
        
        return [gamma, di_gamma]
    
    """
    Estimate value of A, B and pi given gamma and digamma
    """
    def estimate(self, gamma, di_gamma):
        T = len(self.O)
        N = len(self.A)
        M = len(self.B[0])

        # estimation of pi
        for i in range(N):
            self.pi[0][i] = gamma[0][i]
        
        # estimation of A
        for i in range(N):
            denom = 0
            for t in range(T-1):
                denom += gamma[t][i]
            for j in range(N):
                numer = 0
                for t in range(T-1):
                    numer += di_gamma[t][i][j]
                self.A[i][j] = numer/denom
        
        # estimation of B
        for i in range(N):
            denom = 0
            for t in range(T):
                denom += gamma[t][i]
            for j in range(M):
                numer = 0
                for t in range(T):
                    if self.O[t] == j:
                        numer += gamma[t][i]
                self.B[i][j] = numer/denom
    """
    Calculates log(P(O|lambda))
    """
    def log_prob(self, scale):
        T = len(self.O)
        logProb = 0
        for t in range(T):
            logProb += math.log(scale[t])
        logProb = -logProb
        return logProb

    def print_line(self, matrix):
        print(str(len(matrix)) + ' ' + str(len(matrix[0])), end=' ')
        for i in matrix:
            for j in i:
                print(round(j, 6), end=' ')
        print()
    

    """
    Estimate model parameters A, B and pi until we reach max number of 
    iterations or we no longer increase accuracy
    """
    def baum_welch(self, max):
        self.init()
        old_log_prob = -math.inf
        
        for i in range(max):
            alpha, scale = self.forward()
            beta = self.backward(scale)
            gamma, di_gamma = self.gamma(alpha, beta)
            self.estimate(gamma, di_gamma)

            # ensure that log(P(O|lamda)) is increasing each iteration
            log_prob = self.log_prob(scale)
            if log_prob > old_log_prob:
                old_log_prob = log_prob
            else:
                break
        self.print_line(self.A)
        self.print_line(self.B)
            

if __name__ == '__main__':
    HMM().baum_welch(100)
    
    