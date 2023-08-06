import uuid
from typing import Union
from google.protobuf.descriptor_pb2 import DescriptorProto, FieldDescriptorProto, FileDescriptorProto
from google.protobuf import message_factory, descriptor_pool


class EasyProto:
    # Standard Google Definition Mapping
    type_dict = {
        float: 1,
        int: 3,
        bool: 8,
        str: 9,
        bytes: 12
    }
    MESSAGE = 11

    library = {}

    @classmethod
    def serialize(cls, raw_data: Union[list, dict], label: str = "", sample_data: dict = None, message_class=None):
        """Serialize Data from json format to

        Args:
            label (str): Label of compiled object in order to reuse it. Leave it empty if data structure is dynamic
            raw_data (list or dict): Python object
            sample_data (dict): A dictionary who has all fields, will parse raw_data if not provided
            message_class : A given message class to be used
        Returns:
            message class: Message class
            list of bytes: List of serialized object
        """
        if not label:
            label = "L" + str(uuid.uuid4()).replace("-", "")
        file_name = label.lower() + ".proto"
        file_desc = FileDescriptorProto(name=file_name, package="", syntax="proto3")
        serialized_list = []
        raw_data = [raw_data] if isinstance(raw_data, dict) else raw_data
        if label in cls.library:
            message_class = cls.library[label]
        if message_class is None:
            if sample_data is None:
                sample_data = {}
                for raw_dict in raw_data:
                    cls._sample_from_dict(raw_dict, sample_data)
            data_desc = cls._pb_from_dict(label, sample_data)
            file_desc.message_type.add().MergeFrom(data_desc)
            message_class = message_factory.GetMessages([file_desc])[label]
            cls.library[label] = message_class
        for raw_dict in raw_data:
            message = message_class()
            cls._dict_to_message(raw_dict, message)
            serialized_list.append(message.SerializeToString())
        return message_class, serialized_list

    @classmethod
    def _dict_to_message(cls, data_dict: dict, message):
        """Set message value from a given data dictionary

        Args:
            data_dict: data dictionary with value
            message: protobuf message
        """
        for key, value in data_dict.items():
            if isinstance(value, (str, bool, float, int, bytes)):
                setattr(message, key, value)
            elif isinstance(value, dict) and value:
                child_message = getattr(message, key)
                cls._dict_to_message(value, child_message)
            elif isinstance(value, list) and value:
                child_node = getattr(message, key)
                if isinstance(value[0], (str, bool, float, int, bytes)):
                    child_node.extend(value)
                elif isinstance(value[0], dict):
                    for item in value:
                        child_message = child_node.add()
                        cls._dict_to_message(item, child_message)

    @classmethod
    def _sample_from_dict(cls, origin: dict, sample_dict: dict):
        """Get the "maximum" possible fields

        Args:
            origin (dict): Data dictionary
            sample_dict (dict): Target dictionary to be enriched
        """
        for key, value in origin.items():
            if isinstance(value, (str, bool, float, int, bytes)):
                if key not in sample_dict:
                    sample_dict[key] = value
            elif isinstance(value, dict) and value:
                sample_dict[key] = sample_dict[key] if key in sample_dict else {}
                cls._sample_from_dict(value, sample_dict[key])
            elif isinstance(value, list) and value:
                if isinstance(value[0], (str, bool, float, int, bytes)):
                    if key not in sample_dict:
                        sample_dict[key] = value
                elif isinstance(value[0], dict):
                    sample_dict[key] = sample_dict[key] if key in sample_dict else [{}]
                    for line in value:
                        cls._sample_from_dict(line, sample_dict[key][0])

    @classmethod
    def _pb_from_dict(cls, label: str, data: dict) -> DescriptorProto:
        """Get descriptor from python dictionary

        Args:
            label: top data class name
            data: dictionary type of data

        Returns:
            File descriptor
        """
        fields, children = [], []
        for i, (key, value) in enumerate(data.items()):
            if isinstance(value, (str, bool, float, int, bytes)):
                fields.append(FieldDescriptorProto(name=key, number=i+1, label=1, type=cls.type_dict[type(value)]))
            elif isinstance(value, dict) and value:  # ignore empty dict
                children.append(cls._pb_from_dict(key.title(), value))
                fields.append(FieldDescriptorProto(name=key, number=i+1, label=1, type=cls.MESSAGE,
                                                   type_name=".".join([label, key.title()])))
            elif isinstance(value, list) and value:  # ignore empty list
                if isinstance(value[0], (str, bool, float, int, bytes)):
                    fields.append(FieldDescriptorProto(name=key, number=i + 1, label=3,
                                                       type=cls.type_dict[type(value[0])]))
                elif isinstance(value[0], dict) and value:
                    children.append(cls._pb_from_dict(key.title(), value[0]))
                    fields.append(FieldDescriptorProto(name=key, number=i + 1, label=3, type=cls.MESSAGE,
                                                       type_name=".".join([label, key.title()])))
        desc = DescriptorProto(name=label.split(".")[-1], field=fields)
        for child in children:
            desc.nested_type.add().MergeFrom(child)
        return desc
