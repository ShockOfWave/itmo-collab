import Button from "./Button";
import {useState} from "react";
import {backend} from "../constants";

function ComponentRTC(props) {

    const [is_translation, setTranslation] = useState(false)
    const [is_connecting, setConnection] = useState(false)

    const hostUrl = backend + '/rtc/offer'

    function createPeerConnection() {
        var config = {
            sdpSemantics: 'unified-plan'
        };
        config.iceServers = [{urls: ['stun:stun.l.google.com:19302']}];

        pc = new RTCPeerConnection(config);

        // connect audio / video
        pc.addEventListener('track', function(evt) {
            if (evt.track.kind == 'video')
                document.getElementById('video').srcObject = evt.streams[0];
                setConnection(false)
        });

        return pc;
    }

    var pc = createPeerConnection()

    function negotiate() {
        return pc.createOffer().then(function(offer) {
            return pc.setLocalDescription(offer);
        }).then(function() {
            // wait for ICE gathering to complete
            return new Promise(function(resolve) {
                if (pc.iceGatheringState === 'complete') {
                    resolve();
                } else {
                    function checkState() {
                        if (pc.iceGatheringState === 'complete') {
                            pc.removeEventListener('icegatheringstatechange', checkState);
                            resolve();
                        }
                    }
                    pc.addEventListener('icegatheringstatechange', checkState);
                }
            });
        }).then(function() {
            var offer = pc.localDescription;
            // offer.sdp = sdpFilterCodec('video', 'default', offer.sdp);
            return fetch(hostUrl, {
                body: JSON.stringify({
                    sdp: offer.sdp,
                    type: offer.type,
                    cv: true
                }),
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'POST'
            });
        }).then(function(response) {
            return response.json();
        }).then(function(answer) {
            return pc.setRemoteDescription(answer);
        }).catch(function(e) {
            alert(e);
        });
    }

    const start = () => {

        setTranslation(true)
        setConnection(true)

        var constraints = {
            video: false
        };
        constraints.video = {
                    width: 720,
                    height: 1280
                };
        if (constraints.video) {
            if (constraints.video) {
                document.getElementById('media').style.display = 'block';
            }
            navigator.mediaDevices.getDisplayMedia(constraints).then(function(stream) {
                stream.getTracks().forEach(function(track) {
                    pc.addTrack(track, stream);
                });
                return negotiate();
            }, function(err) {
                alert('Could not acquire media: ' + err);
            });
            } else {
                negotiate();
            }
    }
    const stop = () => {
        setTranslation(false)
        setConnection(false)

        // close transceivers
        if (pc.getTransceivers) {
            pc.getTransceivers().forEach(function(transceiver) {
                if (transceiver.stop) {
                    transceiver.stop();
                }
            });
        }
        // close local audio / video
        pc.getSenders().forEach(function(sender) {
            sender.track.stop();
        });
        // close peer connection
        setTimeout(function() {
            pc.close();
        }, 500);
    }

    return (<div>
                <div className="d-flex justify-content-center">
                    <div className="mt-5">
                        {
                            !(is_translation) ? (
                            <Button service={start} text="Транслировать экран" className="btn btn-success">
                            </Button>) :
                                (<Button service={stop} text="Остановить" className="btn btn-danger">
                            </Button>)
                        }
                    </div>
                </div>
            <div className="d-flex justify-content-center">
                 <div className="mt-5">
                        {
                            (is_connecting) ? (
                               <div className="spinner-grow text-light" role="status"></div>
                            ) : <div></div>
                        }
                    </div>
            </div>
                <div className="d-flex justify-content-center">
                    <div className="mt-5">
                        <div id="media" >
                            {is_translation && <video id="video" autoPlay="true" playsInline="true" className="object-fit-contain border rounded"></video>}
                        </div></div>
                </div>
            </div>
        )
}

export default ComponentRTC