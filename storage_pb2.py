# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: storage.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rstorage.proto\x12\x07storage\":\n\x07Request\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12\x13\n\x0bsource_node\x18\x03 \x01(\t\"\x19\n\x08Response\x12\r\n\x05value\x18\x01 \x01(\t\"}\n\x0bSyncRequest\x12,\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x1e.storage.SyncRequest.DataEntry\x12\x13\n\x0bsource_node\x18\x02 \x01(\t\x1a+\n\tDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x1f\n\x0cSyncResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2\xfb\x01\n\rKeyValueStore\x12*\n\x03Put\x12\x10.storage.Request\x1a\x11.storage.Response\x12*\n\x03Get\x12\x10.storage.Request\x1a\x11.storage.Response\x12-\n\x06\x44\x65lete\x12\x10.storage.Request\x1a\x11.storage.Response\x12*\n\x03Set\x12\x10.storage.Request\x1a\x11.storage.Response\x12\x37\n\x08SyncData\x12\x14.storage.SyncRequest\x1a\x15.storage.SyncResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'storage_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _SYNCREQUEST_DATAENTRY._options = None
  _SYNCREQUEST_DATAENTRY._serialized_options = b'8\001'
  _globals['_REQUEST']._serialized_start=26
  _globals['_REQUEST']._serialized_end=84
  _globals['_RESPONSE']._serialized_start=86
  _globals['_RESPONSE']._serialized_end=111
  _globals['_SYNCREQUEST']._serialized_start=113
  _globals['_SYNCREQUEST']._serialized_end=238
  _globals['_SYNCREQUEST_DATAENTRY']._serialized_start=195
  _globals['_SYNCREQUEST_DATAENTRY']._serialized_end=238
  _globals['_SYNCRESPONSE']._serialized_start=240
  _globals['_SYNCRESPONSE']._serialized_end=271
  _globals['_KEYVALUESTORE']._serialized_start=274
  _globals['_KEYVALUESTORE']._serialized_end=525
# @@protoc_insertion_point(module_scope)
