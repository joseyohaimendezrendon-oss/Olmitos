-- Ejecuta este archivo en HeidiSQL o phpMyAdmin de Laragon

CREATE DATABASE IF NOT EXISTS aseguradora;
USE aseguradora;

CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellidos VARCHAR(100),
    fecha_nacimiento DATE,
    genero VARCHAR(20),
    curp VARCHAR(18),
    telefono VARCHAR(10),
    correo VARCHAR(100),
    ocupacion VARCHAR(100),
    ingreso_mensual DECIMAL(10,2)
);

CREATE TABLE polizas (
    id_poliza INT AUTO_INCREMENT PRIMARY KEY,
    numero_poliza INT,
    fecha_inicio DATE,
    fecha_fin DATE,
    prima_mensual DECIMAL(10,2),
    suma_asegurada DECIMAL(12,2),
    tipo_poliza VARCHAR(50),
    estatus VARCHAR(20),
    cliente_id INT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id_cliente)
);

CREATE TABLE beneficiarios (
    id_beneficiario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellidos VARCHAR(100),
    fecha_nacimiento DATE,
    parentesco VARCHAR(50),
    porcentaje_asignado DECIMAL(5,2),
    poliza_id INT,
    FOREIGN KEY (poliza_id) REFERENCES polizas(id_poliza)
);

CREATE TABLE pagos (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    fecha_pago DATE,
    monto_pagado DECIMAL(10,2),
    metodo_pago VARCHAR(50),
    referencia VARCHAR(100),
    poliza_id INT,
    FOREIGN KEY (poliza_id) REFERENCES polizas(id_poliza)
);

CREATE TABLE siniestros (
    id_siniestro INT AUTO_INCREMENT PRIMARY KEY,
    fecha_reporte DATE,
    fecha_ocurrencia DATE,
    tipo_siniestro VARCHAR(100),
    monto_reclamado DECIMAL(12,2),
    monto_aprobado DECIMAL(12,2),
    estatus_siniestro VARCHAR(50),
    poliza_id INT,
    FOREIGN KEY (poliza_id) REFERENCES polizas(id_poliza)
);
