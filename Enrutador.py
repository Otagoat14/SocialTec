def enrutador(mensaje):
    if mensaje == "login":
        return "Hola login"
    #Retorno el metodo encargado del login

    if mensaje == "grafo":
        return "Hola grafo"
    #Retorno el metodo para agregar en el grafo un nuevo usuario

    if mensaje == "verificar_amistad":
        return "Hola amistad"
    #Reorno el metodo que se encarga si exite el camino de un nodo a otro

    if mensaje == "estadisticas_usuario":
        return "Hola stats"
    #Retorno el metodo que se encarga de mostrar que usuario tiene más amigos

    
