$(function() {
    $("#get_btn").click(function() {
        $.ajax({
            url: 'http://localhost:8000/reporte_final',
            type: 'GET',
            success: function(data) {

                var html = '<table>';

                var bandera = 0;

                for (var i = 0; i < 4; i++) {
                    html += '<tr>';
                    html += '<th>FACULTAD:</th>';
                    html += '<td>' + data['REPORTE'][i]['FACULTAD'] + '</td>';
                    html += '</tr>';
                    bandera++;
                    for (var e = 0; e < data['REPORTE'][i]['ESCUELAS'].length; e++) {

                        var arreglo = data.REPORTE;


                        var escuelas = arreglo[0]['ESCUELAS'][0]['NOMBRE_ESCUELA'];
                        html += '<tr>';
                        html += '<th>ESCUELA:</th>';
                        html += '<td>' + arreglo[i]['ESCUELAS'][e]['NOMBRE_ESCUELA'] + '</td>';
                        html += '</tr>';

                        html += '<tr>';
                        html += '<th>NOMBRE PARTIDO</th>';
                        html += '<th><span id="scnd-th-left-margin">CANTIDAD VOTOS</span></th>';
                        html += '<th>PORCENTAJE VOTOS</th>';
                        html += '</tr>';
                        var tamano = arreglo[i]['ESCUELAS'][e]['PARTIDOS'].length;

                        for (var p = 0; p < arreglo[i]['ESCUELAS'][e]['PARTIDOS'].length; p++) {

                            var arreglo_esc = data.REPORTE;
                            var partidos = arreglo[i]['ESCUELAS'][e]['PARTIDOS'][1]['NOMBRE'];

                            html += '<tr>';
                            html += '<td>' + arreglo[i]['ESCUELAS'][e]['PARTIDOS'][p]['NOMBRE'] + '</td>';
                            html += '<td><span id="td-results-left-margin">' + arreglo[i]['ESCUELAS'][e]['PARTIDOS'][p]['VOTOS'] + '</span></td>';
                            html += '<td><span id="td-porcentj-left-margin">' + arreglo[i]['ESCUELAS'][e]['PARTIDOS'][p]['PORCENTAJE_VOTOS'] + '</span></td>';
                            html += '</tr>';


                        }
                        html += '<tr>';
                        html += '<th>TOTAL VOTOS ESCUELA</th>';
                        html += '<td><span id="td-results-left-margin">' + arreglo[i]['ESCUELAS'][e]['TOTAL_VOTOS'] + '</span></td>';
                        html += '<td><span id="td-porcentj-left-margin">' + arreglo[i]['ESCUELAS'][e]['PORCENTAJE_VOTO_ESCUELA'] + '</span></td>';
                        html += '</tr>';

                        html += '<tr>';
                        html += '<th>ESTUDIANTES ACTIVOS</th>';
                        html += '<td><span id="td-results-left-margin">' + arreglo[i]['ESCUELAS'][e]['TOTAL_E_ACTIVOS'] + '</span></td>';
                        html += '<td><span id="td-porcentj-left-margin">' + arreglo[i]['ESCUELAS'][e]['PORCENTAJE_EST_ACTIVOS'] + '</span></td>';
                        html += '</tr>';

                        html += '<tr>';
                        html += '<th>ABSTENCIONISMO</th>';
                        html += '<td><span id="td-results-left-margin">' + arreglo[i]['ESCUELAS'][e]['TOTAL_ABSTENCION_ESCUELA'] + '</span></td>';
                        html += '<td><span id="td-porcentj-left-margin">' + arreglo[i]['ESCUELAS'][e]['PORCENTAJE_ABSTENCION'] + '</span></td>';
                        html += '</tr>';

                        html += '<tr>';
                        html += '<td><br></td>';
                        html += '</tr>';
                    }




                }

                html += '<tr>';
                html += '<td><br></td>';
                html += '</tr>';

                html += '<tr>';
                html += '<th>ESTUDIANTES INSCRITOS:</th>';
                html += '<td><span id="td-results-left-margin">' + data['E_REGISTRADOS']+ '</span></td>';
                html += '<td><span id="td-porcentj-left-margin">-</span></td>';
                html += '</tr>';

                html += '<tr>';
                html += '<th>TOTAL DE VOTANTES:</th>';
                html += '<td><span id="td-results-left-margin">' + data['E_VOTANTES']+ '</span></td>';
                html += '<td><span id="td-porcentj-left-margin">'+data['PORCENTAJE_VOTANTES']+'</span></td>';
                html += '</tr>';

                html += '<tr>';
                html += '<th>ABSTENCIONISMO TOTAL:</th>';
                html += '<td><span id="td-results-left-margin">' + data['E_ABSTENCION']+ '</span></td>';
                html += '<td><span id="td-porcentj-left-margin">'+data['ABSTENCION_TOTAL']+'</span></td>';
                html += '</tr>';


                html += '</table>';
                console.log(data);
                document.getElementById('tablewrapper').innerHTML = html;

            }
        });
    });
});


function myFunction() {
    window.print();
}
