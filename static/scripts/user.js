
function setActiveButton(button) {
    var buttons = document.getElementsByClassName('button');
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove('active');
    }
    button.classList.add('active');
    showInputField(button.innerHTML.toLowerCase());
}

function showInputField(divId) {
    var divs = document.querySelectorAll('.middle-side > div');
    divs.forEach(function(div) {
        div.style.display = 'none';
    });

    var targetDiv = document.getElementById(divId);
    targetDiv.style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function() {
    var button = document.getElementById('submitBtn');
    button.addEventListener('click', sendData);
});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


async function sendData() {
    var result = "";
    var response = "";
    var formData = collectFormData(); // save collected data to formData
    console.log(formData);
    var loader = document.getElementById('loader');
    loader.style.display = 'block';
    var submitBtn = document.getElementById('submitBtn');
    submitBtn.style.display = 'none';
    // await sleep(5000);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', `/process/${JSON.stringify(formData)}`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    // console.error('Request failed. Status: ');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            loader.style.display = 'none';

            if (xhr.status === 200) {
            // 處理伺服器回傳的資料
                // console.log(xhr.responseText);
                response = JSON.parse(xhr.responseText);
                console.log(response);
            // 處理回傳資料的其他操作

            } else {
            // 處理請求失敗的情況
                console.error('Request failed. Status: ' + xhr.status);
            }
        }
    }
    xhr.send();
    
    await sleep(5000);
    loader.style.display = 'none';
    submitBtn.style.display = 'block';
    // var response = JSON.parse(xhr.responseText);
    console.log(response['預測價格']);
    var result = parseResponse(result);
    
    
    // add marker to map
    initMap(result['map']);

    // disply result as a form
    initTable(result['table']);
    initOutput(result['table']);
}


function collectFormData() {
    // determine the building type
    var buttons = document.getElementsByClassName('button');
    var building_type;
    for (var i = 0; i < buttons.length; i++) {
        if(buttons[i].classList.contains('active')) {
            building_type = buttons[i].innerHTML.toLowerCase();
        }
    }

    // collect data from specific building type
    var divEmt = document.getElementById(building_type)
    var inputEmts = divEmt.getElementsByTagName('input');
    

    if(building_type == "building") {
        return {
            'type': "building",
            'addr': inputEmts[0].value,
            'age': inputEmts[1].value,
            'area': inputEmts[2].value
        }
    } else if(building_type == "apartment") {
        return {
            'type': "apartment",
            'addr': inputEmts[0].value,
            'age': inputEmts[1].value,
            'floor': inputEmts[2].value,
            'car': inputEmts[3].value
        }
    } else if(building_type == "house"){
        return {
            'type': "house",
            'addr': inputEmts[0].value,
            'age': inputEmts[1].value,
            'floor': inputEmts[2].value,
            'trans1': inputEmts[3].value,
            'trans2': inputEmts[4].value,
        }
    }
    
}

function parseResponse(response) {
    const properties = [
        {
          address: "台南市東區青年路454號",
          description: "Tainan House",
          price: "$ 305803.863048/pin",
          type: "home",
          bed: 4,
          bath: 3,
          size: 200,
          position: {
            lat: 22.990939981766,
            lng: 120.217639999566,
          },
        },
        {
          address: "台南市東區勝利路75號",
          description: "Tainan House",
          price: "$ 297682.725384/pin",
          type: "home",
          bed: 5,
          bath: 4,
          size: 700,
          position: {
            lat: 22.991049994245,
            lng: 120.217619966817,
          },
        },
        {
            address: "台南市東區青年路454號",
          description: "Tainan House",
          price: "$ 307335.567368",
          type: "home",
          bed: 4,
          bath: 3,
          size: 200,
          position: {
            lat: 22.990939981766,
            lng: 120.217639999566,
          },
        },
    ];

    const samples = [
        ['ID', 'x座標', 'y座標', '容積率', '屋齡', '土地移轉總面積(坪)', '建物移轉總面積(坪)', 'population_density', '主建物面積', 'YIMBY_1000', 'price/pin'],
        ['61292', '169784.988043', '2.543494e+06', '1.584118', '33.232033', '3.023834', '3.483861', '4049.0', '4.679535', '112.0', '305803.863048'],
        ['68233', '169776.988039', '2.543503e+06', '1.584118', '33.993155', '3.023834', '3.483861', '4049.0', '4.679535', '112.0', '297682.725384'],
        ['68232', '169776.988039', '2.543503e+06', '1.584118', '33.993155', '3.023834', '3.483861', '6330.0', '4.679535', '112.0', '297682.725384'],
        ['61291', '169784.988043', '2.543494e+06', '1.584118', '33.232033', '3.023834', '3.483861', '6330.0', '4.679535', '112.0', '305803.863048'],
        ['61289', '169784.988043', '2.543494e+06', '1.584118', '33.232033', '3.023834', '3.483861', '8164.0', '4.679535', '112.0', '307335.567368'],
    ]

      var res = {
        'map': properties,
        'table': samples
      }

      return res;
}

function initTable(data) {
    var tbl = document.querySelector("#eval-table");
    var trs = tbl.getElementsByTagName('tr');
    
    for(var i=0; i<6; i++) {
        var tr = trs[i];

        // clear all child emts
        while (tr.firstChild) {
            tr.removeChild(tr.lastChild);
        }

        for(var j=0; j<11; j++) {
            if(i == 0) {
                var emt = document.createElement('th');
            } else {
                var emt = document.createElement('td');
            }
            emt.innerHTML = data[i][j];
            tr.appendChild(emt);
        }
    }

    // var desc = document.querySelector('div.eval-desc');
    // desc.innerHTML = 'Based on 5 neighboring samples, predicted price is $302861.748846/pin.';
}

function initOutput(data){
    var tbl = document.querySelector("#table-desc");
    var trs = tbl.getElementsByTagName('tr');
    
    for(var i=0; i<2; i++) {
        var tr = trs[i];

        // clear all child emts
        while (tr.firstChild) {
            tr.removeChild(tr.lastChild);
        }

        for(var j=0; j<11; j++) {
            if(i == 0) {
                var emt = document.createElement('th');
            } else {
                var emt = document.createElement('td');
            }
            emt.innerHTML = data[i][j];
            tr.appendChild(emt);
        }
    }
}