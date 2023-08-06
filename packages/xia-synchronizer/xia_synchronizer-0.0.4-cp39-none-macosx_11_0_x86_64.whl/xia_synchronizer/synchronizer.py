from typing import Type, List
from datetime import datetime
from xia_models import DataModel, DataAddress


class Synchronizer:
    """Synchronizer get the data from the source and put it into target
    """
    model_manager: Type[DataModel] = None  # Data Model Management
    address_manager: Type[DataAddress] = None  # Data Address Management

    @classmethod
    def synchronize(cls, domain_name: str, model_name: str, doc_list: list, source_address: str, target_address: str):
        """copy data from source to target

        Args:
            domain_name: data model domain name
            model_name: data model name
            doc_list: list of document id
            source_address: source address
            target_address: target address
        """
        source_model = cls.address_manager.get_addressed_model(domain_name, model_name, source_address,
                                                               cls.model_manager)
        target_model = cls.address_manager.get_addressed_model(domain_name, model_name, target_address,
                                                               cls.model_manager)
        task_results = []
        for doc_id in doc_list:
            source_doc = source_model.load(doc_id)
            if source_doc:
                task_result = {"id": source_doc.get_id(), "op": "L"}
                try:
                    target_doc = target_model()
                    target_doc._data = source_doc._data  # Just pass the data
                    target_doc._id = source_doc._id  # Should also use the correct id name
                    target_doc.save()
                    task_result.update({"time": datetime.now().timestamp(), "status": 200})
                except Exception as e:
                    task_result.update({"time": datetime.now().timestamp(), "status": 500})
                task_results.append(task_result)
        return task_results
