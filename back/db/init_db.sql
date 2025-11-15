CREATE DATABASE IF NOT EXISTS IDS;
use IDS;

CREATE TABLE IF NOT EXISTS usuarios (
  id UUID PRIMARY KEY,
  usuario VARCHAR(25) NOT NULL UNIQUE,
  email VARCHAR(50) NOT NULL UNIQUE,
  contrasena VARCHAR(12) NOT NULL,
  fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS proveedores (
  id UUID PRIMARY KEY,
  usuario_id UUID NOT NULL,
  descripcion VARCHAR(500),
  ubicacion VARCHAR(255),
  telefono VARCHAR(20),
  calificacion_promedio FLOAT DEFAULT 0,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);