## running project or deployment 

## clone 
```
git clone <url>
```
## local via venv 
```
# create virtual env 
python3 -m venv imageapi

cd imageapi

# activate venv 
source bin/activate 

# install dependency 
pip install -r requirements.txt

# run directly using python3 
python3 run.py

# run from uwsgi 
gunicorn app:app 
```

## docker-compose
```
docker-compose up --build
```


## testing via curl 
```
curl -X POST -H "Content-Type: multipart/form-data" http://localhost:8000/predict -F "file=@test_img/cat_1.jpg"  > cat.json
```

