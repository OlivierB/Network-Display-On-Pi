function TextFormatter() {

}

TextFormatter.formatNumber = function(number) {
	var magnitude = 'kB';
	if (number > 10000) {
		number = number / 1024;
		magnitude = 'MB';

		if (number > 10000) {
			number = number / 1024;
			magnitude = 'GB';

			if (number > 10000) {
				number = number / 1024;
				magnitude = 'TB';
			}
		}
	}
	return $.number(number) + ' ' + magnitude;
}

