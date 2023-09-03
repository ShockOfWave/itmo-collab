import ReactPlayer from "react-player";


function VideoPlayerComponent(props) {
    return (
        <ReactPlayer url={props.src} type={props.type} width="100%" height="100%" controls className="object-fit-contain border rounded"/>
    )
}

export default VideoPlayerComponent;
