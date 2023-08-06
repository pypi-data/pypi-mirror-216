"""
This module defines data classes that are used by the IDUN Data API, defined with Pydantic.
"""

from enum import Enum
from datetime import datetime
from pydantic import BaseModel, root_validator, validator
from .parameters import MAX_ID_LENGTH


class DataStreams(BaseModel):
    "Real time data streams available to return to the client"

    bandpass_eeg: bool = False
    "Enables a stream of bandpass filtered EEG signal"
    # The following options are not yet supported
    # raw_eeg: bool = False
    # spectrogram: bool= False

    @root_validator
    def validate_streaming_modes(cls, values):
        "Forbid invalid streaming mode selection"
        return values


class RecordingConfig(BaseModel):
    data_stream_subscription: DataStreams | None = None
    "Subscribe to real time data streams. No data stream by default."


class recordingstatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    ONGOING = "ONGOING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class _RecordingStatus(BaseModel):
    stopped: bool
    "Is the recording still receiving data?"


class RecordingStatusIn(_RecordingStatus):
    pass


class RecordingStatusOut(_RecordingStatus):
    status: recordingstatus | None = None
    message: str | None = None
    "Explanation about the current status"
    startDeviceTimestamp: datetime | None = None
    """Device timestamp of the first message in the recording.
    It is provided by the client, so it can be unreliable for BI purposes.
    """
    stopDeviceTimestamp: datetime | None = None
    """Device timestamp of the last message in the recording.
    It is provided by the client, so it can be unreliable for BI purposes.
    """
    createdAt: datetime | None = None
    """Local timestamp of the API at the moment that this recording was created.
    """
    stoppedAt: datetime | None = None
    """Local timestamp of the API at the moment that this recording was stopped.
    """


class _Recording(BaseModel):
    recordingID: str
    deviceID: str
    displayName: str
    "User-friendly name used in the UI"

    @validator("recordingID", "deviceID", "displayName")
    def limit_length(cls, v, field):
        # TODO: validate ID regex
        if len(v) > MAX_ID_LENGTH:
            raise ValueError(f"{field} is too long. Max length: {MAX_ID_LENGTH}")
        return v


class RecordingIn(_Recording):
    """
    RecordingIn can be used to create/update recordings in the IDUN REST API.
    A Recording is a contiguous data capture session of the IDUN Guardian through a specific frontend client.
    """

    config: RecordingConfig | None = None


class RecordingOut(_Recording):
    """
    RecordingOut is returned by the IDUN REST API to describe existing recordings.
    A Recording is a contiguous data capture session of the IDUN Guardian through a specific frontend client.
    """

    status: RecordingStatusOut
    config: RecordingConfig | None = None
    cursor: str | None = None
    "Continue fetching objects from this point onward"
