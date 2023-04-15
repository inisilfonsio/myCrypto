$(function () {
    var currentPage = 1;
    var elementsPerPage = 5;
    var totalElements = $('#my-list li').length;
    var totalPages = Math.ceil(totalElements / elementsPerPage);

    showPage(currentPage);

    $('.pagination').on('click', '.prev-page', function () {
        if (currentPage > 1) {
            currentPage--;
            showPage(currentPage);
        }
    });

    $('.pagination').on('click', '.next-page', function () {
        if (currentPage < totalPages) {
            currentPage++;
            showPage(currentPage);
        }
    });

    function showPage(page) {
        var start = (page - 1) * elementsPerPage;
        var end = start + elementsPerPage;

        $('#my-list li').hide();
        $('#my-list li').slice(start, end).show();

        $('.pagination button').removeAttr('disabled');

        if (currentPage == 1) {
            $('.pagination .prev-page').attr('disabled', 'disabled');
        }

        if (currentPage == totalPages) {
            $('.pagination .next-page').attr('disabled', 'disabled');
        }
    }
});

$('#cargar-movimientos').click(function () {
    currentPage++;
    $.ajax({
        url: '/inicio?page=' + currentPage + '&per_page=' + elementsPerPage,
        success: function (data) {
            if (data.movs.length > 0) {
                var newMovs = '';
                $.each(data.movs, function (index, value) {
                    newMovs += '<tr><td>' + value.fecha + '</td><td>' + value.hora + '</td><td>' + value.origen + '</td><td class="numero">' + value.invertido + '</td><td>' + value.destino + '</td><td class="numero">' + value.obtenido + '</td><td class="numero">' + value.unitario + '</td></tr>';
                });
                $('#my-list').append(newMovs);
                totalElements += data.movs.length;
                totalPages = Math.ceil(totalElements / elementsPerPage);
                $('.pagination .next-page').removeAttr('disabled');
                if (currentPage == totalPages) {
                    $('.pagination .next-page').attr('disabled', 'disabled');
                }
            } else {
                $('.pagination .next-page').attr('disabled', 'disabled');
            }
        },
        error: function () {
            alert('Ha ocurrido un error al cargar los movimientos');
        }
    });
});

