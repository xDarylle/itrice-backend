import numpy as np
from sklearn.linear_model import LinearRegression


def predict(X, Y):
    x = np.array(X).reshape((-1, 1))
    y = np.array(Y)

    model = LinearRegression().fit(x, y)
    y_pred = model.predict(x)
    return y_pred

