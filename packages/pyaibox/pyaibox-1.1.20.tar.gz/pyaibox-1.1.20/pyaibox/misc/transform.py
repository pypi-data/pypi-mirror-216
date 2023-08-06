#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : transform.py
# @author    : Zhi Liu
# @email     : zhiliu.mind@gmail.com
# @homepage  : http://iridescent.ink
# @date      : Sun Nov 11 2019
# @version   : 0.0
# @license   : The GNU General Public License (GPL) v3.0
# @note      : 
# 
# The GNU General Public License (GPL) v3.0
# Copyright (C) 2013- Zhi Liu
#
# This file is part of pyaibox.
#
# pyaibox is free software: you can redistribute it and/or modify it under the 
# terms of the GNU General Public License as published by the Free Software Foundation, 
# either version 3 of the License, or (at your option) any later version.
#
# pyaibox is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with pyaibox. 
# If not, see <https://www.gnu.org/licenses/>. 
#

import numpy as np
from pyaibox.utils.const import EPS
from pyaibox.base.arrayops import sl
from pyaibox.base.mathops import nextpow2, c2r, r2c


def standardization(X, mean=None, std=None, axis=None, extra=False):
    r"""standardization

    .. math::
        \bar{X} = \frac{X-\mu}{\sigma}


    Args:
        X (ndarray): data to be normalized,
        mean (list or None, optional): mean value (the default is None, which means auto computed)
        std (list or None, optional): standard deviation (the default is None, which means auto computed)
        axis (list, tuple or int, optional): specify the axis for computing mean and standard deviation (the default is None, which means all elements)
        extra (bool, optional): if True, also return the mean and std (the default is False, which means just return the standardized data)

    Returns:
        (ndarray): Standardized/Normalized ndarray.
    """

    if type(X) is not np.ndarray:
        X = np.array(X)

    axis = tuple(axis) if type(axis) is list else axis

    if mean is None:
        if axis is None:
            mean = np.mean(X)
        else:
            mean = np.mean(X, axis, keepdims=True)
    if std is None:
        if axis is None:
            std = np.std(X)
        else:
            std = np.std(X, axis, keepdims=True)
    if extra is True:
        return (X - mean) / (std + EPS), mean, std
    else:
        return (X - mean) / (std + EPS)


def scale(X, st=[0, 1], sf=None, istrunc=True, extra=False):
    r"""

    Scale data.

    .. math::
        x \in [a, b] \rightarrow y \in [c, d]

    .. math::
        y = (d-c)*(x-a) / (b-a) + c.

    Args:
        X (ndarray): The data to be scaled.
        st (tuple, list, optional): Specifies the range of data after beening scaled. Default [0, 1].
        sf (tuple, list, optional): Specifies the range of data. Default [min(X), max(X)].
        istrunc (bool): Specifies wether to truncate the data to [a, b], For example,
            If sf == [a, b] and 'istrunc' is true,
            then X[X < a] == a and X[X > b] == b.
        extra (bool): If ``True``, also return :attr:`st` and :attr:`sf`.

    Returns:
        out (ndarray): Scaled data ndarray.
        st, sf (list or tuple): If :attr:`extra` is true, also be returned

    Raises:
        Exception: Description
    """

    if type(X) is not np.ndarray:
        X = np.array(X)

    cflag = False
    if np.any(np.iscomplex(X)):
        cflag = True

    if cflag:
        X = c2r(X)

    X = X.astype(np.float32)

    if not(isinstance(st, (tuple, list)) and len(st) == 2):
        raise Exception("'st' is a tuple or list, such as (-1,1)")
    if sf is not None:
        if not(isinstance(sf, (tuple, list)) and len(sf) == 2):
            raise Exception("'sf' is a tuple or list, such as (0, 255)")
    else:
        sf = [np.min(X) + 0.0, np.max(X) + 0.0]
    if sf[0] is None:
        sf = (np.min(X) + 0.0, sf[1])
    if sf[1] is None:
        sf = (sf[0], np.max(X) + 0.0)

    a = sf[0] + 0.0
    b = sf[1] + 0.0
    c = st[0] + 0.0
    d = st[1] + 0.0

    if istrunc:
        X[X < a] = a
        X[X > b] = b

    if cflag:
        X = r2c(X)

    if extra:
        return (X - a) * (d - c) / (b - a + EPS) + c, st, sf
    else:
        return (X - a) * (d - c) / (b - a + EPS) + c


def quantization(X, idrange=None, odrange=[0, 31], odtype='auto', extra=False):
    r"""

    Quantize data.

    .. math::
        {\bm X} \in [a, b] \rightarrow y \in [c, d]

    .. math::
        {\bm Y} = \lfloor (d-c) (X-a) / (b-a) + c \rfloor.

    Args:
        X (ndarray): The data to be quantized with shape :math:`{\bm X} \in {\mathbb R}^{N_a×N_r}`, or :math:`{\bm X} \in {\mathbb C}^{N_a×N_r}`.
        idrange (tuple, list, optional): Specifies the range of data. Default :math:`[{\rm min}(X), {\rm max}(X)]`.
        odrange (tuple, list, optional): Specifies the range of data after beening quantized. Default [0, 31].
        odtype (str or None, optional): output data type, supportted are ``'auto'`` (auto infer, default), or numpy ndarray's dtype string.
            If the type of :attr:`odtype` is not string(such as None), the type of output data is the same with input.
        extra (bool): If ``True``, also return :attr:`idrange` and :attr:`odrange`.

    Returns:
        (ndarray): Quantized data ndarray, if the input is complex, will return a ndarray with shape :math:`{\bm Y} \in {\mathbb R}^{N_a×N_r×2}`.
        idrange, odrange (list or tuple): If :attr:`extra` is true, also be returned

    Raises:
        Exception: :attr:`idrange` and :attr:`odrange` should be (tulpe) or (list)
    """

    if type(X) is not np.ndarray:
        X = np.array(X)
    cflag = False
    if np.any(np.iscomplex(X)):
        cflag = True

    if cflag:
        X = c2r(X)

    if not(isinstance(odrange, (tuple, list)) and len(odrange) == 2):
        raise Exception("'odrange' is a tuple or list, such as (-1,1)")
    if idrange is not None:
        if not(isinstance(idrange, (tuple, list)) and len(idrange) == 2):
            raise Exception("'idrange' is a tuple or list, such as (0, 255)")
    else:
        idrange = [X.min() + 0.0, X.max() + 0.0]
    if idrange[0] is None:
        idrange = (X.min() + 0.0, idrange[1])
    if idrange[1] is None:
        idrange = (idrange[0], X.max() + 0.0)

    a = idrange[0] + 0.0
    b = idrange[1] + 0.0
    c = odrange[0] + 0.0
    d = odrange[1] + 0.0

    X[X < a] = a
    X[X > b] = b

    X = (X - a) * (d - c) / (b - a + EPS) + c

    if odtype in ['auto', 'AUTO']:
        if odrange[0] >= 0:
            odtype = 'np.uint'
        else:
            odtype = 'np.int'
        odtype = odtype + str(nextpow2(odrange[1] - odrange[0]))

    if type(odtype) is str:
        X = X.to(eval(odtype))

    if cflag:
        X = r2c(X)

    if extra:
        return X, idrange, odrange
    else:
        return X


def db20(x):
    r"""compute dB

    Parameters
    ----------
    x : float or array
        linear value

    Returns
    -------
    float or array
        the dB value of x.
    """

    return 20. * np.log10(np.abs(x))


def ct2rt(x, axis=0):
    r"""Converts a complex-valued tensor to a real-valued tensor

    Converts a complex-valued tensor :math:`{\bf x}` to a real-valued tensor with FFT and conjugate symmetry.


    Parameters
    ----------
    x : Tensor
        The input tensor :math:`{\bf x}`.
    axis : int
        The axis for excuting FFT.

    Returns
    -------
    Tensor
        The output tensor :math:`{\bf y}`.

    see also :func:`rt2ct`.

    Examples
    ---------

    .. image:: ./_static/CT2RTRT2CTdemo.png
       :scale: 100 %
       :align: center

    The results shown in the above figure can be obtained by the following codes.

    ::

        import numpy as np
        import pyaibox as pb


        datafolder = pb.data_path('optical')
        xr = pb.imread(datafolder + 'Einstein256.png')
        xi = pb.imread(datafolder + 'LenaGRAY256.png')

        x = xr + 1j * xi

        y = pb.ct2rt(x, axis=0)
        z = pb.rt2ct(y, axis=0)

        print(x.shape, y.shape, z.shape)
        print(x.dtype, y.dtype, z.dtype)

        print(np.min(np.abs(x)), np.max(np.abs(x)))
        print(np.min(np.abs(y)), np.max(np.abs(y)))
        print(np.min(np.abs(z)), np.max(np.abs(z)))


        plt = pb.imshow([x.real, x.imag, y.real, y.imag, z.real, z.imag], nrows=3, ncols=2,
                        titles=['original(real)', 'original(imag)', 'converted(real)', 
                        'converted(imag)', 'reconstructed(real)', 'reconstructed(imag)'])
        plt.show()


    """

    d = np.ndim(x)
    n = x.shape[axis]
    X = np.fft.fft(x, axis=axis)
    X0 = X[sl(d, axis, [[0]])]
    Y = np.concatenate((X0.real, X[sl(d, axis, range(1, n))], X0.imag, np.conj(X[sl(d, axis, range(n - 1, 0, -1))])), axis=axis)

    del x, X
    y = np.fft.ifft(Y, axis=axis)

    return y


def rt2ct(y, axis=0):
    r"""Converts a real-valued tensor to a complex-valued tensor

    Converts a real-valued tensor :math:`{\bf y}` to a complex-valued tensor with FFT and conjugate symmetry.


    Parameters
    ----------
    y : Tensor
        The input tensor :math:`{\bf y}`.
    axis : int
        The axis for excuting FFT.

    Returns
    -------
    Tensor
        The output tensor :math:`{\bf x}`.
    
    see also :func:`ct2rt`.
    
    """

    d = np.ndim(y)
    n = y.shape[axis]

    Y = np.fft.fft(y, axis=axis)
    X = Y[sl(d, axis, range(0, int(n / 2)))]
    X[sl(d, axis, [[0]])] = X[sl(d, axis, [[0]])] + 1j * Y[sl(d, axis, [[int(n / 2)]])].real
    del y, Y
    x = np.fft.ifft(X, axis=axis)
    return x


if __name__ == '__main__':

    x = np.array([1, 2, 3]) + np.array([1, 2, 3]) * 1j

    y = ct2rt(x)
    z = rt2ct(y)

    print(x)
    print(y)
    print(z)

    X = np.random.randn(4, 3, 5, 6)
    XX = standardization(X, axis=(0, 2, 3))
    XX, meanv, stdv = standardization(X, axis=(0, 2, 3), extra=True)
    print(meanv, stdv)

    X = np.random.randn(4, 3, 5, 6) * 255
    XX = standardization(X, axis=(0, 2, 3))
    XX, meanv, stdv = standardization(X, axis=(0, 2, 3), extra=True)
    print(meanv, stdv)
    print(XX)

    XX = scale(X, st=[0, 1])
    print(XX)
