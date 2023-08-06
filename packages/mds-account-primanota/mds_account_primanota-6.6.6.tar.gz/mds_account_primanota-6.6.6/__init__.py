# -*- coding: utf-8 -*-
# This file is part of the prima-nota-module for Tryton from m-ds.de.
# The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .primanota import PrimaNota, PrimaNotaContext
from .analytic import PrimaNotaAnalytic


def register():
    Pool.register(
        PrimaNota,
        PrimaNotaContext,
        module='account_primanota',
        type_='model')
    Pool.register(
        PrimaNotaAnalytic,
        module='account_primanota',
        type_='model',
        depends=['analytic_account'])
