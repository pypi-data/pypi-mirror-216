# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/protobuf/debug.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$tensorflow/core/protobuf/debug.proto\x12\ntensorflow\"\x8e\x01\n\x10\x44\x65\x62ugTensorWatch\x12\x11\n\tnode_name\x18\x01 \x01(\t\x12\x13\n\x0boutput_slot\x18\x02 \x01(\x05\x12\x11\n\tdebug_ops\x18\x03 \x03(\t\x12\x12\n\ndebug_urls\x18\x04 \x03(\t\x12+\n#tolerate_debug_op_creation_failures\x18\x05 \x01(\x08\"\x81\x01\n\x0c\x44\x65\x62ugOptions\x12=\n\x17\x64\x65\x62ug_tensor_watch_opts\x18\x04 \x03(\x0b\x32\x1c.tensorflow.DebugTensorWatch\x12\x13\n\x0bglobal_step\x18\n \x01(\x03\x12\x1d\n\x15reset_disk_byte_usage\x18\x0b \x01(\x08\"j\n\x12\x44\x65\x62uggedSourceFile\x12\x0c\n\x04host\x18\x01 \x01(\t\x12\x11\n\tfile_path\x18\x02 \x01(\t\x12\x15\n\rlast_modified\x18\x03 \x01(\x03\x12\r\n\x05\x62ytes\x18\x04 \x01(\x03\x12\r\n\x05lines\x18\x05 \x03(\t\"K\n\x13\x44\x65\x62uggedSourceFiles\x12\x34\n\x0csource_files\x18\x01 \x03(\x0b\x32\x1e.tensorflow.DebuggedSourceFileB\x83\x01\n\x18org.tensorflow.frameworkB\x0b\x44\x65\x62ugProtosP\x01ZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto\xf8\x01\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tensorflow.core.protobuf.debug_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030org.tensorflow.frameworkB\013DebugProtosP\001ZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto\370\001\001'
  _DEBUGTENSORWATCH._serialized_start=53
  _DEBUGTENSORWATCH._serialized_end=195
  _DEBUGOPTIONS._serialized_start=198
  _DEBUGOPTIONS._serialized_end=327
  _DEBUGGEDSOURCEFILE._serialized_start=329
  _DEBUGGEDSOURCEFILE._serialized_end=435
  _DEBUGGEDSOURCEFILES._serialized_start=437
  _DEBUGGEDSOURCEFILES._serialized_end=512
# @@protoc_insertion_point(module_scope)
