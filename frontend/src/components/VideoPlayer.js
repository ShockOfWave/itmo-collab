import VideoPlayer from "react-video-js-player";

function VideoPlayerComponent(props) {
    return (
        <VideoPlayer src={props.src} type={props.type} width="auto" height="720" className="object-fit-contain border rounded"/>
    )
}

export default VideoPlayerComponent;
