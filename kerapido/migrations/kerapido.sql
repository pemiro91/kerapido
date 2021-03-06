INSERT INTO kerapido_provincia (nombre)
VALUES ('Pinar del Río');
INSERT INTO kerapido_provincia (nombre)
VALUES ('Artemisa');
INSERT INTO kerapido_provincia (nombre)
VALUES ('Mayabeque');
INSERT INTO kerapido_provincia (nombre)
VALUES ('La Habana');
INSERT INTO kerapido_provincia (nombre)
VALUES ('Matanzas');
INSERT INTO kerapido_provincia (nombre)
VALUES ('Villa Clara');
INSERT INTO kerapido_provincia (nombre)
VALUES ('Cienfuegos');
INSERT INTO kerapido_provincia (nombre)
VALUES ('Sancti Spíritus');
INSERT INTO kerapido_provincia (nombre)
VALUES ('Ciego de Ávila');
INSERT INTO kerapido_provincia (nombre)
VALUES ('Camagüey');
INSERT INTO kerapido_provincia (nombre)
VALUES ('Las Tunas');
INSERT INTO kerapido_provincia (nombre)
VALUES ('Holguín');
INSERT INTO kerapido_provincia (nombre)
VALUES ('Granma');
INSERT INTO kerapido_provincia (nombre)
VALUES ('Santiago de Cuba');
INSERT INTO kerapido_provincia (nombre)
VALUES ('Guantánamo');
INSERT INTO kerapido_provincia (nombre)
VALUES ('Isla de la Juventud');

INSERT INTO kerapido_municipio (nombre, provincia_id)
VALUES ('Diez de Octubre', 4);
INSERT INTO kerapido_municipio (nombre, provincia_id)
VALUES ('Arroyo Naranjo', 4);
INSERT INTO kerapido_municipio (nombre, provincia_id)
VALUES ('Boyeros', 4);
INSERT INTO kerapido_municipio (nombre, provincia_id)
VALUES ('Playa', 4);
INSERT INTO kerapido_municipio (nombre, provincia_id)
VALUES ('Habana del Este', 4);
INSERT INTO kerapido_municipio (nombre, provincia_id)
VALUES ('San Miguel del Padrón', 4);
INSERT INTO kerapido_municipio (nombre, provincia_id)
VALUES ('Plaza de la Revolución', 4);
INSERT INTO kerapido_municipio (nombre, provincia_id)
VALUES ('Centro Habana', 4);
INSERT INTO kerapido_municipio (nombre, provincia_id)
VALUES ('Marianao', 4);
INSERT INTO kerapido_municipio (nombre, provincia_id)
VALUES ('La Lisa', 4);
INSERT INTO kerapido_municipio (nombre, provincia_id)
VALUES ('Cerro', 4);
INSERT INTO kerapido_municipio (nombre, provincia_id)
VALUES ('Guanabacoa', 4);
INSERT INTO kerapido_municipio (nombre, provincia_id)
VALUES ('Habana Vieja', 4);
INSERT INTO kerapido_municipio (nombre, provincia_id)
VALUES ('Cotorro', 4);
INSERT INTO kerapido_municipio (nombre, provincia_id)
VALUES ('Regla', 4);

INSERT INTO kerapido_macro (nombre)
VALUES ('Comercio y Gastronomía');
INSERT INTO kerapido_macro (nombre)
VALUES ('Mercado');
INSERT INTO kerapido_macro (nombre)
VALUES ('Transporte');

INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Restaurantes de comida criolla e internacionales', '', 1);
INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Pizzerías y cafeterías ', '', 1);
INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Hamburguesera', '', 1);
INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Juguera', '', 1);
INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Bar', '', 1);
INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Dulcería', '', 1);
INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Heladería', '', 1);
INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Billar', '', 1);
INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Florería', '', 1);
INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Piscina', '', 1);
INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Comida rápida', '', 1);
INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Agromercado', '', 2);
INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Carnicería', '', 2);
INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Pescadería', '', 2);
INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Mercado mixto', '', 2);
INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Moto', '', 3);
INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Carro', '', 3);
INSERT INTO kerapido_categoria_negocio (nombre, descripcion, macro_id)
VALUES ('Bicicleta', '', 3);

INSERT INTO kerapido_servicio (nombre, descripcion, color)
VALUES ('Para recoger', '', 'amber');
INSERT INTO kerapido_servicio (nombre, descripcion, color)
VALUES ('Entrega a domicilio', '', 'green');
INSERT INTO kerapido_servicio (nombre, descripcion, color)
VALUES ('Mesas y Espacios', '', 'grey');

INSERT INTO kerapido_frecuencia (nombre)
VALUES ('Lunes');
INSERT INTO kerapido_frecuencia (nombre)
VALUES ('Martes');
INSERT INTO kerapido_frecuencia (nombre)
VALUES ('Miércoles');
INSERT INTO kerapido_frecuencia (nombre)
VALUES ('Jueves');
INSERT INTO kerapido_frecuencia (nombre)
VALUES ('Viernes');
INSERT INTO kerapido_frecuencia (nombre)
VALUES ('Sábado');
INSERT INTO kerapido_frecuencia (nombre)
VALUES ('Domingo');