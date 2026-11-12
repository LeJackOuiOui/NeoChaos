# 🚨 Reporte Post-Mortem del Incidente

**Equipo Afectado (Nosotros):** NeoGenesis AI\
**Equipo Saboteador:** Cunitech\
**Tiempo Total de Resolución:** 10 minutos

## 1. Detección y Síntomas

No funcionaba la subida de datos para la base de datos y tampoco leía la información ya escrita en la misma base de datos.

## 2. Diagnóstico y Causa Raíz

Al investigar, se encontró que las keys con las que se podía hacer acceso a la base de datos, habían sido modificadas para no permitirnos el acceso.

## 3. Resolución y Evaluación del Runbook

- **Pasos de Solución:**
  1. Detuvimos la aplicación.
  2. Ingresamos al proyecto a verificar los serviciós de la API.
  3. Verificamos las llaves antes vs. después del sabotaje.
  4. Restauramos las llaves correspondientes para su funcionamiento normal por medio de `git checkout -- lib/main.dart`
  5. Reiniciamos por completo el proyecto.
- **Utilidad del Runbook:** 🟢 Muy útil, el error estaba tipificado explicitamente.

## 4. Acciones de Mejora Preventiva

- INC-11 — Fallo de variables de entorno o secretos faltantes en Supabase.
- INC-12 — Conflicto de versiones del SDK de Supabase o dependencias de Dart bloqueadas.
- INC-13 — Bloqueo por caché local del navegador o sesión corrupta en Flutter Web.
