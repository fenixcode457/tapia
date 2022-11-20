from typing import Optional
from pydantic import BaseModel

class Cliente(BaseModel):
    Nombre: str
    Direccion: str
    Telefono: Optional[str] = None
    Email: str
  
    
    