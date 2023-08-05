/*!
 * Quasar Framework v2.11.10
 * (c) 2015-present Razvan Stoenescu
 * Released under the MIT License.
 */
(function(e,a){"object"===typeof exports&&"undefined"!==typeof module?module.exports=a():"function"===typeof define&&define.amd?define(a):(e="undefined"!==typeof globalThis?globalThis:e||self,e.Quasar=e.Quasar||{},e.Quasar.lang=e.Quasar.lang||{},e.Quasar.lang.es=a())})(this,function(){"use strict";var e={isoName:"es",nativeName:"Español",label:{clear:"Borrar",ok:"OK",cancel:"Cancelar",close:"Cerrar",set:"Establecer",select:"Seleccionar",reset:"Restablecer",remove:"Eliminar",update:"Actualizar",create:"Crear",search:"Buscar",filter:"Filtrar",refresh:"Actualizar",expand:e=>e?`Expandir "${e}"`:"Expandir",collapse:e=>e?`Ocultar "${e}"`:"Colapsar"},date:{days:"Domingo_Lunes_Martes_Miércoles_Jueves_Viernes_Sábado".split("_"),daysShort:"Dom_Lun_Mar_Mié_Jue_Vie_Sáb".split("_"),months:"Enero_Febrero_Marzo_Abril_Mayo_Junio_Julio_Agosto_Septiembre_Octubre_Noviembre_Diciembre".split("_"),monthsShort:"Ene_Feb_Mar_Abr_May_Jun_Jul_Ago_Sep_Oct_Nov_Dic".split("_"),firstDayOfWeek:1,format24h:!0,pluralDay:"dias"},table:{noData:"Sin datos disponibles",noResults:"No se han encontrado resultados",loading:"Cargando...",selectedRecords:e=>e>1?e+" filas seleccionadas.":(0===e?"Sin":"1")+" fila seleccionada.",recordsPerPage:"Filas por página:",allRows:"Todas",pagination:(e,a,r)=>e+"-"+a+" de "+r,columns:"Columnas"},editor:{url:"URL",bold:"Negrita",italic:"Itálico",strikethrough:"Tachado",underline:"Subrayado",unorderedList:"Lista Desordenada",orderedList:"Lista Ordenada",subscript:"Subíndice",superscript:"Superíndice",hyperlink:"Hipervínculo",toggleFullscreen:"Alternar pantalla completa",quote:"Cita",left:"Alineación izquierda",center:"Alineación centro",right:"Alineación derecha",justify:"Justificar alineación",print:"Imprimir",outdent:"Disminuir indentación",indent:"Aumentar indentación",removeFormat:"Eliminar formato",formatting:"Formato",fontSize:"Tamaño de Fuente",align:"Alinear",hr:"Insertar línea horizontal",undo:"Deshacer",redo:"Rehacer",heading1:"Encabezado 1",heading2:"Encabezado 2",heading3:"Encabezado 3",heading4:"Encabezado 4",heading5:"Encabezado 5",heading6:"Encabezado 6",paragraph:"Párrafo",code:"Código",size1:"Muy pequeño",size2:"Pequeño",size3:"Normal",size4:"Mediano",size5:"Grande",size6:"Muy grande",size7:"Máximo",defaultFont:"Fuente por defecto",viewSource:"Ver fuente"},tree:{noNodes:"Sin nodos disponibles",noResults:"No se encontraron nodos correspondientes"}};return e});