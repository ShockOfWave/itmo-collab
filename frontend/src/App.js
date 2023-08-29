import {useState} from "react";
import UploadComponent from "./components/Upload";
import Button from "./components/Button";
import ComponentRTC from "./components/RTC";


function App() {
    const [isType, setType] = useState('upload')

  return (
      <div className="d-flex align-items-center justify-content-center">
      <div className="container mt-3">
          <div className="row">
          <div className="d-flex justify-content-center">
              <input type="radio" className="btn-check" name="btnradio" id="btnradio1" autoComplete="off"
                     checked={isType==='upload'} onClick={()=>setType('upload')}/>
              <label className="btn btn-outline-primary" htmlFor="btnradio1">Загрузить видео</label>

              <input type="radio" className="btn-check" name="btnradio" id="btnradio2" autoComplete="off"
                     checked={isType==='stream'} onClick={()=>setType('stream')}/>
              <label className="btn btn-outline-primary" htmlFor="btnradio2">Прямой эфир</label>
                  </div>
            </div>
          {(isType==='upload') ? (<UploadComponent />) : <ComponentRTC></ComponentRTC>}
      </div>
      </div>
  );
}

export default App;
