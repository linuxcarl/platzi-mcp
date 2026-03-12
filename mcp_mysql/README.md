# MCP MySQL Server

Servidor MCP que permite ejecutar queries SQL contra una base de datos MySQL.

## Herramientas disponibles

- **`query(sql)`** — Ejecuta cualquier query SQL y retorna los resultados como JSON
- **`describe_table(table_name)`** — Retorna los detalles de columnas de una tabla
- **Recurso `schema://tables`** — Lista todas las tablas y sus columnas

## Requisitos

- Python 3.12+
- MySQL 8+ (local o Docker)

## Setup

### 1. Levantar MySQL con Docker (opcional)

```bash
docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=secret -e MYSQL_DATABASE=testdb mysql:8
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus credenciales de MySQL
```

### 3. Instalar dependencias

```bash
uv sync
```

### 4. Ejecutar el servidor

```bash
# Modo desarrollo (con inspector MCP)
uv run mcp dev server.py

# Modo producción (stdio)
uv run mcp run server.py
```

## Seguridad

Por defecto, solo se permiten queries de lectura (`SELECT`, `SHOW`, `DESCRIBE`, `EXPLAIN`). Para habilitar escritura, cambia `MYSQL_ALLOW_WRITE=true` en tu `.env`.
