# Prueba técnica: Tuya SA
Repositorio de prueba técnica de la empresa Tuya SA para aplicar al cargo de Ingeniero de Datos

## Estructura del repositorio:
```
prueba_tuya_sa/
├── ejercicio_1/            # Proceso ETL y los conceptos de KPIs
│   ├── .github/workflows
│   │   └── pipeline.yaml       # Configuración de la automatización
│   ├── data
│   │   ├── raw/                # Datos de entrada
│   │   └── processed/          # Dataset final validado
│   ├── src/
│   │   ├── main.py             # Script principal de ETL
│   │   └── utils.py            # Funciones de limpieza y validación
│   └── tests/ 
│       └── test_validation.py  # Pruebas unitarias para los teléfonos
│
├── ejercicio_3/            # Scripts SQL y archivo de rachas
│   ├── load_data.py            # Script para carga de tablas a formato .db
│   ├── Prueba Tecnica.xlsx     # Insumo de Excel con las tablas
│   ├── solution_database.db    # Archivo .db resultante de la carga
│   ├── query.sql               # Consulta SQL con la solución requerida
│   └── schema.sql              # Esquema de la tabla a cargar en load_data.py
│
├── ejercicio_4/           # Procesador de imágenes POO
│   ├── file_orchestrator.py    # Buscador de archivos HTML dentro de la carpeta definida en main.py y consolidador de reportes al final
│   ├── html_processor.py       # Parser de los archivos HTML recibidos, busca tag <img> y clasifica "success" o "fail"
│   ├── image_encoder.py        # Conversor de imágenes de formato binario a base64
│   └── main.py                 # "Pipeline" principal para instanciar las clases .py
└── README.md                   # Archivo con la documentación y explicación completa del código
```

## 1. Ejercicio Conceptual de Creación de Dataset de Números de Teléfono de Clientes
Se implementó una lógica de limpieza de datos para la normalización de registros telefónicos. El proceso utiliza Regex para identificar patrones y remover ruido, asegurando un estándar en los teléfonos resultantes o descartando aquellos que no son válidos. 
- Se asume que todos los números telefónicos a ingresar son de Colombia (+57) 
- Se asume que la salida siempre debe incluir el identificativo

Se incluye una suite de pruebas unitarias con Pytest automatizadas con un archivo .yaml para validar el comportamiento del script ante diversos formatos de entrada, garantizando la integridad del dataset final antes de su procesamiento y subida a lo que sería desarrollo.


## 2. Ejercicio Conceptual de KPI's
Para garantizar la integridad de la información y asegurar que el ciclo de vida del dato sea confiable, se proponen los siguientes mecanismos de control y monitoreo:

### KPI's
Más allá de la ejecución exitosa del script, es importante validar los resultados mediante métricas automatizadas al finalizar cada proceso ETL, para ello es útil calcular:

- Porcentaje de registros procesados y validados respecto al total.
- Cantidad de nulos o vacíos detectados.
- Cantidad de duplicados.

### Trazabilidad
Para garantizar trazabilidad en los datos y tener capacidad de respuesta ante inconvenientes se pueden realizar prácticas útiles como:

- Generar logs para el código los cuales se almacenen en un archivo .txt o .json.
- Conservar una tabla de auditorías en la cual se tenga registro de todas las tablas relacionadas al proyecto y todos los pipelines existentes.
- Control de nube mediante la arquitectura medallón (bronze, silver y gold) para tener versionamiento de código.

### Gobierno de datos
Para velar por un orden y control en el manejo de los datos, existen algunas alternativas bastante seguras tales como:

- Garantizar roles con permisos y restricciones definidos para cada usuario involucrado en la generación de código, previniendo alteraciones inesperadas.
- Políticas de Backup para optimizar costos sin perder trazabilidad histórica.
- Definir claramente quiénes son los encargados de actualizar y modificar la tabla, para garantizar que la información no se distorsione.


## 3. Análisis de Rachas
Para dar solución al problema de consecutividad de retiros mensuales utilizando SQL avanzado se ha realizado el siguiente procedimiento:

- Script load_data.py que automatiza la creación de la base de datos SQLite y carga los datos desde Excel y los pasa a formato .bd.
- Implementación de CTEs y funciones de ventana (ROW_NUMBER, LAG) para identificar conjuntos de meses consecutivos.
- Creación de esquema de las tablas en formato .bd a generar, garantizando que el tipado de los datos sea el esperado.


## 4. Procesamiento de archivos HTML en Python
Para crear una herramienta modular, útil para la conversión de imágenes locales a formato embebido (Base64) se empleó el siguiente método:

- Se basó el código en Programación Orientada a Objetos y principios SOLID para garantizar calidad en el código.
- Se desarrollaron las funciones utilizando únicamente las liberías estándar de Python.
- Se modularizó cada clase en un archivo .py distinto, garantizando orden y facilidad para realizar modificaciones.
- Se garantiza el procesamiento de archivos individuales o directorios con navegación recursiva profunda. Genera un reporte final de ejecución en formato JSON con el estado de cada recurso procesado.

## Notas de ejecución

### Ejercicio 1
- **Ejecución:** ```python ejercicio_1/src/main.py```
- **Tests:** ```python -m unittest ejercicio_1/tests/test_validation.py```

### Ejercicio 3
Asegúrese de tener instaladas las dependencias necesarias (pandas y openpyxl) antes de ejecutar esta parte del código. Para ello puede utilizar los siguientes comandos:

```
# 1. Crear y activar entorno virtual
python -m venv .venv

# 2 Activar entorno virtual
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Generar Base de Datos y ejecutar consulta
python ejercicio_3/load_data.py
```

**Nota:** Utilice un cliente de SQLite para ejecutar la lógica de ```query.sql``` sobre el archivo ```solution_database.db``` generado.


### Ejercicio 4
Para el punto 4, coloque los archivos a procesar en una carpeta dentro de ```ejercicio_4``` con nombre ```data_html``` o bien modifique la ruta a su elección en ```main.py``` en la variable ```paths_to_process```, puede agregar más de una carpeta a la lista para mayor libertad.

**Ejecución:** ```python ejercicio_4/main.py```
**Resultado:** Los archivos procesados se generarán con el sufijo ```_b64.html```.
