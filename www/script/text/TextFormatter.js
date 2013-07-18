/**
 * Class giving tools to handle the text formating.
 * @author Matrat Erwan
 **/

function TextFormatter() {

}

/**
 * format given number to the corresponding bit flow.
 * 1000 => 1000 kB
 * 12500 => 13 Mb
 **/
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
};

