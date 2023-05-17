from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid

app = FastAPI()

# Lista para almacenar las publicaciones
posts = []

# Modelo de la publicación
class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    creado_en: datetime = datetime.now()
    publicado_en: Optional[datetime]
    publicado: bool = False

# Endpoint de la raíz
@app.get('/')
def leer_raiz():
    return {"bienvenido": "Bienvenido a mi API REST"}

# Obtener todas las publicaciones
@app.get('/posts')
def obtener_publicaciones():
    return posts

# Crear una nueva publicación
@app.post('/posts')
def guardar_publicacion(publicacion: Post):
    publicacion.id = str(uuid())  # Generar un ID único para la publicación
    posts.append(publicacion.dict())  # Convertir el objeto de la publicación a un diccionario y agregarlo a la lista
    return "Recibido"

# Obtener una publicación específica por su ID
@app.get('/posts/{id_publicacion}')
def obtener_publicacion(id_publicacion: str):
    for publicacion in posts:
        if publicacion["id"] == id_publicacion:
            return publicacion
    raise HTTPException(status_code=404, detail="Elemento no encontrado")

# Eliminar una publicación por su ID
@app.delete('/posts/{id_publicacion}')
def eliminar_publicacion(id_publicacion: str):
    for indice, publicacion in enumerate(posts):
        if publicacion["id"] == id_publicacion:
            posts.pop(indice)
            return {"mensaje": "La publicación se ha eliminado satisfactoriamente"}
    raise HTTPException(status_code=404, detail="Elemento no encontrado")

# Actualizar una publicación por su ID
@app.put('/posts/{id_publicacion}')
def actualizar_publicacion(id_publicacion: str, publicacion_actualizada: Post):
    for indice, publicacion in enumerate(posts):
        if publicacion["id"] == id_publicacion:
            posts[indice]["title"] = publicacion_actualizada.dict()["title"]
            posts[indice]["content"] = publicacion_actualizada.dict()["content"]
            posts[indice]["author"] = publicacion_actualizada.dict()["author"]
            return {"mensaje": "La publicación se ha actualizado exitosamente"}
    raise HTTPException(status_code=404, detail="Elemento no encontrado")
