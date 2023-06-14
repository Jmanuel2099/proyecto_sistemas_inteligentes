# proyecto_sistemas_inteligentes
Machine learning microservices 

# Project setup
- Create virtual environment 
```sh
py -m venv venv
```
- Activate virtual environment
```sh
.\venv\Scripts\activate
```

- Download python libraries used in the project
```sh
pip install -r requirements.txt
```

# Run project
.\venv\Scripts\activate
uvicorn gateway_api:app --reload
