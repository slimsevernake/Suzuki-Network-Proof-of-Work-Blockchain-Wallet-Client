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

Development demos:
- Tx Pool Demo: https://streamable.com/x9fdii