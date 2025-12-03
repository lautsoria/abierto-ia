DROP SCHEMA IF EXISTS ids;
CREATE DATABASE IF NOT EXISTS ids;
USE ids;

CREATE TABLE IF NOT EXISTS roles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  rol VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario VARCHAR(25) NOT NULL UNIQUE,
  email VARCHAR(50) NOT NULL UNIQUE,
  contrasena VARCHAR(12) NOT NULL,
  rol_id INT,
  telefono VARCHAR(20),
  fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (rol_id) REFERENCES roles(id)
);

CREATE TABLE IF NOT EXISTS proveedores (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NULL,
  descripcion VARCHAR(500),
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS categorias (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL UNIQUE,
  descripcion TEXT,
  fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS servicios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  proveedor_id INT NOT NULL,
  categoria_id INT NOT NULL,
  nombre VARCHAR(255) NOT NULL,
  descripcion TEXT,
  precio DECIMAL(10,2) NOT NULL,
  hora_inicio INT CHECK (hora_inicio BETWEEN 1 AND 24),
  hora_fin INT CHECK (hora_fin BETWEEN 1 AND 24),
  duracion INT CHECK (duracion BETWEEN 1 AND 12),
  fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT check_horas CHECK (hora_fin > hora_inicio),
  FOREIGN KEY (proveedor_id) REFERENCES proveedores(id),
  FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE IF NOT EXISTS reservas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NOT NULL,
  servicio_id INT NOT NULL,
  fecha_reserva DATETIME DEFAULT CURRENT_TIMESTAMP,
  fecha_servicio DATETIME NOT NULL,
  hora_servicio INT NOT NULL,
  direccion VARCHAR(100),
  estado ENUM('pendiente', 'confirmado', 'realizado', 'cancelado') DEFAULT 'pendiente',
  comentarios_cliente TEXT,
  token_qr VARCHAR(64),
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
  FOREIGN KEY (servicio_id) REFERENCES servicios(id)
);

CREATE TABLE IF NOT EXISTS resenas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NOT NULL,
  servicio_id INT NOT NULL,
  puntuacion INT CHECK (puntuacion BETWEEN 1 AND 5),
  comentarios_cliente TEXT,
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
  FOREIGN KEY (servicio_id) REFERENCES servicios(id)
);

CREATE TABLE IF NOT EXISTS barrios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS barrios_usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NOT NULL,
  barrio_id INT NOT NULL,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
  FOREIGN KEY (barrio_id) REFERENCES barrios(id)
);


-- Roles
INSERT INTO roles (rol) VALUES
('cliente'),
('proveedor'),
('admin');

-- Usuarios
INSERT INTO usuarios (usuario, email, contrasena, rol_id, telefono, fecha_registro) VALUES
('juan_perez','juan@gmail.com','pass123',2,'11-5555-1234',NOW()),
('maria_gomez','maria@gmail.com','pass456',1,'11-5555-2345',NOW()),
('carlos_ruiz','carlos@hotmail.com','pass789',2,'11-5555-5678',NOW()),
('ana_lopez','ana@yahoo.com','pass101',1,'11-5555-3456',NOW()),
('luis_martin','luis@gmail.com','pass202',2,'11-5555-9012',NOW()),
('sofia_garcia','sofia@outlook.com','pass303',1,'11-5555-4567',NOW()),
('diego_torres','diego@gmail.com','pass404',2,'11-5555-3456',NOW()),
('laura_vazquez','laura@gmail.com','pass505',1,'11-5555-5678',NOW());

-- Categorias
INSERT INTO categorias (nombre, descripcion, fecha_creacion) VALUES
('Plomería','Servicios de instalación y reparación de plomería',NOW()),
('Electricidad','Instalaciones eléctricas y reparaciones',NOW()),
('Carpintería','Trabajos en madera y muebles',NOW()),
('Limpieza','Servicios de limpieza para hogares y oficinas',NOW()),
('Jardinería','Mantenimiento de jardines y áreas verdes',NOW()),
('Pintura','Pintura interior y exterior',NOW());

-- Barrios
INSERT INTO barrios (nombre) VALUES
('Palermo'),('Belgrano'),('Caballito'),('Recoleta');

-- Barrios_usuarios (para proveedores)
INSERT INTO barrios_usuarios (usuario_id, barrio_id) VALUES
(1,1), -- juan_perez -> Palermo
(3,2), -- carlos_ruiz -> Belgrano
(5,3), -- luis_martin -> Caballito
(7,4); -- diego_torres -> Recoleta

-- Proveedores
INSERT INTO proveedores (usuario_id, descripcion) VALUES
(1,'Plomero profesional con 10 años de experiencia'),
(3,'Electricista certificado, trabajos garantizados'),
(5,'Carpintero especializado en muebles a medida'),
(7,'Servicio de limpieza profesional');

-- Servicios
INSERT INTO servicios (proveedor_id, categoria_id, nombre, descripcion, precio, hora_inicio, hora_fin, duracion, fecha_creacion) VALUES
(1,1,'Reparación de cañerías','Arreglo de pérdidas y cambio de cañerías',3500,8,18,2,NOW()),
(3,2,'Instalación de luminarias','Instalación de luces LED y artefactos',4000,8,18,3,NOW()),
(5,3,'Fabricación de muebles','Muebles personalizados de calidad',15000,8,18,8,NOW()),
(7,4,'Limpieza profunda','Limpieza completa incluyendo cocina y baños',2500,8,18,4,NOW());

-- Reservas de prueba
INSERT INTO reservas (usuario_id, servicio_id, fecha_reserva, fecha_servicio, hora_servicio, direccion, estado, comentarios_cliente) VALUES
(2,1,NOW(),DATE_ADD(NOW(), INTERVAL 3 DAY),10,'Av. Santa Fe 1234, Palermo','pendiente','Por favor llegar a tiempo'),
(4,2,NOW(),DATE_ADD(NOW(), INTERVAL 2 DAY),12,'Av. Corrientes 2500, Balvanera','confirmado','Servicio urgente'),
(6,3,NOW(),DATE_ADD(NOW(), INTERVAL 5 DAY),9,'Av. Cabildo 3400, Belgrano','pendiente','Muy recomendable'),
(8,4,NOW(),DATE_ADD(NOW(), INTERVAL 1 DAY),14,'Av. Rivadavia 5678, Caballito','pendiente','');

-- Reseñas
INSERT INTO resenas (usuario_id, servicio_id, puntuacion, comentarios_cliente, fecha) VALUES
(2,1,5,'Excelente servicio',NOW()),
(4,2,4,'Buen servicio pero llegó tarde',NOW()),
(6,3,5,'Muy satisfecho con el resultado',NOW()),
(8,4,4,'Cumplió con lo prometido',NOW());
