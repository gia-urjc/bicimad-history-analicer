# bicimad-history-analicer - Introduction
bicimad-history-analicer is a software that find to create lists of users of Bike shered system of Madrid(Bicimad) and London(Santander Cycles) and stations configuration files to run in the simulator Bike3S-Simulator. <br />
In other hand, This software is capable of creating a demand matrix from historical data(preconditioned) <br/>
Further, You can also create demand matrices from historical data.

## Usage
To run this app is necesary TODO

### User configuration

To create user configuration file of BiciMad, you must add the historical files provided in [https://opendata.emtmadrid.es/Datos-estaticos/Datos-generales-(1)](https://opendata.emtmadrid.es/Datos-estaticos/Datos-generales-(1)). These data require a preprocessed to adapt them to our application, something like this <br/>
`[
{ "_id" : { "oid" : "x" }, "user_day_code" : "x", "idplug_base" : 25, "user_type" : 1, "idunplug_base" : 15, "travel_time" : 154, "idunplug_station" : 39, "ageRange" : 0, "idplug_station" : 35, "unplug_hourTime" : { "date" : "2019-03-01T00:00:00.000+0100" }, "zip_code" : "" },
{ "_id" : { "oid" : "x" }, "user_day_code" : "x", "idplug_base" : 12, "user_type" : 1, "idunplug_base" : 4, "travel_time" : 211, "idunplug_station" : 164, "ageRange" : 5, "idplug_station" : 168, "unplug_hourTime" : { "date" : "2019-03-01T00:00:00.000+0100" }, "zip_code" : "28015" }
]
`<br/>
these files must be in the folder project: data/routesInfo/Madrid and another configuration file with the information of the system stations is necessary. This configuration file contains the id, capacity and position{latitude and longtude} of the stations of the Byke sharing system. <br/>
