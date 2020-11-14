# api_ds4a

¿Que hace nuestra API?: 

Creamos un modelo que facilita a las entidades contratantes la asignación del código UNSPSC (The United Nations Standard Products and Services Code). Nuestro modelo predictivo fue entrenado con los datos de los contratos existentes, teniendo en cuenta variables de interés y métricas para su ajuste

Esta interfaz recibe un JSON por medio del method 'POST' con la descripcion del objeto de contratacion y retorna la predicion los grupos con mas probabilidad y sus respectivos 3 segmentos mas probables segun los códigos UNSPSC.

Codigo para HTTP:

POST /predict? HTTP/1.1
Host: ec2-18-217-22-128.us-east-2.compute.amazonaws.com:8080
Content-Type: application/json

{"texto":"prestacion de servicios como enfermera jefe para el hospital universitario del valle"}
   

Como resultado al ejecutar el API se obtiene un JSON con el resultado de la predicion:

Respuesta API:

{"resultado":"Primer grupo sugerido 
			F: Servicios
			Segmentos con mayor probabilidad
			85: Servicios de Salud
			80: Servicios de Gestión, Servicios Profesionales de Empresa y Servicios Administrativos
			92: Servicios de Defensa Nacional, Orden Publico, Seguridad y Vigilancia


			Segundo grupo sugerido 
			E: Productos de uso final
			Segmentos con mayor probabilidad
			42: Equipo Médico, Accesorios y Suministros
			51: Medicamentos y Productos Farmacéuticos
			55: Publicaciones Impresas, Publicaciones Electrónicas y Accesorios


			Tercer grupo sugerido 
			B: Materias primas
			Segmentos con mayor probabilidad
			12: Material Químico incluyendo Bioquímicos y Materiales de Gas
			14: Materiales y Productos de Papel
			11: Material Mineral, Textil y  Vegetal y Animal No Comestible
			"}