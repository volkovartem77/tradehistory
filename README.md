# Trade history bot for Binance. Deploy on server Ubuntu 16, 18

## INSTALL PYTHON & PIP

`sudo add-apt-repository ppa:jonathonf/python-3.6`  

> if it gives  ***add-apt-repository: command not found***   than use: `sudo apt-get install software-properties-common`

**Put each command separatly, one by one**
```
sudo apt update
sudo apt install python3.6
sudo apt install python3.6-dev
sudo apt install python3.6-venv
sudo apt install python3-distutils
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.6 get-pip.py
sudo ln -s /usr/bin/python3.6 /usr/local/bin/python3
sudo ln -s /usr/local/bin/pip /usr/local/bin/pip3
sudo ln -s /usr/bin/python3.6 /usr/local/bin/python
```



## Install project tradehistory

```
sudo apt-get install git-core
git clone https://github.com/volkovartem77/tradehistory.git
```
> You may do not need to run decommenter if you deploy it on local machine
```
cd ~/tradehistory; . decommenter.sh
```


## Creating virtualenv using Python 3.6

```
sudo pip install virtualenv
virtualenv -p /usr/bin/python3.6 ~/tradehistory/venv
```

# Before launching
## Prepare back-end
**Clone the project and install all dependencies**
```
cd ~/tradehistory; . venv/bin/activate
pip install -r requirements.txt
deactivate
```
**Install InfluxDB**
```
echo "deb https://repos.influxdata.com/ubuntu bionic stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
sudo apt-get update
sudo apt-get install -y influxdb
sudo systemctl enable --now influxdb
sudo systemctl is-enabled influxdb
```
**Create database**
(in terminal)
```
influx
> CREATE DATABASE storage
> SHOW DATABASES
```
**Make sure that you have `storage` in databases list and then**\
```> exit```


## Prepare front-end
**Install Node.js and NPM**
```
sudo apt update
sudo apt install nodejs
sudo apt install npm
```

**Install all dependencies in package.json**
```
cd ~/tradehistory/front
sudo pm install
sudo npm install simple-websocket
```
> No worries if you see follow warnings
```
npm WARN optional Skipping failed optional dependency /chokidar/fsevents:
npm WARN notsup Not compatible with your operating system or architecture: fsevents@1.2.9

```

## Install & config supervisor

```
sudo apt-get install supervisor
cd ~/tradehistory; cp app.conf /etc/supervisor/conf.d/app.conf
mkdir /var/log/tradehistory
supervisorctl reread
supervisorctl reload
```

# Run app
## Launch Python back-end
**Using supervisor (if you are in remote server, like VDS)**
```
sudo supervisorctl start wsBinanceDOM
sudo supervisorctl start wsServer
```
Check the state by following command
```
sudo supervisorctl status
```
If both wsBinanceDOM and wsServer has RUNNING status so everything is right.


**Without supervisor (if you are in local machine or IDE)**
1. launch wsBinanceDOM.py. 
The output is going to be like this:
```
start websocket Binance
['MATIC_BTC', 'MATIC_USDT', 'TNT_BTC', 'TNT_USDT']
maticbtc@trade/maticusdt@trade/tntbtc@trade/tntusdt@trade/
### opened ###
MATICBTC {'e': 'trade', 'E': 1559283040963, 's': 'MATICBTC' ...
```
2. launch wsServer.py
It is internal websocket server. There is no output for now.
3. launch front-end\
```npm run dev```\
You'll see a GUI with charts and default data\
Select pair to start getting data

## Launch front-end
**Set up external IP to have access remotly**
Find your computer's address on the network. In terminal, type `ifconfig` and look for the en1 section or the one with something like inet 192.168.1.111\
Paste this IP in package.json by this command (don't forget to change 192.168.1.111 to yours): `cd ~/tradehistory/front; sed -i "s%"0.0.0.0"%"192.168.1.111"%g" "package.json"`
```
sudo supervisorctl start front
sudo supervisorctl status
```
