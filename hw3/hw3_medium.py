import numpy as np


class StrMixin:
    def __str__(self):
        return str(self.data)


class SaveMixin:
    def savetxt(self, filepath):
        np.savetxt(filepath, self.data)


class GetSetMixin:
    def __get__(self, instance, owner):
        return self.data

    def __set__(self, value):
        self.data = value


class Matrix(np.lib.mixins.NDArrayOperatorsMixin, SaveMixin, StrMixin, GetSetMixin):
    def __init__(self, data):
        self.data = np.asarray(data)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        inputs = tuple(x.data if isinstance(x, Matrix) else x for x in inputs)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.data)


np.random.seed(0)

a = Matrix(np.random.randint(0, 10, (10, 10)))
b = Matrix(np.random.randint(0, 10, (10, 10)))
(a + b).savetxt(r'artifacts/medium/matrix+.txt')
(a * b).savetxt(r'artifacts/medium/matrix1.txt')
(a @ b).savetxt('artifacts/medium/matrix@.txt')
