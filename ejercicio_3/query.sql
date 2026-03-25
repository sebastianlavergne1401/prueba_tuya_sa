-- Querys de validación
-- Control de duplicados en historia
--SELECT
--    identificacion,
--    corte_mes,
--    COUNT(*)    AS num_registros,
--    MIN(saldo)  AS saldo_min,
--    MAX(saldo)  AS saldo_max
--FROM historia
--GROUP BY identificacion, corte_mes
--HAVING COUNT(*) > 1;

---- Clientes con registros en historia DESPUÉS de su fecha de retiro
--SELECT h.identificacion, h.corte_mes, r.fecha_retiro
--FROM historia h
--INNER JOIN retiros r ON r.identificacion = h.identificacion
--WHERE h.corte_mes > r.fecha_retiro
--ORDER BY h.identificacion, h.corte_mes;


-- Solución con CTEs paso a paso para claridad y mantenibilidad.
-- Parámetros
WITH params AS (
    SELECT
        '2027-02-28' AS fecha_base,
        3 AS n
),


-- 1. Fechas de cortes <= fecha_base
cortes AS (
    SELECT DISTINCT corte_mes
    FROM historia
    WHERE corte_mes <= (SELECT fecha_base FROM params)
),

-- 2. Primera aparición de cada cliente en la historia
primera_aparicion AS (
    SELECT
        identificacion,
        MIN(corte_mes) AS primer_corte
    FROM historia
    GROUP BY identificacion
),

-- 3. Cruce clientes x cortes con reglas de inclusión:
-- Se excluyen meses anteriores a la primera aparición del cliente.
-- Se toman cortes desde la primera aparición del cliente hasta fecha retiro (si existe) o fecha_base.
clientes_cortes AS (
    SELECT
        pa.identificacion,
        c.corte_mes
    FROM primera_aparicion AS pa
    CROSS JOIN cortes AS c
    LEFT JOIN retiros AS r ON r.identificacion = pa.identificacion
    WHERE
        c.corte_mes >= pa.primer_corte
        AND (r.fecha_retiro IS NULL OR c.corte_mes <= r.fecha_retiro)
),

-- 4. Saldos limpios
-- Deduplica clientes con más de un registro en el mismo mes
-- prioriza el de saldo máximo.
saldos_limpios AS (
    SELECT
        identificacion,
        corte_mes,
        MAX(saldo) AS saldo
    FROM historia
    GROUP BY identificacion, corte_mes
),

-- 5. Cruce clientes_cortes x saldos limpios
--    Para los meses donde el cliente no tiene registro (pero sí
--    debería estar activo), se imputa saldo = 0 | nivel N0.
saldos_completos AS (
    SELECT
        cc.identificacion,
        cc.corte_mes,
        COALESCE(sl.saldo, 0) AS saldo
    FROM clientes_cortes AS cc
    LEFT JOIN saldos_limpios AS sl
        ON  sl.identificacion = cc.identificacion
        AND sl.corte_mes = cc.corte_mes
),

-- 6. Clasifiación por nivel de deuda
saldos_nivel AS (
    SELECT
        identificacion,
        corte_mes,
        saldo,
        CASE
            WHEN saldo >= 0 AND saldo < 300000 THEN 'N0'
            WHEN saldo >= 300000 AND saldo < 1000000 THEN 'N1'
            WHEN saldo >= 1000000 AND saldo < 3000000 THEN 'N2'
            WHEN saldo >= 3000000 AND saldo < 5000000 THEN 'N3'
            WHEN saldo >= 5000000 THEN 'N4'
        END AS nivel
    FROM saldos_completos
),

-- 7. Cálculo de nivel anterior para cada cliente y corte
-- se genera nueva columna "nivel_anterior" que contiene el nivel del mes anterior para cada cliente.
con_lag AS (
    SELECT
        identificacion,
        corte_mes,
        nivel,
        LAG(nivel) OVER (
            PARTITION BY identificacion
            ORDER BY corte_mes
        ) AS nivel_anterior
    FROM saldos_nivel
),

-- 8. Detección de cambios de nivel (inicio de racha)
-- Se marca con "es_inicio_racha" = 1 cuando hay un cambio de nivel respecto al mes anterior (o es el primer mes del cliente).
-- Se marca con "es_inicio_racha" = 0 cuando el nivel es igual al mes anterior (continuación de racha).
cambios AS (
    SELECT
        identificacion,
        corte_mes,
        nivel,
        -- Es 1 cuando hay un cambio de nivel (o es el primer mes del cliente)
        CASE
            WHEN nivel_anterior IS NULL OR nivel != nivel_anterior THEN 1
            ELSE 0
        END AS es_inicio_racha
    FROM con_lag
),

-- 9. Agrupador de rachas
-- Se asigna un número de grupo a cada racha de niveles iguales para cada cliente.
-- Util para luego calcular el largo de cada racha y sus fechas de inicio y fin.
grupos AS (
    SELECT
        identificacion,
        corte_mes,
        nivel,
        SUM(es_inicio_racha) OVER (
            PARTITION BY identificacion
            ORDER BY corte_mes
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS grupo_racha
    FROM cambios
),

-- 10. Métricas por racha
-- Largo, fecha de inicio y fecha de fin de cada racha.
rachas AS (
    SELECT
        identificacion,
        nivel,
        grupo_racha,
        COUNT(*) AS largo_racha,
        MIN(corte_mes) AS fecha_inicio,
        MAX(corte_mes) AS fecha_fin
    FROM grupos
    GROUP BY identificacion, nivel, grupo_racha
),

-- 11. Filtro: solo rachas que cumplan con largo mínimo definido en parámetros (n)
rachas_validas AS (
    SELECT
        r.identificacion,
        r.nivel,
        r.largo_racha,
        r.fecha_fin
    FROM rachas AS r
    WHERE r.largo_racha >= (SELECT n FROM params) -- n definido en parámetros
),

-- 12. Selección de la mejor racha por cliente según criterios definidos en orden de prioridad:
-- 1. Racha más larga
-- 2. En caso de empate, la racha con fecha de fin más reciente
mejor_racha AS (
    SELECT
        rv.identificacion,
        rv.largo_racha AS racha,
        rv.fecha_fin,
        rv.nivel,
        ROW_NUMBER() OVER (
            PARTITION BY rv.identificacion
            ORDER BY
                rv.largo_racha DESC,
                rv.fecha_fin DESC
        ) AS rn
    FROM rachas_validas AS rv
    WHERE rv.fecha_fin <= (SELECT fecha_base FROM params)
)

-- RESULTADO FINAL
SELECT
    identificacion,
    racha,
    fecha_fin,
    nivel
FROM mejor_racha
WHERE rn = 1
ORDER BY identificacion;