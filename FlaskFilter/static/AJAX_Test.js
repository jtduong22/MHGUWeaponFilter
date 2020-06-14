

function init_board()
{
  console.log("Hello");
  var myRequest = new XMLHttpRequest();

  // URL = "http://127.0.0.1:5000/Palico"
  URL = "weapons/Palico"
  HTTP_TYPE = "GET"

  // create connection
  myRequest.open(HTTP_TYPE, URL);

  // send information
  myRequest.send();

  // what to do with information once it arrives
  myRequest.onreadystatechange = function()
  {
    if (myRequest.readyState === 4)
    {
      console.log(JSON.parse(myRequest.responseText))
    }
  };
}

  function create_table(data)
  {
    table = document.createElement("table");
    for(var i = 0; i < data.length; i++)
    {
      row = table.insertRow(-1);

      for (var j = 0; j < data[i].length; j++)
      {
        col = row.insertCell(-1);
        col.innerHTML = data[i][j]
      }
    }

    return table;

}

