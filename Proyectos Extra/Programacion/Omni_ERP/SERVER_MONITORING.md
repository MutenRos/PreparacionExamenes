# Configuración de Supervisión - OmniERP Server

## Estado Actual

El servidor OmniERP está configurado con supervisión automática para evitar caídas no detectadas.

### 1. **Systemd Service** (Gestor de Servicios)
**Archivo:** `/etc/systemd/system/omnierp.service`

**Características:**
- ✅ Reinicio automático si el proceso falla
- ✅ Límites de memoria: 1GB
- ✅ Límites de CPU: 80%
- ✅ Se inicia automáticamente al boot
- ✅ Logs guardados en journalctl

**Comandos útiles:**
```bash
# Ver estado del servicio
sudo systemctl status omnierp

# Ver logs en tiempo real
sudo journalctl -u omnierp -f

# Reiniciar manualmente
sudo systemctl restart omnierp

# Detener
sudo systemctl stop omnierp

# Ver logs últimas 50 líneas
sudo journalctl -u omnierp -n 50
```

### 2. **Monitor Script** (Verificación Periódica)
**Archivo:** `/home/dario/monitor_omnierp.sh`

**Qué hace:**
- Verifica cada 5 minutos si el servidor responde a `/health`
- Si no responde, intenta 3 veces con retrasos
- Si sigue sin responder, reinicia automáticamente
- Registra todos los eventos en `/home/dario/omnierp_monitor.log`

**Cron Entry:**
```
*/5 * * * * /home/dario/monitor_omnierp.sh
```

### 3. **Logs y Debugging**

**Ver logs del servicio systemd:**
```bash
sudo journalctl -u omnierp -n 100 -f
```

**Ver logs del monitor:**
```bash
tail -f /home/dario/omnierp_monitor.log
```

**Síntomas de problema:**
```
[2025-12-11 06:25:45] ✗ Error al reiniciar servidor  # Problema serio, investigar
[2025-12-11 06:25:45] Server down, intentando reiniciar  # Caída detectada y reparada
```

### 4. **Métricas de Recurso**

Verificar uso de memoria/CPU:
```bash
sudo systemctl status omnierp | grep Memory
ps aux | grep uvicorn
```

Si consume demasiado:
- Aumentar `MemoryLimit` en `/etc/systemd/system/omnierp.service`
- Investigar memory leaks en el código

### 5. **Próximos Pasos Recomendados**

- [ ] Revisar logs periodicamente (especialmente primeras 24h)
- [ ] Si hay caídas frecuentes: `sudo journalctl -u omnierp -n 200 | grep -i error`
- [ ] Considerar agregar alertas por email si cae múltiples veces
- [ ] Backup automático de base de datos

---

**Última actualización:** 11 de Diciembre de 2025
**Estado:** ✅ Servicio activo con supervisión
