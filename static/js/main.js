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

                break;

            case "Dashboard · RS Report":



                break;

            default:
                break;
        }

    });


})();