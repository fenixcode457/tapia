from typing import Optional
from pydantic import BaseModel

class Libro(BaseModel):
    Autor: str
    Titulo: str
    Edicion: str
    Editorial: str
    Fk_catalogo :str
 
    
    