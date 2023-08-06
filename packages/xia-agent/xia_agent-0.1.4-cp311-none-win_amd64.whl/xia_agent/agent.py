import logging
from typing import Type, Union, Dict
from xia_fields import StringField
from xia_fields import DictField
from xia_engine import ListField, EmbeddedDocumentField
from xia_engine import Document, EmbeddedDocument
from xia_models import DataAddress, DataModel
from xia_logger import Logger, DataLog


class MetaFunction(type):
    """It defines some clss attributes level"""
    def __new__(mcs, *args, **kwargs):
        cls = super().__new__(mcs, *args, **kwargs)
        cls.logger_class.model_manager = cls.model_manager
        cls.logger_class.address_manager = cls.address_manager
        return cls


class AgentFunction(metaclass=MetaFunction):
    """Function of an agent. An agent could have several functions
    """
    logger_class: Type[Logger] = Logger  # Logger class
    model_manager: Type[DataModel] = DataModel  # Data Model Management
    address_manager: Type[DataAddress] = DataAddress  # Data Address Management


class AddressMapping(EmbeddedDocument):
    """Default Address Mapping"""
    _key_fields = ["domain_name", "model_name", "address_name"]

    domain_name: str = StringField(description="Data Domain Name")
    model_name: str = StringField(description="Data Model Name")
    address_name: str = StringField(description="Address Name", sample="sqlite_db1")
    runtime_module: str = StringField(description="Runtime Module Name")
    runtime_class: str = StringField(description="Runtime Class Name")
    runtime_replica: str = StringField(description="Runtime Replica Name", sample="sqlite")


class Agent(Document):
    """Agent organized in an agency who takes care of the data replications
    """
    _key_fields = ["agency_name", "agent_name"]

    agency_name: str = StringField(description="Agency Name")
    agent_name: str = StringField(description="Agent Name")

    runtime_mapping: list = ListField(EmbeddedDocumentField(document_type=AddressMapping),
                                      description="Predefined Runtime Models", default=[])
    source_config: dict = DictField(description="Default Address",
                                    default={"": {"": {}}},
                                    sample={"": {"": {"param_name": "sqlite"}}})
    logger_config: dict = DictField(description="Default Logger",
                                    default={"": {"": ""}},
                                    sample={"": {"": "logger name"}})
    target_config: dict = DictField(description="Default Target",
                                    default={"": {"": {}}},
                                    sample={"": {"": {"address_1": {}, "address_2": {}}}})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # We will put the predefined classes into Data Manager
        for mapping_item in self.runtime_mapping:
            # Step 1: Load runtime class
            runtime_model = AgentFunction.model_manager.load_class_from_runtime(
                mapping_item.runtime_module, mapping_item.runtime_class
            )
            if not runtime_model:
                raise ValueError(f"No Runtime Module Found {mapping_item.runtime_module}.{mapping_item.runtime_class}")
            # Step 2: Save to a temporary copy
            dumped_models = AgentFunction.model_manager.dump_models(runtime_model, {}, mapping_item.domain_name)
            for model_name, data_model in dumped_models.items():
                data_model.save()
            model_address = AgentFunction.address_manager.dump_address(runtime_model, mapping_item.runtime_replica)
            # Step 3: Reload the model
            loaded_model = dumped_models[mapping_item.runtime_class].load_class()
            model_address.assign_address(loaded_model)  # Assign address to the root
            # Step 4: Cache the model
            AgentFunction.model_manager.cache_model(mapping_item.domain_name, mapping_item.model_name, loaded_model)
            AgentFunction.address_manager.cache_addressed_model(
                mapping_item.domain_name, mapping_item.model_name, mapping_item.address_name, loaded_model
            )
            # Step 5: Clean the saved models from local RAM database
            for model_name, data_model in dumped_models.items():
                data_model.delete()


    def get_default_source(self, domain_name: str, model_name: str, address_name: str) -> Union[DataAddress, None]:
        """Get default source address configuration

        Args:
            domain_name: Data domain name
            model_name: Data model name
            address_name: Data address name

        Returns:
            None means the given data is not defined. So the treatment will be ignored.
            Or the DataAddress Object holding the default source configuration
        """
        domain_source = self.source_config.get(domain_name, self.source_config.get("", None))
        if not isinstance(domain_source, dict):
            return None
        address_config = domain_source.get(model_name, domain_source.get("", None))
        if address_config:
            address_config.update({"domain_name": domain_name, "model_name": model_name, "address_name": address_name})
            return DataAddress(**address_config)
        else:
            return None

    def get_default_logger(self, domain_name: str, model_name: str):
        """Get default Logger Name

        Args:
            domain_name: Data domain name
            model_name: Data model name

        Returns:
            None means the given logger is not defined. So the treatment will be ignored.
            Or the DataAddress Object holding the default source configuration
        """
        domain_logger = self.logger_config.get(domain_name, self.logger_config.get("", None))
        if not domain_logger:
            return None
        default_logger = domain_logger.get(model_name, domain_logger.get("", None))
        return default_logger if default_logger else None

    def get_default_target(self, domain_name: str, model_name: str) -> Dict[str, DataAddress]:
        """Get default target address configuration in dictionary

        Args:
            domain_name: Data domain name
            model_name: Data model name

        Returns:
            Empty dictionary means the given data is not defined. So the treatment will be ignored.
            Or the DataAddress Object holding the default source configuration
        """
        domain_target = self.target_config.get(domain_name, self.target_config.get("", None))
        if not domain_target:
            return {}
        default_target = domain_target.get(model_name, domain_target.get("", None))
        if not default_target:
            return {}
        default_target_objects = {}
        for target_address, target_config in default_target.items():
            if target_config:
                target_config.update(
                    {"domain_name": domain_name, "model_name": model_name, "address_name": target_address})
                default_target_objects[target_address] = DataAddress(**target_config)
            else:
                default_target_objects[target_address] = None
        return default_target_objects
