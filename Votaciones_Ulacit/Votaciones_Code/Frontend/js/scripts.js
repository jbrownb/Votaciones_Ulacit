$(document).ready(function() {

    $("#btn_fiscal").click(function(e) {

        var id_fiscal = $('#id_fiscal').val()
        var password = $('#password_fiscal').val()
        console.log(id_fiscal);
        console.log(password);

        var Id = id_fiscal;
        var Password = password;

        e.preventDefault();

        $.ajax({
            type: "POST",
            url: "http://localhost:8000/iniciar_fiscal/",
            contentType: "application/x-www-form-urlencoded",
            data: {
                Id,
                Password
            },
            success: function(result) {
                if (result.Status == ("CORRECTO")) {
                    id_fiscal = result.ID_FISCAL;
                    swal({
                        text: 'Bienvenido ' + id_fiscal,
                        confirmButtonColor: '#F98C16',
                        confirmButtonText: 'Ingresar',
                        allowOutsideClick: false,
                        allowEscapeKey: false,
                        showLoaderOnConfirm: true
                    }).then(function() {
                        //Editar con la ruta del proyecto
                        $(location).attr('href', 'index.html');
                    })

                } else {
                    if (result.Status == ("ID_Incorrecto")) {
                        swal({
                            title: 'Acceso denegado',
                            type: 'error',
                            text: 'El id del fiscal no está registrado',
                            showCloseButton: true,
                            confirmButtonText: 'Ok',
                            confirmButtonColor: '#F98C16'
                        })
                    } else if (result.Status == ("Pass_Incorrecto")) {
                        swal({
                            title: 'Acceso denegado',
                            type: 'error',
                            text: 'La contraseña es incorrecta',
                            showCloseButton: true,
                            confirmButtonText: 'Ok',
                            confirmButtonColor: '#F98C16'
                        })
                    }
                }

            },
            error: function(result) {
                alert('error' + result);
            }
        });
    });







    $("#btn_cerrar_sesion").click(function(e) {
        e.preventDefault();

        $.ajax({
            type: "POST",
            url: "http://localhost:8000/cerrar_sesion/",
            contentType: "application/x-www-form-urlencoded",
            data: {

            },
            success: function(result) {
                if (result.Status == ("Sesión cerrada")) {
                    swal({
                        text: 'Se cierra sesión, no quedan fiscales activos en el sistema',
                        type: 'warning',
                        confirmButtonColor: '#3F2A55',
                        confirmButtonText: 'Ok',
                        allowOutsideClick: false,
                        allowEscapeKey: false,
                        showLoaderOnConfirm: true
                    }).then(function() {
                        //Editar con la ruta del proyecto
                        $(location).attr('href', 'cambio_fiscal.html');
                    })

                } else {
                    alert('Error al cerrar sesión');
                }
                console.log(result.Status);
            },
            error: function(result) {
                alert('error' + result);
            }
        });
    });



    $("#btn_cambio_fiscal").click(function(e) {
        $(location).attr('href', 'cambio_fiscal.html');
    });



    $("#btn_voto").click(function(e) {
        $(location).attr('href', 'voto.html');
    });




    $("#btn_buscar_estudiante").click(function(e) {
        var id_estudiante = $('#id_estudiante_buscar').val()

        e.preventDefault();

        $.ajax({
            type: "POST",
            url: "http://localhost:8000/buscar_votante",
            contentType: "application/x-www-form-urlencoded",
            data: {
                id_estudiante
            },
            success: function(result) {
                if (result.ID_ESTUDIANTE == ("No_encontrado")) {
                    swal({
                        title: 'Sin resultado',
                        type: 'error',
                        text: 'Estudiante no encontrado, verifique la identificación',
                        showCloseButton: true,
                        confirmButtonText: 'Ok',
                        confirmButtonColor: '#F98C16'
                    })
                    //Editar con la ruta del proyecto
                    //$(location).attr('href','index.html');
                } else {

                    $("#nombre").text(result.NOMBRE);

                    var escuelas = result.ESCUELAS;
                    var nombre_escuelas = [];
                    var texto_escuelas = "";

                    for (var posicion in escuelas) {
                        nombre = escuelas[posicion].ESCUELA;
                        console.log(nombre);
                        nombre_escuelas.push(nombre);
                        texto_escuelas += nombre + "     "
                    }

                    $("#escuelas").text(texto_escuelas);

                    var estado = result.ESCUELAS[0].ESTADO_VOTO;
                    $("#estado").text(estado);

                    if (estado == ("Activo") || estado == "Terminado") {
                        $('#btn_habilitar').attr("disabled", true);

                    }

                }
            },
            error: function(result) {
                alert('error' + result);
            }
        });
    });



    $("#btn_habilitar").click(function(e) {

        var id_estudiante = $('#id_estudiante_buscar').val()

        e.preventDefault();

        $.ajax({
            type: "POST",
            url: "http://localhost:8000/habilitar_voto",
            contentType: "application/x-www-form-urlencoded",
            data: {
                id_estudiante
            },
            success: function(result) {
                $("#estado").text("Activo");

                $(location).attr('href', 'index.html');
            },
            error: function(result) {
                alert('error' + result);
            }
        });
    });


    $("#btn_generarpapeleta").click(function(e) {
        e.preventDefault();
        var id_estudiante = $('#input_id').val()


        if (id_estudiante) {
            $.ajax({
                type: "GET",
                url: "http://localhost:8000/papeletaEstudiante/id=" + id_estudiante,
                success: function(result) {
                    console.log(result);
			
			ArrayEscuelaPartido = [];

                    if (result.ESTADO == "CORRECTO") {

                        if (result.ESCUELAS.length > 0) {

                            for (var posicion in result.ESCUELAS) {
                                if (result.ESCUELAS[posicion].Partidos.length > 0) {
                                    ArrayEscuelaPartido.push("True");
                                } else {
                                    ArrayEscuelaPartido.push("False");
                                }
                            }

                            if (ArrayEscuelaPartido.includes("True")) {
                                window.location.href = 'terminal_muestra.html' + '#' + id_estudiante;
                                $("#label_nombre").text(result.ID_ESTUDIANTE);
                            } else {
                                alert("Su escuela(s) no tiene partidos asociados");
                            }


                        } else if (result.ESCUELAS.length == 0) {
                            swal({
                                title: 'No habilitado',
                                type: 'warning',
                                text: 'El estudiante ya votó o no existen partidos disponibles',
                                showCloseButton: true,
                                confirmButtonText: 'Ok',
                                confirmButtonColor: '#3F2A55'
                            })

                        }
                    } else if (result.ESTADO == "INCORRECTO") {
                        swal({
                            title: 'No habilitado',
                            type: 'warning',
                            text: 'El id es incorrecto o no ha sido registrado por el fiscal',
                            showCloseButton: true,
                            confirmButtonText: 'Ok',
                            confirmButtonColor: '#3F2A55'
                        })
                    }
                }
            });
        } else {
            swal({
                title: 'Sin resultado',
                type: 'warning',
                text: 'Ingrese su id',
                showCloseButton: true,
                confirmButtonText: 'Ok',
                confirmButtonColor: '#3F2A55'
            })
        }


    });

    $("#btn_votoFinal").click(function(e) {
        e.preventDefault();

        var cantidad_papeletas = $("form").size();
        var partidos_votados = [];
        var id_estudiante = $("#label_id_estudiante").text();
        console.log(id_estudiante);

        for (var posicion_papeleta = 0; posicion_papeleta < cantidad_papeletas; posicion_papeleta++) {
            var papeleta = "papeleta" + posicion_papeleta;
            var id_partido = $("input[name=partido]:checked", "#" + papeleta).val();

            if (!isNaN(id_partido)) {
                partidos_votados.push(id_partido);
            }
        }

        if (cantidad_papeletas == partidos_votados.length) {
            for (var posicion_papeleta = 0; posicion_papeleta < cantidad_papeletas; posicion_papeleta++) {
                var papeleta = "papeleta" + posicion_papeleta;

                var id_partido = $("input[name=partido]:checked", "#" + papeleta).val();

                if (!isNaN(id_partido)) {
                    hacer_voto(e, id_partido, id_estudiante);
                }
            }
        } else {
            swal({
                title: 'Incompleto',
                type: 'warning',
                text: 'No has votado en todas las papeletas',
                showCloseButton: true,
                confirmButtonText: 'Ok',
                confirmButtonColor: '#3F2A55'
            })
        }


    });



    function hacer_voto(e, id_partido, id_estudiante) {

        var ID_PARTIDO = id_partido;
        var ID_ESTUDIANTE = id_estudiante;

        e.preventDefault();

        $.ajax({
            type: "POST",
            url: "http://localhost:8000/voto/",
            contentType: "application/x-www-form-urlencoded",
            data: {
                ID_PARTIDO,
                ID_ESTUDIANTE
            },
            success: function(result) {
                $(location).attr('href', 'terminal_vota.html');
            },
            error: function(result) {
                console.log(result);
            }
        });

    }
});
