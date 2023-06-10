# WhatsAppPlus

* Autor: Kostya Gladkiy (Ucrania)
* [Canal de telegram](https://t.me/unigramPlus)

##Información sobre la oportunidad de donar al desarollador:

Si tienes el deseo, y lo más importante, la oportunidad de apoyar al desarrollador de este complemento, puedes hacerlo usando los siguientes detalles:

* PayPal: gladkiy.kostya@gmail.com.
* Sistema ucraniano de donaciones: https://unigramplus.diaka.ua/donate.
* Número de tarjeta: 5169360009004502 (Gladkiy Constantine).

Se agrega un gran número de atajos para un trabajo productivo y cómodo con el programa, los cuales se pueden encontrar a continuación.

### Características generales del complemento

* Ahora el campo de entrada de mensaje cambiará de nombre Cuando respondamos a un mensaje.
* se agregan etiquetas para algunos elementos del programa que los lectores de pantalla no leen.

## Lista de teclas rápidas:

* ALT+1 - Mover el foco a la lista de chats.
* ALT+2 - Mover el foco al último mensaje en el chat actual.
* ALT+D - Mover el foco al campo de edición. Si el foco ya se encuentra en el campo de edición, se moverá entonces hacia donde se encontraba anteriormente.
* ALT+T - Anunciar el nombre y estado del chat actual.
* ALT+shift+C - Llamar a un grupo o contacto, o unirse a una llamada grupal en curso.
* ALT+shift+V - Videollamar a un contacto o grupo.
* ALT+shift+Y - Aceptar llamada.
* ALT+shift+N - Presionar el botón "Rechazar llamada" si hay una llamada entrante, "o el botón "Llamar" si hay una llamada en curso.
* ALT+A - Silenciar y desilenciar micrófono.
* ALT+V - Activar y desactivar la cámara.
* ALT+O - Presionar el botón "Más opciones".
* control+R - Grabar y enviar un mensaje de voz.
* control+D - Cancelar mensaje de voz.
* control+shift+D - Pausar/reanudar grabación de mensajes de voz.
* ALT+suprimir - Eliminar mensaje o chat.
* control+shift+P - Abrir el perfil del chat actual.
* control+shift+E - Alterna el modo que quita la lectura del número de usuario al leer mensajes que no están en la lista de contactos.
* ALT+S - Destacar mensaje.
* ALT+F - Reenviar mensaje.
* ALT+R - Responder al mensaje.
* ALT+shift+R - Marcar chat como leído.
* control+C - Copiar mensaje si este contiene texto.
* ALT+C - Mostrar texto del mensaje en una ventana emergente.
* NVDA+control+W - Abrir la ventana de configuración de WhatsAppPlus.
* ALT+3 - Mover el foco a la etiqueta de "mensajes no leídos".
* ALT+shift+A - Presionar el botón "Adjuntar".
* ALT +L: Activa la lectura automática de mensajes en el chat actual.
* Control+S: Aumenta o disminuye la velocidad de reproducción de los mensajes de voz.
* ALT+P: Reproduce o pausa el mensaje de voz actualmente en reproducción.
* ALT+U: Anuncia el valor actual de la barra de progreso. Si se pulsa dos veces, activa o desactiva el anuncio automático de los indicadores.
* Control+Espacio: Cambiar al modo de selección.

##Historial de cambios

### Versión 1.9.0

* Se añadió un atajo de teclado que abre una lista de todos los atajos de WhatsApp Plus. De forma predeterminada, esta función se asigna al gesto ALT+h.
* Se corrigió un error por el que los gestos ALT+2 y ALT+3 no funcionavan.
* Se corrigió un error por el que era imposible activar algunas funciones del menú contextual utilizando gestos.
* Se corrigió un error por el que el cambio de velocidad de los mensajes de voz y pausar los mensajes de voz no funcionava siempre.
* Se corrigió un error por el cuál al enfocarse en tus mensajes enviados en los chats, en lugar de la palabra "tú", el lector de pantalla anunciava un número personal. Para esquivar esto, debes especificar el número de teléfono en las opciones de WhatsApp Plus y después de eso, el complemento no lo anunciará en tus mensajes.
* Se corrigió un error por el que WhatsApp Plus solicitaba actualizarse en pantallas seguras. Para prevenir que suceda de nuevo, debes hacer click en el botón "Utilizar opciones actualmente guardadas durante el inicio de sesión y en pantallas seguras (requiere privilegios de administrador)" en las opciones generales de NVDA.
* El gesto para aceptar una llamada se cambió a ALT+shift+Y, y el gesto para rechazar una llamada se cambió a ALT+shift+N. Esto es para asegurarse de que estos gestos no estén en conflicto con los gestos de Unigram Plus.
* Los gestos para activar o desactivar la cámara y el micrófono durante una llamada ahora funcionan correctamente.
* Se eliminó el gesto para reaccionar a los mensajes, ya que en las últimas versiones de WhatsApp, las reacciones están disponibles directamente en el menú contextual.

### Versión 1.8.0

* El complemento se probó para asegurar la compatibilidad con NVDA-2023.
* Se añadió un atajo de teclado para seleccionar mensajes. Para entrar al modo de selección, pulsa control+espacio, y luego  usa espacio para seleccionar el siguiente mensaje.
* Se añadió una función para anunciar automáticamente la actividad de un chat. Esta función se activa presionando dos veces la combinación ALT+T. Esto ayuda a los usuarios a obtener actualizaciones sobre nuevos mensajes y otra actividad del chat.
* La función que anuncia automáticamente nuevos mensajes en el chat se ha revisado sustancialmente para un funcionamiento más estable. Esto garantiza que los usuarios reciban alertas de nuevos mensajes de manera precisa y confiable.
* Se agregaron etiquetas para algunos botones sin etiquetar.


### Versión 1.7.0

* Se agrega una función que anuncia automáticamente el valor de la barra de progreso si el foco está en un mensaje.
* Se agrega un atajo para anunciar el valor de la barra de progreso  si el foco está en un mensaje. De forma predeterminada, la combinación de teclas ALT+U está asignada a esta función. Si esta combinación se presiona dos veces, la función de anuncio automático de los indicadores se activa.
* Se corrije un error que causa que el foco no pueda moverse a la lista de chats.
* Se añadieron etiquetas a algunos elementos.

### Versión 1.6.0

* Añadida la capacidad de responder rápidamente a los miembros del grupo. Para introducir un mensaje, vasta con escribir el símbolo "@" en el cuadro de edición mensaje, usar las flechas arriba y abajo para seleccionar a quién responder, y luego presionar la tecla intro.
* Agregada la capacidad de insertar rápidamente emoticonos. Para hacer esto, debes escribir dos puntos y el nombre del emoticono que quieres encontrar en el cuadro de edición mensaje. Después, usa las flechas arriba y abajo para encontrar el emoticono deseado y usa intro para insertarlo en el mensaje.
* En las opciones de WhatsApp Plus, se añadióagregó una opción para activar la reproducción de sonidos al grabar, pausar y enviar mensajes de voz.
* Se cambió el atajo para abrir el perfil de la conversación actual a Control+Shift+P.
* Añadida localización al Nepalí.
* Se corrigieron errores, incluyendo uno que causó que la lectura automática de mensajes en el chat actual no funcione para algunos usuarios.

### Versión 1.5.0

* Se agregó un atajo para cambiar la velocidad de reproducción del mensaje de voz en reproducción. El gesto predeterminado es Control+S. Solo funcionará cuando un mensaje se está reproduciendo en el chat actual.
* Se agregó un atajo para pausar un mensaje de voz que se está reproduciendo. El gesto predeterminado es ALT+P. Solo funcionará si un mensaje se está reproduciendo en el chat actual.
* Ahora el anuncio de un nuevo mensaje en un chat abierto se puede activar hasta que NVDA se reinicie, pero también para siempre.

### Versión 1.4.0

* Se adaptó a la última versión de WhatsApp.
* Se añadió la función lectura automática de nuevos mensajes en el chat. De forma predeterminada, esta función se activa presionando ALT+L. La característica se mantiene activada hasta que NVDA se reinicie. Puede generar problemas de estabilidad si hay muchos mensajes nuevos.
* Se añadió localización al Francés.

### Versión 1.3.0

* Ahora se lee la descripción de los enlaces adjuntos a los mensajes.
* Ahora se anuncia la duración de los mensajes de voz.
* Ahora puedes abrir los enlaces adjuntos a los mensajes con la barra espaciadora.
* Añadidas etiquetas para algunos elementos de la interfaz.
* Se adaptó a la última versión de WhatsApp, así que todas las funciones funcionan correctamente.
* Se corrigieron algunos errores.

### Versión 1.2.0

* Ahora, cuando te enfocas en un mensaje escrito en respuesta a otro mensaje, se verbaliza primero el texto de ese mensaje y luego el mensaje para el cual fue enviado.
* Se anuncia el nombre y el tipo de los archivos enviados en la conversación.
* Ahora ALT+1 funciona cuando la sección chats archivados o mensajes seleccionados está abierta.
* Alt + flecha izquierda ayudan a cerrar las listas de chats archivados o mensajes seleccionados si están abiertas.
* Ahora, presionando Control+D, además de cancelar mensajes de voz, se cancela la respuesta al mensaje.
* Ahora se anuncia la incapacidad de grabar un mensaje de voz si el cuadro de edición no está bacío. Esto corrige un problema donde Control+R enviaba un mensaje de texto en lugar de iniciar la grabación de un mensaje de voz.
* Añadidas etiquetas para algunos elementos que no tenían etiqueta.

###Versión 1.1.0

* Se agrega atajo de teclado para navegar hacia los mensajes no leídos. Ya que esta función depende del idioma, Se puede configurar en los ajustes de WhatsAppPlus.
* Se agrega un atajo de teclado para presionar el botón "Nuevo chat".
* Se agrega un atajo de teclado para presionar el botón "Adjuntar archivo".
* Ahora, cuando se grabe un mensaje de voz, El sintetizador no anunciará los nombres de los controles de grabación.
* Se agrega traducción al rumano, Servio, Croata, Español y Turco.
* Se agregan etiquetas para algunos elementos que no tenían etiquetas para lectores de pantallas.
* Ahora la info acerca de reacciones a un mensaje se anunciará al situarse en dicho mensaje.
* Ahora al reproducir tus propios mensajes de voz con la barra espaciadora, no aparecerá una ventana emergente.
* Se corrigen errores menores.