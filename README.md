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
Due to confidential issues, the 
flask --app app run