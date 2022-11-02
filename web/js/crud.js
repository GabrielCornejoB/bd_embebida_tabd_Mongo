function update_table () {
    console.log("update_table() called");
    eel.select(table_name)(load_table);
}

window.onload = function () { 
    if (table_name === "index") {
        eel.select("v_pescas_detalle")(load_table);
    }
    else {
        eel.select(table_name)(load_table);
        if (table_name === "pescas") {
            eel.select("metodos")(load_select_met);
            eel.select("cuencas")(load_select_cue);
        }
    }  
}

function load_select_met (output) {
    parsed_output = JSON.parse(output);
    if (typeof parsed_output === 'string' && parsed_output.startsWith("[ERR]")) {
        write_error(parsed_output);
        return
    }
    const zeroPad = (num, places) => String(num).padStart(places, '0');
    select_string = "<option disabled selected value style'color:#cfcfcf59'>---</option>";
    parsed_output.forEach(row => select_string = select_string.concat("<option value='", row[0], "'>", zeroPad(row[0],2), " - ", row[1], "</option>"));
    document.getElementById("create_arg_2").innerHTML = select_string;
    document.getElementById("update_arg_2").innerHTML = select_string;
}
function load_select_cue (output) {
    parsed_output = JSON.parse(output);
    if (typeof parsed_output === 'string' && parsed_output.startsWith("[ERR]")) {
        write_error(parsed_output);
        return
    }
    const zeroPad = (num, places) => String(num).padStart(places, '0');
    select_string = "<option disabled selected value style'color:#cfcfcf59'>---</option>";
    parsed_output.forEach(row => select_string = select_string.concat("<option value='", row[0], "'>", zeroPad(row[0],2), " - ", row[1], "</option>"));
    document.getElementById("create_arg_1").innerHTML = select_string;
    document.getElementById("update_arg_1").innerHTML = select_string;
}

// READ
function load_table (output) {
    console.log("READ");
    parsed_output = JSON.parse(output);

    if (typeof parsed_output === 'string' && parsed_output.startsWith("[ERR]")) {
        write_error(parsed_output);
        return
    }

    table_string = "";
    select_string = "<option disabled selected value style='color:#cfcfcf59'>---</option>";
    const zeroPad = (num, places) => String(num).padStart(places, '0');
    if (table_name === "cuencas" || table_name === "metodos") {
        if (table_name === "cuencas") {
            table_string = "<thead><tr><th>Id Cuenca</th><th>Cuenca Hidrográfica</th></tr></thead><tbody>";
        }
        else if (table_name === "metodos") {
            table_string = "<thead><tr><th>Id método</th><th>Método de pesca</th></tr></thead><tbody>";
        }
        parsed_output.forEach(row => table_string = table_string.concat("<tr><td>", row[0] , "</td><td>", row[1], "</td></tr>"));
        parsed_output.forEach(row => select_string  = select_string.concat("<option value='", row[0], "'>", zeroPad(row[0],2), " - ", row[1], "</option>"));
    }
    else if (table_name === "pescas") {
        table_string = "<thead><tr><th>Id pesca</th><th>Id cuenca</th><th>Id método</th><th>Fecha</th><th>Peso total</th></tr></thead><tbody>";
        parsed_output.forEach(row => table_string = table_string.concat("<tr><td>", row[0], "</td><td>", row[1], "</td><td>", row[2], "</td><td>", row[3], "</td><td>", row[4], "</td></tr>"));
        parsed_output.forEach(row => select_string = select_string.concat("<option value='", row[0], "'>", zeroPad(row[0],2), " - (", row[1], ", ", row[2], ", ", row[3], ", ", row[4], ")</option>"));
    }
    else if (table_name === "index") {
        table_string = "<thead><tr><th>Id Pesca</th><th>Cuenca</th><th>Método</th><th>Fecha</th><th>Peso total</th></tr></thead><tbody>";
        parsed_output.forEach(row => table_string = table_string.concat("<tr><td>", row[0], "</td><td>", row[1], "</td><td>", row[2], "</td><td>", row[3], "</td><td>", row[4], "</td></tr>"));
        count = parsed_output.length;
        document.getElementById("count_pescas").innerHTML = count;
    }
    table_string = table_string.concat("</tbody>");
    document.getElementById("data").innerHTML = table_string;
    if (table_name !== "index") {
        document.getElementById("update_select").innerHTML = select_string;
        document.getElementById("delete_select").innerHTML = select_string;
    }  
}

//CREATE
if (table_name !== "index") {
    document.querySelector(".crud_create").onclick = function() {
        l_args = []
        create_arg_1 = document.getElementById("create_arg_1").value;
        l_args.push(create_arg_1);
    
        if (table_name === "pescas") {
            create_arg_2 = document.getElementById("create_arg_2").value;
            create_arg_3 = document.getElementById("create_arg_3").value;
            create_arg_4 = document.getElementById("create_arg_4").value;
            l_args.push(create_arg_2);
            l_args.push(create_arg_3);
            l_args.push(create_arg_4);
        }
        eel.create(table_name, l_args)(add_register);    
    }
}
function add_register(output) {
    console.log("CREATE");
    clean_fields();
    parsed_output = JSON.parse(output);
    if (parsed_output.startsWith("[ERR]")) {
        write_error(parsed_output);
        return
    }
    else if (parsed_output.startsWith("[MSG]")) {
        write_msg(parsed_output);
        update_table();
    }
}

// UPDATE
if (table_name !== "index") {
    document.querySelector(".crud_update").onclick = function() {
        l_args = [];
        update_arg_1 = document.getElementById("update_arg_1").value;
        l_args.push(update_arg_1);
        if (table_name === "cuencas" || table_name === "metodos") {
            update_arg_2 = document.getElementById("update_select").value;
            l_args.push(update_arg_2);
        }
        else if (table_name === "pescas") {
            update_arg_2 = document.getElementById("update_arg_2").value;
            update_arg_3 = document.getElementById("update_arg_3").value;
            update_arg_4 = document.getElementById("update_arg_4").value;
            update_arg_5 = document.getElementById("update_select").value;
            l_args.push(update_arg_2);
            l_args.push(update_arg_3);
            l_args.push(update_arg_4);
            l_args.push(update_arg_5);
        }
        eel.update(table_name, l_args)(update_register);
    }
}
function update_register(output) {
    console.log("UPDATE");
    clean_fields();
    parsed_output = JSON.parse(output);
    if (parsed_output.startsWith("[ERR]")) {
        write_error(parsed_output);
        return
    }
    else if (parsed_output.startsWith("[MSG]")) {
        write_msg(parsed_output);
        update_table();
    }
}

// DELETE
if (table_name !== "index") {
    document.querySelector(".crud_delete").onclick = function() {
        delete_arg_1 = document.getElementById("delete_select").value;
        eel.delete(table_name, delete_arg_1)(delete_register);
    }
}
function delete_register(output) {
    console.log("DELETE");
    clean_fields();
    parsed_output = JSON.parse(output);
    if (parsed_output.startsWith("[ERR]")) {
        write_error(parsed_output);
        return
    }
    else if (parsed_output.startsWith("[MSG]")) {
        write_msg(parsed_output);
        update_table();
    }
}


// OTHER
if (table_name === "index") {
    document.querySelector(".logs").onclick = function() {
        eel.get_logs()(show_logs);
    }
}
function show_logs(output) {
    parsed_output = JSON.parse(output);
    document.getElementById("logs_div").innerHTML = parsed_output;
    toggle_popup("popup_logs")
}