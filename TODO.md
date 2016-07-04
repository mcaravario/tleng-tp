## TODO ##

# Código #

* Los comentarios pueden ir a la derecha de las instrucciones
	Ejemplo:
		a=10; #Comentario

* Soportar indexación de vectores/matrices de registros
	Ejemplo:
		a = {v1:[1,2],v2:[3,4]};
		b = {v1:[2,4],v2:[3,4]};
		c = [a,b];
		d = c[1].v3;

* Emprolijar y revisar informe de errores en general

* Emprolijar código y nombres

# Informe #

* Actualizar la gramática

* Problemas que nos encontramos en la escritura de la gramatica
	* Dangling else
	* Ambiguedad en la escritura de las operaciones aritméticas
	* Eleccion de precedencia
  * Ambiguedad en las listas
  * Conflicto con los comentarios (nueva linea y despues de instruccion)
	* etc
	
* Ir poniendo pruebas de codigo validas e invalidas en la
  seccion de pruebas que expliquen como elegimos precedencia y
  demás

* Mucho y mucho más
