function pollForUpdate(gid){
    setInterval(()=>{
        fetch(`/game/${gid}`)
            .then(res=>res.text())
            .then(html=>{
                document.body.innerHTML = html;
            });
    }, 2000);
}
