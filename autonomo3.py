import pyodbc
from tabulate import tabulate
from decimal import Decimal
import datetime

def conectar_a_base_de_datos():
    """Permite al usuario conectarse a la base de datos"""
    
    try:
        connection = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=DESKTOP-HJ4FTRI\\SQLEXPRESS;"
            "Database=Trabajo autonomo;"
            "Trusted_Connection=yes;"
        )
        placeholder = '?'  # Placeholder para SQL Server
        return connection, placeholder
    except pyodbc.Error as e:
        print(f"Error al conectar a SQL Server: {e}")
        return None, None 

def convertir_tipo_datos(resultados):
    """Convierte los tipos de datos en los resultados para que sean compatibles con tabulate"""
    resultados_convertidos = []
    for fila in resultados:
        fila_convertida = []
        for valor in fila:
            if isinstance(valor, Decimal):
                valor = float(valor)
            elif isinstance(valor, datetime.date):
                valor = str(valor)
            fila_convertida.append(valor)
        resultados_convertidos.append(tuple(fila_convertida))
    return resultados_convertidos

def ejecutar_consulta(cursor, consulta, params=None):
    """Ejecuta una consulta SQL y devuelve los resultados formateados en una tabla"""
    try:
        cursor.execute(consulta, params or ())
        results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        # print(f"Descripción de las columnas: {columns}")
        # print(f"Resultados obtenidos: {results}")
        if not results:
            print("No se encontraron resultados.")
            return "No data available"
        results = convertir_tipo_datos(results)
        table = tabulate(results, headers=columns, tablefmt="grid")
        print("Consulta ejecutada correctamente.")
        return table
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return "Error ejecutando la consulta"

def leer_script_sql(nombre_archivo):
    """Lee el contenido de un archivo SQL"""
    try:
        with open(nombre_archivo, 'r') as file:
            script = file.read()
        return script
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no se encontró.")
        return None

def main():
    conexion, placeholder = conectar_a_base_de_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            while True:
                print("\n--- SISTEMA DE STREAMING---")
                print("1. Mostrar todas las peliculas")
                print("2. Buscar pelicula por nombre")
                print("3. Buscar pelicula por género")
                print("4. Buscar pelicula por director")
                print("5. Actualizar la clasificación de una pelicula")
                print("6. Añadir una pelicula a favoritos")
                print("7. Eliminar pelicula de favoritos")
                print("8. Mostrar favoritos")
                print("9. Top 5 usuarios con más favoritos")
                print("10. Catálogo de películas ordenado por demanda")
                print("11. Salir")
                opcion = input("Elige una opción: ")

                if opcion == '1':
                    consulta = """
                    SELECT p.peli_id AS ID, 
                           p.peli_nom AS Título, 
                           p.peli_año AS Año,
                           p.peli_dur AS Duracción,
                           p.peli_clas AS Clasificación, 
                           g.gen_nom AS Género, 
                           d.direc_nom AS Director
                    FROM Pelicula p
                    INNER JOIN Género g ON p.gen_id = g.gen_id
                    INNER JOIN Director d ON p.direc_id = d.direc_id
                    """
                    #muestra las peliculas con sus caracteristicas 
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)
                elif opcion == '2':
                    nombre_buscar = input("Ingresa el nombre de la película: ")
                    
                    # El operador LIKE busca coincidencias parciales. El comodín % se añade en los parámetros.
                    consulta = """
                    SELECT p.peli_id AS ID, 
                           p.peli_nom AS Título, 
                           p.peli_clas AS Clasificación, 
                           p.peli_año AS Año,
                           p.peli_dur AS Duracción,
                           g.gen_nom AS Género, 
                           d.direc_nom AS Director
                    FROM Pelicula p
                    INNER JOIN Género g ON p.gen_id = g.gen_id
                    INNER JOIN Director d ON p.direc_id = d.direc_id
                    WHERE p.peli_nom LIKE ?
                    """
                    # Pasamos el parámetro envolviendo el texto entre símbolos de porcentaje '%'
                    parametro = f"%{nombre_buscar}%"
                    
                    resultado = ejecutar_consulta(cursor, consulta, (parametro))
                    print(resultado)
                elif opcion == '3':
                    genero_buscar = input("Ingresa el género de la película: ")
                    
                    # El operador LIKE busca coincidencias parciales. El comodín % se añade en los parámetros.
                    consulta = """
                    SELECT p.peli_id AS ID, 
                           p.peli_nom AS Título, 
                           p.peli_año AS Año,
                           p.peli_dur AS Duracción,
                           p.peli_clas AS Clasificación, 
                           g.gen_nom AS Género, 
                           d.direc_nom AS Director
                    FROM Pelicula p
                    INNER JOIN Género g ON p.gen_id = g.gen_id
                    INNER JOIN Director d ON p.direc_id = d.direc_id
                    WHERE g.gen_nom LIKE ?
                    """
                    # Pasamos el parámetro envolviendo el texto entre símbolos de porcentaje '%'
                    parametro = f"%{genero_buscar}%"
                    
                    resultado = ejecutar_consulta(cursor, consulta, (parametro))
                    print(resultado)
                elif opcion == '4':
                    director_buscar = input("Ingresa el nombre del director: ")
                    
                    # El operador LIKE busca coincidencias parciales. El comodín % se añade en los parámetros.
                    consulta = """
                    SELECT p.peli_id AS ID, 
                           p.peli_nom AS Título, 
                           p.peli_año AS Año,
                           p.peli_dur AS Duracción,
                           p.peli_clas AS Clasificación, 
                           g.gen_nom AS Género, 
                           d.direc_nom AS Director
                    FROM Pelicula p
                    INNER JOIN Género g ON p.gen_id = g.gen_id
                    INNER JOIN Director d ON p.direc_id = d.direc_id
                    WHERE d.direc_nom LIKE ?
                    """
                    # Pasamos el parámetro envolviendo el texto entre símbolos de porcentaje '%'
                    parametro = f"%{director_buscar}%"
                    
                    resultado = ejecutar_consulta(cursor, consulta, (parametro))
                    print(resultado)
                elif opcion == '5':
                    idpelicula = input("Ingrese el ID de la película: ")
                    nueva_clas = input("Ingrese la nueva clasificación: ")

                    consulta = f"""
                    UPDATE Pelicula
                    SET peli_clas = {placeholder}
                    WHERE peli_id = {placeholder}
                    """

                    cursor.execute(consulta, (nueva_clas, idpelicula))
                    conexion.commit()
                    print("Clasificación actualizada correctamente.")
                elif opcion == '6':
                    try:
                        idusuario = input("ingresa el id del usuario:")
                        idpelicula = input("ingresa el id de la pelicula:")
                        
                        consulta = f"INSERT INTO Favorito (peli_id, usu_id) VALUES ({placeholder}, {placeholder})"
                        cursor.execute(consulta, (idpelicula, idusuario))
                        conexion.commit()  
                        print("¡Película añadida a favoritos con éxito!")
                    
                    except ValueError:
                        print("Error: Los IDs deben ser números enteros.")
                    
                    except Exception as e:
                        print(f"Error al añadir a favoritos: {e}")
                elif opcion == '7':
                    try:
                        idusuario = input("ingresa el id del usuario:")
                        idpelicula = input("ingresa el id de la pelicula:")
                        
                        consulta = f"DELETE FROM Favorito WHERE peli_id = {placeholder} AND usu_id = {placeholder}"
                        cursor.execute(consulta, (idpelicula, idusuario))
                        conexion.commit() 
                        if cursor.rowcount > 0: 
                            print("¡Película eliminada de favoritos con éxito!")
                        else:
                            print("No se encontro esa pelicula en favoritos")
                    except ValueError:
                        print("Error: Los IDs deben ser números enteros.")
                    
                    except Exception as e:
                        print(f"Error al eliminar de favoritos: {e}")
                elif opcion == '8':
                    idusuario = input("Ingresa tu ID de usuario para ver tus favoritos: ")
                    
                    consulta = f"""
                    SELECT f.fav_id AS [ID Favorito], 
                           p.peli_nom AS Título, 
                           g.gen_nom AS Género, 
                           d.direc_nom AS Director
                    FROM Favorito f 
                    INNER JOIN Pelicula p ON f.peli_id = p.peli_id
                    INNER JOIN Usuario u ON f.usu_id = u.usu_id
                    INNER JOIN Género g ON p.gen_id = g.gen_id     
                    INNER JOIN Director d ON p.direc_id = d.direc_id 
                    WHERE f.usu_id = {placeholder}
                    """
                    #mostrara los favoritos solo del usuario seleccionado
                    resultado = ejecutar_consulta(cursor, consulta, (idusuario))
                    print(resultado)
                elif opcion == '9':
                    consulta = f"""
                    SELECT TOP 5 u.usu_id AS ID,
                                u.usu_nom AS Usuario, 
                                COUNT(f.fav_id) AS TotalFavoritos
                    FROM Usuario u
                    INNER JOIN Favorito f ON u.usu_id = f.usu_id
                    GROUP BY u.usu_id, u.usu_nom
                    ORDER BY COUNT(f.fav_id) DESC
                    """
                    #TOP 5 para solo incluir los 5 con mas favoritos
                    #GROUP BY agrupación obligatoria por el COUNT
                    #ORDER BY DESC para ordenar los resultados de mayor a menor de usuarios con mas favoritos
                    
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)
                elif opcion == '10':
                    consulta = f"""
                    SELECT p.peli_id AS ID, 
                           p.peli_nom AS Título, 
                           p.peli_año AS Año,
                           p.peli_dur AS Duracción,
                           p.peli_clas AS Clasificación, 
                           g.gen_nom AS Género, 
                           d.direc_nom AS Director,
                           COUNT(f.fav_id) AS VecesEnFavoritos
                    FROM Pelicula p
                    INNER JOIN Género g ON p.gen_id = g.gen_id 
                    INNER JOIN Director d ON p.direc_id = d.direc_id
                    LEFT JOIN Favorito f ON p.peli_id = f.peli_id
                    GROUP BY p.peli_id, p.peli_nom, p.peli_año, p.peli_dur, p.peli_clas, g.gen_nom, d.direc_nom
                    ORDER BY VecesEnFavoritos DESC 
                    """
                    #LEFT JOIN para incluir películas con 0 favoritos
                    #GROUP BY agrupación obligatoria por el COUNT
                    #ORDER BY DESC para ordenar los resultados de mayor a menor popularidad
                
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)      
                elif opcion == '11':
                    print("Saliendo...")
                    break
                #rompe el bucle para que ya no salga la consulta de opciones
                else:
                    print("Opción no válida, intenta de nuevo.")
        except Exception as e:
            print(f"Error durante la operación: {e}")
        finally:
            cursor.close()
            conexion.close()
    else:
        print("No se pudo conectar a la base de datos.")

if __name__ == "__main__":
    main()