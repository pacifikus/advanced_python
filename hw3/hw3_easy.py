import numpy as np


class DimensionError(ValueError):
    def __init__(
            self,
            x1_shape,
            x2_shape,
            message="A shape of the first matrix doesn't match a shape of the second",
    ):
        super().__init__(f'{message}: {x1_shape}, {x2_shape}')


class Matrix:
    def __init__(self, data):
        self.data = data
        self.shape = len(data), len(data[0])

    def __add__(self, other) -> 'Matrix':
        if self.shape != other.shape:
            raise DimensionError(self.shape, other.shape)
        data = [x + y for x, y in zip(self.data, other.data)]
        data = np.array(data).reshape(self.shape)
        return Matrix(data=data)

    def __mul__(self, other):
        if self.shape != other.shape:
            raise DimensionError(self.shape, other.shape)
        data = [x * y for x, y in zip(self.data, other.data)]
        data = np.array(data).reshape(self.shape)
        return Matrix(data=data)

    def __matmul__(self, other):
        if self.shape[1] != other.shape[0]:
            raise DimensionError(
                self.shape,
                other.shape,
                message='Matrices dimensions are mismatched: '
                        'you need (n?,k),(k,m?)->(n?,m?), but have: '
            )
        n = self.shape[0]
        m = other.shape[1]
        result = Matrix(np.zeros((n, m)))
        for i in range(n):
            for j in range(m):
                for k in range(m):
                    result.data[i][j] += self.data[i][k] * other.data[k][j]
        return result

    def to_text(self, filepath):
        as_str = np.array2string(self.data)
        with open(filepath, mode='w') as f:
            f.write(as_str)


np.random.seed(0)

a = Matrix(np.random.randint(0, 10, (10, 10)))
b = Matrix(np.random.randint(0, 10, (10, 10)))
(a + b).to_text(r'artifacts/easy/matrix+.txt')
(a * b).to_text(r'artifacts/easy/matrix*.txt')
(a @ b).to_text('artifacts/easy/matrix@.txt')
