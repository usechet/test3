Este proyecto simula una plataforma para subir imágenes y procesarlas por etapas: redimensionado, marca de agua y detección de contenido. Todo el sistema es distribuido y funciona de forma asíncrona usando RabbitMQ y Docker Compose.

La API hecha en Python con Flask permite subir imágenes desde /upload y consultar su estado en /status/{id}. Una vez recibida, la imagen se guarda en un volumen compartido y se manda a una cola para ser procesada. Cada etapa del procesamiento (resize, watermark, detection) se maneja con un worker independiente. Los workers están conectados a RabbitMQ, usan confirmaciones manuales y prefetch=1 para repartir bien la carga. Después del procesamiento, se publica un mensaje al exchange processed_images y un servicio notify se entera y avisa por consola.

El sistema usa Docker Compose, con volúmenes para las imágenes y la data de RabbitMQ. Además, se incluye Traefik para exponer los servicios y proteger la interfaz de RabbitMQ con autenticación básica (la contraseña se genera con formato $apr1$...).Se puede escalar fácilmente agregando réplicas de workers en docker-compose.yml, y como se usan colas duraderas, los mensajes no se pierden si algo falla.



