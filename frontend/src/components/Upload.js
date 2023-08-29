import VideoPlayerComponent from "./VideoPlayer";
import {useState} from "react";



function UploadComponent(props) {
    const [streamURI, setStreamURI] = useState('')
    const [downloadURL, setDownloadURL] = useState('')

    const [selectedFile, selectFile] = useState(null)
    const [loading, setLoading] = useState(false)

    const hostUrl = 'http://127.0.0.1:5556/video/molecules'

    const sendVideo = async () => {
        if (selectedFile!=null) {
            setStreamURI('')
            setLoading(true);
            const formData = new FormData();
            formData.append('file', selectedFile)

            const res= await fetch(hostUrl, {
                method: 'POST',
                body: formData}
            );
            const data = await res.json();
            console.log(data['stream_url'])
            setStreamURI(data['stream_url'])
            setDownloadURL(data['download_url'])

            console.log(streamURI);
            setLoading(false);

        }
    }

    const setFile = (e) => {
       selectFile(e.target.files[0])
    }

     return (<>
        <div>
         <div className="mt-3"><div className="input-group">
            <input type="file" className="form-control" id="inputGroupFile04" aria-describedby="inputGroupFileAddon04"
                   aria-label="Upload" accept="video/*,.avi" onChange={setFile} />
            <button className="btn btn-outline-secondary" type="button" id="inputGroupFileAddon04"
            onClick={sendVideo}>Загрузить</button>
         </div>
         </div>
            <div className="d-flex justify-content-center">
                <div className="mt-5">
                    {loading ? (<div className="spinner-grow text-light" role="status"></div>) :
                        !(streamURI==='') ? (<div><VideoPlayerComponent src={streamURI} type='video/x-mpegURL'/>
                            <div className="d-flex justify-content-center">
                                            <div className="mt-3">
                            <a href={downloadURL} className="btn btn-success btn-lg active" role="button" aria-pressed="true">Скачать mp4</a>
                                            </div>
                            </div>
                        </div>):<div></div>
                    }
                </div>
            </div>
        </div></>
     )
}


export default UploadComponent;