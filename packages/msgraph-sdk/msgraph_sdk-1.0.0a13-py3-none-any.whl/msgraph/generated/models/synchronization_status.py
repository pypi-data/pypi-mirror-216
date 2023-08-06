from __future__ import annotations
import datetime
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .string_key_long_value_pair import StringKeyLongValuePair
    from .synchronization_progress import SynchronizationProgress
    from .synchronization_quarantine import SynchronizationQuarantine
    from .synchronization_status_code import SynchronizationStatusCode
    from .synchronization_task_execution import SynchronizationTaskExecution

@dataclass
class SynchronizationStatus(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The code property
    code: Optional[SynchronizationStatusCode] = None
    # The countSuccessiveCompleteFailures property
    count_successive_complete_failures: Optional[int] = None
    # The escrowsPruned property
    escrows_pruned: Optional[bool] = None
    # The lastExecution property
    last_execution: Optional[SynchronizationTaskExecution] = None
    # The lastSuccessfulExecution property
    last_successful_execution: Optional[SynchronizationTaskExecution] = None
    # The lastSuccessfulExecutionWithExports property
    last_successful_execution_with_exports: Optional[SynchronizationTaskExecution] = None
    # The OdataType property
    odata_type: Optional[str] = None
    # The progress property
    progress: Optional[List[SynchronizationProgress]] = None
    # The quarantine property
    quarantine: Optional[SynchronizationQuarantine] = None
    # The steadyStateFirstAchievedTime property
    steady_state_first_achieved_time: Optional[datetime.datetime] = None
    # The steadyStateLastAchievedTime property
    steady_state_last_achieved_time: Optional[datetime.datetime] = None
    # The synchronizedEntryCountByType property
    synchronized_entry_count_by_type: Optional[List[StringKeyLongValuePair]] = None
    # The troubleshootingUrl property
    troubleshooting_url: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> SynchronizationStatus:
        """
        Creates a new instance of the appropriate class based on discriminator value
        Args:
            parse_node: The parse node to use to read the discriminator value and create the object
        Returns: SynchronizationStatus
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return SynchronizationStatus()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .string_key_long_value_pair import StringKeyLongValuePair
        from .synchronization_progress import SynchronizationProgress
        from .synchronization_quarantine import SynchronizationQuarantine
        from .synchronization_status_code import SynchronizationStatusCode
        from .synchronization_task_execution import SynchronizationTaskExecution

        from .string_key_long_value_pair import StringKeyLongValuePair
        from .synchronization_progress import SynchronizationProgress
        from .synchronization_quarantine import SynchronizationQuarantine
        from .synchronization_status_code import SynchronizationStatusCode
        from .synchronization_task_execution import SynchronizationTaskExecution

        fields: Dict[str, Callable[[Any], None]] = {
            "code": lambda n : setattr(self, 'code', n.get_enum_value(SynchronizationStatusCode)),
            "countSuccessiveCompleteFailures": lambda n : setattr(self, 'count_successive_complete_failures', n.get_int_value()),
            "escrowsPruned": lambda n : setattr(self, 'escrows_pruned', n.get_bool_value()),
            "lastExecution": lambda n : setattr(self, 'last_execution', n.get_object_value(SynchronizationTaskExecution)),
            "lastSuccessfulExecution": lambda n : setattr(self, 'last_successful_execution', n.get_object_value(SynchronizationTaskExecution)),
            "lastSuccessfulExecutionWithExports": lambda n : setattr(self, 'last_successful_execution_with_exports', n.get_object_value(SynchronizationTaskExecution)),
            "@odata.type": lambda n : setattr(self, 'odata_type', n.get_str_value()),
            "progress": lambda n : setattr(self, 'progress', n.get_collection_of_object_values(SynchronizationProgress)),
            "quarantine": lambda n : setattr(self, 'quarantine', n.get_object_value(SynchronizationQuarantine)),
            "steadyStateFirstAchievedTime": lambda n : setattr(self, 'steady_state_first_achieved_time', n.get_datetime_value()),
            "steadyStateLastAchievedTime": lambda n : setattr(self, 'steady_state_last_achieved_time', n.get_datetime_value()),
            "synchronizedEntryCountByType": lambda n : setattr(self, 'synchronized_entry_count_by_type', n.get_collection_of_object_values(StringKeyLongValuePair)),
            "troubleshootingUrl": lambda n : setattr(self, 'troubleshooting_url', n.get_str_value()),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        Args:
            writer: Serialization writer to use to serialize this model
        """
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_enum_value("code", self.code)
        writer.write_int_value("countSuccessiveCompleteFailures", self.count_successive_complete_failures)
        writer.write_bool_value("escrowsPruned", self.escrows_pruned)
        writer.write_object_value("lastExecution", self.last_execution)
        writer.write_object_value("lastSuccessfulExecution", self.last_successful_execution)
        writer.write_object_value("lastSuccessfulExecutionWithExports", self.last_successful_execution_with_exports)
        writer.write_str_value("@odata.type", self.odata_type)
        writer.write_collection_of_object_values("progress", self.progress)
        writer.write_object_value("quarantine", self.quarantine)
        writer.write_datetime_value("steadyStateFirstAchievedTime", self.steady_state_first_achieved_time)
        writer.write_datetime_value("steadyStateLastAchievedTime", self.steady_state_last_achieved_time)
        writer.write_collection_of_object_values("synchronizedEntryCountByType", self.synchronized_entry_count_by_type)
        writer.write_str_value("troubleshootingUrl", self.troubleshooting_url)
        writer.write_additional_data_value(self.additional_data)
    

