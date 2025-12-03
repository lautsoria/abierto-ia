DROP SCHEMA IF EXISTS ids;
CREATE DATABASE IF NOT EXISTS ids;
USE ids;

-- ==========================================
-- SCHEMA DEFINITION
-- ==========================================

CREATE TABLE IF NOT EXISTS roles (
  id VARCHAR(36) PRIMARY KEY,
  rol VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS usuarios (
  id VARCHAR(36) PRIMARY KEY,
  usuario VARCHAR(25) NOT NULL UNIQUE,
  email VARCHAR(50) NOT NULL UNIQUE,
  contrasena VARCHAR(255) NOT NULL,
  rol_id VARCHAR(36),
  telefono VARCHAR(20),
  fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (rol_id) REFERENCES roles(id)
);

CREATE TABLE IF NOT EXISTS proveedores (
  id VARCHAR(36) PRIMARY KEY,
  descripcion VARCHAR(500),
  FOREIGN KEY (id) REFERENCES usuarios(id) ON DELETE CASCADE
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
  FOREIGN KEY (proveedor_id) REFERENCES proveedores(id) ON DELETE CASCADE,
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
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  FOREIGN KEY (servicio_id) REFERENCES servicios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS resenas (
  id VARCHAR(36) PRIMARY KEY,
  usuario_id VARCHAR(36) NOT NULL,
  servicio_id VARCHAR(36) NOT NULL,
  reserva_id VARCHAR(36) NOT NULL UNIQUE,
  puntuacion INT CHECK (puntuacion BETWEEN 1 AND 5),
  comentarios_cliente TEXT,
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  FOREIGN KEY (servicio_id) REFERENCES servicios(id) ON DELETE CASCADE,
  FOREIGN KEY (reserva_id) REFERENCES reservas(id) ON DELETE CASCADE
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
  FOREIGN KEY (servicio_id) REFERENCES servicios(id) ON DELETE CASCADE,
  FOREIGN KEY (barrio_id) REFERENCES barrios(id) ON DELETE CASCADE
);

-- ==========================================
-- INSERT ROLES
-- ==========================================
INSERT INTO roles (id, rol) VALUES
(UUID(), 'cliente'),
(UUID(), 'proveedor'),
(UUID(), 'admin');

-- ==========================================
-- INSERT ADMIN USER (admin/admin)
-- ==========================================
INSERT INTO usuarios (id, usuario, email, contrasena, rol_id, telefono, fecha_registro) VALUES
(UUID(), 'admin', 'admin@abierto.ia', 'admin', (SELECT id FROM roles WHERE rol = 'admin'), '11-0000-0000', NOW());

-- ==========================================
-- INSERT CLIENTES (8 clientes)
-- ==========================================
INSERT INTO usuarios (id, usuario, email, contrasena, rol_id, telefono, fecha_registro) VALUES
(UUID(), 'maria_gomez', 'maria@gmail.com', 'pass456', (SELECT id FROM roles WHERE rol = 'cliente'), '11-5555-2345', NOW()),
(UUID(), 'ana_lopez', 'ana@yahoo.com', 'pass101', (SELECT id FROM roles WHERE rol = 'cliente'), '11-5555-3456', NOW()),
(UUID(), 'sofia_garcia', 'sofia@outlook.com', 'pass303', (SELECT id FROM roles WHERE rol = 'cliente'), '11-5555-4567', NOW()),
(UUID(), 'laura_vazquez', 'laura@gmail.com', 'pass505', (SELECT id FROM roles WHERE rol = 'cliente'), '11-5555-5678', NOW()),
(UUID(), 'pablo_mendez', 'pablo@gmail.com', 'pass606', (SELECT id FROM roles WHERE rol = 'cliente'), '11-5555-6789', NOW()),
(UUID(), 'lucia_fernandez', 'lucia@hotmail.com', 'pass707', (SELECT id FROM roles WHERE rol = 'cliente'), '11-5555-7890', NOW()),
(UUID(), 'martin_silva', 'martin@gmail.com', 'pass808', (SELECT id FROM roles WHERE rol = 'cliente'), '11-5555-8901', NOW()),
(UUID(), 'camila_rojas', 'camila@outlook.com', 'pass909', (SELECT id FROM roles WHERE rol = 'cliente'), '11-5555-9012', NOW());

-- ==========================================
-- INSERT PROVEEDORES (8 proveedores)
-- ==========================================
INSERT INTO usuarios (id, usuario, email, contrasena, rol_id, telefono, fecha_registro) VALUES
(UUID(), 'juan_perez', 'juan@gmail.com', 'pass123', (SELECT id FROM roles WHERE rol = 'proveedor'), '11-5555-1234', NOW()),
(UUID(), 'carlos_ruiz', 'carlos@hotmail.com', 'pass789', (SELECT id FROM roles WHERE rol = 'proveedor'), '11-5555-5678', NOW()),
(UUID(), 'luis_martin', 'luis@gmail.com', 'pass202', (SELECT id FROM roles WHERE rol = 'proveedor'), '11-5555-9012', NOW()),
(UUID(), 'diego_torres', 'diego@gmail.com', 'pass404', (SELECT id FROM roles WHERE rol = 'proveedor'), '11-5555-3456', NOW()),
(UUID(), 'roberto_sanchez', 'roberto@gmail.com', 'pass111', (SELECT id FROM roles WHERE rol = 'proveedor'), '11-5555-1111', NOW()),
(UUID(), 'fernando_diaz', 'fernando@hotmail.com', 'pass222', (SELECT id FROM roles WHERE rol = 'proveedor'), '11-5555-2222', NOW()),
(UUID(), 'alejandro_castro', 'alejandro@gmail.com', 'pass333', (SELECT id FROM roles WHERE rol = 'proveedor'), '11-5555-3333', NOW()),
(UUID(), 'gabriel_moreno', 'gabriel@outlook.com', 'pass444', (SELECT id FROM roles WHERE rol = 'proveedor'), '11-5555-4444', NOW());

-- ==========================================
-- INSERT CATEGORIES
-- ==========================================
INSERT INTO categorias (id, nombre, descripcion, fecha_creacion) VALUES
(UUID(), 'Plomería', 'Servicios de instalación y reparación de plomería', NOW()),
(UUID(), 'Electricidad', 'Instalaciones eléctricas y reparaciones', NOW()),
(UUID(), 'Carpintería', 'Trabajos en madera y muebles', NOW()),
(UUID(), 'Limpieza', 'Servicios de limpieza para hogares y oficinas', NOW()),
(UUID(), 'Jardinería', 'Mantenimiento de jardines y áreas verdes', NOW()),
(UUID(), 'Pintura', 'Pintura interior y exterior', NOW()),
(UUID(), 'Cerrajería', 'Apertura de puertas y cambio de cerraduras', NOW()),
(UUID(), 'Mudanzas', 'Servicio de mudanzas y fletes', NOW());

-- ==========================================
-- INSERT BARRIOS (48 barrios de CABA)
-- ==========================================
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

-- ==========================================
-- INSERT PROVEEDORES TABLE
-- ==========================================
INSERT INTO proveedores (id, descripcion) VALUES
((SELECT id FROM usuarios WHERE usuario = 'juan_perez'), 'Plomero profesional con 10 años de experiencia. Trabajo garantizado.'),
((SELECT id FROM usuarios WHERE usuario = 'carlos_ruiz'), 'Electricista matriculado. Instalaciones residenciales y comerciales.'),
((SELECT id FROM usuarios WHERE usuario = 'luis_martin'), 'Carpintero especializado en muebles a medida y restauración.'),
((SELECT id FROM usuarios WHERE usuario = 'diego_torres'), 'Servicio de limpieza profesional. Personal capacitado.'),
((SELECT id FROM usuarios WHERE usuario = 'roberto_sanchez'), 'Jardinero con experiencia en diseño de espacios verdes.'),
((SELECT id FROM usuarios WHERE usuario = 'fernando_diaz'), 'Pintor profesional. Interiores y exteriores.'),
((SELECT id FROM usuarios WHERE usuario = 'alejandro_castro'), 'Cerrajero 24hs. Urgencias y seguridad.'),
((SELECT id FROM usuarios WHERE usuario = 'gabriel_moreno'), 'Mudanzas y fletes. Servicio cuidadoso y puntual.');

-- ==========================================
-- INSERT SERVICES (32 servicios - 4 por proveedor)
-- ==========================================

-- Servicios de Juan Pérez (Plomería)
INSERT INTO servicios (id, proveedor_id, categoria_id, nombre, descripcion, imagen, precio, hora_inicio, hora_fin, duracion, fecha_creacion) VALUES
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'juan_perez'), (SELECT id FROM categorias WHERE nombre = 'Plomería'), 'Reparación de cañerías', 'Arreglo de pérdidas y cambio de cañerías. Incluye materiales básicos.', 1, 3500.00, 8, 18, 2, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'juan_perez'), (SELECT id FROM categorias WHERE nombre = 'Plomería'), 'Destapación de cañerías', 'Servicio de destapación con máquina profesional.', 2, 4500.00, 8, 20, 2, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'juan_perez'), (SELECT id FROM categorias WHERE nombre = 'Plomería'), 'Instalación de termotanque', 'Instalación completa de termotanques eléctricos o a gas.', 3, 8000.00, 9, 17, 3, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'juan_perez'), (SELECT id FROM categorias WHERE nombre = 'Plomería'), 'Reparación de griferías', 'Cambio y reparación de canillas y griferías.', 4, 2500.00, 8, 18, 1, NOW());

-- Servicios de Carlos Ruiz (Electricidad)
INSERT INTO servicios (id, proveedor_id, categoria_id, nombre, descripcion, imagen, precio, hora_inicio, hora_fin, duracion, fecha_creacion) VALUES
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'carlos_ruiz'), (SELECT id FROM categorias WHERE nombre = 'Electricidad'), 'Instalación de luminarias', 'Instalación de luces LED y artefactos de iluminación.', 5, 4000.00, 8, 18, 3, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'carlos_ruiz'), (SELECT id FROM categorias WHERE nombre = 'Electricidad'), 'Instalación de tomas', 'Instalación de enchufes y tomas eléctricas.', 6, 3200.00, 9, 18, 2, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'carlos_ruiz'), (SELECT id FROM categorias WHERE nombre = 'Electricidad'), 'Revisión de tablero eléctrico', 'Inspección y mantenimiento de tableros.', 7, 5500.00, 8, 17, 3, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'carlos_ruiz'), (SELECT id FROM categorias WHERE nombre = 'Electricidad'), 'Instalación de aire acondicionado', 'Instalación eléctrica para splits.', 8, 12000.00, 9, 19, 4, NOW());

-- Servicios de Luis Martín (Carpintería)
INSERT INTO servicios (id, proveedor_id, categoria_id, nombre, descripcion, imagen, precio, hora_inicio, hora_fin, duracion, fecha_creacion) VALUES
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'luis_martin'), (SELECT id FROM categorias WHERE nombre = 'Carpintería'), 'Fabricación de muebles', 'Muebles personalizados de calidad premium.', 9, 15000.00, 8, 18, 8, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'luis_martin'), (SELECT id FROM categorias WHERE nombre = 'Carpintería'), 'Reparación de puertas', 'Ajuste y reparación de puertas de madera.', 10, 3800.00, 10, 18, 4, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'luis_martin'), (SELECT id FROM categorias WHERE nombre = 'Carpintería'), 'Instalación de estanterías', 'Colocación de estantes y repisas personalizadas.', 1, 6500.00, 9, 19, 5, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'luis_martin'), (SELECT id FROM categorias WHERE nombre = 'Carpintería'), 'Restauración de muebles', 'Restauración y pulido de muebles antiguos.', 2, 9000.00, 9, 17, 6, NOW());

-- Servicios de Diego Torres (Limpieza)
INSERT INTO servicios (id, proveedor_id, categoria_id, nombre, descripcion, imagen, precio, hora_inicio, hora_fin, duracion, fecha_creacion) VALUES
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'diego_torres'), (SELECT id FROM categorias WHERE nombre = 'Limpieza'), 'Limpieza profunda de hogar', 'Limpieza completa incluyendo cocina y baños.', 3, 2500.00, 8, 18, 4, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'diego_torres'), (SELECT id FROM categorias WHERE nombre = 'Limpieza'), 'Limpieza de oficinas', 'Servicio de limpieza empresarial completo.', 4, 8000.00, 7, 15, 6, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'diego_torres'), (SELECT id FROM categorias WHERE nombre = 'Limpieza'), 'Limpieza de vidrios', 'Lavado profesional de ventanas y cristales.', 5, 2200.00, 9, 17, 3, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'diego_torres'), (SELECT id FROM categorias WHERE nombre = 'Limpieza'), 'Limpieza post-obra', 'Limpieza especializada después de refacciones.', 6, 5500.00, 8, 18, 5, NOW());

-- Servicios de Roberto Sánchez (Jardinería)
INSERT INTO servicios (id, proveedor_id, categoria_id, nombre, descripcion, imagen, precio, hora_inicio, hora_fin, duracion, fecha_creacion) VALUES
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'roberto_sanchez'), (SELECT id FROM categorias WHERE nombre = 'Jardinería'), 'Mantenimiento de jardín', 'Corte de césped y poda de plantas.', 7, 4200.00, 8, 16, 3, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'roberto_sanchez'), (SELECT id FROM categorias WHERE nombre = 'Jardinería'), 'Diseño de jardines', 'Diseño y planificación de espacios verdes.', 8, 15000.00, 9, 18, 6, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'roberto_sanchez'), (SELECT id FROM categorias WHERE nombre = 'Jardinería'), 'Instalación de riego', 'Sistema de riego automático.', 9, 25000.00, 8, 17, 8, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'roberto_sanchez'), (SELECT id FROM categorias WHERE nombre = 'Jardinería'), 'Poda de árboles', 'Poda y mantenimiento de árboles grandes.', 10, 6000.00, 7, 15, 4, NOW());

-- Servicios de Fernando Díaz (Pintura)
INSERT INTO servicios (id, proveedor_id, categoria_id, nombre, descripcion, imagen, precio, hora_inicio, hora_fin, duracion, fecha_creacion) VALUES
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'fernando_diaz'), (SELECT id FROM categorias WHERE nombre = 'Pintura'), 'Pintura de interiores', 'Pintura profesional de ambientes. Incluye materiales.', 1, 12000.00, 9, 18, 8, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'fernando_diaz'), (SELECT id FROM categorias WHERE nombre = 'Pintura'), 'Pintura de fachadas', 'Pintura exterior de edificios y casas.', 2, 18000.00, 8, 20, 10, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'fernando_diaz'), (SELECT id FROM categorias WHERE nombre = 'Pintura'), 'Empapelado', 'Colocación de papel tapiz.', 3, 8000.00, 9, 17, 5, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'fernando_diaz'), (SELECT id FROM categorias WHERE nombre = 'Pintura'), 'Pintura decorativa', 'Técnicas especiales: estucado, esponjeado, etc.', 4, 15000.00, 10, 18, 6, NOW());

-- Servicios de Alejandro Castro (Cerrajería)
INSERT INTO servicios (id, proveedor_id, categoria_id, nombre, descripcion, imagen, precio, hora_inicio, hora_fin, duracion, fecha_creacion) VALUES
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'alejandro_castro'), (SELECT id FROM categorias WHERE nombre = 'Cerrajería'), 'Apertura de puertas', 'Servicio de apertura de emergencia 24hs.', 5, 5000.00, 6, 22, 1, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'alejandro_castro'), (SELECT id FROM categorias WHERE nombre = 'Cerrajería'), 'Cambio de cerraduras', 'Instalación de cerraduras de seguridad.', 6, 8500.00, 8, 20, 2, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'alejandro_castro'), (SELECT id FROM categorias WHERE nombre = 'Cerrajería'), 'Copia de llaves', 'Duplicado de llaves comunes y de seguridad.', 7, 1500.00, 9, 18, 1, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'alejandro_castro'), (SELECT id FROM categorias WHERE nombre = 'Cerrajería'), 'Instalación de cerrojos', 'Colocación de cerrojos y pasadores.', 8, 4000.00, 8, 19, 2, NOW());

-- Servicios de Gabriel Moreno (Mudanzas)
INSERT INTO servicios (id, proveedor_id, categoria_id, nombre, descripcion, imagen, precio, hora_inicio, hora_fin, duracion, fecha_creacion) VALUES
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'gabriel_moreno'), (SELECT id FROM categorias WHERE nombre = 'Mudanzas'), 'Mudanza local', 'Mudanza dentro de CABA. Incluye embalaje básico.', 9, 25000.00, 7, 19, 6, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'gabriel_moreno'), (SELECT id FROM categorias WHERE nombre = 'Mudanzas'), 'Flete pequeño', 'Transporte de objetos pequeños y medianos.', 10, 8000.00, 8, 20, 2, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'gabriel_moreno'), (SELECT id FROM categorias WHERE nombre = 'Mudanzas'), 'Mudanza con embalaje', 'Servicio completo con embalaje profesional.', 1, 45000.00, 6, 18, 10, NOW()),
(UUID(), (SELECT id FROM usuarios WHERE usuario = 'gabriel_moreno'), (SELECT id FROM categorias WHERE nombre = 'Mudanzas'), 'Guardamuebles', 'Almacenamiento temporal de muebles.', 2, 15000.00, 8, 17, 3, NOW());

-- ==========================================
-- LINK BARRIOS TO SERVICES (max 3 por servicio)
-- ==========================================

-- Primera ronda: Todos los servicios reciben 1 barrio aleatorio
INSERT INTO barrios_servicios (id, servicio_id, barrio_id)
SELECT 
  UUID(),
  s.id, 
  (SELECT id FROM barrios ORDER BY RAND() LIMIT 1)
FROM servicios s;

-- Segunda ronda: 70% de los servicios reciben un segundo barrio
INSERT IGNORE INTO barrios_servicios (id, servicio_id, barrio_id)
SELECT 
  UUID(),
  s.id, 
  b.id
FROM servicios s
CROSS JOIN (SELECT id FROM barrios ORDER BY RAND() LIMIT 1) b
WHERE RAND() < 0.7
AND NOT EXISTS (
  SELECT 1 FROM barrios_servicios bs WHERE bs.servicio_id = s.id AND bs.barrio_id = b.id
);

-- Tercera ronda: 40% de los servicios reciben un tercer barrio
INSERT IGNORE INTO barrios_servicios (id, servicio_id, barrio_id)
SELECT 
  UUID(),
  s.id, 
  b.id
FROM servicios s
CROSS JOIN (SELECT id FROM barrios ORDER BY RAND() LIMIT 1) b
WHERE RAND() < 0.4
AND (SELECT COUNT(*) FROM barrios_servicios bs WHERE bs.servicio_id = s.id) < 3
AND NOT EXISTS (
  SELECT 1 FROM barrios_servicios bs WHERE bs.servicio_id = s.id AND bs.barrio_id = b.id
);

-- ==========================================
-- PAST RESERVATIONS (realizadas y canceladas)
-- Fechas en el pasado: hace 7-90 días
-- ==========================================

-- Reservas realizadas (completadas exitosamente)
INSERT INTO reservas (id, usuario_id, servicio_id, fecha_reserva, fecha_servicio, hora_servicio, direccion, estado, comentarios_cliente)
SELECT 
  UUID(),
  u.id,
  s.id,
  DATE_SUB(NOW(), INTERVAL (FLOOR(RAND() * 83) + 8) DAY),
  DATE_SUB(NOW(), INTERVAL (FLOOR(RAND() * 83) + 8) DAY),
  s.hora_inicio + FLOOR(RAND() * (s.hora_fin - s.hora_inicio - s.duracion + 1)),
  CONCAT('Av. ', 
    ELT(FLOOR(1 + RAND() * 10), 'Corrientes', 'Santa Fe', 'Rivadavia', 'Cabildo', 'Libertador', 'Belgrano', 'Callao', 'Córdoba', 'Las Heras', 'Pueyrredón'),
    ' ', FLOOR(100 + RAND() * 9900)
  ),
  'realizado',
  ELT(FLOOR(1 + RAND() * 5), 
    'Excelente trabajo, muy conforme.',
    'Muy profesional y puntual.',
    'Cumplió con lo acordado.',
    'Buen servicio, lo recomiendo.',
    'Todo perfecto, gracias.')
FROM (SELECT id FROM usuarios WHERE usuario IN ('maria_gomez', 'ana_lopez', 'sofia_garcia', 'laura_vazquez', 'pablo_mendez', 'lucia_fernandez', 'martin_silva', 'camila_rojas') ORDER BY RAND() LIMIT 8) u
CROSS JOIN servicios s
ORDER BY RAND()
LIMIT 80;

-- Reservas canceladas (en el pasado)
INSERT INTO reservas (id, usuario_id, servicio_id, fecha_reserva, fecha_servicio, hora_servicio, direccion, estado, comentarios_cliente)
SELECT 
  UUID(),
  u.id,
  s.id,
  DATE_SUB(NOW(), INTERVAL (FLOOR(RAND() * 60) + 15) DAY),
  DATE_SUB(NOW(), INTERVAL (FLOOR(RAND() * 60) + 15) DAY),
  s.hora_inicio + FLOOR(RAND() * (s.hora_fin - s.hora_inicio - s.duracion + 1)),
  CONCAT('Calle ', 
    ELT(FLOOR(1 + RAND() * 8), 'Lavalle', 'Tucumán', 'Sarmiento', 'Perón', 'Alem', 'Maipú', 'Florida', 'Reconquista'),
    ' ', FLOOR(100 + RAND() * 2000)
  ),
  'cancelado',
  ELT(FLOOR(1 + RAND() * 4), 
    'Surgió un imprevisto.',
    'Tuve que reprogramar.',
    'Ya no necesito el servicio.',
    'Encontré otra opción.')
FROM (SELECT id FROM usuarios WHERE usuario IN ('maria_gomez', 'ana_lopez', 'sofia_garcia', 'laura_vazquez') ORDER BY RAND() LIMIT 4) u
CROSS JOIN servicios s
ORDER BY RAND()
LIMIT 15;

-- ==========================================
-- FUTURE RESERVATIONS (pendientes)
-- Fechas en el futuro: próximos 1-30 días
-- ==========================================
INSERT INTO reservas (id, usuario_id, servicio_id, fecha_reserva, fecha_servicio, hora_servicio, direccion, estado, comentarios_cliente)
SELECT 
  UUID(),
  u.id,
  s.id,
  NOW(),
  DATE_ADD(NOW(), INTERVAL (FLOOR(RAND() * 29) + 1) DAY),
  s.hora_inicio + FLOOR(RAND() * (s.hora_fin - s.hora_inicio - s.duracion + 1)),
  CONCAT('Av. ', 
    ELT(FLOOR(1 + RAND() * 10), 'Corrientes', 'Santa Fe', 'Rivadavia', 'Cabildo', 'Libertador', 'Belgrano', 'Callao', 'Córdoba', 'Las Heras', 'Pueyrredón'),
    ' ', FLOOR(100 + RAND() * 9900)
  ),
  'pendiente',
  ELT(FLOOR(1 + RAND() * 5), 
    'Por favor llegar a horario.',
    'Llamar al llegar.',
    'Portero eléctrico: 2A',
    'Timbre roto, golpear la puerta.',
    '')
FROM (SELECT id FROM usuarios WHERE usuario IN ('pablo_mendez', 'lucia_fernandez', 'martin_silva', 'camila_rojas', 'maria_gomez', 'ana_lopez') ORDER BY RAND() LIMIT 6) u
CROSS JOIN servicios s
ORDER BY RAND()
LIMIT 25;

-- ==========================================
-- INSERT REVIEWS (solo para reservas realizadas)
-- ==========================================
INSERT INTO resenas (id, usuario_id, servicio_id, reserva_id, puntuacion, comentarios_cliente, fecha)
SELECT 
  UUID(),
  r.usuario_id,
  r.servicio_id,
  r.id,
  FLOOR(3 + RAND() * 3),
  ELT(FLOOR(1 + RAND() * 15),
    'Excelente trabajo, muy recomendable.',
    'Muy profesional y amable.',
    'Cumplió perfectamente con el trabajo.',
    'Llegó puntual y trabajó muy bien.',
    'Muy conforme con el resultado.',
    'Lo volvería a contratar sin dudarlo.',
    'Buen precio por un excelente servicio.',
    'Súper recomendado, muy prolijo.',
    'Trabajo impecable, gracias!',
    'Muy buena atención y calidad.',
    'Solucionó el problema rápidamente.',
    'Profesional de primera.',
    'Muy satisfecho con el servicio.',
    'Excelente relación precio-calidad.',
    'Todo perfecto, muy agradecido.'
  ),
  DATE_ADD(r.fecha_servicio, INTERVAL (FLOOR(RAND() * 5) + 1) DAY)
FROM reservas r
WHERE r.estado = 'realizado'
AND NOT EXISTS (SELECT 1 FROM resenas res WHERE res.reserva_id = r.id)
ORDER BY RAND()
LIMIT 60;
