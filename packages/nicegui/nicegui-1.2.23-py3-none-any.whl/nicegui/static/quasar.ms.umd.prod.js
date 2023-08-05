/*!
 * Quasar Framework v2.11.10
 * (c) 2015-present Razvan Stoenescu
 * Released under the MIT License.
 */
(function(a,e){"object"===typeof exports&&"undefined"!==typeof module?module.exports=e():"function"===typeof define&&define.amd?define(e):(a="undefined"!==typeof globalThis?globalThis:a||self,a.Quasar=a.Quasar||{},a.Quasar.lang=a.Quasar.lang||{},a.Quasar.lang.ms=e())})(this,function(){"use strict";var a={isoName:"ms",nativeName:"Bahasa Melayu",label:{clear:"Semula",ok:"OK",cancel:"Batal",close:"Tutup",set:"Set",select:"Pilih",reset:"Reset",remove:"Keluarkan",update:"Kemaskini",create:"Tambah",search:"Cari",filter:"Saring",refresh:"Muat semula",expand:a=>a?`Kembangkan "${a}"`:"Kembangkan",collapse:a=>a?`Runtuhkan "${a}"`:"Runtuh"},date:{days:"Ahad_Isnin_Selasa_Rabu_Khamis_Jummat_Sabtu".split("_"),daysShort:"Ahad_Isnin_Selasa_Rabu_Khamis_Jummat_Sabtu".split("_"),months:"Januari_Februari_Mac_April_Mei_Jun_Julai_Ogos_Oktober_November_Disember".split("_"),monthsShort:"Jan_Feb_Mac_Apr_Mei_Jun_Jul_Ogos_Sep_Okt_Nov_Dis".split("_"),firstDayOfWeek:1,format24h:!1,pluralDay:"hari"},table:{noData:"Tiada data tersedia",noResults:"Tiada rekod sepadan yang dijumpai",loading:"Sedang dalam proses..",selectedRecords:a=>a>1?a+" rekod terpilih.":(0===a?"tiada":"1")+" rekod terpilih.",recordsPerPage:"Rekod per halaman:",allRows:"Semua",pagination:(a,e,i)=>a+"-"+e+" dari "+i,columns:"Kolum"},editor:{url:"URL",bold:"Tebal",italic:"Italik",strikethrough:"Garis Tengah",underline:"Garis Bawah",unorderedList:"Daftar Tidak Tersusun",orderedList:"Daftar Tersusun",subscript:"Subskrip",superscript:"Superskrip",hyperlink:"Hyperlink",toggleFullscreen:"Alihkan Layar Penuh",quote:"Petikan",left:"Selaras Kiri",center:"Selaras Tengah",right:"Selaras Kanan",justify:"Selaras Sisi",print:"Cetak",outdent:"Kurangkan Indentasi",indent:"Tambah indentasi",removeFormat:"Buang Format",formatting:"Format",fontSize:"Saiz Tulisan",align:"Selaras",hr:"Masukkan Aturan Horizontal",undo:"Undo",redo:"Redo",heading1:"Heading 1",heading2:"Heading 2",heading3:"Heading 3",heading4:"Heading 4",heading5:"Heading 5",heading6:"Heading 6",paragraph:"Paragraf",code:"Kod",size1:"Paling Kecil",size2:"Agak Kecil",size3:"Normal",size4:"Sederhana",size5:"Besar",size6:"Paling Besar",size7:"Maksimum",defaultFont:"Tulisan Asal",viewSource:"Lihat sumber"},tree:{noNodes:"Tiada nod tersedia",noResults:"Tiada nod yang sesuai dijumpai"}};return a});