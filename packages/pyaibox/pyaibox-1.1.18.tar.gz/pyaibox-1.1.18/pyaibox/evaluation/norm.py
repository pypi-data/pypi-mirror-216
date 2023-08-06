#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @file      : norm.py
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
import pyaibox as pb


def fnorm(X, caxis=None, axis=None, reduction='mean'):
    r"""obtain the f-norm of a array

    Both complex and real representation are supported.

    .. math::
       {\rm fnorm}({\bf X}) = \|{\bf X}\|_2 = \left(\sum_{x_i\in {\bf X}}|x_i|^2\right)^{\frac{1}{2}} = \left(\sum_{x_i\in {\bf X}}(u_i^2 + v_i^2)\right)^{\frac{1}{2}}

    where, :math:`u, v` are the real and imaginary part of :math:`x`, respectively.

    Parameters
    ----------
    X : array
        input
    caxis : int or None
        If :attr:`X` is complex-valued, :attr:`caxis` is ignored. If :attr:`X` is real-valued and :attr:`caxis` is integer
        then :attr:`X` will be treated as complex-valued, in this case, :attr:`caxis` specifies the complex axis;
        otherwise (None), :attr:`X` will be treated as real-valued
    axis : int or None
        The dimension axis (:attr:`caxis` is not included) for computing norm. The default is :obj:`None`, which means all. 
    reduction : str, optional
        The operation in batch dim, :obj:`None`, ``'mean'`` or ``'sum'`` (the default is ``'mean'``)
    
    Returns
    -------
    array
         the inputs's f-norm.

    Examples
    ---------

    ::

        np.random.seed(2020)
        X = np.random.randn(5, 2, 3, 4)

        # real
        C1 = fnorm(X, caxis=None, axis=(-2, -1), reduction=None)
        C2 = fnorm(X, caxis=None, axis=(-2, -1), reduction='sum')
        C3 = fnorm(X, caxis=None, axis=(-2, -1), reduction='mean')
        print(C1, C2, C3)

        # complex in real format
        C1 = fnorm(X, caxis=1, axis=(-2, -1), reduction=None)
        C2 = fnorm(X, caxis=1, axis=(-2, -1), reduction='sum')
        C3 = fnorm(X, caxis=1, axis=(-2, -1), reduction='mean')
        print(C1, C2, C3)

        # complex in complex format
        X = X[:, 0, ...] + 1j * X[:, 1, ...]
        C1 = fnorm(X, caxis=None, axis=(-2, -1), reduction=None)
        C2 = fnorm(X, caxis=None, axis=(-2, -1), reduction='sum')
        C3 = fnorm(X, caxis=None, axis=(-2, -1), reduction='mean')
        print(C1, C2, C3)

        # ---output
        ---norm
        [[3.18214671 3.28727232]
        [3.52423801 3.45821738]
        [3.07757733 3.23720035]
        [2.45488229 3.98372024]
        [2.23480914 3.73551246]] 32.1755762254205 3.21755762254205
        [4.57517398 4.93756225 4.46664844 4.67936684 4.35297889] 23.011730410021634 4.602346082004327
        [4.57517398 4.93756225 4.46664844 4.67936684 4.35297889] 23.011730410021634 4.602346082004327

    """

    if X.dtype in pb.dtypes('int') + pb.dtypes('uint'):
        X = X.astype(np.float64)

    if np.iscomplex(X).any():  # complex in complex
        if axis is None:
            F = np.sqrt(np.sum(X.real*X.real + X.imag*X.imag))
        else:
            F = np.sqrt(np.sum(X.real*X.real + X.imag*X.imag, axis=axis))
    else:
        if caxis is None:  # real
            if axis is None:
                F = np.sqrt(np.sum(X**2))
            else:
                F = np.sqrt(np.sum(X**2, axis=axis))
        else:  # complex in real
            d = np.ndim(X)
            idxreal = pb.sl(d, axis=caxis, idx=[0])
            idximag = pb.sl(d, axis=caxis, idx=[1])

            if axis is None:
                F = np.sqrt(np.sum(X[idxreal]**2 + X[idximag]**2))
            else:
                F = np.sqrt(np.sum(X[idxreal]**2 + X[idximag]**2, axis=axis))

    if reduction in ['mean', 'MEAN']:
        F = np.mean(F)
    if reduction in ['sum', 'SUM']:
        F = np.sum(F)

    return F

def pnorm(X, caxis=None, axis=None, p=2, reduction='mean'):
    r"""obtain the p-norm of a array

    Both complex and real representation are supported.

    .. math::
       {\rm pnorm}({\bf X}) = \|{\bf X}\|_p = \left(\sum_{x_i\in {\bf X}}|x_i|^p\right)^{\frac{1}{p}} = \left(\sum_{x_i\in {\bf X}}\sqrt{u_i^2+v^2}^p\right)^{\frac{1}{p}}

    where, :math:`u, v` are the real and imaginary part of :math:`x`, respectively.

    Parameters
    ----------
    X : array
        input
    caxis : int or None
        If :attr:`X` is complex-valued, :attr:`caxis` is ignored. If :attr:`X` is real-valued and :attr:`caxis` is integer
        then :attr:`X` will be treated as complex-valued, in this case, :attr:`caxis` specifies the complex axis;
        otherwise (None), :attr:`X` will be treated as real-valued
    axis : int or None
        The dimension axis (:attr:`caxis` is not included) for computing norm. The default is :obj:`None`, which means all. 
    p : int
        Specifies the power. The default is 2.
    reduction : str, optional
        The operation in batch dim, :obj:`None`, ``'mean'`` or ``'sum'`` (the default is ``'mean'``)
    
    Returns
    -------
    array
         the inputs's p-norm.

    Examples
    ---------

    ::

        np.random.seed(2020)
        X = np.random.randn(5, 2, 3, 4)

        # real
        C1 = pnorm(X, caxis=None, axis=(-2, -1), reduction=None)
        C2 = pnorm(X, caxis=None, axis=(-2, -1), reduction='sum')
        C3 = pnorm(X, caxis=None, axis=(-2, -1), reduction='mean')
        print(C1, C2, C3)

        # complex in real format
        C1 = pnorm(X, caxis=1, axis=(-2, -1), reduction=None)
        C2 = pnorm(X, caxis=1, axis=(-2, -1), reduction='sum')
        C3 = pnorm(X, caxis=1, axis=(-2, -1), reduction='mean')
        print(C1, C2, C3)

        # complex in complex format
        X = X[:, 0, ...] + 1j * X[:, 1, ...]
        C1 = pnorm(X, caxis=None, axis=(-2, -1), reduction=None)
        C2 = pnorm(X, caxis=None, axis=(-2, -1), reduction='sum')
        C3 = pnorm(X, caxis=None, axis=(-2, -1), reduction='mean')
        print(C1, C2, C3)

        # ---output
        ---pnorm
        [[3.18214671 3.28727232]
        [3.52423801 3.45821738]
        [3.07757733 3.23720035]
        [2.45488229 3.98372024]
        [2.23480914 3.73551246]] 32.1755762254205 3.21755762254205
        [4.57517398 4.93756225 4.46664844 4.67936684 4.35297889] 23.011730410021634 4.602346082004327
        [4.57517398 4.93756225 4.46664844 4.67936684 4.35297889] 23.011730410021634 4.602346082004327
    """

    if X.dtype in pb.dtypes('int') + pb.dtypes('uint'):
        X = X.astype(np.float64)

    if np.iscomplex(X).any():  # complex in complex
        if axis is None:
            F = np.power(np.sum(np.power(np.abs(X), p)), 1/p)
        else:
            F = np.power(np.sum(np.power(np.abs(X), p), axis=axis), 1/p)
    else:
        if caxis is None:  # real
            if axis is None:
                F = np.power(np.sum(np.power(np.abs(X), p)), 1/p)
            else:
                F = np.power(np.sum(np.power(np.abs(X), p), axis=axis), 1/p)
        else:  # complex in real
            d = np.ndim(X)
            idxreal = pb.sl(d, axis=caxis, idx=[0])
            idximag = pb.sl(d, axis=caxis, idx=[1])

            if axis is None:
                F = np.power(np.sum(np.power(np.sqrt(X[idxreal]**2 + X[idximag]**2), p)), 1/p)
            else:
                F = np.power(np.sum(np.power(np.sqrt(X[idxreal]**2 + X[idximag]**2), p), axis=axis), 1/p)

    if reduction in ['mean', 'MEAN']:
        F = np.mean(F)
    if reduction in ['sum', 'SUM']:
        F = np.sum(F)

    return F


if __name__ == '__main__':

    np.random.seed(2020)
    X = np.random.randn(5, 2, 3, 4)

    # real
    C1 = fnorm(X, caxis=None, axis=(-2, -1), reduction=None)
    C2 = fnorm(X, caxis=None, axis=(-2, -1), reduction='sum')
    C3 = fnorm(X, caxis=None, axis=(-2, -1), reduction='mean')
    print(C1, C2, C3)

    # complex in real format
    C1 = fnorm(X, caxis=1, axis=(-2, -1), reduction=None)
    C2 = fnorm(X, caxis=1, axis=(-2, -1), reduction='sum')
    C3 = fnorm(X, caxis=1, axis=(-2, -1), reduction='mean')
    print(C1, C2, C3)

    # complex in complex format
    X = X[:, 0, ...] + 1j * X[:, 1, ...]
    C1 = fnorm(X, caxis=None, axis=(-2, -1), reduction=None)
    C2 = fnorm(X, caxis=None, axis=(-2, -1), reduction='sum')
    C3 = fnorm(X, caxis=None, axis=(-2, -1), reduction='mean')
    print(C1, C2, C3)

    np.random.seed(2020)
    X = np.random.randn(5, 2, 3, 4)

    # real
    C1 = pnorm(X, caxis=None, axis=(-2, -1), reduction=None)
    C2 = pnorm(X, caxis=None, axis=(-2, -1), reduction='sum')
    C3 = pnorm(X, caxis=None, axis=(-2, -1), reduction='mean')
    print(C1, C2, C3)

    # complex in real format
    C1 = pnorm(X, caxis=1, axis=(-2, -1), reduction=None)
    C2 = pnorm(X, caxis=1, axis=(-2, -1), reduction='sum')
    C3 = pnorm(X, caxis=1, axis=(-2, -1), reduction='mean')
    print(C1, C2, C3)

    # complex in complex format
    X = X[:, 0, ...] + 1j * X[:, 1, ...]
    C1 = pnorm(X, caxis=None, axis=(-2, -1), reduction=None)
    C2 = pnorm(X, caxis=None, axis=(-2, -1), reduction='sum')
    C3 = pnorm(X, caxis=None, axis=(-2, -1), reduction='mean')
    print(C1, C2, C3)
