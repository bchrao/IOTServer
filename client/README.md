# Installation:
1. copy files in client folder to device
2. Install Python packages:

```shell
run sudo pip install -r requirements.txt
```

3. Edit the script [getdata.py](getdata.py) to add your server host name or IP
4. Install the Python script to run as a service:

```shell
sudo cp getdata.service /lib/systemd/system/getdata.service
sudo chmod 644 /lib/systemd/system/getdata.service 
sudo systemctl daemon-reload 
sudo systemctl enable getdata.service 
sudo reboot
```

5. Check the service to verify functionality

```shell
sudo systemctl status getdata.service
```
