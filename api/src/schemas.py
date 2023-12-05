from pydantic import BaseModel


class Offer(BaseModel):
    sdp: str
    type: str
    cv: bool


class RTCOffer(BaseModel):
    sdp: str
    type: str
