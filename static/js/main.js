(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {

        var title = document.title;

        var progressbar = $('#progressbar');
        var one = $('#one');
        var two = $('#two');
        var three = $('#three')


        var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))

        var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl)
        })

        /* CKEDITOR.replace('placedescription', {
            language: 'es',
            extraPlugins: 'editorplaceholder,autogrow',
            editorplaceholder: 'Describe el lugar en el cual realizaste las mediciones; toda la información se guarda, incluyendo el formato del texto, imágenes, tablas, etc...',
            autoGrow_minHeight: 250,
            autoGrow_maxHeight: 400,
            removePlugins: 'resize'
        }); */

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

                break;

            case "Resumen del Análisis · RS Report":

                progressbar.prop('style', 'width: 100%;');

                two.removeClass('btn-secondary');
                two.addClass('btn-primary');

                three.removeClass('btn-secondary');
                three.addClass('btn-primary');

                var map = L.map('mapid').setView([5.567541725282831, -73.33807725929755], 17);

                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                }).addTo(map);

                L.marker([5.567541725282831, -73.33807725929755]).addTo(map)
                    .bindPopup('Tooltip de Prueba')
                    .openPopup()

                break;

            case "Dashboard · RS Report":



                break;

            default:
                break;
        }

    });


})();