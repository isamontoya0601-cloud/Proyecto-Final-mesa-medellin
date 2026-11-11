-- Datos Usuario --

INSERT INTO usuario (u_nombre_completo, u_telefono, u_correo, u_ciudad_origen, u_tipo_cliente, u_estado) 
VALUES ('Carlos Andrés Pérez', 3012345678, 'carlos.perez@email.com', 'Medellín', 'FRECUENTE', 'ACTIVO');

INSERT INTO usuario (u_nombre_completo, u_telefono, u_correo, u_ciudad_origen, u_tipo_cliente, u_estado) 
VALUES ('María Alejandra Gómez', 3109876543, 'maria.gomez@email.com', 'Bogotá', 'VIP', 'ACTIVO');

INSERT INTO usuario (u_nombre_completo, u_telefono, u_correo, u_ciudad_origen, u_tipo_cliente, u_estado) 
VALUES ('Juan David Londoño', 3114567890, 'juan.londono@email.com', 'Medellín', 'OCASIONAL', 'ACTIVO');

INSERT INTO usuario (u_nombre_completo, u_telefono, u_correo, u_ciudad_origen, u_tipo_cliente, u_estado) 
VALUES ('Ana Sofía Restrepo', 3123456789, 'ana.restrepo@email.com', 'Envigado', 'VIP', 'ACTIVO');

INSERT INTO usuario (u_nombre_completo, u_telefono, u_correo, u_ciudad_origen, u_tipo_cliente, u_estado) 
VALUES ('Luis Fernando Mejía', 3135678901, 'luis.mejia@email.com', 'Cali', 'OCASIONAL', 'INACTIVO');

INSERT INTO usuario (u_nombre_completo, u_telefono, u_correo, u_ciudad_origen, u_tipo_cliente, u_estado) 
VALUES ('Valentina Jaramillo', 3146789012, 'valentina.jaramillo@email.com', 'Medellín', 'FRECUENTE', 'ACTIVO');

INSERT INTO usuario (u_nombre_completo, u_telefono, u_correo, u_ciudad_origen, u_tipo_cliente, u_estado) 
VALUES ('Mateo Orozco Echeverri', 3157890123, 'mateo.orozco@email.com', 'Bello', 'OCASIONAL', 'ACTIVO');

INSERT INTO usuario (u_nombre_completo, u_telefono, u_correo, u_ciudad_origen, u_tipo_cliente, u_estado) 
VALUES ('Manuela Giraldo', 3168901234, 'manuela.giraldo@email.com', 'Sabaneta', 'VIP', 'ACTIVO');

INSERT INTO usuario (u_nombre_completo, u_telefono, u_correo, u_ciudad_origen, u_tipo_cliente, u_estado) 
VALUES ('Esteban Rúa Zapata', 3179012345, 'esteban.rua@email.com', 'Itagüí', 'OCASIONAL', 'INACTIVO');

INSERT INTO usuario (u_nombre_completo, u_telefono, u_correo, u_ciudad_origen, u_tipo_cliente, u_estado) 
VALUES ('Camila Andrea Valencia', 3180123456, 'camila.valencia@email.com', 'Medellín', 'FRECUENTE', 'ACTIVO');

-- Datos --

INSERT INTO restaurante (r_nombre, r_tipo_cocina, r_direccion, r_capacidad_maxima, r_precio_promedio, r_estado) 
VALUES ('El Cielo', 'Autor', 'Cra. 40 #10A-22, El Poblado', 60, 150000.00, 'ACTIVO');

INSERT INTO restaurante (r_nombre, r_tipo_cocina, r_direccion, r_capacidad_maxima, r_precio_promedio, r_estado) 
VALUES ('Mondongos', 'Colombiana', 'Cl. 10 #38-38, El Poblado', 120, 55000.00, 'ACTIVO');

INSERT INTO restaurante (r_nombre, r_tipo_cocina, r_direccion, r_capacidad_maxima, r_precio_promedio, r_estado) 
VALUES ('Crepes y Waffles', 'Fusión', 'Centro Comercial El Tesoro', 100, 42000.00, 'ACTIVO');

INSERT INTO restaurante (r_nombre, r_tipo_cocina, r_direccion, r_capacidad_maxima, r_precio_promedio, r_estado) 
VALUES ('Carmen', 'Autor', 'Cra. 36 #10A-27, El Poblado', 80, 130000.00, 'ACTIVO');

INSERT INTO restaurante (r_nombre, r_tipo_cocina, r_direccion, r_capacidad_maxima, r_precio_promedio, r_estado) 
VALUES ('Alambique', 'Fusión', 'Cl. 10 #43D-66, El Poblado', 50, 70000.00, 'ACTIVO');

INSERT INTO restaurante (r_nombre, r_tipo_cocina, r_direccion, r_capacidad_maxima, r_precio_promedio, r_estado) 
VALUES ('Il Forno', 'Italiana', 'Av. El Poblado #7-35', 90, 48000.00, 'ACTIVO');

INSERT INTO restaurante (r_nombre, r_tipo_cocina, r_direccion, r_capacidad_maxima, r_precio_promedio, r_estado) 
VALUES ('Hatoviejo', 'Colombiana', 'Km 9 Vía Las Palmas', 150, 65000.00, 'ACTIVO');

INSERT INTO restaurante (r_nombre, r_tipo_cocina, r_direccion, r_capacidad_maxima, r_precio_promedio, r_estado) 
VALUES ('Cambalache', 'Argentina', 'Cra. 35 #7-67, El Poblado', 70, 95000.00, 'EN MANTENIMIENTO');

INSERT INTO restaurante (r_nombre, r_tipo_cocina, r_direccion, r_capacidad_maxima, r_precio_promedio, r_estado) 
VALUES ('Pergamino Cafe', 'Café y Brunch', 'Cra. 37 #8A-37, El Poblado', 40, 28000.00, 'ACTIVO');

INSERT INTO restaurante (r_nombre, r_tipo_cocina, r_direccion, r_capacidad_maxima, r_precio_promedio, r_estado) 
VALUES ('San Carbon', 'Carnes', 'Av. Las Palmas #30-65', 200, 110000.00, 'INACTIVO');

-- Datos Zona Medellin -- 

INSERT INTO zona_medellin (z_nombre_zona, z_comuna_barrio, z_sector_turistico, z_estrato_predominante, z_estado) 
VALUES ('El Poblado', 'Comuna 14 - El Poblado', 1, 6, 'HABILITADA');

INSERT INTO zona_medellin (z_nombre_zona, z_comuna_barrio, z_sector_turistico, z_estrato_predominante, z_estado) 
VALUES ('Laureles', 'Comuna 11 - Laureles-Estadio', 1, 5, 'HABILITADA');

INSERT INTO zona_medellin (z_nombre_zona, z_comuna_barrio, z_sector_turistico, z_estrato_predominante, z_estado) 
VALUES ('Envigado Centro', 'Zona Centro Envigado', 0, 4, 'HABILITADA');

INSERT INTO zona_medellin (z_nombre_zona, z_comuna_barrio, z_sector_turistico, z_estrato_predominante, z_estado) 
VALUES ('Centro de Medellín', 'Comuna 10 - La Candelaria', 1, 3, 'HABILITADA');

INSERT INTO zona_medellin (z_nombre_zona, z_comuna_barrio, z_sector_turistico, z_estrato_predominante, z_estado) 
VALUES ('Sabaneta', 'Parque de Sabaneta', 1, 4, 'HABILITADA');

INSERT INTO zona_medellin (z_nombre_zona, z_comuna_barrio, z_sector_turistico, z_estrato_predominante, z_estado) 
VALUES ('Bello Centro', 'Comuna 1 - Centro Bello', 0, 2, 'HABILITADA');

INSERT INTO zona_medellin (z_nombre_zona, z_comuna_barrio, z_sector_turistico, z_estrato_predominante, z_estado) 
VALUES ('Estadio', 'Comuna 11 - Laureles-Estadio', 0, 4, 'HABILITADA');

INSERT INTO zona_medellin (z_nombre_zona, z_comuna_barrio, z_sector_turistico, z_estrato_predominante, z_estado) 
VALUES ('Belén', 'Comuna 16 - Belén', 0, 3, 'HABILITADA');

INSERT INTO zona_medellin (z_nombre_zona, z_comuna_barrio, z_sector_turistico, z_estrato_predominante, z_estado) 
VALUES ('Manrique', 'Comuna 3 - Manrique', 0, 2, 'NO HABILITADA');

INSERT INTO zona_medellin (z_nombre_zona, z_comuna_barrio, z_sector_turistico, z_estrato_predominante, z_estado) 
VALUES ('Robledo', 'Comuna 7 - Robledo', 0, 3, 'HABILITADA');

-- Datos Reserva Restaurante --

INSERT INTO reserva_restaurante (r_id_usuario, r_id_restaurante, r_id_zona, r_fecha_hora, r_numero_personas, r_deposito_reserva, r_estado) 
VALUES (1, 1, 1, TO_DATE('2026-11-15 20:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2, 50000.00, 'CONFIRMADA');

INSERT INTO reserva_restaurante (r_id_usuario, r_id_restaurante, r_id_zona, r_fecha_hora, r_numero_personas, r_deposito_reserva, r_estado) 
VALUES (2, 2, 1, TO_DATE('2026-11-12 13:30:00', 'YYYY-MM-DD HH24:MI:SS'), 4, 0.00, 'COMPLETADA');

INSERT INTO reserva_restaurante (r_id_usuario, r_id_restaurante, r_id_zona, r_fecha_hora, r_numero_personas, r_deposito_reserva, r_estado) 
VALUES (3, 3, 2, TO_DATE('2026-11-18 19:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3, 30000.00, 'CONFIRMADA');

INSERT INTO reserva_restaurante (r_id_usuario, r_id_restaurante, r_id_zona, r_fecha_hora, r_numero_personas, r_deposito_reserva, r_estado) 
VALUES (4, 4, 1, TO_DATE('2026-11-10 21:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2, 80000.00, 'COMPLETADA');

INSERT INTO reserva_restaurante (r_id_usuario, r_id_restaurante, r_id_zona, r_fecha_hora, r_numero_personas, r_deposito_reserva, r_estado) 
VALUES (5, 5, 1, TO_DATE('2026-11-05 20:30:00', 'YYYY-MM-DD HH24:MI:SS'), 5, 40000.00, 'CANCELADA');

INSERT INTO reserva_restaurante (r_id_usuario, r_id_restaurante, r_id_zona, r_fecha_hora, r_numero_personas, r_deposito_reserva, r_estado) 
VALUES (6, 6, 2, TO_DATE('2026-11-20 14:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2, 0.00, 'CONFIRMADA');

INSERT INTO reserva_restaurante (r_id_usuario, r_id_restaurante, r_id_zona, r_fecha_hora, r_numero_personas, r_deposito_reserva, r_estado) 
VALUES (7, 7, 5, TO_DATE('2026-11-01 12:30:00', 'YYYY-MM-DD HH24:MI:SS'), 6, 60000.00, 'NO ASISTIO');

INSERT INTO reserva_restaurante (r_id_usuario, r_id_restaurante, r_id_zona, r_fecha_hora, r_numero_personas, r_deposito_reserva, r_estado) 
VALUES (8, 9, 1, TO_DATE('2026-11-22 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2, 20000.00, 'CONFIRMADA');

INSERT INTO reserva_restaurante (r_id_usuario, r_id_restaurante, r_id_zona, r_fecha_hora, r_numero_personas, r_deposito_reserva, r_estado) 
VALUES (9, 3, 3, TO_DATE('2026-11-08 19:30:00', 'YYYY-MM-DD HH24:MI:SS'), 4, 30000.00, 'COMPLETADA');

INSERT INTO reserva_restaurante (r_id_usuario, r_id_restaurante, r_id_zona, r_fecha_hora, r_numero_personas, r_deposito_reserva, r_estado) 
VALUES (10, 6, 2, TO_DATE('2026-11-25 21:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2, 25000.00, 'CONFIRMADA');

COMMIT;
