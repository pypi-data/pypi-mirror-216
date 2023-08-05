# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Ops related to Tensor Processing Units.
"""

import sys as _sys

from . import experimental
from tensorflow.python.tpu.bfloat16 import bfloat16_scope
from tensorflow.python.tpu.ops.tpu_ops import cross_replica_sum
from tensorflow.python.tpu.tpu import PaddingSpec
from tensorflow.python.tpu.tpu import XLAOptions
from tensorflow.python.tpu.tpu import batch_parallel
from tensorflow.python.tpu.tpu import initialize_system
from tensorflow.python.tpu.tpu import replicate
from tensorflow.python.tpu.tpu import rewrite
from tensorflow.python.tpu.tpu import shard
from tensorflow.python.tpu.tpu import shutdown_system
from tensorflow.python.tpu.tpu_name_util import core
from tensorflow.python.tpu.tpu_optimizer import CrossShardOptimizer
from tensorflow.python.tpu.tpu_replication import outside_compilation