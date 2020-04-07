**Activate the Virtual Environment**
Inside the primary-blockchain directory:
```
source primary-env/bin/activate
```
**Install Dependencies**
```
pip3 install -r requirements.txt
```
**Test**
```
python3 -m pytest backend/tests/
```
**Launch Application + API**
```
python3 -m backend.app
```
**Launch a Peer Instance**
```
export PEER=True && python3 -m backend.app
```
**Test User Interface [Option i]**
Set HOST and POST environment variables.
Install the Node Modules at the frontend directory.
Then, via the shell:
```
npm run start
```
Via a second shell, this time in the root directory:
```
python3 -m backend.app
```
Via a third shell, also from the root directory:
```
python3 -m backend.scripts.simulate_app
```
Run the simulation as many times as desired to mine new blocks.

**Test User Interface [Option ii]**
Run the backend as a pre-seeded instance with:
```
export SEED=True && python3 -m backend.app
```

Development demos:
- Tx Pool Demo: https://streamable.com/x9fdii