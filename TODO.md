## TODO ##

# Código #

* Soporte para BEGIN y END

* For solo con segundo parametro obligatorio
	Ejemplo: 
		a=1;
		for(;true;)
			a += 1;
* En los if con cuerpos sin encerrarse entre llaves
  puede ir muchos lineas de comentario y despues la instruccion
	Ejemplo:
		if(true)
			\# Comentario1
			\# Comentario2
			\# Comentario3
			a=10;

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
	* etc
	
* Ir poniendo pruebas de codigo validas e invalidas en la
  seccion de pruebas que expliquen como elegimos precedencia y
  demás

* Mucho y mucho más
