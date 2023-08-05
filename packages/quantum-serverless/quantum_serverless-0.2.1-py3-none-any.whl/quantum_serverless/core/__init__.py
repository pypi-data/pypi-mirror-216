# This code is a Qiskit project.
#
# (C) Copyright IBM 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
============================================
Core module (:mod:`quantum_serverless.core`)
============================================

.. currentmodule:: quantum_serverless.core

Quantum serverless core module classes and functions
====================================================

Core abstractions
-----------------

.. autosummary::
    :toctree: ../stubs/

    Provider
    GatewayProvider
    KuberayProvider
    ComputeResource

    save_result
    distribute_task
    get
    put
    get_refs_by_status


Events classes
--------------

.. autosummary::
    :toctree: ../stubs/

    EventHandler
    RedisEventHandler
    ExecutionMessage

State classes
-------------

.. autosummary::
    :toctree: ../stubs/

    StateHandler
    RedisStateHandler
"""

from .provider import Provider, ComputeResource, KuberayProvider, GatewayProvider
from .decorators import (
    remote,
    get,
    put,
    get_refs_by_status,
    distribute_task,
)
from .events import RedisEventHandler, EventHandler, ExecutionMessage
from .state import RedisStateHandler, StateHandler
from .job import save_result
