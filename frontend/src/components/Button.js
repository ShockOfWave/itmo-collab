function Button(props) {
    return <div>
    <button className={props.className} onClick={props.service}>{props.text}</button>
    </div>
}

export default Button;
