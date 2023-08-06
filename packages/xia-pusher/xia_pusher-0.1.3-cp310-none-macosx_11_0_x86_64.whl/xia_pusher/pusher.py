from xia_engine import Document
from xia_logger import DataLog
from xia_agent import Agent, AgentFunction


class Pusher(AgentFunction):
    """Pusher receive the log data and put it into target
    """

    @classmethod
    def push(cls, data_log: DataLog, agent: Agent):
        """Push data to destinations

        Args:
            data_log: List of data logs
            agent: Agent configuration object

        Returns:
            list of replication results. each result will have the following keys:
                * id: document id
                * op: operation type: "I" for insert, "D" for delete, "U" for update, "L" for load
                * time: time when data is replicated
                * status: status code of HTTP protocol
        """
        # Step 1: Get target information:
        domain_name, model_name = data_log.domain_name, data_log.model_name
        target_objects = agent.get_default_target(domain_name, model_name)
        # Step 2: Get parsed document
        task_results = []
        for parsed_doc in cls.logger_class.parse_log(data_log):
            header: DataLog = parsed_doc[0]
            doc: Document = parsed_doc[1]
            for address_name in target_objects:
                addressed_model = cls.address_manager.get_addressed_model(domain_name, model_name, address_name,
                                                                          cls.model_manager,
                                                                          target_objects[address_name])
                replication_task = {"content": doc, "op": header.operation_type, "seq": header.create_seq}
                task_results += addressed_model.replicate([replication_task])
        return task_results
