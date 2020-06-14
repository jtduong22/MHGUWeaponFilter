import * as g from './init_filter.js'

var title = document.createElement("p")
title.innerHTML = "MHGU Filter"
document.body.appendChild(title)

var weapon_dropdown = document.createElement("select")
weapon_dropdown.id = "weapon_dropdown"
document.body.appendChild(weapon_dropdown)

var request = new XMLHttpRequest()
request.open("GET",  "weapon/list")
request.send()
request.onreadystatechange = function()
{
    if (request.readyState === 4)
    {
        console.log("recieved weapons")
        var results = JSON.parse(request.responseText)

        for (var i in results)
        {
            var option = document.createElement("option")
            option.value = i
            option.innerHTML = results[i]
            weapon_dropdown.appendChild(option)
        }
        weapon_dropdown.onchange = g.weapon_selection_changed

        g.weapon_selection_changed()
    }
}

var filter_fieldset = document.createElement("fieldset")
filter_fieldset.id = "filter_fieldset"
document.body.appendChild(filter_fieldset)

var search_button = document.createElement("button")
search_button.innerHTML = "Search"
search_button.id = "search_button"
document.body.appendChild(search_button)

var table = document.createElement("table")
table.id = "results_table"
document.body.appendChild(table)

console.log("done with init_page")