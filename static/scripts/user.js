
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
    var groupData="";
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
                console.log(response)
                groupData = JSON.parse(response['groupData'])
            // 處理回傳資料的其他操作

            } else {
            // 處理請求失敗的情況
                console.error('Request failed. Status: ' + xhr.status);
            }
        }
    }
    xhr.send();
    
    await sleep(8000);
    loader.style.display = 'none';
    submitBtn.style.display = 'block';
    
    var result = parseResponse(groupData,response);
    
    
    // add marker to map
    initMap(result['map'],result['lat'], result['lon'],17,true);

    // disply result as a form
    initTable(result['table'],result['color']);
    initOutput(result['input'], result['thColor']);
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
            'far': inputEmts[2].value,
            'trans1': inputEmts[3].value,
            'trans2': inputEmts[4].value,
        }
    }
    
}
roundTo = function( num, decimal ) { return Math.round( ( num + Number.EPSILON ) * Math.pow( 10, decimal ) ) / Math.pow( 10, decimal ); }

function parseResponse(groupData, response) {
    var properties = [
        {
          address: "台南市東區青年路454號",
          description: "Tainan House",
          price: "$ 305803.863048/pin",
          type: "building",
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
          type: "building",
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
          type: "building",
          bed: 4,
          bath: 3,
          size: 200,
          position: {
            lat: 22.990939981766,
            lng: 120.217639999566,
          },
        },
        {
            address: "台南市東區青年路454號",
          description: "Tainan House",
          price: "$ 307335.567368",
          type: "building",
          bed: 4,
          bath: 3,
          size: 200,
          position: {
            lat: 22.990939981766,
            lng: 120.217639999566,
          },
        },
        {
            address: "台南市東區青年路454號",
          description: "Tainan House",
          price: "$ 307335.567368",
          type: "building",
          bed: 4,
          bath: 3,
          size: 200,
          position: {
            lat: 22.990939981766,
            lng: 120.217639999566,
          },
        },
    ];
    var mapRenderFeatures = ['addr','lat','lon','建物現況格局-房','建物現況格局-衛','主建物面積','price_pin']
    
    var thColor = 0;
    var renderFeatures = [];
    var houseRenderFeatures = ['addr', 'far', 'house_age', '土地移轉總面積(坪)', '建物移轉總面積(坪)', 'total_floor', '車位移轉總面積(坪)','population_density', '主建物面積', 'n_c_1000', 'price_pin']
    var apartmentRenderFeatures = ['addr', 'house_age','total_floor', '車位移轉總面積(坪)','far', '土地移轉總面積(坪)', '建物移轉總面積(坪)', 'population_density', '主建物面積', 'n_c_1000', 'price_pin']
    var buildingRenderFeatures = ['addr', 'house_age','主建物面積','far', '土地移轉總面積(坪)', '建物移轉總面積(坪)', 'population_density','total_floor', '車位移轉總面積(坪)', 'n_c_1000', 'price_pin']
    
    if(response['output']['type']=='apartment'){
        renderFeatures = apartmentRenderFeatures;
        thColor = 4;
    }else if(response['output']['type']=='house'){
        renderFeatures = houseRenderFeatures;
        thColor = 5;
    }else{
        renderFeatures = buildingRenderFeatures;
        thColor = 3;
    }

    var mapGroupData = [
        ['addr','lat','lon','建物現況格局-房','建物現況格局-衛','主建物面積','price_pin'],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','',''],
        ['','','','','','','']
    ]
    var colors = [
        ['地址', '容積率', '屋齡', '土地移轉總面積(坪)', 'total_floor', '車位移轉總面積(坪)', '建物移轉總面積(坪)', 'population_density', '主建物面積', 'YIMBY_1000', 'price_pin'],
        ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],
        ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],
        ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],
        ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],
        ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],
    ];
    var outputGroupData = [
        ['地址', '容積率', '屋齡', '土地移轉總面積(坪)', 'total_floor', '車位移轉總面積(坪)', '建物移轉總面積(坪)', 'population_density', '主建物面積', 'YIMBY_1000', 'price_pin'],
        ['', '1.584118', '33.232033', '3.023834', '3.483861', '4049.0', '4.679535', '112.0', '305803.863048'],
        ['', '1.584118', '33.993155', '3.023834', '3.483861', '4049.0', '4.679535', '112.0', '297682.725384'],
        ['', '1.584118', '33.993155', '3.023834', '3.483861', '6330.0', '4.679535', '112.0', '297682.725384'],
        ['', '1.584118', '33.232033', '3.023834', '3.483861', '6330.0', '4.679535', '112.0', '305803.863048'],
        ['', '1.584118', '33.232033', '3.023834', '3.483861', '8164.0', '4.679535', '112.0', '307335.567368'],
    ];
    var outputInputData = [
        ['地址', '容積率', '屋齡', '土地移轉總面積(坪)', 'total_floor', '車位移轉總面積(坪)', '建物移轉總面積(坪)', 'population_density', '主建物面積', 'YIMBY_1000', 'price_pin'],
        ['', '1.584118', '33.232033', '3.023834', '3.483861', '4049.0', '4.679535', '112.0', '305803.863048'],
        ];
    for (var i = 0; i < renderFeatures.length; i++){
        outputInputData[0][i] = renderFeatures[i];
        var obj = response['output'][renderFeatures[i]];
        if(i!=0){
            obj = parseFloat(obj);
            obj = roundTo(obj, 2);
        }
        
        outputInputData[1][i] = obj;
        
    }
    for (var i = 0; i < renderFeatures.length; i++){
        var obj = groupData[renderFeatures[i]];
        outputGroupData[0][i] = renderFeatures[i];
        var j = 1;
        for (var key in obj){
          var value = obj[key];
          
          
          if(i!=0){
            value = parseFloat(value);
            value = roundTo(value, 2);
          };
          outputGroupData[j][i] = value;
          // Get the bin color
          if(response['output']['type']=='building'){
            if(renderFeatures[i]=='house_age'){
                if(value>=outputInputData[1][i]){
                    colors[j][i] = '#cc0033';
                } else{
                    colors[j][i] = '#007e78';
                } 
            }
            if(renderFeatures[i]=='主建物面積'){
                if(value>=outputInputData[1][i]){
                    colors[j][i] = '#cc0033';
                } else{
                    colors[j][i] = '#007e78';
                } 
            }
          }else if(response['output']['type']=='house'){
            if(renderFeatures[i]=='house_age'){
                if(value>=outputInputData[1][i]){
                    colors[j][i] = '#cc0033'
                } else{
                    colors[j][i] = '#007e78'
                } 
            }
            if(renderFeatures[i]=='far'){
                if(value>=outputInputData[1][i]){
                    colors[j][i] = '#cc0033'
                } else{
                    colors[j][i] = '#007e78'
                } 
            }
            if(renderFeatures[i]=='土地移轉總面積(坪)'){
                if(value>=outputInputData[1][i]){
                    colors[j][i] = '#cc0033'
                } else{
                    colors[j][i] = '#007e78'
                } 
            }
            if(renderFeatures[i]=='建物移轉總面積(坪)'){
                if(value>=outputInputData[1][i]){
                    colors[j][i] = '#cc0033'
                } else{
                    colors[j][i] = '#007e78'
                } 
            }
          }else{
            if(renderFeatures[i]=='house_age'){
                if(value>=outputInputData[1][i]){
                    colors[j][i] = '#cc0033'
                } else{
                    colors[j][i] = '#007e78'
                } 
            }
            if(renderFeatures[i]=='total_floor'){
                if(value>=outputInputData[1][i]){
                    colors[j][i] = '#cc0033'
                } else{
                    colors[j][i] = '#007e78'
                } 
            }
            if(renderFeatures[i]=='車位移轉總面積(坪)'){
                if(value>=outputInputData[1][i]){
                    colors[j][i] = '#cc0033'
                } else{
                    colors[j][i] = '#007e78'
                } 
            }
          }
          if(renderFeatures[i]=='price_pin'){
            if(value>=outputInputData[1][i]){
                colors[j][i] = '#cc0033'
            } else{
                colors[j][i] = '#007e78'
            } 
          }
          
          j++;
        }
    }
    // Render group five on map
   
    for (var i = 0; i < mapRenderFeatures.length; i++){
        var obj = groupData[mapRenderFeatures[i]];
        var j = 1;
        for (var key in obj){
          var value = obj[key];
          if(i!=0){
            value = parseFloat(value);
            
          };
          mapGroupData[j][i] = value;
          
          j++;
        }
    }
    var id = 1;
    //'建物現況格局-房','建物現況格局-廳','建物現況格局-衛',
    for (const property of properties){
        property.address = mapGroupData[id][0];
        property.position.lat = parseFloat(mapGroupData[id][1]);
        property.position.lng = parseFloat(mapGroupData[id][2]);
        var tmpPrice = '$ '
        property.type = 'house'
        property.description = mapGroupData[id][0];
        property.bed = parseFloat(mapGroupData[id][3]);
        property.bath = parseFloat(mapGroupData[id][4]);
        property.size = parseFloat(mapGroupData[id][5]);
        property.price = tmpPrice.concat(roundTo(parseFloat(mapGroupData[id][6]),2));
        // property.description = 
        id++;
    }
      
    

    var res = {
    'map': properties,
    'table': outputGroupData,
    'color': colors,
    'input':outputInputData,
    'thColor':thColor,
    'lat':response['output']['lat'],
    'lon':response['output']['lon']
    };

    return res;
}

function initTable(data, colors) {
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
                emt.style.backgroundColor = '#C0C0C0'
            } else {
                var emt = document.createElement('td');
            }
            emt.style.color = colors[i][j];
            emt.innerHTML = data[i][j];
            tr.appendChild(emt);
        }
    }

    // var desc = document.querySelector('div.eval-desc');
    // desc.innerHTML = 'Based on 5 neighboring samples, predicted price is $302861.748846/pin.';
}

function initOutput(data, thColor){
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
                emt.style.backgroundColor = '#C0C0C0';
                
            } else {
                var emt = document.createElement('td');
            }
            if(j>=thColor && j!=10 && i!=0){
                emt.style.color = '#C0C0C0';
            }
            // emt.style.backgroundColor = '#696969';
            emt.innerHTML = data[i][j];
            tr.appendChild(emt);
        }
    }
}