from aiortc import RTCPeerConnection, RTCSessionDescription
from fastapi import APIRouter

from ..rtc import VideoStream, relay, recorder, pcs
from ..schemas import Offer, RTCOffer

router = APIRouter(prefix='/rtc')

@router.post('/offer')
async def offer(offer: Offer):
    pc = RTCPeerConnection()
    pcs.add(pc)


    rtc_offer = RTCSessionDescription(sdp=offer.sdp, type=offer.type)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    def on_track(track):
        pc.addTrack(
            VideoStream(
                relay.subscribe(track), offer.cv
            )
        )

        @track.on("ended")
        async def on_ended():
            await recorder.stop()

    await pc.setRemoteDescription(rtc_offer)
    await recorder.start()

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return RTCOffer(sdp=pc.localDescription.sdp,
                    type=pc.localDescription.type)