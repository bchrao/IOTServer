# IOTServer
A basic IOT environment to capture temperature consisting of:
1. DB - InfluxDB for storing data
2. MQTT - Mosquitto MQTT for recieving data from iot devices
3. Telegraf - for taking data from mqtt and storing to influx
4. Grafana - for creating a dashboard to view devices
5. Client - Raspberry Pi with Waveshare BME280 sensor
