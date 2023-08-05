/*!
 * Quasar Framework v2.11.10
 * (c) 2015-present Razvan Stoenescu
 * Released under the MIT License.
 */
(function(e,t){"object"===typeof exports&&"undefined"!==typeof module?module.exports=t():"function"===typeof define&&define.amd?define(t):(e="undefined"!==typeof globalThis?globalThis:e||self,e.Quasar=e.Quasar||{},e.Quasar.lang=e.Quasar.lang||{},e.Quasar.lang.bg=t())})(this,function(){"use strict";var e={isoName:"bg",nativeName:"български език",label:{clear:"Изчисти",ok:"OK",cancel:"Отказ",close:"Затвори",set:"Задай",select:"Избери",reset:"Отначало",remove:"Изтрий",update:"Обнови",create:"Създай",search:"Търси",filter:"Филтър",refresh:"Презареди",expand:e=>e?`Разширете "${e}"`:"Разширяване",collapse:e=>e?`Свиване на "${e}"`:"Свиване"},date:{days:"Неделя_Понеделник_Вторник_Сряда_Четвъртък_Петък_Събота".split("_"),daysShort:"Нд_Пн_Вт_Ср_Чт_Пт_Сб".split("_"),months:"Януари_Февруари_Март_Април_Май_Юни_Юли_Август_Септември_Октомври_Ноември_Декември".split("_"),monthsShort:"Яну_Фев_Мар_Апр_Май_Юни_Юли_Авг_Сеп_Окт_Ное_Дек".split("_"),firstDayOfWeek:1,format24h:!0,pluralDay:"дни"},table:{noData:"Няма данни",noResults:"Нищо не е намерено",loading:"Зареждане...",selectedRecords:e=>e>1?e+" избрани реда.":(0===e?"Няма":"1")+" избрани редове.",recordsPerPage:"Редове на страница:",allRows:"Всички",pagination:(e,t,a)=>e+"-"+t+" от "+a,columns:"Колони"},editor:{url:"URL",bold:"Удебелен",italic:"Курсив",strikethrough:"Задраскан",underline:"Подчертан",unorderedList:"Неподреден списък",orderedList:"Номериран списък",subscript:"Долен индекс",superscript:"Горен индекс",hyperlink:"Хипер-линк",toggleFullscreen:"На цял екран",quote:"Цитат",left:"Ляво подравняване",center:"Центриране",right:"Дясно подравняване",justify:"Подравняване по ширина",print:"Отпечатване",outdent:"Намали отстъпа",indent:"Увеличи отстъпа",removeFormat:"Без форматиране",formatting:"Форматиране",fontSize:"Размер на шрифта",align:"Подравняване",hr:"Вмъкни хоризонтална линия",undo:"Отмени",redo:"Повтори",heading1:"Заглавие 1",heading2:"Заглавие 2",heading3:"Заглавие 3",heading4:"Заглавие 4",heading5:"Заглавие 5",heading6:"Заглавие 6",paragraph:"Параграф",code:"Програмен код",size1:"Много малък",size2:"Малък",size3:"Нормален",size4:"Среден",size5:"Голям",size6:"Много голям",size7:"Огромен",defaultFont:"Шрифт по подразбиране",viewSource:"Виж HTML кода"},tree:{noNodes:"Няма повече възли",noResults:"Нищо не е намерено"}};return e});