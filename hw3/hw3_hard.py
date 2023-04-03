import numpy as np
from functools import lru_cache


class HashMixin:
    def __hash__(self):
        hash_value = self.data.sum() // 100 + self.data.sum() % 100
        return int(hash_value)

    def __eq__(self, other):
        return (self.data == other.data).all()


class DimensionError(ValueError):
    def __init__(
        self,
        x1_shape,
        x2_shape,
        message="A shape of the first matrix doesn't match a shape of the second",
    ):
        super().__init__(f'{message}: {x1_shape}, {x2_shape}')


class Matrix(HashMixin):
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

    @lru_cache()
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


np.random.seed(54)
A = Matrix(np.array([[1, 2], [3, 4]]))
B = Matrix(np.array([[1, 1], [1, 1]]))
C = Matrix(np.random.randint(0, 100, (2, 2)))
D = Matrix(np.array([[1, 1], [1, 1]]))

if hash(A) == hash(C) and A != C and B == D and A @ B != C @ D:
    A.to_text('artifacts/hard/A.txt')
    B.to_text('artifacts/hard/B.txt')
    C.to_text('artifacts/hard/C.txt')
    D.to_text('artifacts/hard/D.txt')
    (A @ B).to_text('artifacts/hard/AB.txt')
    (C @ D).to_text('artifacts/hard/CD.txt')
    with open('artifacts/hard/hash.txt', 'w') as f:
        f.write(str(hash(A @ B)))
        f.write('\n')
        f.write(str(hash(C @ D)))
