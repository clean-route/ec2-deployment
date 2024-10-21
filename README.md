# CleanRoute: Web Tool for LEAP & LCO2 routes
This is a web tool for finding out least air pollution and least carbon dioxide emission path. It also features forecasting capability. 

>> Please use Linux Terminal/GITBASH for as Terminal for typing your commands. 

### IMPORTANT
Before you begin with frontend setup: Make sure you've completed the backend setup and the server is up and running.

Recommended steps for bootstrapping the servers: 
1. Setup and run the ML server
2. Setup and run Go backend server
3. Setup and run frontend client


### Prerequisites
1. Make sure you have Python3 installed in your system. You can confirm by running 
```which python3``` 
and hope it's not saying `python3 not found`. Otherwise, you'll have to install it. You can follow this [article](https://phoenixnap.com/kb/how-to-install-python-3-windows) for this.

- Verify Python is setup in your $PATH by running running `python --version`

2. Install dependencies
```
pip install -r requirements.txt
```
3. Add downloaded models to `/models` directory: 120min and 300min would be fine.

4. Run the server
```
uvicorn main:app --host 0.0.0.0 --port 8000              
```
