from flask import Flask,request,json

import json
from flask import g
import pymysql
from flask import Flask
from flask import g
from flask import Response
from flask import request
import json
from flask_cors import CORS, cross_origin



#SQL Configurations

app = Flask(__name__)
CORS(app)

@app.before_request
def db_connect():
  g.conn = pymysql.connect(host='127.0.0.1',
                             user='votaciones',
                             password='votaciones',
                             db='votaciones_ulacit',
                             charset='utf8mb4',
                             autocommit=True)
  g.cursor = g.conn.cursor()


@app.after_request
def db_disconnect(response):
      g.cursor.close()
      g.conn.close()
      return response


def query_db(query, args=(), one=False):
  g.cursor.execute(query, args)
  rv = [dict((g.cursor.description[idx][0], value)
     for idx, value in enumerate(row)) for row in g.cursor.fetchall()]
  return (rv[0] if rv else None) if one else rv


@app.route('/iniciar_fiscal/', methods=['GET','POST'])
def iniciar_fiscal():

    print(request.form)

    if request.method == 'POST':
        id = request.form['Id']
        password=request.form['Password']

        try:
            # Read a single record

            result = query_db("SELECT * FROM T_fiscal WHERE ID_FISCAL= %s",id)
            print(result)

            if not result:

                data={'Status':'ID_Incorrecto','ID_FISCAL':'Null'}

            else:
                if result[0]["CONTRASENA"] == password:
                    data = {"Status": "CORRECTO", "ID_FISCAL": id}

                    fiscal_activo=query_db("SELECT * FROM fiscal_activo")
                    #print(fiscal_activo)
                    if not fiscal_activo:
                        g.cursor.execute("INSERT INTO fiscal_activo VALUES (1,%s)", id)
                        #print("insert fiscal")
                    else:
                        g.cursor.execute("UPDATE fiscal_activo SET ID_FISCAL=%s where ID_FISCAL_ACTIVO=1",id)
                        #print("update fiscal")

                else:
                    data = {"Status": "Pass_Incorrecto", "ID_FISCAL": id}

        finally:
            final_response = json.dumps(data)
            resp = Response(final_response, status=200, mimetype='application/json')
            return resp

    else:
        return "error"



@app.route('/papeletaEstudiante/id=<id_estudiante>', methods=['GET'])
def papeletaEstudiante(id_estudiante):

    try:
        # Read a single record
        bitacora = query_db("SELECT * FROM t_bitacora WHERE ID_ESTUDIANTE= %s",id_estudiante)

        data=""
        escuelas={}
        Arreglo_Partidos=[]
        Partido={}
        Diccionario_Escuelas={}
        Arreglo_escuelas=[]

        Diccionario_Papeleta={}

        if not bitacora:
            data={"ESTADO":"INCORRECTO"}
        else:
            if bitacora[0]["ESTADO_VOTO"]=='Activo':
                data="ENTRO"

                for each_bitacora_counter in range(len(bitacora)):
                    Diccionario_Escuelas={}
                    ID_ESCUELA=bitacora[each_bitacora_counter]["ID_ESCUELA"]

                    catalogo_escuela = query_db("SELECT * FROM catalogo_escuela WHERE ID_ESCUELA = %s",ID_ESCUELA)
                    Nombre_escuela=catalogo_escuela[0]["ESCUELA"]
                    escuelas["ID_ESCUELA"]=ID_ESCUELA
                    escuelas["ESCUELA"]=Nombre_escuela

                    query_partido = query_db("SELECT ID_PARTIDO,NOMBRE_PARTIDO,SIGLAS FROM t_partido WHERE ID_ESCUELA = %s",ID_ESCUELA)

                    ''''
                    for each_partido_counter in range(len(query_partido)):
                        Id_partido=query_partido[each_partido_counter]["ID_PARTIDO"]

                        Nombre_partido=query_partido[each_partido_counter]["NOMBRE_PARTIDO"]
                        Siglas=query_partido[each_partido_counter]["SIGLAS"]
                        Partido["ID_PARTIDO"]=Id_partido
                        Partido["NOMBRE_PARTIDO"]=Nombre_partido
                        Partido["SIGLAS"]=Siglas
                    '''
                    #Arreglo_Partidos.append(query_partido)

                    Diccionario_Escuelas["ID_Escuela"]=ID_ESCUELA
                    Diccionario_Escuelas["ESCUELA"]=Nombre_escuela
                    Diccionario_Escuelas["Partidos"]=query_partido
                    print("DICCIONARIO DE ESCUELAs")
                    print(Diccionario_Escuelas)
                    Arreglo_escuelas.append(Diccionario_Escuelas)
                    print("ARREGLO DE ESCUELAS")
                    print(Arreglo_escuelas)

            nombre=query_db("SELECT CONCAT(t_estudiante.NOMBRE,' ', t_estudiante.PRIMER_APELLIDO,' ',t_estudiante.SEGUNDO_APELLIDO) AS NOMBRE FROM t_estudiante WHERE ID_ESTUDIANTE=%s",id_estudiante)

            Diccionario_Papeleta["ID_ESTUDIANTE"]=id_estudiante
            Diccionario_Papeleta["NOMBRE"]=nombre[0]["NOMBRE"]
            Diccionario_Papeleta["ESCUELAS"] = Arreglo_escuelas
            Diccionario_Papeleta["ESTADO"] = "CORRECTO"
            data = Diccionario_Papeleta
    finally:

        final_response = json.dumps(data)
        resp = Response(final_response, status=200, mimetype='application/json')
        return resp



@app.route('/voto/', methods=['GET','POST'])
def voto():
    print(request.form['ID_PARTIDO'])
    print(request.form['ID_ESTUDIANTE'])

    if request.method == 'POST':
        id_partido = request.form['ID_PARTIDO']
        id_estudiante=request.form['ID_ESTUDIANTE']
        print(id_partido)

        try:
            # Read a single record

            g.cursor.execute("INSERT INTO t_voto (ID_PARTIDO) VALUES (%s)", id_partido)
            g.cursor.execute("UPDATE t_partido SET CANTIDAD_VOTOS = (CANTIDAD_VOTOS+1) WHERE ID_PARTIDO =%s",id_partido)
            g.cursor.execute("UPDATE t_bitacora SET ESTADO_VOTO='Terminado' WHERE ID_ESTUDIANTE=%s AND ESTADO_VOTO='Activo' ",id_estudiante)

            data={"Estado":"Success"}


        finally:
            final_response = json.dumps(data)
            resp = Response(final_response, status=200, mimetype='application/json')
            return resp
    else:
        return "error"


@app.route('/getfiscalactivo', methods=['GET'])
def fiscalactivo():
    catalogo_escuela = query_db("SELECT * FROM fiscal_activo WHERE ID_FISCAL_ACTIVO = 1")

    final_response = json.dumps(catalogo_escuela)
    resp = Response(final_response, status=200, mimetype='application/json')
    return resp




@app.route('/cerrar_sesion/', methods=['GET','POST'])
def cerrar_sesion():
    if request.method == 'POST':

        try:
            g.cursor.execute("DELETE FROM fiscal_activo WHERE ID_FISCAL_ACTIVO=1 ")

            data = {'Status': 'Sesión cerrada'}

        finally:
            final_response = json.dumps(data)
            resp = Response(final_response, status=200, mimetype='application/json')
            return resp

    else:
        return "error"





def consulta_votante(id_estudiante):
    Diccionario_Escuelas = {}
    info_votante = query_db(
        "SELECT DISTINCT  "
        "catalogo_plan.ID_ESCUELA, catalogo_escuela.ESCUELA, t_bitacora.ESTADO_VOTO "
        "FROM plan_estudiante "
        "INNER JOIN catalogo_plan "
        "ON plan_estudiante.ID_PLAN=catalogo_plan.ID_PLAN "
        "INNER JOIN catalogo_escuela "
        "ON catalogo_plan.ID_ESCUELA=catalogo_escuela.ID_ESCUELA "
        "INNER JOIN t_estudiante "
        "ON plan_estudiante.ID_ESTUDIANTE = t_estudiante.ID_ESTUDIANTE "
        "INNER JOIN t_bitacora "
        "ON t_estudiante.ID_ESTUDIANTE = t_bitacora.ID_ESTUDIANTE AND catalogo_escuela.ID_ESCUELA = t_bitacora.ID_ESCUELA "
        "WHERE plan_estudiante.ID_ESTUDIANTE= %s", id_estudiante)

    Diccionario_Escuelas["ESCUELAS"] = info_votante

    print(info_votante)
    response = json.dumps(Diccionario_Escuelas)

    resultado_bitacora = json.dumps(Diccionario_Escuelas, ensure_ascii=False)
    return Diccionario_Escuelas


@app.route("/buscar_votante", methods=['GET', 'POST'])
def buscar_votante():
    ingresado_msg=""
    id_estudiante = request.form['id_estudiante']
    if request.method == 'POST':
        try:#busca en tabla bitacora para ver si ya pasó por el fiscal
            consulta_bitacora = query_db(
                "SELECT * FROM t_bitacora WHERE ID_ESTUDIANTE = %s",id_estudiante)
            bandera = 0
            if not consulta_bitacora:
                #ejecuta el siguiente query para ver si es estudiante y si está asociado a un plan
                select = query_db(
                    "SELECT DISTINCT plan_estudiante.ID_ESTUDIANTE, catalogo_plan.ID_ESCUELA, catalogo_escuela.ESCUELA "
                    "FROM plan_estudiante "
                    "INNER JOIN catalogo_plan "
                    "ON plan_estudiante.ID_PLAN=catalogo_plan.ID_PLAN INNER JOIN catalogo_escuela "
                    "ON catalogo_plan.ID_ESCUELA=catalogo_escuela.ID_ESCUELA "
                    "WHERE plan_estudiante.ID_ESTUDIANTE = %s", id_estudiante)
                if not select:
                    # si no encuentra la cedula, quiere decir que no es estudiante o no está en algún plan
                    no_encontrado = {
                        "ID_ESTUDIANTE": "No_encontrado",
                        "NOMBRE": "No_encontrado",
                        "ESCUELAS": "No_encontrado"
                        }
                    mensaje_json = json.dumps(no_encontrado)

                    sin_resultado = Response(mensaje_json, status=200, mimetype='application/json')
                    bandera = 2

                else:#si lo encuentra agrega los datos necesarios a la tabla bitacora, con estado= Inactivo
                    bandera = 1
                    g.cursor.execute(
                        "INSERT INTO t_bitacora (ID_ESCUELA, ID_ESTUDIANTE, FECHA_HORA, ID_FISCAL, ESTADO_VOTO) "
                        "SELECT DISTINCT catalogo_plan.ID_ESCUELA, plan_estudiante.ID_ESTUDIANTE, NOW(), fiscal_activo.ID_FISCAL, 'INACTIVO' "
                        "FROM plan_estudiante "
                        "INNER JOIN catalogo_plan "
                        "ON plan_estudiante.ID_PLAN=catalogo_plan.ID_PLAN "
                        "INNER JOIN catalogo_escuela "
                        "ON catalogo_plan.ID_ESCUELA=catalogo_escuela.ID_ESCUELA "
                        "INNER JOIN fiscal_activo "
                        "WHERE plan_estudiante.ID_ESTUDIANTE= %s",id_estudiante)

                    #despues de que se inserta la informacion, devuelve nombre, escuela y estado_voto tiene que ser INACTIVO.

                    consulta = consulta_votante(id_estudiante)

                    Diccionario_resultado = {}

                    nombre = query_db(
                        "SELECT CONCAT(t_estudiante.NOMBRE,' ', t_estudiante.PRIMER_APELLIDO,' ',t_estudiante.SEGUNDO_APELLIDO) AS NOMBRE FROM t_estudiante WHERE ID_ESTUDIANTE=%s",
                        id_estudiante)

                    Diccionario_resultado["ID_ESTUDIANTE"] = id_estudiante;
                    Diccionario_resultado["NOMBRE"] = nombre[0]["NOMBRE"]
                    Diccionario_resultado["ESCUELAS"] = consulta_votante(id_estudiante)["ESCUELAS"]


                    resultado_insert = json.dumps(Diccionario_resultado, ensure_ascii=False)

            else:
                #si hay resultado en bitacora devuelve la info de la vista (nombre, escuela, estado)
                  #si estado = activo, el boton Habilitar voto permanece inactivo, si estado = inactivo, se habilita el voto
                  #se cambia estado a activo, si ya votboton habilitat voto permaneceó, el boton habilitat voto permanece inactivo.

                consulta= consulta_votante(id_estudiante)

                Diccionario_resultado={}

                nombre= query_db("SELECT CONCAT(t_estudiante.NOMBRE,' ', t_estudiante.PRIMER_APELLIDO,' ',t_estudiante.SEGUNDO_APELLIDO) AS NOMBRE FROM t_estudiante WHERE ID_ESTUDIANTE=%s",id_estudiante)

                Diccionario_resultado["ID_ESTUDIANTE"]=id_estudiante;
                Diccionario_resultado["NOMBRE"]=nombre[0]["NOMBRE"]
                Diccionario_resultado["ESCUELAS"]=consulta_votante(id_estudiante)["ESCUELAS"]

                resultado_bitacora = json.dumps(Diccionario_resultado, ensure_ascii=False)

        finally:
            if bandera == 0:
                #muestra nombre, escuela y estado_voto tiene que ser ACTIVO o EFECTUADO.
                resp = Response(resultado_bitacora, status=200, mimetype='application/json')

                return resp
            elif bandera == 1:
                print("Ingresado a bitacora")
                resp = Response(resultado_insert, status=200, mimetype='application/json')
                return resp
            else:
                return sin_resultado
    else:
        return "Error"


@app.route("/habilitar_voto", methods=['POST'])
def habilitar_voto():
    id_estudiante = request.form['id_estudiante']
    actualizar_estado= query_db("UPDATE t_bitacora SET ESTADO_VOTO='Activo' WHERE ID_ESTUDIANTE=%s", id_estudiante)
    data = json.dumps(actualizar_estado, ensure_ascii=False)
    resp = Response(data, status=200, mimetype='application/json')
    return resp




@app.route('/arregloEscuelas/id=<id_estudiante>', methods=['GET'])
def arregloEscuelas(id_estudiante):

        Diccionario_Escuelas={}
        info_votante = query_db(
            "SELECT DISTINCT CONCAT(t_estudiante.NOMBRE,' ', t_estudiante.PRIMER_APELLIDO,' ',t_estudiante.SEGUNDO_APELLIDO) AS NOMBRE, "
            "plan_estudiante.ID_ESTUDIANTE, "
            "catalogo_plan.ID_ESCUELA, catalogo_escuela.ESCUELA, t_bitacora.ESTADO_VOTO "
            "FROM plan_estudiante "
            "INNER JOIN catalogo_plan "
            "ON plan_estudiante.ID_PLAN=catalogo_plan.ID_PLAN "
            "INNER JOIN catalogo_escuela "
            "ON catalogo_plan.ID_ESCUELA=catalogo_escuela.ID_ESCUELA "
            "INNER JOIN t_estudiante "
            "ON plan_estudiante.ID_ESTUDIANTE = t_estudiante.ID_ESTUDIANTE "
            "INNER JOIN t_bitacora "
            "ON t_estudiante.ID_ESTUDIANTE = t_bitacora.ID_ESTUDIANTE AND catalogo_escuela.ID_ESCUELA = t_bitacora.ID_ESCUELA "
            "WHERE plan_estudiante.ID_ESTUDIANTE= %s", id_estudiante)
        Diccionario_Escuelas["ID_ESTUDIANTE"] = id_estudiante
        Diccionario_Escuelas["ESCUELAS"] = info_votante

        print(info_votante)
        response = json.dumps(Diccionario_Escuelas)
        resp = Response(response, status=200, mimetype='application/json')
        return resp


@app.route("/reporte_final")
def reporteFinal():

    facultad = query_db("SELECT * FROM catalogo_facultad")


    reporte_final = []
    array_facultades = []

    for eachfacultad in range(len(facultad)):

        array_info_facultad = []

        VAR_ID_FACULTAD = facultad[eachfacultad]["ID_FACULTAD"]
        VAR_NOMBRE_FACULTAD = facultad[eachfacultad]["Descripcion"]

        escuela = query_db("SELECT * FROM catalogo_escuela WHERE ID_FACULTAD = %s", VAR_ID_FACULTAD)

        array_escuelas = []
        agrega_info = False
        for eachEscuela in range(len(escuela)):

            array_info_escuelas = []

            VAR_ID_ESCUELA = escuela[eachEscuela]["ID_ESCUELA"]
            VAR_NOMBRE_ESCUELA = escuela[eachEscuela]["ESCUELA"]
            partido = query_db("SELECT * FROM t_partido WHERE ID_ESCUELA = %s", VAR_ID_ESCUELA)
            array_partidos = []

            #selecciona y suma los votos de todos los partidos pertenecientes a una escuela, incluyendo el partido nulo
            votos_escuela = query_db("SELECT COUNT(t_voto.ID_VOTO) AS VOTOS_ESCUELA FROM t_voto INNER JOIN t_partido "
                                         "ON t_voto.ID_PARTIDO = t_partido.ID_PARTIDO WHERE t_partido.ID_ESCUELA = %s",VAR_ID_ESCUELA)
            total_votos_escuela = votos_escuela[0]["VOTOS_ESCUELA"]

            #selecciona la cantidad de estudiantes activos pertenicientes a una escuela
            estudiantes_escuela = query_db("SELECT count(plan_estudiante.ID_ESTUDIANTE) AS ESTUDIANTES_ESCUELA FROM plan_estudiante "
                                           "INNER JOIN catalogo_plan ON plan_estudiante.ID_PLAN=catalogo_plan.ID_PLAN "
                                           "INNER JOIN catalogo_escuela ON catalogo_plan.ID_ESCUELA=catalogo_escuela.ID_ESCUELA "
                                           "WHERE catalogo_plan.ID_ESCUELA = %s", VAR_ID_ESCUELA)
            total_estudiantes_escuela = estudiantes_escuela[0]["ESTUDIANTES_ESCUELA"]

            porcentaje_abstencion=0
            try:
                abstencion = int(total_estudiantes_escuela)-int(total_votos_escuela)
                porcentaje_abstencion = str(round((abstencion / int(total_estudiantes_escuela))*100,2)) +"%"
            except ZeroDivisionError:
                error = "sin retorno"


            for eachPartido in range(len(partido)):
                VAR_NOMBRE_PARTIDO = partido[eachPartido]["NOMBRE_PARTIDO"]
                VAR_CANTIDAD_VOTOS = partido[eachPartido]["CANTIDAD_VOTOS"]
                VAR_ID_PARTIDO = partido[eachPartido]["ID_PARTIDO"]

                VAR_VOTO_PARTIDO = query_db("SELECT COUNT(ID_VOTO) AS NUMERO_VOTOS FROM t_voto WHERE ID_PARTIDO = %s",
                                                VAR_ID_PARTIDO)

                VAR_CANTIDAD_VOTO_PARTIDO = VAR_VOTO_PARTIDO[0]["NUMERO_VOTOS"]

                porcentaje_voto_partido=""

                try:
                    porcentaje_voto_partido = str(round((int(VAR_CANTIDAD_VOTO_PARTIDO)/int(total_votos_escuela))*100,2))+"%"
                except ZeroDivisionError:
                    error ="sin retorno"

                if partido:
                    if VAR_CANTIDAD_VOTO_PARTIDO == VAR_CANTIDAD_VOTOS:
                        array_info_partido = []

                        array_info_partido=({"NOMBRE": VAR_NOMBRE_PARTIDO,"VOTOS" : VAR_CANTIDAD_VOTOS,"PORCENTAJE_VOTOS":porcentaje_voto_partido})
                        array_partidos.append(array_info_partido)

            if partido:#agrega al arreglo escuelas solo si la escuela tiene partidos
                array_info_escuelas=({"NOMBRE_ESCUELA": VAR_NOMBRE_ESCUELA,"PARTIDOS" : array_partidos,
                                      "TOTAL_VOTOS":str(total_votos_escuela), "TOTAL_E_ACTIVOS":total_estudiantes_escuela,
                                      "TOTAL_ABSTENCION_ESCUELA":abstencion,"PORCENTAJE_ABSTENCION":porcentaje_abstencion,"PORCENTAJE_VOTO_ESCUELA":"100%","PORCENTAJE_EST_ACTIVOS":"100%"})
                array_escuelas.append(array_info_escuelas)
                agrega_info = True

        if agrega_info:#agrega al arreglo facultad solo si la escuela tiene partidos
            array_info_facultad=({"FACULTAD":VAR_NOMBRE_FACULTAD,"ESCUELAS" : array_escuelas})
            array_facultades.append(array_info_facultad)

    e_registrados=query_db("SELECT COUNT(DISTINCT ID_ESTUDIANTE) AS E_REGISTRADOS FROM plan_estudiante;")
    total_registrados = e_registrados[0]["E_REGISTRADOS"]

    cantidad_votantes = query_db("SELECT COUNT(ID_ESTUDIANTE) AS E_VOTANTES FROM t_bitacora WHERE ESTADO_VOTO ='Terminado'")
    total_votantes = cantidad_votantes[0]["E_VOTANTES"]
    porcentaje_votantes = str(round((total_votantes / int(total_registrados)) * 100, 2)) + "%"

    abstencion_total = int(total_registrados) - int(total_votantes)
    porcentaje_abs_total = str(round((abstencion_total / int(total_registrados)) * 100, 2)) + "%"

    reporte_final= ({"E_REGISTRADOS":total_registrados,"E_VOTANTES":total_votantes,"E_ABSTENCION":abstencion_total,
                     "ABSTENCION_TOTAL":porcentaje_abs_total,"PORCENTAJE_VOTANTES":porcentaje_votantes,"REPORTE": array_facultades})

    resultado_reporte = json.dumps(reporte_final, ensure_ascii=False)
    resp = Response(resultado_reporte, status=200, mimetype='application/json')

    return resp


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
