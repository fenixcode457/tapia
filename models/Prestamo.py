from typing import Optional
from pydantic import BaseModel

class Prestamo(BaseModel):
    Fecha_devolucion: str
    Fk_numempleado: int
    FK_cliente: int
    FK_libro: int
    FK_status: int
  