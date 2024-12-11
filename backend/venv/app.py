from flask import Flask, request, jsonify
from flask_cors import CORS
from pyswip import Prolog

app = Flask(__name__)
CORS(app)

# Cargar el archivo de Prolog con los hechos y reglas
prolog = Prolog()
prolog.consult("gatosSE.pl")

@app.route('/sugerir-gatos', methods=['POST'])
def sugerir_gatos():
    try:
        # Recibe los datos JSON desde el frontend
        datos = request.json
        print(f"Datos recibidos: {datos}")  # Verifica los datos recibidos
        
        # Obtener las características desde los datos JSON
        caracteristicas = datos.get("caracteristicas", [])
        if not caracteristicas:
            return jsonify({
                "error": "Características no proporcionadas",
                "resultado": False
            }), 400
        
        try:
            # Convertir características a formato de lista de Prolog
            caract_prolog = '[' + ','.join([f'{c}' for c in caracteristicas]) + ']'
            print(f"Consulta Prolog: {caract_prolog}")  # Verifica la consulta generada

            # Construir la consulta de Prolog
            consulta = f"sugerir_gatos({caract_prolog}, Tipos)."
            resultados = list(prolog.query(consulta))
            
            if resultados and 'Tipos' in resultados[0]:
                tipos_gatos = resultados[0]['Tipos']
                return jsonify({
                    "resultado": True,
                    "tipos_gatos": tipos_gatos
                }), 200
            else:
                return jsonify({
                    "resultado": False,
                    "mensaje": "No se encontraron tipos de gatos con esas características"
                }), 200

        except Exception as prolog_error:
            return jsonify({
                "error": f"Error en la consulta de Prolog: {str(prolog_error)}",
                "resultado": False
            }), 400

    except Exception as e:
        return jsonify({
            "error": f"Error del servidor: {str(e)}",
            "resultado": False
        }), 500

@app.route('/enfermedades-tratamientos', methods=['POST'])
def enfermedades_tratamientos():
    try:
        datos = request.json
        print(f"Datos recibidos: {datos}")

        tipo_gato = datos.get("tipo_gato", "")
        if not tipo_gato:
            return jsonify({
                "error": "Tipo de gato no proporcionado",
                "resultado": False
            }), 400
        try:
            consulta = f"enfermedades_y_tratamientos({tipo_gato}, EnfermedadesYTratamientos)."
            resultados = list(prolog.query(consulta))
            
            if resultados and 'EnfermedadesYTratamientos' in resultados[0]:
                enfermedades_tratamientos = resultados[0]['EnfermedadesYTratamientos']
                return jsonify({
                    "resultado": True,
                    "enfermedades_tratamientos": enfermedades_tratamientos
                }), 200
            else:
                return jsonify({
                    "resultado": False,
                    "mensaje": "No se encontraron enfermedades y tratamientos para ese tipo de gato"
                }), 200

        except Exception as prolog_error:
            return jsonify({
                "error": f"Error en la consulta de Prolog: {str(prolog_error)}",
                "resultado": False
            }), 400

    except Exception as e:
        return jsonify({
            "error": f"Error del servidor: {str(e)}",
            "resultado": False
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
