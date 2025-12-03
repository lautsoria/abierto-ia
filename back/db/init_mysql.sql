DROP SCHEMA IF EXISTS ids;
CREATE DATABASE IF NOT EXISTS ids;
USE ids;

CREATE TABLE IF NOT EXISTS roles (
  id VARCHAR(36) PRIMARY KEY,
  rol VARCHAR(50) UNIQUE NOT NULL
  -- hay que tener en cuenta que debemos tener solo 3 roles
  -- (cliente, proveedor, admin)
);

CREATE TABLE IF NOT EXISTS usuarios (
  id VARCHAR(36) PRIMARY KEY,
  usuario VARCHAR(25) NOT NULL UNIQUE,
  email VARCHAR(50) NOT NULL UNIQUE,
  contrasena VARCHAR(12) NOT NULL,
  rol_id VARCHAR(36),
  telefono VARCHAR(20),
  fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (rol_id) REFERENCES roles(id)
);

CREATE TABLE IF NOT EXISTS proveedores (
  id VARCHAR(36) PRIMARY KEY,
  descripcion VARCHAR(500),
  FOREIGN KEY (id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS categorias (
  id VARCHAR(36) PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL UNIQUE,
  descripcion TEXT,
  fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS servicios (
  id VARCHAR(36) PRIMARY KEY,
  proveedor_id VARCHAR(36) NOT NULL,
  categoria_id VARCHAR(36) NOT NULL,
  nombre VARCHAR(255) NOT NULL,
  descripcion TEXT,
  imagen INT NOT NULL DEFAULT 1 CHECK (imagen BETWEEN 1 AND 10),
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
  id VARCHAR(36) PRIMARY KEY,
  usuario_id VARCHAR(36) NOT NULL,
  servicio_id VARCHAR(36) NOT NULL,
  fecha_reserva DATETIME DEFAULT CURRENT_TIMESTAMP,
  fecha_servicio DATETIME NOT NULL,
  hora_servicio INT NOT NULL,
  direccion VARCHAR(100),
  estado ENUM('pendiente', 'confirmado', 'realizado', 'cancelado') DEFAULT 'pendiente',
  comentarios_cliente TEXT,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
  FOREIGN KEY (servicio_id) REFERENCES servicios(id)
);

CREATE TABLE IF NOT EXISTS resenas (
  id VARCHAR(36) PRIMARY KEY,
  usuario_id VARCHAR(36) NOT NULL,
  servicio_id VARCHAR(36) NOT NULL,
  reserva_id VARCHAR(36) NOT NULL UNIQUE,
  puntuacion INT CHECK (puntuacion BETWEEN 1 AND 5),
  comentarios_cliente TEXT,
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
  FOREIGN KEY (servicio_id) REFERENCES servicios(id),
  FOREIGN KEY (reserva_id) REFERENCES reservas(id)
);

CREATE TABLE IF NOT EXISTS barrios (
  id VARCHAR(36) PRIMARY KEY,
  nombre VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS barrios_servicios (
  id VARCHAR(36) PRIMARY KEY,
  servicio_id VARCHAR(36) NOT NULL,
  barrio_id VARCHAR(36) NOT NULL,
  UNIQUE KEY unique_servicio_barrio (servicio_id, barrio_id),
  FOREIGN KEY (servicio_id) REFERENCES servicios(id),
  FOREIGN KEY (barrio_id) REFERENCES barrios(id)
);

-- Insert Roles
INSERT INTO roles (id, rol) VALUES
(UUID(), 'cliente'),
(UUID(), 'proveedor'),
(UUID(), 'admin');

-- Insert Users
INSERT INTO usuarios (id, usuario, email, contrasena, rol_id, telefono, fecha_registro) VALUES
(UUID(), 'juan_perez', 'juan@gmail.com', 'pass123', (SELECT id FROM roles WHERE rol = 'proveedor'), '11-5555-1234', NOW()),
(UUID(), 'maria_gomez', 'maria@gmail.com', 'pass456', (SELECT id FROM roles WHERE rol = 'cliente'), '11-5555-2345', NOW()),
(UUID(), 'carlos_ruiz', 'carlos@hotmail.com', 'pass789', (SELECT id FROM roles WHERE rol = 'proveedor'), '11-5555-5678', NOW()),
(UUID(), 'ana_lopez', 'ana@yahoo.com', 'pass101', (SELECT id FROM roles WHERE rol = 'cliente'), '11-5555-3456', NOW()),
(UUID(), 'luis_martin', 'luis@gmail.com', 'pass202', (SELECT id FROM roles WHERE rol = 'proveedor'), '11-5555-9012', NOW()),
(UUID(), 'sofia_garcia', 'sofia@outlook.com', 'pass303', (SELECT id FROM roles WHERE rol = 'cliente'), '11-5555-4567', NOW()),
(UUID(), 'diego_torres', 'diego@gmail.com', 'pass404', (SELECT id FROM roles WHERE rol = 'proveedor'), '11-5555-3456', NOW()),
(UUID(), 'laura_vazquez', 'laura@gmail.com', 'pass505', (SELECT id FROM roles WHERE rol = 'cliente'), '11-5555-5678', NOW());

-- Insert Categories
INSERT INTO categorias (id, nombre, descripcion, fecha_creacion) VALUES
(UUID(), 'Plomería', 'Servicios de instalación y reparación de plomería', NOW()),
(UUID(), 'Electricidad', 'Instalaciones eléctricas y reparaciones', NOW()),
(UUID(), 'Carpintería', 'Trabajos en madera y muebles', NOW()),
(UUID(), 'Limpieza', 'Servicios de limpieza para hogares y oficinas', NOW()),
(UUID(), 'Jardinería', 'Mantenimiento de jardines y áreas verdes', NOW()),
(UUID(), 'Pintura', 'Pintura interior y exterior', NOW());

-- Insert Barrios
INSERT INTO barrios (id, nombre) VALUES
(UUID(), 'Agronomía'), (UUID(), 'Almagro'), (UUID(), 'Balvanera'), (UUID(), 'Barracas'), 
(UUID(), 'Belgrano'), (UUID(), 'Boedo'), (UUID(), 'Caballito'), (UUID(), 'Chacarita'), 
(UUID(), 'Coghlan'), (UUID(), 'Colegiales'), (UUID(), 'Constitución'), (UUID(), 'Flores'), 
(UUID(), 'Floresta'), (UUID(), 'La Boca'), (UUID(), 'La Paternal'), (UUID(), 'Liniers'), 
(UUID(), 'Mataderos'), (UUID(), 'Monte Castro'), (UUID(), 'Monserrat'), (UUID(), 'Nueva Pompeya'), 
(UUID(), 'Núñez'), (UUID(), 'Palermo'), (UUID(), 'Parque Avellaneda'), (UUID(), 'Parque Chacabuco'), 
(UUID(), 'Parque Chas'), (UUID(), 'Parque Patricios'), (UUID(), 'Puerto Madero'), (UUID(), 'Recoleta'), 
(UUID(), 'Retiro'), (UUID(), 'Saavedra'), (UUID(), 'San Cristóbal'), (UUID(), 'San Nicolás'), 
(UUID(), 'San Telmo'), (UUID(), 'Vélez Sársfield'), (UUID(), 'Versalles'), (UUID(), 'Villa Crespo'), 
(UUID(), 'Villa del Parque'), (UUID(), 'Villa Devoto'), (UUID(), 'Villa General Mitre'), (UUID(), 'Villa Lugano'), 
(UUID(), 'Villa Luro'), (UUID(), 'Villa Ortúzar'), (UUID(), 'Villa Pueyrredón'), (UUID(), 'Villa Real'), 
(UUID(), 'Villa Riachuelo'), (UUID(), 'Villa Santa Rita'), (UUID(), 'Villa Soldati'), (UUID(), 'Villa Urquiza');

-- Insert Proveedores (Linking to existing Usuarios)
INSERT INTO proveedores (id, descripcion) 
SELECT 
  id,
  CASE 
    WHEN usuario = 'juan_perez' THEN 'Plomero profesional con 10 años de experiencia'
    WHEN usuario = 'carlos_ruiz' THEN 'Electricista certificado, trabajos garantizados'
    WHEN usuario = 'luis_martin' THEN 'Carpintero especializado en muebles a medida'
    WHEN usuario = 'diego_torres' THEN 'Servicio de limpieza profesional'
  END
FROM usuarios 
WHERE usuario IN ('juan_perez', 'carlos_ruiz', 'luis_martin', 'diego_torres');

-- Insert Initial Services
INSERT INTO servicios (id, proveedor_id, categoria_id, nombre, descripcion, imagen, precio, hora_inicio, hora_fin, duracion, fecha_creacion)
SELECT 
  UUID(),
  p.id,
  c.id,
  CASE 
    WHEN c.nombre = 'Plomería' THEN 'Reparación de cañerías'
    WHEN c.nombre = 'Electricidad' THEN 'Instalación de luminarias'
    WHEN c.nombre = 'Carpintería' THEN 'Fabricación de muebles'
    WHEN c.nombre = 'Limpieza' THEN 'Limpieza profunda de hogar'
  END,
  CASE 
    WHEN c.nombre = 'Plomería' THEN 'Arreglo de pérdidas y cambio de cañerías'
    WHEN c.nombre = 'Electricidad' THEN 'Instalación de luces LED y artefactos'
    WHEN c.nombre = 'Carpintería' THEN 'Muebles personalizados de calidad'
    WHEN c.nombre = 'Limpieza' THEN 'Limpieza completa incluyendo cocina y baños'
  END,
  FLOOR(1 + (RAND() * 10)),
  CASE 
    WHEN c.nombre = 'Plomería' THEN 3500.00
    WHEN c.nombre = 'Electricidad' THEN 4000.00
    WHEN c.nombre = 'Carpintería' THEN 15000.00
    WHEN c.nombre = 'Limpieza' THEN 2500.00
  END,
  8, 18, 
  CASE 
    WHEN c.nombre = 'Plomería' THEN 2
    WHEN c.nombre = 'Electricidad' THEN 3
    WHEN c.nombre = 'Carpintería' THEN 8
    WHEN c.nombre = 'Limpieza' THEN 4
  END,
  NOW()
FROM proveedores p
JOIN usuarios u ON p.id = u.id
CROSS JOIN categorias c
WHERE (u.usuario = 'juan_perez' AND c.nombre = 'Plomería')
   OR (u.usuario = 'carlos_ruiz' AND c.nombre = 'Electricidad')
   OR (u.usuario = 'luis_martin' AND c.nombre = 'Carpintería')
   OR (u.usuario = 'diego_torres' AND c.nombre = 'Limpieza')
LIMIT 4;

-- Insert Additional Services
INSERT INTO servicios (id, proveedor_id, categoria_id, nombre, descripcion, imagen, precio, hora_inicio, hora_fin, duracion, fecha_creacion) VALUES
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'juan_perez'), (SELECT id FROM categorias WHERE nombre = 'Plomería'), 'Destapación de cañerías', 'Servicio de destapación con máquina profesional', FLOOR(1 + (RAND() * 10)), 4500.00, 8, 20, 2, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'carlos_ruiz'), (SELECT id FROM categorias WHERE nombre = 'Electricidad'), 'Instalación de tomas', 'Instalación de enchufes y tomas eléctricas', FLOOR(1 + (RAND() * 10)), 3200.00, 9, 18, 2, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'carlos_ruiz'), (SELECT id FROM categorias WHERE nombre = 'Electricidad'), 'Revisión de tablero eléctrico', 'Inspección y mantenimiento de tableros', FLOOR(1 + (RAND() * 10)), 5500.00, 8, 17, 3, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'luis_martin'), (SELECT id FROM categorias WHERE nombre = 'Carpintería'), 'Reparación de puertas', 'Ajuste y reparación de puertas de madera', FLOOR(1 + (RAND() * 10)), 3800.00, 10, 18, 4, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'luis_martin'), (SELECT id FROM categorias WHERE nombre = 'Carpintería'), 'Instalación de estanterías', 'Colocación de estantes y repisas personalizadas', FLOOR(1 + (RAND() * 10)), 6500.00, 9, 19, 5, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'diego_torres'), (SELECT id FROM categorias WHERE nombre = 'Limpieza'), 'Limpieza de oficinas', 'Servicio de limpieza empresarial completo', FLOOR(1 + (RAND() * 10)), 8000.00, 7, 15, 6, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'diego_torres'), (SELECT id FROM categorias WHERE nombre = 'Limpieza'), 'Limpieza de vidrios', 'Lavado profesional de ventanas y cristales', FLOOR(1 + (RAND() * 10)), 2200.00, 9, 17, 3, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'juan_perez'), (SELECT id FROM categorias WHERE nombre = 'Jardinería'), 'Mantenimiento de jardín', 'Corte de césped y poda de plantas', FLOOR(1 + (RAND() * 10)), 4200.00, 8, 16, 5, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'carlos_ruiz'), (SELECT id FROM categorias WHERE nombre = 'Pintura'), 'Pintura de interiores', 'Pintura profesional de ambientes', FLOOR(1 + (RAND() * 10)), 12000.00, 9, 18, 8, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'luis_martin'), (SELECT id FROM categorias WHERE nombre = 'Pintura'), 'Pintura de fachadas', 'Pintura exterior de edificios y casas', FLOOR(1 + (RAND() * 10)), 18000.00, 8, 20, 10, NOW());

-- ==========================================
-- CRITICAL UPDATE: Link Barrios to Services
-- ==========================================
-- Guaranteed: EVERY service gets at least 1 random barrio
INSERT INTO barrios_servicios (id, servicio_id, barrio_id)
SELECT 
  UUID(),
  s.id, 
  (SELECT id FROM barrios ORDER BY RAND() LIMIT 1)
FROM servicios s;

-- Optional: Add a second random barrio to 30% of services to vary the data
INSERT INTO barrios_servicios (id, servicio_id, barrio_id)
SELECT 
  UUID(),
  s.id, 
  (SELECT id FROM barrios ORDER BY RAND() LIMIT 1)
FROM servicios s
WHERE RAND() < 0.3
AND NOT EXISTS (
  SELECT 1 FROM barrios_servicios bs2 
  WHERE bs2.servicio_id = s.id 
  GROUP BY bs2.servicio_id 
  HAVING COUNT(*) >= 2
);

-- ==========================================
-- INSERT RESERVATIONS & REVIEWS
-- ==========================================

-- Insert past reservations (completed)
INSERT INTO reservas (id, usuario_id, servicio_id, fecha_reserva, fecha_servicio, hora_servicio, direccion, estado, comentarios_cliente)
SELECT 
  UUID(),
  u.id,
  s.id,
  DATE_FORMAT(DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 60) + 7 DAY), '%Y-%m-%d %H:%i:%s'),
  DATE_FORMAT(DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 60) + 7 DAY), '%Y-%m-%d %H:%i:%s'),
  s.hora_inicio + (FLOOR(RAND() * (FLOOR((s.hora_fin - s.duracion - s.hora_inicio) / s.duracion) + 1)) * s.duracion),
  'Av. Siempre Viva 123',
  'realizado',
  'Servicio de prueba'
FROM usuarios u
CROSS JOIN servicios s
WHERE u.usuario IN ('maria_gomez', 'ana_lopez', 'sofia_garcia', 'laura_vazquez')
ORDER BY RAND()
LIMIT 60;

-- Insert Reviews (3 per service) - MySQL compatible version
INSERT INTO resenas (id, usuario_id, servicio_id, reserva_id, puntuacion, comentarios_cliente, fecha)
SELECT 
  UUID(),
  usuario_id,
  servicio_id,
  id,
  FLOOR(3 + (RAND() * 3)),
  'Excelente trabajo, muy recomendable.',
  DATE_FORMAT(DATE_ADD(fecha_servicio, INTERVAL 1 DAY), '%Y-%m-%dT%H:%i')
FROM (
  SELECT 
    r.*,
    @row_num := IF(@servicio = r.servicio_id, @row_num + 1, 1) as rn,
    @servicio := r.servicio_id
  FROM reservas r
  CROSS JOIN (SELECT @row_num := 0, @servicio := NULL) vars
  WHERE r.estado = 'realizado'
  ORDER BY r.servicio_id, RAND()
) ranked_reservations
WHERE ranked_reservations.rn <= 3;
