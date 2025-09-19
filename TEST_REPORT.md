# 🧪 Informe de Pruebas — VORTEX-512

**Fecha:** 19 de septiembre de 2025  
**Autor:** Juan Arnau  
**Versión del sistema:** VORTEX-512 con autenticación HMAC-SHA256

---

## ✅ Pruebas ejecutadas

| Test | Descripción | Resultado |
|------|-------------|-----------|
| `test_encrypt_decrypt` | Verifica que el cifrado y descifrado de datos funciona correctamente | ✅ OK |
| `test_authentication_failure` | Detecta manipulación de datos cifrados mediante HMAC | ✅ OK |
| `test_padding_unpadding` | Comprueba que el relleno PKCS7 se aplica y se elimina correctamente | ✅ OK |
| `test_sbox_reversibility` | Verifica que la sustitución S-box es reversible | ✅ OK |
| `test_encrypt_decrypt_folder` | Cifra y descifra múltiples archivos en una carpeta | ✅ OK |
| `test_authentication_failure_folder` | Detecta corrupción en archivos cifrados dentro de una carpeta | ✅ OK |

---

## 📂 Cobertura

- Cifrado por bloques con CBC personalizado
- Autenticación con HMAC-SHA256
- Cifrado y descifrado de archivos individuales
- Cifrado y descifrado de carpetas completas
- Validación de integridad y reversibilidad

---

## 📌 Observaciones

- Todos los tests pasaron correctamente.
- El sistema detecta alteraciones en los datos cifrados.
- La interfaz gráfica aún no tiene validación visual de autenticidad por archivo (pendiente de mejora).

---

## 🧠 Recomendaciones

- Añadir pruebas de rendimiento con archivos grandes
- Incluir verificación de subdirectorios en carpetas
- Generar logs de errores para trazabilidad