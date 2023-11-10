# Scrapper

### 1. Acceder al proyecto
```sh
cd scrapper
```
### 2. Instalar dependencias
```sh
pip install -r requirements.txt
```

### 3. Arrancar el proyecto en servidor en Mac
```sh
uvicorn main:app --reload --host 0.0.0.0 --port=8081
```

## Ubuntu
### 2. Ver ip del servidor
```sh
ip addr show
```
### 3. Arrancar el proyecto en servidor
```sh
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port=8081
```
 
 # Deployment
### Eliminar, Crear y Levantarlo
```sh
sudo docker rm sanscontainer -f && sudo docker build -t sansdocker . && sudo docker run --restart=always -d --name sanscontainer -p 8083:8083 sansdocker
```
