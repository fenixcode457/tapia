


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
        
        conexion.execute(f"insert into cliente(nombre,email) values('{persona.Nombre}','{persona.Email}')")
        conexion.commit()
        conexion.close()
        
        return {"Se agrego el bibliotecario"}
    
    except:

      print("No se creo de manera adecuado")
