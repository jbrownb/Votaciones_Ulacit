$(document).ready(function() {

            var id_estudiante = window.location.hash.substring(1);
            console.log("El id es" + id_estudiante);

            $.ajax({
                    type: "GET",
                    url: "http://localhost:8000/papeletaEstudiante/id=" + id_estudiante,
                    success: function(result) {


                        $("#label_nombre").text(result.NOMBRE);
                        $("#label_id_estudiante").text(result.ID_ESTUDIANTE);

                        var arreglo_escuelas = result.ESCUELAS
                        cantidad_escuelas = result.ESCUELAS.length;

                        for (var posicion_escuela = 0; posicion_escuela < cantidad_escuelas - 1; posicion_escuela++) {
                            $("#papeleta0").clone().attr('id', 'papeleta' + (posicion_escuela + 1)).insertAfter("#papeleta0");
                        }

                        for (var posicion_escuela = 0; posicion_escuela < cantidad_escuelas; posicion_escuela++) {

                            var papeleta = "papeleta" + posicion_escuela;
                            //console.log(papeleta);



                            nombre_escuela = result.ESCUELAS[posicion_escuela].ESCUELA;

                            $("#" + papeleta + " " + "#Nombre_Escuela").text(nombre_escuela);

                            var cantidad_partidos = result.ESCUELAS[posicion_escuela].Partidos.length;
                            console.log(cantidad_partidos);
                            escuela = result.ESCUELAS[posicion_escuela];

                            if (cantidad_partidos == 3) {

                                var partido01 = escuela.Partidos[0];
                                var partido02 = escuela.Partidos[1];
                                var partido03 = escuela.Partidos[2];

                                $("#" + papeleta + " " + "#NombrePartido01").text(partido01.NOMBRE_PARTIDO);
                                $("#" + papeleta + " " + "#NombrePartido02").text(partido02.NOMBRE_PARTIDO);
                                $("#" + papeleta + " " + "#NombrePartido03").text(partido03.NOMBRE_PARTIDO);
                                $("#" + papeleta + " " + "#btn_radio01").val(partido01.ID_PARTIDO);
                                $("#" + papeleta + " " + "#btn_radio02").val(partido02.ID_PARTIDO);
                                $("#" + papeleta + " " + "#btn_radio03").val(partido03.ID_PARTIDO);

                                $("#" + papeleta + " " + "#img_partido01").attr("src", "imgs/" + partido01.ID_PARTIDO + ".png");
                                $("#" + papeleta + " " + "#img_partido02").attr("src", "imgs/" + partido02.ID_PARTIDO + ".png");
                                //$("#"+papeleta+ " "+"#img_partido03").attr("src","imgs/"".jpg");

                            } else if (cantidad_partidos == 2) {
                                var partido01 = escuela.Partidos[0];
                                var partido02 = escuela.Partidos[1];


                                $("#" + papeleta + " " + "#NombrePartido01").text(partido01.NOMBRE_PARTIDO);
                                $("#" + papeleta + " " + "#NombrePartido02").text(partido02.NOMBRE_PARTIDO);
                                $("#" + papeleta + " " + "#btn_radio01").val(partido01.ID_PARTIDO);
                                $("#" + papeleta + " " + "#btn_radio02").val(partido02.ID_PARTIDO);

                                $("#" + papeleta + " " + "#img_partido01").attr("src", "imgs/" + partido01.ID_PARTIDO + ".png");
                                //$("#"+papeleta+ " "+"#img_partido02").attr("src","imgs/"+partido02.ID_PARTIDO+".png");

                                $("#" + papeleta + " " + "#Partido03").hide(true);
                            } else if (cantidad_partidos == 0) {

                                $("#" + papeleta + " " + "#Nombre_Escuela").text(nombre_escuela + " (NO TIENE PARTIDOS ASOCIADOS)");

                                $("#" + papeleta + " " + "#Partido01").hide(true);
                                $("#" + papeleta + " " + "#Partido02").hide(true);
                                $("#" + papeleta + " " + "#Partido03").hide(true);
                            }

                        }

                    }
                });
            });
