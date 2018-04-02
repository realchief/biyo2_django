var resizer = function(elem) {
			$(elem).find('.box-body span').css('font-size', Math.max(Math.min($(elem).width() / (2*10), parseFloat(25)), parseFloat(14)));
			$(elem).find('.box-body span').css('line-height', Math.max(Math.min($(elem).width() / (2*10), parseFloat(25)), parseFloat(14))+'px');
			$(elem).find('.box-footer span').css('font-size', Math.max(Math.min($(elem).width() / (1.2*10), parseFloat(30)), parseFloat(14)));
			$(elem).find('.box-footer').css('line-height', Math.max(Math.min($(elem).width() / (1.2*10), parseFloat(30)), parseFloat(14))+'px');
			$(elem).find('.avatar').css('width', Math.max(Math.min($(elem).width() / (10), parseFloat(120)), parseFloat(40))+'px');

};