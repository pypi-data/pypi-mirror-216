# Generador de Certificados OASIS4© para Django

Este módulo permite la generación de los certificados tributarios, comerciales, de asociados, estados de cuenta y fincas
de los clientes y asociados que se encuentran matriculados en la base de datos OASIS4©.

El módulo provee algunas apis para:

* Consultar certificados disponibles "/document/list/"
* Generar el certificado escogido "/document/generator/"
* Descargar un certificado específico "/document/get/"
* Solicitar el envío a través de correo electrónico de un certificado "/document/send/"

Todos las API aqui relacionadas requieren para su operación estar auténticados y ser un asociado o cliente registrado en el portal y en el sistema.

# Versiones Liberadas
* 1.0.0: Versión con la generación y compatibilidad necesarias para la generación de certificados standard.