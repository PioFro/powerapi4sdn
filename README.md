# Description
This docker works as a connection layer between the SRE mechanism and the data gathered by the powerAPI sensor and formula. It enables the SRE to optimize its routing from the energy consumption point of view. If there is no data in the mongodb the SRE will try to estimate the energy usage based on previously gathered characteristics of the dependency between traffic load and energy consumption.

# Parameters:
1. ctrl_ip - the IP address of the controller with SRE installed.
2. mongo_db  - the IP address of the mongodb instance that is being fed data from the powerAPI formula. Note that this image uses default port of mongodb only and the db/collection is also static = outpow/outpow1. 
3. update_window - the number of seconds after each update (get from db, process, send to the SRE) takes place. By default 100 [s]. Shouldn't be lower than 1[s].

# Example setup of the PowerAPI sensor+formula
Sensor:
```bash
docker run --privileged --net=host --name powerapi-sensor --privileged -td -v /sys:/sys -v /var/lib/docker/containers:/var/lib/docker/containers:ro -v /tmp/powerapi-sensor-reporting:/reporting powerapi/hwpc-sensor -n of:0000000000000003 -r "mongodb" -U "mongodb://localhost:27017" -D power -C power1 -s "rapl" -o -e RAPL_ENERGY_PKG
```
Formula:
```bash
docker run -td --net=host --name powerapi-formula powerapi/rapl-formula -s --input mongodb -u mongodb://localhost:27017 -d power -c power1 --output mongodb -u mongodb://localhost:27017 -d outpow -c outpow1
```
# Run command for the example setup:
```bash
docker run -e "ctrl_ip=localhost" -e "mongo_db=localhost" -e "update_window=10" pfrohlich/powerapi4sdn:latest
```