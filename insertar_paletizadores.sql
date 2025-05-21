-- Elimina la tabla 'palletizer_info' si ya existe
-- Esto evita errores por duplicación al ejecutar múltiples veces el script
DROP TABLE IF EXISTS palletizer_info;

-- Crea una nueva tabla llamada 'palletizer_info' con información técnica de los paletizadores
CREATE TABLE palletizer_info (
    machine_id VARCHAR(10) PRIMARY KEY,         -- Identificador único de la máquina
    model VARCHAR(50),                          -- Modelo del paletizador (ej. KUKA, ABB)
    location VARCHAR(100),                      -- Ubicación física de la máquina
    install_date DATE,                          -- Fecha de instalación
    last_maintenance DATE,                      -- Fecha del último mantenimiento
    certified_operator VARCHAR(100)             -- Nombre del operador certificado
);

-- Inserta registros de prueba con datos realistas para análisis posterior
-- Cada registro representa una máquina paletizadora en distintas ubicaciones
INSERT INTO palletizer_info (
    machine_id, model, location, install_date, last_maintenance, certified_operator
) VALUES
('M001', 'KUKA KR40', 'Planta Norte', '2022-01-10', '2023-12-15', 'Carlos Pérez'),
('M002', 'ABB IRB 460', 'Planta Sur', '2021-06-22', '2023-11-01', 'Lucía Gómez'),
('M003', 'FANUC M410iC', 'Zona Industrial 3', '2020-08-30', '2023-10-20', 'Luis Torres'),
('M004', 'YASKAWA MPL80', 'Bodega Central', '2019-12-18', '2024-01-12', 'Ana Martínez'),
('M005', 'KUKA KR40', 'Sucursal Quito', '2023-03-05', '2024-03-10', 'Pedro Sánchez');
