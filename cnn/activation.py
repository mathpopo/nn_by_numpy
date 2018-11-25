# coding:utf-8

import numpy as np

def fc_forward(X, W, b):
    out = X @ W + b # np.matmul(x, w)
    cache = (W, X)
    return out, cache

def fc_backward(dout, cache):
    w, h = cache

    dW = h.T @ dout
    db = np.sum(dout, axis=0)
    dX = dout @ w.T

    return dX, dW, db

def relu_forward(x):
    out = np.maximum(x, 0) #compare with 0
    cache = x
    return out, cache

def relu_backward(dout, cache):
    dX = dout.copy()
    dX[cache<=0] = 0
    return dX

# leaky relu
def lrelu_forward(x, a=1e-3):
    out = np.maximum(a*x, x)
    cache = (x, a)
    return out, cache

def lrelu_backward(dout, cache):
    x, a = cache
    dx = dout.copy()
    dx[x<0] *= a
    return dx

# https://blog.csdn.net/yuechuen/article/details/71502503
def bn_forward(x, gamma, beta, cache, momentum=0.9, train=True):
    running_mean, running_var = cache

    if train:
        mu = np.mean(x, axis=0)
        var = np.var(x, axis=0)

        x_norm = (x - mu) / np.sqrt(var + 1e-7)
        out = gamma * x_norm + beta

        cache = (x, x_norm, mu, var, gamma, beta)
        running_mean = momentum * running_mean + (1 - momentum) * mu
        running_var = momentum * running_var + (1 - momentum) * var

    else:
        x_norm = (x - running_mean) / np.sqrt(running_var + 1e-7)
        out = gamma * x_norm + beta
        cache = None

    return out, cache, running_mean, running_var

def bn_backward(dout, cache):
    x, x_norm, mu, var, gamma, beta = cache

    N, D = x.shape
    x_mu = x - mu
    std_inv = 1. / np.sqrt(var + 1e-7)

    dx_norm = dout * gamma
    dvar = -0.5 * np.sum(dx_norm * x_mu, axis=0)*std_inv**3
    dmu = -std_inv * np.sum(dx_norm, axis=0) - 2 *dvar * np.sum(x_mu, axis=0) / N

    dx = (dx_norm * std_inv) + (dvar * 2 * x_mu / N) + (dmu / N)
    dgamma = np.sum(dout * x_norm, axis=0)
    dbeta = np.sum(dout, axis=0)

    return dx, dgamma, dbeta

if __name__ == '__main__':
    pass


