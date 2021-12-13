#/usr/bin/python3

import sys
import math

def init_float_list(line, l):
    line = line.replace('\n','').split(' ')
    a = int(line[0])
    b = int(line[1])
    for i in range(a):
        c = []
        for j in range(b):
            c.append(float(line[j + i * b + 2]))
        l.append(c)

def init_seq(line, l):
    line = line.replace('\n','').split(' ')
    a = int(line[0])
    for i in range(a):
        l.append(int(line[i + 1]))

def initialize(transition, emission, init, seq):
    line = sys.stdin.readline()
    init_float_list(line, transition)
    line = sys.stdin.readline()
    init_float_list(line, emission)
    line = sys.stdin.readline()
    init_float_list(line, init)
    line = sys.stdin.readline()
    init_seq(line, seq)

def print_list(l):
    s = ""
    for e in l:
        print(s, end=' ')

def print_res(l):
    print(len(l), len(l[0]), end=' ')
    for i in l:
        for j in i:
            print(round(j, 6), end=' ')
    print('')

def aPass(alpha, transition, emission, init, seq, c):
    N = len(init[0])
    T = len(seq)

    # Initialize alpha and c
    for i in range(T):
        c.append(0)
        a = []
        for j in range(N):
            a.append(0)
        alpha.append(a)

    # compute alpha[0][i]
    for i in range(N):
        alpha[0][i] = init[0][i] * emission[i][seq[0]]
        c[0] += alpha[0][i]
    
    # scale the alpha[o][i]
    c[0] = 1/c[0]
    for i in range(N):
        alpha[0][i] *= c[0]
    
    # compute alpha[t][i]
    for t in range(1, T):
        c[t] = 0
        for i in range(N):
            alpha[t][i] = 0
            for j in range(N):
                alpha[t][i] += alpha[t-1][j] * transition[j][i]
            alpha[t][i] *= emission[i][seq[t]]
            c[t] += alpha[t][i]

        # scale alpha[t][i]
        c[t] = 1/c[t]
        for i in range(N):
            alpha[t][i] *= c[t]

def bPass(beta, transition, emission, init, seq, c):
    N = len(init[0])
    T = len(seq)

    # Initialize beta
    for i in range(T):
        a = []
        for j in range(N):
            a.append(0)
        beta.append(a)
    
    # Let beta[T - 1][i] = 1, scaled by c[T - 1]
    for i in range(N):
        beta[T - 1][i] = c[T - 1]
    
    # beta-pass
    for t in range(T-2, 0, -1):
        for i in range(N):
            beta[t][i] = 0
            for j in range(N):
                beta[t][i] += transition[i][j] * emission[j][seq[t + 1]] * beta[t + 1][j]

            # scale beta[t][i] with same scale factor as alpha[t][i]
            beta[t][i] *= c[t]
    
def gammaCompute(gamma1, gamma2 ,alpha, beta, transition, emission, init, seq):
    N = len(init[0])
    T = len(seq)

    # Initialize gamma1 and gamma2
    for t in range(T):
        a = []
        b = []
        for i in range(N):
            c = []
            a.append(0)
            for j in range(N):
                c.append(0)
            b.append(c)
        gamma1.append(a)
        gamma2.append(b)

    # No neew to normalize gamma2[t][i][j] since using scaled alpha and beta
    for t in range(T-1):
        for i in range(N):
            gamma1[t][i] = 0
            for j in range(N):
                gamma2[t][i][j] = alpha[t][i] * transition[i][j] * emission[j][seq[t + 1]] * beta[t + 1][j]
                gamma1[t][i] += gamma2[t][i][j]
    
    # Special case for gamma1[T - 1][i] (as above, no need to normalize)
    for i in range(N):
        gamma1[T - 1][i] = alpha[T - 1][i]

def reEstimate(gamma1, gamma2, transition, emission, init, seq):
    M = len(emission[0])
    N = len(init[0])
    T = len(seq)

    # Re-estimate init
    for i in range(N):
        init[0][i] = gamma1[0][i]
    
    # Re-estimate transition
    for i in range(N):
        denom = 0
        for t in range(T-1):
            denom += gamma1[t][i]
        for j in range(N):
            numer = 0
            for t in range(T-1):
                numer += gamma2[t][i][j]
            transition[i][j] = numer/denom

    # Re-estimate emission
    for i in range(N):
        denom = 0
        for t in range(T):
            denom += gamma1[t][i]
        for j in range(M):
            numer = 0
            for t in range(T):
                if(seq[t] == j):
                    numer += gamma1[t][i]
            emission[i][j] = numer/denom
    
def computeLogProb(transition, emission, init, seq, c, oldLogProb, iters, maxIters):
    T = len(seq)

    logProb = 0
    for i in range(T):
        logProb += math.log(c[i])
    logProb = -logProb

    iters += 1
    if(iters < maxIters and logProb > oldLogProb):
        oldLogProb = logProb
        estimate(transition, emission, init, seq, c, oldLogProb, iters, maxIters)
    else:
        print(iters)
        print_res(transition)
        print_res(emission)

def estimate(transition, emission, init, seq, c, oldLogProb, iters, maxIters):
    alpha = []
    beta = []
    gamma1 = []
    gamma2 = []

    aPass(alpha, transition, emission, init, seq, c)
    bPass(beta, transition, emission, init, seq, c)
    gammaCompute(gamma1, gamma2, alpha, beta, transition, emission, init, seq)
    reEstimate(gamma1, gamma2, transition, emission, init, seq)
    computeLogProb(transition, emission, init, seq, c, oldLogProb, iters, maxIters)

def run(maxIters):
    iters = 0
    oldLogProb = -math.inf

    c = []
    transition = []
    emission = []
    init = []
    seq = []

    initialize(transition, emission, init, seq)
    estimate(transition, emission, init, seq, c, oldLogProb, iters, maxIters)

run(100)