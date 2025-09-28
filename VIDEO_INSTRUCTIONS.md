# Instrucciones para el Video del Pop-up Black Week

## Especificaciones del Video:

### Archivos necesarios:
1. **Video principal**: `media/videos/Black_Week_Promo.mp4`
2. **Video alternativo**: `media/videos/Black_Week_Promo.webm` (opcional, para mejor compatibilidad)
3. **Imagen de portada**: `media/images/Promocion/Black_Week_Poster.jpg`

### Especificaciones técnicas:
- **Duración**: Exactamente 5 segundos
- **Resolución recomendada**: 1080x1080 (cuadrado) o 16:9
- **Formato**: MP4 (H.264)
- **Calidad**: Alta definición pero optimizada para web
- **Tamaño máximo**: 5-10 MB para carga rápida
- **Audio**: Sin audio (muted) ya que reproduce automáticamente

### Contenido del video:
Basado en la imagen que proporcionaste, el video debería incluir:

1. **Texto animado**:
   - "BLACK WEEK" (blanco)
   - "15%" (naranja/rojo con efectos)
   - "DESCUENTO DE ELECTRODOMÉSTICOS"
   - "Home POWER" (logo animado)

2. **Elementos visuales**:
   - Fondo oscuro/negro
   - Efectos de rayos/lightning
   - Iconos de fuego 🔥
   - Productos electrodomésticos (licuadoras, cafeteras, etc.)

3. **Logos de tiendas** (al final):
   - Titan
   - El Costo  
   - Madison

### Animación sugerida (5 segundos):
- **0-1s**: Aparece "BLACK WEEK" con efecto dramatic
- **1-2s**: "15%" se agranda con efecto de fuego
- **2-3s**: "DESCUENTO DE ELECTRODOMÉSTICOS" se desliza
- **3-4s**: Productos aparecen con zoom
- **4-5s**: Logo "Home POWER" y tiendas aparecen

### Configuración actual del código:
- ✅ Autoplay activado (sin sonido)
- ✅ Loop activado (se repite)
- ✅ Responsive design
- ✅ Fallback a imagen si video falla
- ✅ Controles optimizados para móvil

### Ubicación de archivos:
```
media/
├── videos/
│   ├── Black_Week_Promo.mp4    (archivo principal)
│   └── Black_Week_Promo.webm   (opcional)
└── images/
    └── Promocion/
        └── Black_Week_Poster.jpg (portada/fallback)
```

### Nota importante:
El video se reproduce automáticamente cuando aparece el pop-up y se pausa cuando se cierra. El diseño está optimizado para mostrar el video centrado con overlay de texto sobre él.