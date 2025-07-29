import math

class Dft:
    def __init__(self):
        pass

    def forward_transform(self, matrix):
        """ Computes the forward Fourier transform of the input matrix
        takes as input:
        matrix: a 2d matrix
        returns a complex matrix representing Fourier transform"""
        M = len(matrix)
        N = len(matrix[0])
        result = []

        for u in range(M):
            row = []
            for v in range(N):
                real = 0
                imag = 0
                for x in range(M):
                    for y in range(N):
                        angle = -2 * math.pi * ((u * x) / M + (v * y) / N)
                        real += matrix[x][y] * math.cos(angle)
                        imag += matrix[x][y] * math.sin(angle)
                row.append(complex(real, imag))
            result.append(row)
        return result

    def inverse_transform(self, matrix):
        """ Computes the inverse Fourier transform of the input matrix
        You can implement the inverse transform formula with or without the normalizing factor.
        Both formulas are accepted.
        takes as input:
        matrix: a 2d matrix (DFT) usually complex
        returns a complex matrix representing the inverse Fourier transform"""
        M = len(matrix)
        N = len(matrix[0])
        result = []

        for x in range(M):
            row = []
            for y in range(N):
                real = 0
                imag = 0
                for u in range(M):
                    for v in range(N):
                        angle = 2 * math.pi * ((u * x) / M + (v * y) / N)
                        real += matrix[u][v].real * math.cos(angle) - matrix[u][v].imag * math.sin(angle)
                        imag += matrix[u][v].real * math.sin(angle) + matrix[u][v].imag * math.cos(angle)
                real /= (M * N)
                imag /= (M * N)
                row.append(complex(real, imag))
            result.append(row)
        return result

    def magnitude(self, matrix):
        """ Computes the magnitude of the input matrix (iDFT)
        takes as input:
        matrix: a 2d matrix
        returns a matrix representing the magnitude of the complex matrix"""
        M = len(matrix)
        N = len(matrix[0])
        mag = []

        for i in range(M):
            row = []
            for j in range(N):
                val = matrix[i][j]
                row.append(math.sqrt(val.real**2 + val.imag**2))
            mag.append(row)
        return mag
