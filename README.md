# Express
A house price prediction framework.

## Directory Structure
``` Bash
├── app.py
├── convertCoord.py
├── final_inference
│   ├── all_apartment.csv
│   ├── all_building.csv
│   └── all_house.csv
├── googleAPI.txt
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
Setup the environment.
    conda create --name <env> --file requirements.txt
flask --app app run