

<template>
  <div>
    <button @click="generarPDF">Generar PDF</button>
  </div>
</template>

<script>
import jsPDF from 'jspdf';
import 'jspdf-autotable';

export default {
  methods: {
    async generarPDF() {
      const doc = new jsPDF();
      const aprobadoNoAprobado = (value) => {
        return value ? "Aprobado" : "No Aprobado";
      };

      // Agregar contenido al PDF
      doc.text("Resultado de la Lista de Chequeo", 10, 10);
      doc.text(`Usuario Evaluador: `, 10, 20);
      doc.text(`Experiencia: `, 10, 30);

      // Configurar posición inicial para las tablas
      let startY = 40;

      const Heuristics = {}; // Define Heuristics object if not already defined

      const data1 = [

     ["H01P01:", "El sistema indica la sección donde se encuentra actualmente el usuario: " + aprobadoNoAprobado (Heuristics.value.H01P01) ],
     ["H01P02:", "El sistema informa acerca del estado actual de un proceso/tarea: " + aprobadoNoAprobado ( Heuristics.value.H01P02) ],
     ["H01P03:", "La transición de un estado a otro es fácilmente perceptible: " + aprobadoNoAprobado (Heuristics.value.H01P03) ],
     ["H01P04:", "El sistema muestra claramente las reacciones a las acciones del usuario: " + aprobadoNoAprobado (Heuristics.value.H01P04)],
     ["H01P05:", "El sistema muestra claramente las reacciones a las acciones del usuario: " + aprobadoNoAprobado (Heuristics.value.H01P05) ],
     ["H01P06:", "Los tiempos de respuesta son razonables." + aprobadoNoAprobado (Heuristics.value.H01P06) ],
     ["H01P07:", "Una opción seleccionada se destaca claramente respecto a otras: " + aprobadoNoAprobado (Heuristics.value.H01P07)],
     // Agregar las observaciones al PDF
     ["Observaciones:", Heuristics.value.OBSERVACIONH1 || '']
 ];
      // Configuración de la primera tabla (data1)
      const options1 = {
        startY: startY,
        head: [["Código", "Descripción"]],
        body: data1,
        theme: 'grid'
      };

      // Agregar la primera tabla al PDF
      doc.autoTable(options1);

      const data2 = [
     ["H02P01:", "El sistema usa palabras, frases y conceptos familiares al usuario: " + aprobadoNoAprobado(Heuristics.value.H02P01) ],
     ["H02P02:", "La información es presentada de forma simple, natural y en orden lógico: " + aprobadoNoAprobado(Heuristics.value.H02P02) ],
     ["H02P03:", "El sistema está diseñado en el idioma que indica." + aprobadoNoAprobado(Heuristics.value.H02P03) ],
     ["H02P04:", "La secuencia de pasos de los procesos sigue el modelo mental de los usuarios: " + aprobadoNoAprobado(Heuristics.value.H02P04) ],
     ["H02P05:", "El sistema utiliza metáforas y controles de interfaz que corresponden con la realidad: " + aprobadoNoAprobado(Heuristics.value.H02P05) ],
     ["H02P06:", "Las metáforas son fáciles de comprender." + aprobadoNoAprobado( Heuristics.value.H02P06)],
     ["H02P07:", "Los controles de interfaz importantes se presentan en la pantalla: " + aprobadoNoAprobado(Heuristics.value.H02P07) ],
     ["H02P08:", "En la aplicación se explican elementos complejos: " + aprobadoNoAprobado(Heuristics.value.H02P08) ],
     // Agregar las observaciones al PDF
     ["Observaciones:", Heuristics.value.OBSERVACIONH2 || '']
 ];
 const options2 = {
     startY: doc.autoTable.previous.finalY + 5,// Posición inicial de la segunda tabla (debajo de la primera)
     head: [["Código", "Descripción"]],
     body: data2,
     theme: 'grid' // Tema de la tabla
 };
 doc.autoTable(options2);
 

 const data3 = [
     ["H03P01:", "Es posible deshacer una acción cuando ésta es una función o genera alguna operación:  " +  aprobadoNoAprobado(Heuristics.value.H03P01)],
     ["H03P02:", "En caso de realizar una transacción que posee varios pasos,es posible volver a pasos anteriores del proceso para modificarlos: " + aprobadoNoAprobado(Heuristics.value.H03P02)],
     ["H03P03:", "Existe una salida de emergencia al realizar algún proceso (Cancelar desconecta, va al inicio)." + aprobadoNoAprobado(Heuristics.value.H03P03)],
     ["H03P04:", "No se inician de forma automática acciones que no han sido seleccionadas por el usuario. Por ejemplo, la reproducción de un vídeo: " + aprobadoNoAprobado(Heuristics.value.H03P04)],
     ["H03P05:", "Es posible guardar la información relacionada a una transacción, sea exitosa o no: " + aprobadoNoAprobado(Heuristics.value.H03P05)],
     ["H03P06:", "Existe un vínculo para regresar a la página de inicio: " + aprobadoNoAprobado(Heuristics.value.H03P06)],
   
     // Agregar las observaciones al PDF
     ["Observaciones:", Heuristics.value.OBSERVACIONH3 || '']
 ];
 const options3 = {
     startY: doc.autoTable.previous.finalY + 5,
     head: [["Código", "Descripción"]],
     body: data3,
     theme: 'grid' 
 };
 doc.autoTable(options3);


 const data4= [
     ["H04P01:", "Las etiquetas de vínculos tienen nombres iguales que lostítulos de la página a los que redirige: " + aprobadoNoAprobado(Heuristics.value.H04P01) ],
     ["H04P02:", "Las mismas acciones llevan a los mismos resultados. Por ejemplo, al ingresar a una sección desde distintas partes del sistema, éstas se dirigen a la misma: " + aprobadoNoAprobado(Heuristics.value.H04P02)],
     ["H04P03:", "Los elementos utilizados son similares en todo el sistema: " + aprobadoNoAprobado( Heuristics.value.H04P03)],
     ["H04P04:", "Los controles de interfaz de diferentes pantallas se emplean siempre del mismo modo:  " + aprobadoNoAprobado(Heuristics.value.H04P04)],
     ["H04P05:", "El uso del vocabulario es consistente en todo el sistema: " + aprobadoNoAprobado(Heuristics.value.H04P05)],
     ["H04P06:", "La misma información se muestra de la misma forma en todo el sistema: " + aprobadoNoAprobado(Heuristics.value.H04P06)],
     ["H04P07:", "La información está estructurada de forma similar en todo el sistema: " + aprobadoNoAprobado(Heuristics.value.H04P07)],
     ["H04P08:", "Las interfaces que conforman el sistema tienen un aspecto visual coherente:  " + aprobadoNoAprobado(Heuristics.value.H04P08)],
     ["H04P09:", "En situaciones similares se repiten secuencias de acciones:  " + aprobadoNoAprobado(Heuristics.value.H04P09)],
     ["H04P10:", "Los símbolos utilizados son comprensibles y facilitan la interacción con el sistema:  " + aprobadoNoAprobado(Heuristics.value.H04P10)],
     ["H04P11:", "Se usan colores estándares para vínculos (rojo para advertencia, verde para acción exitosa):  " + aprobadoNoAprobado(Heuristics.value.H04P11)],
     ["H04P12:", "Se siguen los estándares establecidos para los símbolos utilizados (equis para cancelar, etc.): " + aprobadoNoAprobado(Heuristics.value.H04P12)],
     ["H04P13:", "La ubicación de las barras de navegación, herramientas de búsquedas y controles (botones) siguen los estándares comunes establecidos: " + aprobadoNoAprobado(Heuristics.value.H04P13)],
     // Agregar las observaciones al PDF
     ["Observaciones:", Heuristics.value.OBSERVACIONH4 || '']
 ];
   const options4 = {
     startY: doc.autoTable.previous.finalY + 5,
     head: [["Código", "Descripción"]],
     body: data4,
     theme: 'grid' 
 };
 doc.autoTable(options4);


 const data5 = [
     ["H05P01:", "Se le pide confirmación al usuario antes de realizar una acción crítica (eliminar, aceptar, etc):  " + aprobadoNoAprobado(Heuristics.value.H05P01) ],
     ["H05P02:", "El sistema provee mensajes fáciles de entender que previenen posibles errores: " + aprobadoNoAprobado( Heuristics.value.H05P02)],
     ["H05P03:", "El sistema ofrece métodos de selección a los usuarios como alternativas para el ingreso datos: " + aprobadoNoAprobado(Heuristics.value.H05P03) ],
     ["H05P04:", "los campos de entrada de datos contienen valores por defecto cuando corresponde: " + aprobadoNoAprobado( Heuristics.value.H05P05) ],
     ["H05P05:", "Todos los datos de entrada son validados: " + aprobadoNoAprobado( Heuristics.value.H05P05)],
   
     // Agregar las observaciones al PDF
     ["Observaciones:", Heuristics.value.OBSERVACIONH5 || '']
 ];
 const options5 = {
     startY: doc.autoTable.previous.finalY + 5,
     head: [["Código", "Descripción"]],
     body: data5,
     theme: 'grid' 
 };
 doc.autoTable(options5);


 const data6 = [
     ["H06P01:", "Las opciones y/o funciones son fáciles de encontrar:  " + aprobadoNoAprobado( Heuristics.value.H06P01)],
     ["H06P02:", "Los principales controles de interfaz, están siempre disponibles, visibles y son de fácil acceso: " + aprobadoNoAprobado(Heuristics.value.H06P02)],
     ["H06P03:", "Los campos de entrada de datos ya llenos mantienen la información siempre recordada: " + aprobadoNoAprobado(Heuristics.value.H06P03)],
     // Agregar las observaciones al PDF
     ["Observaciones:", Heuristics.value.OBSERVACIONH6 || '']
 ];
 const options6 = {
     startY: doc.autoTable.previous.finalY + 5,
     head: [["Código", "Descripción"]],
     body: data6,
     theme: 'grid' 
 };
 doc.autoTable(options6);


 const data7 = [
     ["H07P01:", "Existen atajos para realizar tareas frecuentes:  " + aprobadoNoAprobado(Heuristics.value.H07P01)],
     ["H07P02:", "El sistema es personalizable, de acuerdo a las necesidades,características,  preferencias personales, etc., de los usuarios: " + aprobadoNoAprobado(Heuristics.value.H07P02)],
     ["H07P03:", "El sistema no pide volver a ingresar información que ya ha sido solicitada con anterioridad: " + aprobadoNoAprobado(Heuristics.value.H07P03)],
     ["H07P04:", "Las acciones que realiza el usuario toman mucho tiempo. " + aprobadoNoAprobado(Heuristics.value.H03P04)],
     ["H07P05:", "El sistema informa al usuario si la ejecución de una acción requiere mucho tiempo: " + aprobadoNoAprobado(Heuristics.value.H07P05)],
     ["H07P06:", "Al rellenar un campo, las opciones disponibles se pueden seleccionar sin tener  que escribirlas: " + aprobadoNoAprobado(Heuristics.value.H07P06)],
     ["H07P07:", "La herramienta de búsqueda es visible en todo el sistema: " + aprobadoNoAprobado(Heuristics.value.H07P07)],
     // Agregar las observaciones al PDF
     // eslint-disable-next-line vue/no-ref-as-operand
     ["Observaciones:", Heuristics.OBSERVACIONH7 || '']
 ];
 const options7 = {
     startY: doc.autoTable.previous.finalY + 5, 
     head: [["Código", "Descripción"]],
     body: data7,
     theme: 'grid' 
 };
 doc.autoTable(options7);


 const data8 = [
     ["H08P01:", "La interfaz del sistema es simple: " + aprobadoNoAprobado(Heuristics.value.H08P01)],
     ["H08P02:", "La interfaz del sistema está sobrecargada de información y elementos que distraen al usuario:  " + aprobadoNoAprobado(Heuristics.value.H08P02)],
     ["H08P03:", "Las alternativas que el usuario necesita para realizar una tarea están visibles: " +aprobadoNoAprobado(Heuristics.value.H08P03)],
     ["H08P04:", "La información presentada es simple, concisa y clara: " + aprobadoNoAprobado(Heuristics.value.H08P04)],
     ["H08P05:", "La información visible es suficiente para realizar alguna acción: " + aprobadoNoAprobado(Heuristics.value.H08P05)],
     ["H08P06:", "Hay iconos o elementos gráficos abstractos: " + aprobadoNoAprobado(Heuristics.value.H08P06)],
     ["H08P07:", "Hay iconos, controles, menús, gráficos, textos u otros elementos redundantes: " + aprobadoNoAprobado(Heuristics.value.H08P07)],
     ["H08P08:", "Hay elementos exclusivamente ornamentales: " + aprobadoNoAprobado(Heuristics.value.H08P08)],
     ["H08P09:", "El sistema presenta información repetida:  " + aprobadoNoAprobado(Heuristics.value.H08P09)],
     ["H08P010:","Los colores utilizados dan un contraste adecuado: " + aprobadoNoAprobado(Heuristics.value.H08P10)],
     ["H08P011", "Los elementos/secciones del sistema están distribuidos correctamente en todo el sistema: " + aprobadoNoAprobado(Heuristics.value.H08P11)],
     // Agregar las observaciones al PDF
     ["Observaciones:", Heuristics.value.OBSERVACIONH8 || '']
 ];
 const options8 = {
     startY: doc.autoTable.previous.finalY + 5,
     head: [["Código", "Descripción"]],
     body: data8,
     theme: 'grid'
 };
 doc.autoTable(options8);


 const data9 = [
     ["H09P01:", "Los mensajes de error son compresibles, escritos en lenguaje común, sin códigos o palabras técnicas:  " + aprobadoNoAprobado(Heuristics.value.H09P01)],
     ["H09P02:", "Los mensajes de error indican la causa del error: " + aprobadoNoAprobado( Heuristics.value.H09P02)],
     ["H09P03:", "Los mensajes de error orientan al usuario para solucion  el problema: " + aprobadoNoAprobado(Heuristics.value.H09P03)],
     ["H09P04:", "Los mensajes de error utilizan una terminología y diseño consistentes:  " + aprobadoNoAprobado(Heuristics.value.H09P04)],
     ["H09P05:", "Los mensajes de error están escritos en una forma constructiva, de tal manera que no atribuyen la culpa ni ofenden al usuario: " + aprobadoNoAprobado(Heuristics.value.H09P05)],
     ["H09P06:", "Los mensajes de error usan palabras violentas u hostiles: " + aprobadoNoAprobado(Heuristics.value.H09P06)],
     // Agregar las observaciones al PDF
     ["Observaciones:", Heuristics.value.OBSERVACIONH9 || '']
 ];
 const options9 = {
     startY: doc.autoTable.previous.finalY + 5,
     head: [["Código", "Descripción"]],
     body: data9,
     theme: 'grid' 
 };
 doc.autoTable(options9);


 const data10 = [
     ["H10P01:", "El sistema ofrece una ayuda clara y simple. " + aprobadoNoAprobado(Heuristics.value.H10P01)],
     ["H10P02:", "La ayuda esta expresada en el lenguaje del usuario, libre de jergas y modismos: " + aprobadoNoAprobado(Heuristics.value.H10P02)],
     ["H10P03:", "La ayuda es fácil de encontrar, entender y aplicar: " + aprobadoNoAprobado(Heuristics.value.H10P03)],
     ["H10P04:", "La ayuda siempre está visible y disponible: " + aprobadoNoAprobado(Heuristics.value.H10P04)],
     ["H10P05:", "La estructura de la información de la ayuda se distingue fácilmente: " +aprobadoNoAprobado(Heuristics.value.H10P05) ],
     ["H10P06:", "Las instrucciones de ayuda siguen la secuencia de acciones a realizar por el  usuario para alcanzar una tarea: " + aprobadoNoAprobado(Heuristics.value.H10P06)],
     ["H10P07:", "La interfaz de la ayuda es consistente con la interfaz de todo el sistema: " + aprobadoNoAprobado(Heuristics.value.H10P07)],
     ["H10P08:", "En la ayuda la información es fácil de encontrar: " + aprobadoNoAprobado(Heuristics.value.H10P08)],
     ["H10P09:", "En el sistema existe ayuda contextual que guía al usuario respecto al uso de los elementos: " + aprobadoNoAprobado(Heuristics.value.H10P09)],
     // Agregar las observaciones al PDF
     ["Observaciones:", Heuristics.value.OBSERVACIONH10 || '']
 ];
 // eslint-disable-next-line no-unused-vars
 const options10 = {
     startY: doc.autoTable.previous.finalY + 5, 
     head: [["Código", "Descripción"]],
     body: data10,
     theme: 'grid' 
 };

      // Crear una URL para el Blob
      const pdfBlob = doc.output('blob');
      const pdfUrl = URL.createObjectURL(pdfBlob);

      // Abrir el PDF en una nueva pestaña
      const eventoPDF = new CustomEvent('pdf-generado', { detail: pdfUrl });
      window.dispatchEvent(eventoPDF);
      window.open(pdfUrl, '_blank');
      doc.save('resultado_checklist.pdf');
    }
  }
};
</script>
