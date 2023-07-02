import math
import numpy as np

fl = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
l = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
bj = np.zeros(10)


class ComputeTraffic:
    def __init__(self):
        self.fl = 0.5
        self.l = 0.05
        self.v = 5000
        self.P = 100
        self.C = 7 * 10 ** 6
        self.BWj = 10
        self.CF = 2110
        self.noise_sigma = -104
        self.d = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.lamda_value=299_792_458/self.CF
        pass

    def g(self, x):
        g = 10 * math.log10((self.lamda_value ** 2) / (4 * math.pi * d ** 2))
        return g

    def calculate_SNR(self, x, P, g):
        snr = (self.P * g(x)) / self.noise_sigma ** 2
        return snr

    def calculate_cj(self, x):
        """
        :param BWj:
        :param x:
        :return:
        """
        p = 2  # to be calculated
        sigma = 1
        cj = self.BWj * math.log2(1 + self.calculate_SNR(x, P, g, sigma))
        return cj

    def calculate_ej(self, x):
        """
        :param x:
        :return:
        """
        ej = (fl(x) * l(x) * bj(x)) / self.calculate_cj(x)
        return ej

    def calculate_TLj(self, x):
        """
        :param x:
        :return:
        """
        TLj = np.sum(self.calculate_ej(x))
        return TLj


def estimate_Lm(j):
    pass


# Function to estimate Lm(j)
# ...

def estimate_Lp(j):
    pass


# Function to estimate Lp(j)
# ...

def disInCoverageAreaOf(j):
    pass


# Function to check if d is in the coverage area of j
# ...

def find_device_fog_mapping(D, J):
    NodeMap = []

    while True:
        for d in D:
            min_cost = float('inf')
            min_node = None
            for j in J:
                if disInCoverageAreaOf(j):
                    Lm_j = estimate_Lm(j)
                    Lp_j = estimate_Lp(j)
                    cost = Lm_j + Lp_j
                    if cost < min_cost:
                        min_cost = cost
                        min_node = j
            NodeMap.append((d, min_node))

        L = []
        for j in J:
            L.append(estimate_Lm(j) + estimate_Lp(j))
        if sum(L) == min(L):
            break

    return NodeMap


# Example usage
D = [...]  # Set of IoT Devices
J = [...]  # Set of Fog Nodes

node_mapping = find_device_fog_mapping(D, J)
print(node_mapping)
