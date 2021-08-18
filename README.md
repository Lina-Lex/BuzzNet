# BUZZNET

IVR API

This API uses for specific functions during phone call between Client and IVR system  

This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, either version 3 of the License, or  
(at your option) any later version.  

This program is distributed in the hope that it will be useful,  
but WITHOUT ANY WARRANTY; without even the implied warranty of  
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the  
GNU General Public License for more details.  

You should have received a copy of the GNU General Public License  
along with this program.  If not, see <https://www.gnu.org/licenses/>.  
************************************************************************************

## Project outline
* The project is built in python flask source package **flaskapp**
* Documentation for Source [flaskapp](flaskapp/) can be found [here](flaskapp/README.md)
* Documentation for [taskscheduler](taskscheduler/) can be found [here](taskscheduler/README.md)
* [gspread_to_postgres](gspread_to_postgres/) is a utility that can be used to pull data stored in google spreadsheet and mapped to given postgress server.

## Installation
```
pip install -r requirements.txt

```
If fails to install ```psycopg2``` on linux try below steps  
**Python 3**
```
sudo apt install libpq-dev python3-dev
sudo apt-get install build-essential
pip install psycopg2
```