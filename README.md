# bicimad-history-analicer - Introduction
<p align='justify'>bicimad-history-analicer is a software that find to create lists of users of Bike shered system of Madrid(Bicimad) and London(Santander Cycles) and stations configuration files to run in the simulator Bike3S-Simulator.<br />
In other hand, This software is capable of creating a demand matrix from historical data(preconditioned)<br/>
Further, You can also create demand matrices from historical data.</p> 

## Usage
To run this app is necesary to run by python command line specifying th econfiguration that you like execute. In this project there are files with examples configuration to run the several options of the system. 
For example, to run the configuration thar return the configurations files of the simulation is:

`
data/stationsinfo/Madrid/stations.json data/routesInfo/Madrid "2018-07-20T00:00:00.000+0200" "2018-07-21T23:59:00.000+0200" results/demandMatrix.json
`

### User configuration

To create user configuration file of BiciMad, you must add the historical files provided in [https://opendata.emtmadrid.es/Datos-estaticos/Datos-generales-(1)](https://opendata.emtmadrid.es/Datos-estaticos/Datos-generales-(1)). These data require a preprocessed to adapt them to our application, something like this <br/>
`[
{ "_id" : { "oid" : "x" }, "user_day_code" : "x", "idplug_base" : 25, "user_type" : 1, "idunplug_base" : 15, "travel_time" : 154, "idunplug_station" : 39, "ageRange" : 0, "idplug_station" : 35, "unplug_hourTime" : { "date" : "2019-03-01T00:00:00.000+0100" }, "zip_code" : "" },
{ "_id" : { "oid" : "x" }, "user_day_code" : "x", "idplug_base" : 12, "user_type" : 1, "idunplug_base" : 4, "travel_time" : 211, "idunplug_station" : 164, "ageRange" : 5, "idplug_station" : 168, "unplug_hourTime" : { "date" : "2019-03-01T00:00:00.000+0100" }, "zip_code" : "28015" }
]
`<br/>
these files must be in the folder project: data/routesInfo/Madrid and another configuration file with the information of the system stations is necessary. This configuration file contains the id, capacity and position{latitude and longtude} of the stations of the Byke sharing system. <br/>

#### Madrid users configuration

In this type of users configuration, the app create a file with the users that fulfill the  date condition.

In this section, the format date is very important, because the historical data file contains this specific typy od date-time:
`
“<YYYY-MM-DDThh:mm:ss.000+TZD>”
`
To run this section in command line, You need to install Python, and when you have this, run this command:

`
python main.py data/stationsinfo/Madrid/stations.json data/routesInfo/Madrid "dateInit" "dateEnd"
`

On the menu, you select the option 1.

#### Second configuration option(user type 3 of historical data of Bicimad(Madrid); usertruck)

this option include in the fileUserConfiguration the special users. This special users are the redistribution employer of the real system that they move the bikes between stations of the city of Madrid.
On the menu, you select the option 6.

#### London users configuration

In this type of users configuration, the app create a file with the users that fulfill the  date condition.

In this section, the format date is very important, because the historical data file contains this specific typy od date-time:
`
“<DD/MM/YYYY hh:mm>”
`
To run this section in command line, You need to install Python, and when you have this, run this command:

`
python main.py data/stationsinfo/London/stations.json data/routesInfo/London "dateInit" "dateEnd"
`

On the menu, you select the option 2.

#### New York users configuration

In this type of users configuration, the app create a file with the users that fulfill the  date condition.

In this section, the format date is very important, because the historical data file contains this specific typy od date-time:
`
“<YYYY-MM-DD hh:mm:ss.mmmm>”
`
To run this section in command line, You need to install Python, and when you have this, run this command:

`
python main.py data/stationsinfo/NY/stations.json data/routesInfo/NY "dateInit" "dateEnd"
`

On the menu, you select the option 3.


### Stations Configuration
### Demand Matrix from historical data of BiciMad

