function update_table () {
    console.log("update_table() called");
    eel.read(table_name)(load_table);
}

window.onload = function () { 
    if (table_name === "index") {
        eel.read("pescas")(load_table);
    }
    else {
        eel.read(table_name)(load_table);
        if (table_name === "pescas") {
            eel.read("metodos")(load_select_met);
            eel.read("cuencas")(load_select_cue);
        }
    }  
}

function load_select_met (output) {
    parsed_output = JSON.parse(output);
    if (typeof parsed_output === 'string' && parsed_output.startsWith("[ERR]")) {
        write_error(parsed_output);
        return
    }
    select_string = "<option disabled selected value style'color:#cfcfcf59'>---</option>";
    parsed_output.forEach(row => select_string = select_string.concat("<option value='", row['metodo'], "'>", row['metodo'], "</option>"));
    document.getElementById("create_arg_2").innerHTML = select_string;
    document.getElementById("update_arg_2").innerHTML = select_string;
}
function load_select_cue (output) {
    parsed_output = JSON.parse(output);
    if (typeof parsed_output === 'string' && parsed_output.startsWith("[ERR]")) {
        write_error(parsed_output);
        return
    }
    select_string = "<option disabled selected value style'color:#cfcfcf59'>---</option>";
    parsed_output.forEach(row => select_string = select_string.concat("<option value='", row['cuenca'], "'>", row['cuenca'], "</option>"));
    document.getElementById("create_arg_1").innerHTML = select_string;
    document.getElementById("update_arg_1").innerHTML = select_string;
}

// READ
function load_table (output) {
    console.log("READ");
    console.log(output)
    parsed_output = JSON.parse(output);

    if (typeof parsed_output === 'string' && parsed_output.startsWith("[ERR]")) {
        write_error(parsed_output);
        return
    }

    table_string = "";
    select_string = "<option disabled selected value style='color:#cfcfcf59'>---</option>";
    if (table_name === "cuencas" || table_name === "metodos") {
        if (table_name === "cuencas") {
            table_string = "<thead><tr><th>Cuenca Hidrográfica</th></tr></thead><tbody>";
            parsed_output.forEach(row => table_string = table_string.concat("<tr><td>", row['cuenca'], "</td></tr>"));
            parsed_output.forEach(row => select_string  = select_string.concat("<option value='", row['_id'], "'>", row['cuenca'], "</option>"));
        }
        else if (table_name === "metodos") {
            table_string = "<thead><tr><th>Método de pesca</th></tr></thead><tbody>";
            parsed_output.forEach(row => table_string = table_string.concat("<tr><td>", row['metodo'], "</td></tr>"));
            parsed_output.forEach(row => select_string  = select_string.concat("<option value='", row['_id'], "'>", row['metodo'], "</option>"));
        }
    }
    else if (table_name === "pescas") {
        table_string = "<thead><tr><th>Id cuenca</th><th>Id método</th><th>Fecha</th><th>Peso total</th></tr></thead><tbody>";
        parsed_output.forEach(row => table_string = table_string.concat("<tr><td>", row['cuenca'], "</td><td>", row['metodo'], "</td><td>", row['fecha'].slice(0,10), "</td><td>", row['peso_total_pesca'], "</td></tr>"));
        parsed_output.forEach(row => select_string = select_string.concat("<option value='", row['_id'], "'>(", row['cuenca'], ", ", row['metodo'], ", ", row['fecha'].slice(0,10), ", ", row['peso_total_pesca'], ")</option>"));
    }
    else if (table_name === "index") {
        table_string = "<thead><tr><th>Cuenca</th><th>Método</th><th>Fecha</th><th>Peso total</th></tr></thead><tbody>";
        parsed_output.forEach(row => table_string = table_string.concat("<tr><td>", row['cuenca'], "</td><td>", row['metodo'], "</td><td>", row['fecha'].slice(0,10), "</td><td>", row['peso_total_pesca'], "</td></tr>"));
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
    
        if (table_name === "pescas") {
            create_arg_2 = document.getElementById("create_arg_2").value;
            create_arg_3 = document.getElementById("create_arg_3").value;
            create_arg_4 = document.getElementById("create_arg_4").value;
            json_args = {
                "cuenca": create_arg_1,
                "metodo": create_arg_2,
                "fecha": create_arg_3,
                "peso_total_pesca": create_arg_4
            }
            eel.create(json_args, "pescas")(add_register)
        }
        else if (table_name === "cuencas") {
            json_args = {
                "cuenca": create_arg_1
            }
            eel.create(json_args, "cuencas")(add_register)
        }
        else if (table_name === "metodos") {
            json_args = {
                "metodo": create_arg_1
            }
            eel.create(json_args, "metodos")(add_register)
        }  
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
        update_arg_1 = document.getElementById("update_select").value;

        if (table_name === "cuencas") {
            update_arg_2 = document.getElementById("update_arg_1").value;
            json_args = {
                "cuenca": update_arg_2
            }
        }
        else if (table_name === "metodos") {
            update_arg_2 = document.getElementById("update_arg_1").value;
            json_args = {
                "metodo": update_arg_2
            }
        }
        else if (table_name === "pescas") {
            update_arg_2 = document.getElementById("update_arg_1").value;
            update_arg_3 = document.getElementById("update_arg_2").value;
            update_arg_4 = document.getElementById("update_arg_3").value;
            update_arg_5 = document.getElementById("update_arg_4").value;

            json_args = {
                "cuenca": update_arg_2,
                "metodo": update_arg_3,
                "fecha": update_arg_4,
                "peso_total_pesca": update_arg_5
            }
        }
        eel.update(update_arg_1, json_args, table_name)(update_register);
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
        eel.delete(delete_arg_1, table_name)(delete_register);
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