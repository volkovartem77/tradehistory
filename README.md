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


## Creating virtualenv using Python 3.6

```
sudo pip install virtualenv
virtualenv -p /usr/bin/python3.6 ~/tradehistory/venv
```

# Before launching
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

Go into the code and check websocket address. Line 68 where Socket is initializing\
```
sudo nano ~/tradehistory/wsServer.py
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


**Without supervisor (if you are in local machine or IDE)**\
- Launch wsBinanceDOM.py. \
The output is going to be like this:
```
start websocket Binance
['MATIC_BTC', 'MATIC_USDT', 'TNT_BTC', 'TNT_USDT']
maticbtc@trade/maticusdt@trade/tntbtc@trade/tntusdt@trade/
### opened ###
MATICBTC {'e': 'trade', 'E': 1559283040963, 's': 'MATICBTC' ...
```
- Launch wsServer.py\
It is internal websocket server. There is no output for now.