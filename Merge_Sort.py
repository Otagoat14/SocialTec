#ESTE CODIGO TENGO QUE MODIFICARLO PARA QUE SE PUEDA HACER CON LA LISTA DE AMIGOS
from Base_de_datos import BaseDeDatos


def merge_sort(lista):

    if len(lista) > 1 :

        lista_izq = lista[:len(lista)//2]
        lista_der = lista[len(lista)//2:]

        merge_sort(lista_izq)
        merge_sort(lista_der)

        i = 0 
        k = 0 
        j = 0

        while i < len(lista_izq) and j < len(lista_der):
            if lista_izq[i] < lista_der[j] :
                lista[k] = lista_izq[i]

                i += 1
                
            else:

                lista[k] = lista_der[j]
                j += 1

            k += 1
            

        while i < len(lista_izq):
            
            lista[k] = lista_izq[i]
            i += 1
            k += 1

        while j < len(lista_der):

            lista[k] = lista_der[j]
            j += 1
            k += 1

    return lista



def amigos_ordenados( username):
    db = BaseDeDatos()
    amigos = db.obtener_amigos_de_usuario(username)
    return merge_sort(amigos)



