/*!
 * Quasar Framework v2.11.10
 * (c) 2015-present Razvan Stoenescu
 * Released under the MIT License.
 */
(function(e,i){"object"===typeof exports&&"undefined"!==typeof module?module.exports=i():"function"===typeof define&&define.amd?define(i):(e="undefined"!==typeof globalThis?globalThis:e||self,e.Quasar=e.Quasar||{},e.Quasar.lang=e.Quasar.lang||{},e.Quasar.lang.eo=i())})(this,function(){"use strict";var e={isoName:"eo",nativeName:"Esperanto",label:{clear:"Vakigi",ok:"Okej",cancel:"Rezigni",close:"Fermi",set:"Agordi",select:"Elekti",reset:"Restartigi",remove:"Forigi",update:"Ĝisdatigi",create:"Krei",search:"Serĉi",filter:"Filtri",refresh:"Reŝargi",expand:e=>e?`Vastigi "${e}"`:"Vastigi",collapse:e=>e?`Kolapsi "${e}"`:"Kolapso"},date:{days:"Dimanĉo_Lundo_Mardo_Merkredo_Jaŭdo_Vendredo_Sabato".split("_"),daysShort:"Dim_Lun_Mar_Mer_Jaŭ_Ven_Sab".split("_"),months:"Januaro_Februaro_Marto_Aprilo_Majo_Junio_Julio_Aŭgusto_Septembro_Oktobro_Novembro_Decembro".split("_"),monthsShort:"Jan_Feb_Mar_Apr_Maj_Jun_Jul_Aŭg_Sep_Okt_Nov_Dec".split("_"),firstDayOfWeek:1,format24h:!0,pluralDay:"tagoj"},table:{noData:"Neniu datumo afiŝenda",noResults:"Neniu datumo trovita",loading:"Ŝarĝado...",selectedRecords:e=>e>0?e+" "+(1===e?"elektita linio":"elektitaj linioj")+".":"Neniu elektita linio.",recordsPerPage:"Linioj po paĝoj:",allRows:"Ĉiuj",pagination:(e,i,a)=>e+"-"+i+" el "+a,columns:"Kolumnoj"},editor:{url:"URL",bold:"Grasa",italic:"Kursiva",strikethrough:"Trastreka",underline:"Substreka",unorderedList:"Neordigita listo",orderedList:"Ordigita listo",subscript:"Indico",superscript:"Supra indico",hyperlink:"Ligilo",toggleFullscreen:"Ŝalti plenekranon",quote:"Citaĵo",left:"Ĝisrandigi maldekstren",center:"Centrigi",right:"Ĝisrandigi dekstren",justify:"Ĝisrandigi ambaŭflanke",print:"Printi",outdent:"Malkrommarĝenigi",indent:"Krommarĝenigi",removeFormat:"Forigi prezenton",formatting:"Prezento",fontSize:"Tipara grando",align:"Ĝisrandigi",hr:"Enmeti horizontalan strekon",undo:"Malfari",redo:"Refari",heading1:"Titolo 1",heading2:"Titolo 2",heading3:"Titolo 3",heading4:"Titolo 4",heading5:"Titolo 5",heading6:"Titolo 6",paragraph:"Paragrafo",code:"Kodo",size1:"Tre malgranda",size2:"Malgranda",size3:"Normala",size4:"Meza",size5:"Granda",size6:"Tre granda",size7:"Maksimuma",defaultFont:"Implicita tiparo",viewSource:"Vida Fonto"},tree:{noData:"Neniu nodo afiŝenda",noResults:"Neniu nodo trovita"}};return e});