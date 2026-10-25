let room='';
async function api(path,body){const r=await fetch('/api'+path,body===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});if(!r.ok)throw Error(String(r.status));return r.json();}
async function enter(join){try{const data=await api(join?'/rooms/'+document.getElementById('code').value+'/join':'/rooms',{displayName:document.getElementById('name').value,language:'ja'});room=data.roomCode;document.getElementById('status').textContent=room;}catch(e){document.getElementById('status').textContent=e.message;}}
document.getElementById('create').onclick=()=>enter(false);document.getElementById('join').onclick=()=>enter(true);
document.getElementById('send').onclick=async()=>{try{await api('/rooms/'+room+'/messages',{text:document.getElementById('draft').value});document.getElementById('draft').value='';}catch(e){document.getElementById('status').textContent=e.message;}};
setInterval(async()=>{if(!room)return;try{document.getElementById('messages').textContent=(await api('/rooms/'+room+'/state')).map(x=>x.text).join('\n');}catch(e){document.getElementById('status').textContent=e.message;}},2000);
