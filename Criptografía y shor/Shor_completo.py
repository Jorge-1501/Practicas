import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from math import gcd
import random
import matplotlib.pyplot as plt
from qiskit_aer import Aer
from fractions import Fraction

# Compuerta c_U
def c_amod15(a, potencia):
    '''Compuerta control con a mod 15'''
    if a not in [2,4,7,8,11,13]:
        raise ValueError("'a' must be 2, 4, 7, 8, 11 o 13")
    U = QuantumCircuit(4)
    for _iteration in range(potencia):
        if a in [2, 13]:
            U.swap(2,3)
            U.swap(1,2)
            U.swap(0,1)
        if a in [7, 8]:
            U.swap(0,1)          
            U.swap(1,2)
            U.swap(2,3)
        if a in [4,11]:
            U.swap(1,3)          
            U.swap(0,2)
        if a in [7,11,13]:
            for q in range(4):
                U.x(q)
    U = U.to_gate()
    U.name = f"{a}^{potencia} mod 15"
    c_U = U.control()
    return c_U

# QFT inversa
def qft_dagger(n):
    '''n-quibit aplica QFTdagger a los primeros n quibits'''
    qc = QuantumCircuit(n)
    # Hacemos los respectivos swaps
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi / float(2**(j-m)), m, j)
        qc.h(j)
    qc.name = "QFT_dagger"
    return qc

# Order-finding algorithm
def quantum_order_finding(a, N):
    """
    Defines and executes the quantum circuit to find the period r of a^r mod N.
    """
    # Number of qubits for register and measurement
    n = int(np.ceil(np.log2(N))) 
    num_qubits = 2 * n  # We use 2n qubits in total
    
    # Definition of the quantum circuit
    qc = QuantumCircuit(num_qubits, n)
    
    # We apply hadarmard to the first n qibits
    for q in range(n):
        qc.h(q)
    
    # We initialize the auxiliary register to 1
    qc.x(n)
    
    # We perform the Control-U operations in the second register
    for q in range (n):
        qc.append(c_amod15(a, 2**q),
                [q] + [i + n for i in range(n)])

    
    # Apply the Inverse Quantum Fourier Transform
    qc.append(qft_dagger(n), range(n))
    
    # Measure the first n qibits
    qc.measure(range(n), range(n))
    
    # We draw the circuit
    qc.draw(fold=-1)

    # Run in the simulator
    aer_sim = Aer.get_backend('aer_simulator')
    t_qc = transpile(qc, aer_sim)
    counts = aer_sim.run(t_qc).result().get_counts()
    plot_histogram(counts)
    
    return counts


def classical_post_processing(counts, N, a):
    """
    Process the results of the quantum circuit to find the period r and obtain the factors of N.
    """
    measured_values = [int(k, 2) for k in counts.keys()]
    measured_values.sort()
    
    for m in measured_values:
        if m == 0:
            continue
        
        # Approximate the period r using continued fractions
        r = round(N / m)
        
        if r % 2 == 1:
            continue  # r must be even to apply factoring
        
        # Obtaining the factors of N
        factor1 = gcd(a**(r//2) - 1, N)
        factor2 = gcd(a**(r//2) + 1, N)
        
        if factor1 > 1 and factor1 < N:
            return factor1, factor2
    
    return None, None

def shor_algorithm(N):
    """
    Implement Shor's algorithm to factor N.
    """
    # A random number is chosen, a < N
    while True:
        a = random.randint(2, N//2) # ¡¡¡DESCUBRIMIENTO!!!
        if gcd(a, N) == 1:
            print(f"a = {a}")
            break
    
    # Run the quantum part
    counts = quantum_order_finding(a, N)
    
    # Classical processing to obtain the factors
    factor1, factor2 = classical_post_processing(counts, N, a)
    
    if factor1 is None:
        print("No factorization found, please try again.")
    else:
        print(f"The factors of {N} are {factor1} and {factor2}.")
    
    return factor1, factor2

# Ejecutar el algoritmo de Shor para un número N
N = 15  # Puedes cambiar este valor
shor_algorithm(N)
