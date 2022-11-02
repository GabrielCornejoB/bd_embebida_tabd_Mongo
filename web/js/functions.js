let file_name = location.pathname.substring(location.pathname.lastIndexOf("/") + 1);
let table_name = file_name.slice(0, -5);
console.log(table_name);

document.getElementById("nav").innerHTML = `
<div class="left_panel_top">
<a href="index.html" title="Inicio"><span class="material-symbols-outlined nav_icons home_icon">home</span></a>               
</div>
<div class="left_panel_middle">
<a href="pescas.html" title="Pescas"><span class="material-symbols-outlined nav_icons" id="pescas_nav">set_meal</span></a>
<a href="metodos.html" title="Métodos"><span class="material-symbols-outlined nav_icons" id="metodos_nav">phishing</span></a>
<a href="cuencas.html" title="Cuencas"><span class="material-symbols-outlined nav_icons" id="cuencas_nav">water</span></a>
<span title="Info" class="material-symbols-outlined nav_icons" onclick="toggle_popup('popup_info')">info</span>
<span title="Ayuda" class="material-symbols-outlined nav_icons" onclick="toggle_popup('popup_help')">help</span> 
</div>
<div class="left_panel_bottom">       
<span title="Ctrl + w" class="material-symbols-outlined nav_icons" onclick="toggle_popup('popup_exit')">logout</span>
</div>
`;

if (table_name === "pescas") {
    document.getElementById("pescas_nav").classList.toggle("selected");
}
else if (table_name === "metodos") {
    document.getElementById("metodos_nav").classList.toggle("selected");
}
else if (table_name === "cuencas") {
    document.getElementById("cuencas_nav").classList.toggle("selected");
}

function write_error (error_msg) {
    console.log("write_error() called");
    document.getElementById("popup_title").innerHTML = "ERROR 😡😾🤬";
    document.getElementById("popup_body").innerHTML = error_msg.substring(5);
    document.getElementById("popup_msg").classList.toggle('active');
    document.getElementById("overlay").classList.toggle('active');
}
function write_msg (msg) {
    console.log("write_msg() called");
    document.getElementById("popup_title").innerHTML = "YEEEI 😉😺🥳";
    document.getElementById("popup_body").innerHTML = msg.substring(5);
    document.getElementById("popup_msg").classList.toggle('active');
    document.getElementById("overlay").classList.toggle('active');
}
function clean_fields () {
    console.log("clean_fields() called");
    inputs = document.getElementsByClassName("crud_input");
    selects = document.getElementsByClassName("crud_select");
    for (let i of inputs) { i.value=""; }
    for (let i of selects) { i.value=""; }
}
function new_window (url) {
    window.open(url);
}

function toggle_popup(popup_id) {
    document.getElementById(popup_id).classList.toggle('active');
    document.getElementById("overlay").classList.toggle('active');
}