# Express
A house price prediction framework.

## Directory Structure
``` Bash
├── app.py
├── app_demo.py
├── convertCoord.py
├── demo
│   ├── building_demo.csv
│   ├── apartment_demo.csv
│   └── house_demo.csv
├── data
│   ├── all_apartment.csv
│   ├── all_building.csv
│   └── all_house.csv
├── apikey.txt
├── imputeMissingValues.py
├── inference.py
├── model
│   ├── 公寓all.pkl
│   ├── 大樓all.pkl
│   └── 透天厝all.pkl
├── README.md
├── requirements.txt
├── selectProperties.py
├── static
│   ├── scripts
│   │   ├── map.js
│   │   ├── script.js
│   │   └── user.js
│   └── styles
│       ├── map.css
│       └── style.css
├── templates
│   └── index.html
└── utils.py
```

## Installation
Recommand conda for setting up the environment, with other applications, the versions of the packages is shown in 'requirements.txt'.
```
conda create --name <env> --file requirements.txt
```

## Demonstration
Due to confidential issue, the complete dataset which is in the folder './data/' can't be provided. Alternatively, we provide a demo version, which can be ran by the command below.

```
flask --app app_demo run
```
For each property type, we randomly selected one property for demonstration, 
### Building
| Address |  House Age  | Main Building Area |
|:-----|:--------:|------:|
| 台中市南屯區文心路一段215號   | 33 | 4.3 |


### Apartment
```
Address: 新北市永和區國中路28號, House Age: 33, Total Floors: 5, Parking Area: 0
```
### House 
```
Address: 高雄市苓雅區林森二路7-7號, House Age: 40, Floor Area Ratio: 3.4, Land Transfer Area: 3.2, Building Transfer Area: 4.1
```
| Left |  Center  | Right |
|:-----|:--------:|------:|
| L0   | **bold** | $1600 |
| L1   |  `code`  |   $12 |
| L2   | _italic_ |    $1 |