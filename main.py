from typing import Optional
from fastapi import FastAPI , Body ,Query ,Path
from sqlalchemy.orm import scoped_session,sessionmaker

from Conexion import conexion
from datetime import datetime
#modelos 
from models.Bibliotecario import Bibliotecario
from models.Cliente import Cliente
from models.Libro import Libro
from models.Prestamo import Prestamo

app = FastAPI()
engine = conexion.get_connection()
session_factory = sessionmaker(bind=engine)
conexion = scoped_session(session_factory)


@app.get("/")
def home():
 
    diccionario=[]
    conexion.execute(f"insert into bibliotecario(NOMBRE,email) values('Julito','julitoloba@hotmail.com')")
    conexion.commit()
    conexion.close()
    
    
    myresult = conexion.fetchall()

    for x in myresult:
        diccionario[x]= myresult

    return {diccionario}

# -----------------------  Biliotecario --------------
@app.get("/ver/bibliotecario")
async def bibliotecario():
 
    diccionario=[]
    datos=conexion.execute(f"select * from bibliotecario").fetchall()
    
    for row in datos:
        diccionario.append({"Nombre":row[1],"Email":row[2]})
    
    return diccionario

@app.post("/insertar/bibliotecario")
def instert(persona: Bibliotecario = Body(...)):
    
    try:
        
        conexion.execute(f"insert into cliente(nombre_empleado,email) values('{persona.Nombre}','{persona.Email}')")
        conexion.commit()
        conexion.close()
        
        return {"Se agrego el bibliotecario"}
    
    except :

      print("No se creo de manera adecuado")

#------------------------------- CLiente -------------------------------- 
@app.post("/insertar/cliente")
def insert(cliente: Cliente = Body(...)):
    
    try:
        
        conexion.execute(f"insert into cliente(nombre_cliente,direccion,telefono,email) values('{cliente.Nombre}','{cliente.Direccion}','{cliente.Telefono}','{cliente.Email}')")
        conexion.commit()
        conexion.close()
        
        return {"Se agrego el cliente"}
    
    except:

        return {" No se agrego el cliente"}

@app.get("/historial/{email}")
async def reaf(email: str = Path(...)):
    
    diccionario=[]
    datos=conexion.execute(f"""select c.nombre_cliente,titulo , fecha_de_prestamo , c.email,d.fecha_devolucion,r.fecha_de_renovacion , p.id_prestamos  
    from libro l
    LEFT JOIN  prestamos p  on l.id_libro  =p.fk_libro  
    LEFT JOIN cliente c on c.id_cliente = p.fk_cliente
    LEFT JOIN devolucion d on p.id_prestamos  = d.fk_prestamo 
    LEFT JOIN renovacion r on p.id_prestamos  = r.fk_prestamo  where email='{email}'""").fetchall()
 
    print(email,datos)
    
    if (datos != None):
        for row in datos:
            diccionario.append({"Nombre":row[0],"Libro":row[1],"Fecha prestamo":row[2],"Fecha devolucion":row[4],"Fecha de renovacion":row[5]})
        
        conexion.close()
        return diccionario
    else:
            conexion.close()
            return {"Libro no encontrado"}
    
    
#--------------------- libro --------------------------------------------

@app.get("/ver/libro/{libro}")
async def read( libro: str = Path(...)):
    
   
    diccionario=[]
    datos=conexion.execute(f"select * from libro where titulo = '{libro}'").fetchall()
 
    print(libro,datos)
    
    if (datos != None):
        for row in datos:
            diccionario.append({"Autor":row[1],"Titulo":row[2],"Editorial":row[3]})
        
        conexion.close()
        return diccionario
    else:
            conexion.close()
            return {"Libro no encontrado"}
        
@app.get("/ver/libro/")
async def read():
    
   
    diccionario=[]
    datos=conexion.execute(f"select * from libro").fetchall()
    
    if (datos != None):
        
        for row in datos:
            diccionario.append({"Autor":row[1],"Titulo":row[2],"Editorial":row[3]})
        conexion.close()
        return diccionario
    else:
            conexion.close()
            return {"Libro no encontrado"}
  
 
 # ver libro por año y fecha  

@app.get("/ver/inventario/{mes}/{year}")
async def read(mes: str = Path(...) , le = 12,
               year: str = Path(...)):
    
     diccionario=[]
     treintayuno=['01','03','05','07','08','10','12']
     treinta=['04','06','09','11']
     
                    #  01 ,   03  ,  05    07   ,  08   ,  10          12
     #Tienen 31 días: Enero, marzo, mayo, julio, agosto, octubre y diciembre.
                    #   04    06      09            11
     # Tienen 30 días: Abril, junio, septiembre y noviembre.

      #Tienen 28 días: Febrero
      
     if(mes == '02'):
       dia=28
     
     for cont in range(0,len(treintayuno)):
         
         if(mes==treintayuno[cont]):
             dia = 31
             
     for cont in range(0,len(treinta)):
         
         if(mes==treinta[cont]):
             dia = 30
             
     print(dia)
    
     datos=conexion.execute(f"""
     select  l.titulo, p.fecha_de_prestamo 
     from prestamos p 
     INNER JOIN libro l ON l.id_libro = p.fk_libro where fecha_de_prestamo > '{year}-{mes}-01' and fecha_de_prestamo < '{year}-{mes}-{dia}'
     """).fetchall()
 
     print(mes,datos)
    
     if (datos != None):
        for row in datos:
            diccionario.append({"Libro":row[0],"Fecha de prestamo":row[1]})
        
        conexion.close()
        return diccionario
     else:
            conexion.close()
 
  
# mes y año actual 
@app.get("/ver/inventario/{mes}")
async def read(mes: str = Path(...) , le = 12):
     
     diccionario=[]
     treintayuno=['01','03','05','07','08','10','12']
     treinta=['04','06','09','11']
     
     year = datetime.now()
     actual=year.date() 
     year = actual.strftime("%Y")
     
     
                    #  01 ,   03  ,  05    07   ,  08   ,  10          12   esto indica el arreglo
     #Tienen 31 días: Enero, marzo, mayo, julio, agosto, octubre y diciembre.
                    #   04    06      09            11
     # Tienen 30 días: Abril, junio, septiembre y noviembre.

      #Tienen 28 días: Febrero
      
     if(mes == '02'):
       dia=28
     
     for cont in range(0,len(treintayuno)):
         
         if(mes==treintayuno[cont]):
             dia = 31
             
     for cont in range(0,len(treinta)):
         
         if(mes==treinta[cont]):
             dia = 30
             
     print(dia)
    
     datos=conexion.execute(f"""
     select  l.titulo, p.fecha_de_prestamo 
     from prestamos p 
     INNER JOIN libro l ON l.id_libro = p.fk_libro where fecha_de_prestamo > '{year}-{mes}-01' and fecha_de_prestamo < '{year}-{mes}-{dia}'
     """).fetchall()
 
     print(mes,datos)
    
     if (datos != None):
        for row in datos:
            diccionario.append({"Libro":row[0],"Fecha de prestamo":row[1]})
        
        conexion.close()
        return diccionario
     else:
            conexion.close()
 
 
   
   
  
    
@app.post("/insetar/libro")
def insert(libro : Libro = Body(...)):
    fecha = datetime.now()
    libro.Autor = libro.Autor.capitalize()
    libro.Titulo = libro.Titulo.capitalize()
    try:
        
        conexion.execute(f"insert into libro(autor,titulo,edicion,editorial,fk_catalogo,fecha_registro) values('{libro.Autor}','{libro.Titulo}','{libro.Edicion}','{libro.Editorial}','{libro.Fk_catalogo}','{fecha}')")
        conexion.commit()
        conexion.close()
        
        return {"Se agrego el libro"}
    
    except  Exception as e:
        
        
        return {" No se agrego el libro", e}
    
    
#---------------------- Prestamos ---------------------------

@app.post("/crear/prestamo")
def insert(prestamo : Prestamo = Body(...)):
    fechaHora = datetime.now()
    datetimeInstance = datetime.today()

    fecha = datetimeInstance.date()
    print(fechaHora)
    print(fecha)

    try:
        
        conexion.execute(f"insert into prestamos(fecha_de_prestamo,fecha_devolucion,fk_numempleado,fk_cliente,fk_libro,fk_estatus,fecha_registro) values('{fecha}','{prestamo.Fecha_devolucion}','{prestamo.Fk_numempleado}','{prestamo.FK_cliente}','{prestamo.FK_libro}','{prestamo.FK_status}','{fechaHora}')")
        conexion.commit()
        conexion.close()
        
        return {"Se agrego un prestamo"}
    
    except :
        
     
        return {" No se agrego el prestamo"}