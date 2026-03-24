# Prueba técnica: Tuya SA
Repositorio de prueba técnica de la empresa Tuya SA para aplicar al cargo de Ingeniero de Datos

## Estructura del repositorio:
```
prueba_tuya_sa/
├── ejercicio_1_y_2/           # Proceso ETL y los conceptos de KPIs
│   ├── .github/workflows/
│   │   └── pipeline.yaml        # Configuración de la automatización
│   ├── data/
│   │   ├── raw/                # Datos de entrada
│   │   └── processed/          # Dataset final validado
│   ├── src/
│   │   ├── main.py             # Script principal de ETL
│   │   └── utils.py            # Funciones de limpieza y validación
│   └── tests/
│       └── test_validation.py  # Pruebas unitarias para los teléfonos
│
├── ejercicio_3_sql/           # Scripts SQL y archivo de rachas
│   ├── load_data.py
│   ├── Prueba Tecnica.xlsx
│   ├── query.sql
│   └── schema.sql
│
├── ejercicio_4_html/          # Procesador de imágenes POO
│   ├── src/
│   └── tests/
└── README.md                  # Archivo con la documentación y explicación completa del código
```

## 1. Ejercicio Conceptual de Creación de Dataset de Números de Teléfono de Clientes

### Comandos importantes:
- Para ejecutar el código: ```python ejercicio_1_y_2/src/main.py```
- Para ejecutar los tests: ```python -m pytest ejercicio_1_y_2/tests/test_validation.py```



## 2. Ejercicio Conceptual de KPI's

Para garantizar la integridad de la información y asegurar que el ciclo de vida del dato sea confiable, se proponen los siguientes mecanismos de control y monitoreo:

### KPI's
Más allá de la ejecución exitosa del script, es importante validar los resultados mediante métricas automatizadas al finalizar cada proceso ETL:

- Porcentaje de registros procesados y validados respecto al total.
- Cantidad de nulos o vacíos detectados.
- Cantidad de duplicados.

### Trazabilidad
Para garantizar trazabilidad en los datos y tener capacidad de respuesta ante inconvenientes se pueden realizar prácticas útiles como:
- Generar logs para el código los cuales se almacenen en un archivo .txt o .json.
- Conservar una tabla de auditorías en la cual se tenga registro de todas las tablas relacionadas al proyecto y todos los pipelines existentes.
- Control de nube mediante la arquitectura medallón (bronze, silver y gold) para tener versionamiento de código.

### Gobierno de datos
- Garantizar roles con permisos y restricciones definidos para cada usuario involucrado en la generación de código, previniendo alteraciones inesperadas.
- Políticas de Backup para optimizar costos sin perder trazabilidad histórica.
- Definir claramente quiénes son los encargados de actualizar y modificar la tabla, para garantizar que la información no se distorsione.

## 3. Rachas

