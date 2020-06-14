export {weapon_selection_changed}

// create dropdown with label
// label_str : string describing dropdown
// data_array : list of strings
function create_dropdown_div(label_str, data_array)
{
    var div = document.createElement("div");
    div.id = `${label_str}-div`
    div.className = "weapon_filter"

    // create label
    var label = document.createElement("label");
    label.innerHTML = label_str;
    div.append(label);

    // create dropdown
    var dropdown = document.createElement("select");
    div.append(dropdown)

    // add each option in data_array to the dropdown
    for (var index in data_array)
    {
        var option = document.createElement("option");
        option.innerHTML = data_array[index];
        option.value = index;
        dropdown.appendChild(option);
    }

    return div;

}

// get weapon information from database
// i.e what parameters describes weapons
// requires AJAX call
// weapon_type : string of weapon type (e.g "Sword and Shield", "Palico", etc)
function get_weapon_info(weapon_type)
{
    // create request
    var request = new XMLHttpRequest();
    
    var http_type = "GET";
    var http_url = `/headers/${weapon_type}`;

    console.log(http_url);
    request.open(http_type, http_url);
    request.send();

    // generate options after received 
    request.onreadystatechange = function()
    {
        if (request.readyState === 4)
        {
            var weapon_info = JSON.parse(request.responseText);
            init_filter(weapon_info["headers"], weapon_info["filterables"])
            console.log("headers : " + weapon_info["headers"])
            console.log(weapon_info["filterables"]);
        }
    }
}

// returns selected string on weapon dropdown menu
function get_selected_weapon_str()
{
    var weapon_dropdown = document.getElementById("weapon_dropdown")
    var selected_index = weapon_dropdown.selectedIndex
    var selected_weapon = weapon_dropdown.options[selected_index].text

    return selected_weapon
}

// called everytime weapon_dropdown menu is changed
// clears out previous weapon filter options and replaces with new options
function weapon_selection_changed()
{    
    var old_fieldset = document.getElementById("filter_fieldset")
    var new_fieldset = document.createElement("fieldset")
    new_fieldset.id = "filter_fieldset"
    old_fieldset.replaceWith(new_fieldset)

    get_weapon_info(get_selected_weapon_str())
}

// headers : list
// filterables : dict
function init_filter(headers, filterables)
{
    // create fieldset to contain all dropdowns
    var filter_fieldset = document.getElementById("filter_fieldset")

    // create dropdown for each sortable parameter in filterable
    for (var key in filterables)
    {
        var data = filterables[key];
        var div = create_dropdown_div(key, data);
        filter_fieldset.appendChild(div);
    }

    // create drop down for "order by"
    var order_by_div = create_dropdown_div("order by", headers);
    filter_fieldset.append(order_by_div);

    // create search button
    var search_button = document.getElementById("search_button");
    search_button.onclick = search_button_clicked
}

// calls everytime search button is clicked
// calls search_database on the selected weapon
function search_button_clicked()
{
    var weapon_str = get_selected_weapon_str()
    search_database(weapon_str)
}

// retreive selected options from filter_fieldset
// returns: dictionary containing optionname and corresponding value
function get_selected_options()
{
    var filters_fieldset = document.getElementById("filter_fieldset")
    var selected_options = {}
    
    // get selected option from each dropdown menu
    for (var i = 0; i < filters_fieldset.childElementCount; i++)
    {
        // get label
        var div = filters_fieldset.children[i]
        var label = div.children[0].innerHTML
        console.log(label)

        // get selected option
        var dropdown = div.children[1]
        var selected_index = dropdown.selectedIndex
        var selected_text = dropdown.options[selected_index].innerHTML
        console.log(`${selected_index} ${selected_text}`)

        // add option to dict
        selected_options[label] = selected_index
    }

    return selected_options
}

// creates URL for accessing database with selected options
// weapon_type: string of which weapon type is going to be retrieved from database
// options: dict created from get_selected_options
// returns: string containing URL
function create_filter_url(weapon_type, options)
{
    var url_string = `/weapon/${weapon_type}?`
    
    var selected_strings = []
    for (var option in options)
    {
        selected_strings.push(`${option}=${options[option]}`)
    }
    
    url_string += selected_strings.join('&')

    return url_string
}

// get selected options
function search_database(weapon_type)
{
    // get selected options
    var options = get_selected_options()

    // create get link with filters as parameters
    var filter_url = create_filter_url(weapon_type, options)

    // create request for information
    var x = new XMLHttpRequest()
    x.open("GET", filter_url)
    x.send()
    console.log(filter_url)
    
    // create table out of data
    x.onreadystatechange = function()
    {
        if (x.readyState === 4)
        {
            var response = JSON.parse(x.responseText)
            var results_table = document.getElementById("results_table")
            var new_table = create_table(response)
            new_table.id = "results_table"
            results_table.replaceWith(new_table)
        }
    }
}

function create_table(data)
{
  var table = document.createElement("table");

  // get headers from first row
  var headers = data[0]
  var header_row = table.insertRow(-1)
  for (var col = 0; col < headers.length; col++)
  {
      
      var header = document.createElement("th")
      header.innerHTML = headers[col];
      header_row.append(header)
  }

  // parse data
  for(var i = 1; i < data.length; i++)
  {
    var row = table.insertRow(-1);

    for (var j = 0; j < data[i].length; j++)
    {
        row.appendChild(parse_table_item(headers[j], data[i][j]))
    //   var col = row.insertCell(-1);
    //   col.innerHTML = data[i][j]
    }
  }

  return table;
}

function parse_table_item(item_type, item_index)
{
    var cell = document.createElement("td")

    switch (item_type)
    {
        case "damage type":
            switch (item_index)
            {
                case 0:
                    cell.innerHTML = 'cutting'
                    break;
                case 1: 
                    cell.innerHTML = 'blunt'
                    break;
                default:
                    break;
            }
            break

        case "balance type":
            switch (item_index)
            {
                case 0:
                    cell.innerHTML = 'balanced'
                    break
                case 1:
                    cell.innerHTML = 'melee'
                    break
                case 2:
                    cell.innerHTML = 'boomerang'
                    break
                default:
                    break
            }
            break
        
        // case "charges":
            

        default:
            cell.innerHTML = item_index
    }

/*     if (item_type === "damage type")
    {
        if (item_index === 0)
        {
            cell.innerHTML = 'cutting'
        }
        else if (item_index === 1)
        {
            cell.innerHTML = 'blunt'
        }
    }
    else if (item_type === "balance type")
    {
        if (item_index === 0)
        {
            cell.innerHTML = "balanced"
        }
        else if (item_index === 1)
        {
            cell.innerHTML = "melee"
        }
        else if (item_index === 2)
        {
            cell.innerHTML = "boomerang"
        }
    }
    else if (item_type === )
    else
    {
        cell.innerHTML = item_index
    } */

    return cell
}