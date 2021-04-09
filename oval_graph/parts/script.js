function prepare_file_object(table_object) {
    var permission = {
        'uread': null,
        'uwrite': null,
        'uexec': null,
        'gread': null,
        'gwrite': null,
        'gexec': null,
        'oread': null,
        'owrite': null,
        'oexec': null
    };
    var new_table_object = {};
    Object.keys(table_object).forEach(key => {
        if (key in permission) {
            permission[key] = table_object[key];
        } else {
            new_table_object[key] = table_object[key];
        }
    });
    for (const key in permission) {
        if (permission[key] === null) {
            return table_object;
        }
    }
    var out = '<code>';
    Object.keys(permission).forEach(key => {
        if (permission[key] == 'true') {
            switch (key.substring(1, key.length)) {
                case 'read':
                    out += "r";
                    break;
                case 'write':
                    out += "w";
                    break;
                case 'exec':
                    out += "x";
                    break;
                default:
                    // pass
                    break;
            }
        } else {
            out += "-";
        }
    });
    out += '</code>';
    new_table_object['permission'] = out;
    return new_table_object;
}

function remove_uuid(str) {
    var index_special_char = str.indexOf('@');
    var text = str.substring(0, index_special_char != -1 ? index_special_char : str.length);
    return text;
}
function format_header(str) {
    var text = remove_uuid(str);
    var text_with_spaces = text.replace("_", " ");
    return text_with_spaces.charAt(0).toUpperCase() + text_with_spaces.slice(1);
}

function create_table(table_object) {
    var created_header = true;
    var html_table = '<div class="table-responsive scrollable"><table class="table table-bordered">';
    Object.keys(table_object).forEach(type => {
        if (typeof table_object[type] === 'object') {
            var fn = this["prepare_" + remove_uuid(type)];
            if (typeof fn === 'function') {
                table_object[type] = fn(table_object[type]);
            }
            if (!(remove_uuid(type) in table_object) || created_header) {
                html_table += '<tr class="active">';
                Object.keys(table_object[type]).forEach(col => {
                    html_table += '<th scope="col">' + format_header(col) + '</th>';
                });
                html_table += '</tr>';
                created_header = false;
            }
            html_table += '<tr>';
            Object.values(table_object[type]).forEach(row => {
                html_table += '<td>' + row + '</td>';
            });
            html_table += '</tr>';

        }
    });
    html_table += '</table></div>';
    $("#content").append(html_table);
}

function show_object(obj) {
    if (Object.values(obj).includes("complete")) {
        $("#content").append("<p>Following items have been found on the system:</p>");
    } else {
        $("#content").append("<p>No items have been found conforming to the following objects:<br>" +
            "Object <b>" + Object.keys(obj)[0] +
            "</b> of type <b>" + Object.keys(obj)[1] + "</b></p>");
    }
}

function open_modal(data) {
    $("#content").empty();
    $("#modal").show();
    $("#content").append(
        "<span class=\"label label-default\">OVAL test result details</span><br>" +
        "<span class=\"label label-info\">" + data.comment + "</span>  " +
        "<span class=\"label label-default\">" + data.id + "</span>" +
        data.result
    );
    data.objects.forEach(object => {
        show_object(object);
        create_table(object);
    });
}

function show_graph(id, data) {
    $(id)
        .on('activate_node.jstree', function (e, data) {
            if (data.node.original.info) {
                open_modal(data.node.original.info);
            }
        })
        .jstree({
            'core': {
                'data': [data]
            }
        });
}

$('#modal').click(function (e) {
    if (!$(e.target).closest('.modal-content').length) {
        $("#modal").hide();
    }
});

$("#close").click(function () {
    $("#modal").hide();
});

var data = JSON.parse(JSON.stringify(data_of_tree));

jQuery.each(data, function (rule, data) {
    rule_id = "#" + rule.replace(/[\_\-\.]/g, "");
    show_graph(rule_id, data);
});

function search() {
    var input = document.getElementById("Search");
    var filter = input.value.toLowerCase();
    var nodes = document.getElementsByClassName('target');
    Array.from(document.getElementsByClassName('target')).forEach(function (node) {
        if (node.children.item(0).innerText.toLowerCase().includes(filter)) {
            node.style.display = "block";
        } else {
            node.style.display = "none";
        }
    });
}
