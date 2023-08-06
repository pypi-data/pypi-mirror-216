from datetime import datetime
from pydantic import BaseModel, validator
from .parameters import MAX_ID_LENGTH


class Message(BaseModel, frozen=True):
    """
    A Message encapsulates encrypted device packets with metadata.
    The IDUN SDK sends Messages with device data to the IDUN Cloud through the websocket API.
    """

    recordingID: str
    deviceID: str
    deviceTimestamp: datetime
    connectionID: str | None = None
    payload: str | None = None
    impedance: float | None = None

    # DEPRECATED: these fields will be replaced by explicit API calls
    stop: bool | None = None
    "Signal that the frontend sends to stop the recording"
    recorded: bool | None = None
    "Signal that the recorder sends to signal that batch processing is complete"
    enableStreamer: bool | None = None
    "Signal that the frontend can send to disable live streaming"

    @validator("recordingID", "deviceID", "connectionID")
    def limit_length(cls, v, field):
        if v and len(v) > MAX_ID_LENGTH:
            raise ValueError(f"{field} is too long. Max length: {MAX_ID_LENGTH}")
        return v
