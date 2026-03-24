CREATE TABLE IF NOT EXISTS historia (
    identificacion TEXT,
    corte_mes DATE,
    saldo REAL
);

CREATE TABLE IF NOT EXISTS retiros (
    identificacion TEXT,
    fecha_retiro DATE
);

-- Índices para optimizar las consultas de búsqueda
CREATE INDEX IF NOT EXISTS idx_historia_id ON historia(identificacion);
CREATE INDEX IF NOT EXISTS idx_historia_fecha ON historia(corte_mes);