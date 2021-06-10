
function move() {
    if ($('body').height() < $(window).height()) {
        $('footer').css({'position': 'absolute', 'bottom': '0'});
    }else{
        $('footer').css({'position': '', 'bottom': ''});
    }
}


/*$(window).resize(function(){
    move();
    console.log('Se mueve');
});*/


(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {

        var title = document.title;

        var progressbar = $('#progressbar');
        var two = $('#two');
        var three = $('#three')


        var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))

        var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl)
        })

        switch (title) {

            case "Seleccionar BD · RS Report":

                progressbar.prop('style', 'width: 0%;');

                two.removeClass('btn-primary');
                two.addClass('btn-secondary');

                three.removeClass('btn-primary');
                three.addClass('btn-secondary');

                break;

            case "Creación del Reporte · RS Report":

                progressbar.prop('style', 'width: 50%;');

                two.removeClass('btn-secondary');
                two.addClass('btn-primary');

                three.removeClass('btn-primary');
                three.addClass('btn-secondary');

                $('#sourceType option:first-child').attr('disabled', 'disabled');

                break;

            case "Resumen del Análisis · RS Report":

                progressbar.prop('style', 'width: 100%;');

                two.removeClass('btn-secondary');
                two.addClass('btn-primary');

                three.removeClass('btn-secondary');
                three.addClass('btn-primary');

                var ph = [
                    $('#max-ph').text(),
                    $('#min-ph').text(),
                    $('#med-ph').text(),
                    $('#mdna-ph').text(),
                ]

                var p_ph = [
                    $('#p-max-ph'),
                    $('#p-min-ph'),
                    $('#p-med-ph'),
                    $('#p-mdna-ph'),
                ]

                var i = 0;
                for (let item of ph) {

                    if (item >= 0 && item <= 6) {
                        p_ph[i].text('Ácido');
                        p_ph[i].addClass('bg-danger');

                    } else if (item > 6 && item < 8) {
                        p_ph[i].text('Neutro');
                        p_ph[i].addClass('bg-success');

                    } else if (item >= 8 && item <= 14) {
                        p_ph[i].text('Alcalino');
                        p_ph[i].addClass('bg-primary');
                    }

                    i++;

                }

                var od = [
                    $('#max-od').text().split(' ')[0],
                    $('#min-od').text().split(' ')[0],
                    $('#med-od').text().split(' ')[0],
                    $('#mdna-od').text().split(' ')[0],
                ]

                var p_od = [
                    $('#p-max-od'),
                    $('#p-min-od'),
                    $('#p-med-od'),
                    $('#p-mdna-od'),
                ]

                i = 0;
                for (let item of od) {

                    if (item >= 0 && item <= 33.333) {
                        p_od[i].text('Bajo');
                        p_od[i].addClass('bg-warning text-dark');

                    } else if (item > 33.333 && item < 66.666) {
                        p_od[i].text('Aceptable');
                        p_od[i].addClass('bg-info text-dark');
                    }

                    else if (item >= 66.666 && item <= 100) {
                        p_od[i].text('Alto');
                        p_od[i].addClass('bg-primary');
                    }

                    i++;

                }

                var t = [
                    $('#max-t').text().split(' ')[0],
                    $('#min-t').text().split(' ')[0],
                    $('#med-t').text().split(' ')[0],
                    $('#mdna-t').text().split(' ')[0],
                ]

                var p_t = [
                    $('#p-max-t'),
                    $('#p-min-t'),
                    $('#p-med-t'),
                    $('#p-mdna-t'),
                ]

                i = 0;
                for (let item of t) {

                    if (item >= 0 && item <= 15) {
                        p_t[i].text('Bajo');
                        p_t[i].addClass('bg-info  text-dark');

                    } else if (item > 15 && item < 25) {
                        p_t[i].text('Normal');
                        p_t[i].addClass('bg-primary');
                    } else if (item >= 25 && item <= 100) {
                        p_t[i].text('Alto');
                        p_t[i].addClass('bg-warning text-dark');
                    }

                    i++;

                }

                break;

            case"Dashboard · RS Report":
                move();
                break;

            default:
                break;
        }

    });


})();