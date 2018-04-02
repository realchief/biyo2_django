/* ==========================================================
 * AdminKIT v1.5
 * tables.js
 * 
 * http://www.mosaicpro.biz
 * Copyright MosaicPro
 *
 * Built exclusively for sale @Envato Marketplaces
 * ========================================================== */ 

$(function()
{
	/* DataTables */
	/*if ($('.dynamicTable').size() > 0)
	{
		$('.dynamicTable').dataTable({
			"sPaginationType": "bootstrap",
			"sDom": "<'row-fluid'<'span6'l><'span6'f>r>t<'row-fluid'<'span6'i><'span6'p>>",
			"oLanguage": {
				"sLengthMenu": "_MENU_ records per page"
			}
		});
	}*/
	
							$('#subscribers, #reviews-table, #sent-emails').dataTable({
								"bLengthChange": true,
								"aaSorting": [ [1,'desc'] ],
								"bPaginate": true,
								"oLanguage": {
									"sProcessing":   "Proszę czekać...",
									"sLengthMenu":   "Pokaż _MENU_ pozycji",
									"sZeroRecords":  "Nie znaleziono żadnych pasujących indeksów",
									"sInfo":         "Pozycje od _START_ do _END_ z _TOTAL_ łącznie",
									"sInfoEmpty":    "Pozycji 0 z 0 dostępnych",
									"sInfoFiltered": "(filtrowanie spośród _MAX_ dostępnych pozycji)",
									"sInfoPostFix":  "",
									"sSearch":       "Szukaj:",
									"sUrl":          "",
									"oPaginate": {
									"sFirst":    "Pierwsza",
									"sPrevious": "Poprzednia",
									"sNext":     "Następna",
									"sLast":     "Ostatnia"
									}
								}})

								
								$('#events-data').dataTable( {
									"aaSorting": [ [1,'desc'] ],
									"bLengthChange": false,
									"oLanguage": {
									"sProcessing":   "Proszę czekać...",
									"sLengthMenu":   "Pokaż _MENU_ pozycji",
									"sZeroRecords":  "Nie znaleziono żadnych pasujących indeksów",
									"sInfo":         "Pozycje od _START_ do _END_ z _TOTAL_ łącznie",
									"sInfoEmpty":    "Pozycji 0 z 0 dostępnych",
									"sInfoFiltered": "(filtrowanie spośród _MAX_ dostępnych pozycji)",
									"sInfoPostFix":  "",
									"sSearch":       "Szukaj:",
									"sUrl":          "",
									"oPaginate": {
										"sFirst":    "Pierwsza",
										"sPrevious": "Poprzednia",
										"sNext":     "Następna",
										"sLast":     "Ostatnia"
										}
									},
									
								})
								
								

							$('#ordertable').dataTable({
								"bLengthChange": false,
								"bPaginate": false,
								"fnDrawCallback": function () {
										$("#ordertable tr").each(function() {
											var attr = $(this).attr('id');
											if (typeof attr !== 'undefined' && attr !== false) {
												$(this).addClass( "expander colapsed" );
											}else{
												$(this).addClass( "expander-inner" );
											}
										  
										});
									},
								"oLanguage": {
									"sProcessing":   "Proszę czekać...",
									"sLengthMenu":   "Pokaż _MENU_ pozycji",
									"sZeroRecords":  "Nie znaleziono żadnych pasujących indeksów",
									"sInfo":         "Pozycje od _START_ do _END_ z _TOTAL_ łącznie",
									"sInfoEmpty":    "Pozycji 0 z 0 dostępnych",
									"sInfoFiltered": "(filtrowanie spośród _MAX_ dostępnych pozycji)",
									"sInfoPostFix":  "",
									"sSearch":       "Szukaj:",
									"sUrl":          "",
									"oPaginate": {
									"sFirst":    "Pierwsza",
									"sPrevious": "Poprzednia",
									"sNext":     "Następna",
									"sLast":     "Ostatnia"
									}
								}})
								
								.rowGrouping({	bExpandableGrouping: true, asExpandedGroups: ["Zamówienie"], sGroupingColumnSortDirection: ["desc"] });
								

								$(".expander").bind("click", function(){
									var elm = $(this).next();
									if(elm.is(':visible')){
										$(this).removeClass("colapsed");
									}else{
										$(this).addClass("colapsed");
									}
									}).children().click(function(e) {
									});
								
});