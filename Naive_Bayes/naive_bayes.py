import numpy as np
from sklearn.naive_bayes import BernoulliNB
from sklearn.utils import check_random_state

class BernoulliNB_(object):
    def __init__(self):
        #self.alpha = alpha
        pass

    def fit(self, X, y):
        m, n = X.shape
        #if y.shape != ()
        y0_index = y == 0
        y1_index = y == 1

        ny_0 = y0_index.sum()
        ny_1 = m - ny_0

        p0 = np.zeros((2, n))
        p1 = np.zeros((2, n))

        # P(x_j = 1 | y = 0)
        p0[1, :] = (X[y0_index, :].sum(axis = 0) + 1).astype(float)/(ny_0 + 2)
        # P(x_j = 0 | y = 0)
        p0[0, :] = 1 - p0[1, :]

        # P(x_j = 1 | y = 1)
        p1[1, :] = (X[y1_index, :].sum(axis = 0) + 1).astype(float)/(ny_1 + 2)
        # P(x_j = 0 | y = 1)
        p1[0, :] = 1 - p1[1, :]

        self.p0_l = np.log(p0)
        self.p1_l = np.log(p1)
        self.ny_0_l = np.log(ny_0)
        self.ny_1_l = np.log(ny_1)

    def predict(self, X):
        y_pred = np.zeros((m, 1), dtype=int)
        #P(x | y = 0) * p(y = 0)
        for i, x in enumerate(X):
            x_ = np.array([1 - x, x])
            #metric0 = 0
            #for j in range(n):
            #    metric0 += p0[x[j], j]

            metric0 = (self.p0_l * x_).sum()

            #metric1 = 0
            #for j in range(n):
            #    metric1 += p1[x[j], j]
            metric1 = (self.p1_l * x_).sum()

            metric0 += self.ny_0_l
            metric1 += self.ny_1_l
            y_pred[i] = int(metric0 < metric1)
        return y_pred


if __name__ == '__main__':

    m = 20000
    n = 100
    rs = check_random_state(seed=None)

    X = rs.randint(2, size=(m, n))
    y = rs.randint(2, size=(m,))

    clf = BernoulliNB(alpha=1, binarize=None, fit_prior=False)
    clf.fit(X, y)

    # print X
    print (y == clf.predict(X)).mean()

    clf = BernoulliNB_()
    clf.fit(X, y)
    print (y == clf.predict(X)).mean()