CREATE DATABASE IF NOT EXISTS ie_base_conocimiento;
 USE ie_base_conocimiento;
 
CREATE TABLE IF NOT EXISTS tb_datos_personales ( 
    -- Clave Primaria y Metadatos
    id_persona INT PRIMARY KEY AUTO_INCREMENT, 
    identificador_documento VARCHAR(255) NOT NULL,
    fecha_extraccion DATETIME NOT NULL,
    fuente_original VARCHAR(50), 
    
    -- Datos Personales
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100),
    curp CHAR(18),
    rfc CHAR(13),
    fecha_nacimiento DATE,
    nacionalidad VARCHAR(50),
    
    -- Domicilio
    calle VARCHAR(150),
    numero_exterior VARCHAR(20),
    numero_interior VARCHAR(20),
    colonia VARCHAR(100),
    codigo_postal VARCHAR(10),
    municipio VARCHAR(100),
    estado VARCHAR(100),

    -- Restricciones de Integridad
    CONSTRAINT uq_curp UNIQUE (curp),
    CONSTRAINT uq_rfc UNIQUE (rfc)
);