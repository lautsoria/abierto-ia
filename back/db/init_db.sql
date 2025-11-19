CREATE DATABASE IF NOT EXISTS ids;
use ids;

CREATE TABLE IF NOT EXISTS usuarios (
  id UUID PRIMARY KEY,
  usuario VARCHAR(25) NOT NULL UNIQUE,
  email VARCHAR(50) NOT NULL UNIQUE,
  contrasena VARCHAR(12) NOT NULL,
  fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS proveedores (
  id UUID PRIMARY KEY,
  usuario_id UUID NULL,
  descripcion VARCHAR(500),
  telefono VARCHAR(20),
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS categorias (
  id UUID PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL UNIQUE,
  descripcion TEXT,
  fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS servicios (
  id UUID PRIMARY KEY,
  proveedor_id UUID NOT NULL,
  categoria_id UUID NOT NULL,
  nombre VARCHAR(255) NOT NULL,
  descripcion TEXT,
  precio DECIMAL(10,2) NOT NULL,
  fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (proveedor_id) REFERENCES proveedores(id),
  FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE IF NOT EXISTS reservas (
  id UUID PRIMARY KEY,
  usuario_id UUID NOT NULL,
  servicio_id UUID NOT NULL,
  fecha_reserva DATETIME DEFAULT CURRENT_TIMESTAMP,
  fecha_servicio DATETIME NOT NULL,
  estado ENUM('pendiente', 'realizado', 'cancelado') DEFAULT 'pendiente',
  comentarios_cliente TEXT,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
  FOREIGN KEY (servicio_id) REFERENCES servicios(id)
);

CREATE TABLE IF NOT EXISTS resenas (
  id UUID PRIMARY KEY,
  usuario_id UUID NOT NULL,
  servicio_id UUID NOT NULL,
  puntuacion INT CHECK (puntuacion BETWEEN 1 AND 5),
  comentarios_cliente TEXT,
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
  FOREIGN KEY (servicio_id) REFERENCES servicios(id)
);

CREATE TABLE IF NOT EXISTS barrios (
  id UUID PRIMARY KEY,
  nombre VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS barrios_usuarios (
  id UUID PRIMARY KEY,
  usuario_id UUID NOT NULL,
  barrio_id UUID NOT NULL,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
  FOREIGN KEY (barrio_id) REFERENCES barrios(id)
);


-- Insert dummy usuarios
INSERT INTO usuarios (id, usuario, email, contrasena, fecha_registro) VALUES
(UUID(), 'juan_perez', 'juan@gmail.com', 'pass123', NOW()),
(UUID(), 'maria_gomez', 'maria@gmail.com', 'pass456', NOW()),
(UUID(), 'carlos_ruiz', 'carlos@hotmail.com', 'pass789', NOW()),
(UUID(), 'ana_lopez', 'ana@yahoo.com', 'pass101', NOW()),
(UUID(), 'luis_martin', 'luis@gmail.com', 'pass202', NOW()),
(UUID(), 'sofia_garcia', 'sofia@outlook.com', 'pass303', NOW()),
(UUID(), 'diego_torres', 'diego@gmail.com', 'pass404', NOW()),
(UUID(), 'laura_vazquez', 'laura@gmail.com', 'pass505', NOW());

-- Insert dummy categorias
INSERT INTO categorias (id, nombre, descripcion, fecha_creacion) VALUES
(UUID(), 'Plomería', 'Servicios de instalación y reparación de plomería', NOW()),
(UUID(), 'Electricidad', 'Instalaciones eléctricas y reparaciones', NOW()),
(UUID(), 'Carpintería', 'Trabajos en madera y muebles', NOW()),
(UUID(), 'Limpieza', 'Servicios de limpieza para hogares y oficinas', NOW()),
(UUID(), 'Jardinería', 'Mantenimiento de jardines y áreas verdes', NOW()),
(UUID(), 'Pintura', 'Pintura interior y exterior', NOW());

-- Insert barrios CABA
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

-- Insert barrios_usuarios for providers
INSERT INTO barrios_usuarios (id, usuario_id, barrio_id)
SELECT UUID(), u.id, b.id
FROM usuarios u
JOIN barrios b ON 
    (u.usuario = 'juan_perez' AND b.nombre = 'Palermo') OR
    (u.usuario = 'carlos_ruiz' AND b.nombre = 'Belgrano') OR
    (u.usuario = 'luis_martin' AND b.nombre = 'Caballito') OR
    (u.usuario = 'diego_torres' AND b.nombre = 'Recoleta');

-- Insert dummy proveedores (using existing user IDs)
INSERT INTO proveedores (id, usuario_id, descripcion, telefono) 
SELECT 
  UUID(),
  id,
  CASE 
    WHEN usuario = 'juan_perez' THEN 'Plomero profesional con 10 años de experiencia'
    WHEN usuario = 'carlos_ruiz' THEN 'Electricista certificado, trabajos garantizados'
    WHEN usuario = 'luis_martin' THEN 'Carpintero especializado en muebles a medida'
    WHEN usuario = 'diego_torres' THEN 'Servicio de limpieza profesional'
  END,
  CASE 
    WHEN usuario = 'juan_perez' THEN '11-5555-1234'
    WHEN usuario = 'carlos_ruiz' THEN '11-5555-5678'
    WHEN usuario = 'luis_martin' THEN '11-5555-9012'
    WHEN usuario = 'diego_torres' THEN '11-5555-3456'
  END
FROM usuarios 
WHERE usuario IN ('juan_perez', 'carlos_ruiz', 'luis_martin', 'diego_torres');

-- Insert dummy servicios
INSERT INTO servicios (id, proveedor_id, categoria_id, nombre, descripcion, precio, fecha_creacion)
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
  CASE 
    WHEN c.nombre = 'Plomería' THEN 3500.00
    WHEN c.nombre = 'Electricidad' THEN 4000.00
    WHEN c.nombre = 'Carpintería' THEN 15000.00
    WHEN c.nombre = 'Limpieza' THEN 2500.00
  END,
  NOW()
FROM proveedores p
CROSS JOIN categorias c
WHERE (p.usuario_id = (SELECT id FROM usuarios WHERE usuario = 'juan_perez') AND c.nombre = 'Plomería')
   OR (p.usuario_id = (SELECT id FROM usuarios WHERE usuario = 'carlos_ruiz') AND c.nombre = 'Electricidad')
   OR (p.usuario_id = (SELECT id FROM usuarios WHERE usuario = 'luis_martin') AND c.nombre = 'Carpintería')
   OR (p.usuario_id = (SELECT id FROM usuarios WHERE usuario = 'diego_torres') AND c.nombre = 'Limpieza')
LIMIT 4;

-- Insert additional services
INSERT INTO servicios (id, proveedor_id, categoria_id, nombre, descripcion, precio, fecha_creacion)
SELECT 
  UUID(),
  (SELECT id FROM proveedores WHERE usuario_id = (SELECT id FROM usuarios WHERE usuario = 'juan_perez')),
  (SELECT id FROM categorias WHERE nombre = 'Plomería'),
  'Instalación de grifería',
  'Instalación y cambio de canillas y grifos',
  2800.00,
  NOW();

-- Insert 10 more varied services
INSERT INTO servicios (id, proveedor_id, categoria_id, nombre, descripcion, precio, fecha_creacion) VALUES
(UUID(), 
 (SELECT id FROM proveedores WHERE usuario_id = (SELECT id FROM usuarios WHERE usuario = 'juan_perez')),
 (SELECT id FROM categorias WHERE nombre = 'Plomería'),
 'Destapación de cañerías', 'Servicio de destapación con máquina profesional', 4500.00, NOW()),

(UUID(), 
 (SELECT id FROM proveedores WHERE usuario_id = (SELECT id FROM usuarios WHERE usuario = 'carlos_ruiz')),
 (SELECT id FROM categorias WHERE nombre = 'Electricidad'),
 'Instalación de tomas', 'Instalación de enchufes y tomas eléctricas', 3200.00, NOW()),

(UUID(), 
 (SELECT id FROM proveedores WHERE usuario_id = (SELECT id FROM usuarios WHERE usuario = 'carlos_ruiz')),
 (SELECT id FROM categorias WHERE nombre = 'Electricidad'),
 'Revisión de tablero eléctrico', 'Inspección y mantenimiento de tableros', 5500.00, NOW()),

(UUID(), 
 (SELECT id FROM proveedores WHERE usuario_id = (SELECT id FROM usuarios WHERE usuario = 'luis_martin')),
 (SELECT id FROM categorias WHERE nombre = 'Carpintería'),
 'Reparación de puertas', 'Ajuste y reparación de puertas de madera', 3800.00, NOW()),

(UUID(), 
 (SELECT id FROM proveedores WHERE usuario_id = (SELECT id FROM usuarios WHERE usuario = 'luis_martin')),
 (SELECT id FROM categorias WHERE nombre = 'Carpintería'),
 'Instalación de estanterías', 'Colocación de estantes y repisas personalizadas', 6500.00, NOW()),

(UUID(), 
 (SELECT id FROM proveedores WHERE usuario_id = (SELECT id FROM usuarios WHERE usuario = 'diego_torres')),
 (SELECT id FROM categorias WHERE nombre = 'Limpieza'),
 'Limpieza de oficinas', 'Servicio de limpieza empresarial completo', 8000.00, NOW()),

(UUID(), 
 (SELECT id FROM proveedores WHERE usuario_id = (SELECT id FROM usuarios WHERE usuario = 'diego_torres')),
 (SELECT id FROM categorias WHERE nombre = 'Limpieza'),
 'Limpieza de vidrios', 'Lavado profesional de ventanas y cristales', 2200.00, NOW()),

(UUID(), 
 (SELECT id FROM proveedores WHERE usuario_id = (SELECT id FROM usuarios WHERE usuario = 'juan_perez')),
 (SELECT id FROM categorias WHERE nombre = 'Jardinería'),
 'Mantenimiento de jardín', 'Corte de césped y poda de plantas', 4200.00, NOW()),

(UUID(), 
 (SELECT id FROM proveedores WHERE usuario_id = (SELECT id FROM usuarios WHERE usuario = 'carlos_ruiz')),
 (SELECT id FROM categorias WHERE nombre = 'Pintura'),
 'Pintura de interiores', 'Pintura profesional de ambientes', 12000.00, NOW()),

(UUID(), 
 (SELECT id FROM proveedores WHERE usuario_id = (SELECT id FROM usuarios WHERE usuario = 'luis_martin')),
 (SELECT id FROM categorias WHERE nombre = 'Pintura'),
 'Pintura de fachadas', 'Pintura exterior de edificios y casas', 18000.00, NOW());

-- Insert dummy reservas
INSERT INTO reservas (id, usuario_id, servicio_id, fecha_reserva, fecha_servicio, estado, comentarios_cliente)
SELECT 
  UUID(),
  u.id,
  s.id,
  DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 30) DAY),
  DATE_ADD(NOW(), INTERVAL FLOOR(RAND() * 14) DAY),
  CASE FLOOR(RAND() * 3)
    WHEN 0 THEN 'pendiente'
    WHEN 1 THEN 'realizado'
    ELSE 'cancelado'
  END,
  CASE FLOOR(RAND() * 3)
    WHEN 0 THEN 'Servicio urgente, por favor confirmar'
    WHEN 1 THEN 'Excelente servicio, muy recomendable'
    ELSE NULL
  END
FROM usuarios u
CROSS JOIN servicios s
WHERE u.usuario IN ('maria_gomez', 'ana_lopez', 'sofia_garcia', 'laura_vazquez')
LIMIT 10;

-- Insert dummy reseñas (only for completed reservas)
-- INSERT INTO resenas (id, usuario_id, servicio_id, puntuacion, comentarios_cliente, fecha)
-- SELECT 
--   UUID(),
--   r.usuario_id,
--   r.servicio_id,
--   FLOOR(3 + (RAND() * 3)),
--   CASE FLOOR(RAND() * 5)
--     WHEN 0 THEN 'Excelente trabajo, muy profesional'
--     WHEN 1 THEN 'Buen servicio pero llegó tarde'
--     WHEN 2 THEN 'Muy satisfecho con el resultado'
--     WHEN 3 THEN 'Cumplió con lo prometido'
--     ELSE 'Recomendable, volvería a contratar'
--   END,
--   DATE_ADD(r.fecha_servicio, INTERVAL 1 DAY)
-- FROM reservas r
-- WHERE r.estado = 'realizado'
-- LIMIT 6;

-- Insert reseñas for ALL services (multiple reviews per service)
INSERT INTO resenas (id, usuario_id, servicio_id, puntuacion, comentarios_cliente, fecha)
SELECT 
  UUID(),
  u.id,
  s.id,
  CASE FLOOR(RAND() * 10)
    WHEN 0 THEN 3
    WHEN 1 THEN 3
    WHEN 2 THEN 4
    WHEN 3 THEN 4
    WHEN 4 THEN 4
    WHEN 5 THEN 4
    WHEN 6 THEN 5
    WHEN 7 THEN 5
    WHEN 8 THEN 5
    ELSE 5
  END,
  CASE FLOOR(RAND() * 15)
    WHEN 0 THEN 'Excelente servicio, muy profesional y puntual'
    WHEN 1 THEN 'Muy satisfecho con el trabajo realizado'
    WHEN 2 THEN 'Recomendable al 100%, volvería a contratar'
    WHEN 3 THEN 'Buen trabajo, aunque llegó un poco tarde'
    WHEN 4 THEN 'Cumplió con todas mis expectativas'
    WHEN 5 THEN 'Profesional y eficiente, excelente atención'
    WHEN 6 THEN 'Trabajo de calidad, muy conforme'
    WHEN 7 THEN 'Rápido y efectivo, lo recomiendo'
    WHEN 8 THEN 'Excelente relación calidad-precio'
    WHEN 9 THEN 'Superó mis expectativas, muy buen servicio'
    WHEN 10 THEN 'Profesional serio y responsable'
    WHEN 11 THEN 'Muy contento con el resultado final'
    WHEN 12 THEN 'Buen servicio pero podría mejorar la comunicación'
    WHEN 13 THEN 'Trabajo impecable, totalmente recomendable'
    ELSE 'Servicio correcto, sin sorpresas'
  END,
  DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 60) DAY)
FROM servicios s
CROSS JOIN usuarios u
WHERE u.usuario IN ('maria_gomez', 'ana_lopez', 'sofia_garcia', 'laura_vazquez')
  AND RAND() < 0.6
ORDER BY RAND()
LIMIT 40;

