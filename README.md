# Fun-A-Holics
```
sudo apt-update 
sudo apt-upgrade 
sudo apt install python3-pip 
pip3 --version 
python3 -m pip install -r requirements
python run.py
```
👉 It runs the application on 5000 port which can be accessed using localhost:5000 if running on the local machine<br>


# To connect to SQL from Cloud shell 
```
gcloud sql connect mysqlp2 --user=root --quiet 
When it asks for password just enter as no password is required

add mysql-connector-python-rf==2.2.2 in requirements.txt for db connection
```
