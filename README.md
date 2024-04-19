# itrice-backend

## **Setup Backend**

#### 1. Set directory

```
cd backend
```

#### 2. Setup virtual environment

```
python -m venv venv
venv/Scripts/activate
```

#### 3. Install dependencies

```
pip install -r requirements.txt
```

#### 4. Run

```
flask run   
```

## API Documentation

Go to http://127.0.0.1:5000/swagger/ for documentation

## Default User Credentials
To change default user credentials, go to `app/configs/default.py` and update the values then restart the app to apply changes.

```
email: admin@email.com
password: admin
```
