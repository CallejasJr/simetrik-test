import json
def main():
    jsonRespuesta = {}

    partidosPorPersona = {
        'Ana':17,
        'Jose':15,
        'Juan':10,
    }
    print('La relacion entre personas y partidos es:',partidosPorPersona,'\n')
    """
    Intento obtener el total de partidos que se jugaron

    Para obtener el total de partidos se suman los partidos de todos, entre el numero de jugadores necesarios en cada partido
    Que para el pin-pong son dos personas
    """

    numJugPorPartido = 2 
    sumaPartidos = 0
    for persona in partidosPorPersona.keys():
        sumaPartidos += partidosPorPersona[persona]

    totalPartidos = int(sumaPartidos/numJugPorPartido)

    print('El total de partidos es:',totalPartidos,'\n')

    """
    Intento buscar el numero minimo de partidos que puede jugar una persona (caso donde pierda siempre)

    Como la logica del juego es que el tercer jugador espera mientras juegan los otros dos, se buscan el numero de partidas 
    jugadas si inicia en la primera partida, o si espera e inicia en la segunda
    """

    partidosPerdidosPrimera = [1 if partida%2!=0 else 0 for partida in range(1,totalPartidos+1)]
    primeraPartida = partidosPerdidosPrimera.count(1)

    print('El numero minimo de juegos al empezar en la primera partida es:',primeraPartida,'\n')

    partidosPerdidosSegunda = [1 if partida%2==0 else 0 for partida in range(1,totalPartidos+1)]
    segundaPartida = partidosPerdidosSegunda.count(1)

    print('El numero minimo de juegos al empezar en la segunda partida es:',segundaPartida,'\n')

    """
    Conociendo el numero minimo de partidas, se itera para saber si alguno de los jugadores tiene el numero de partidas
    igual al iniciar en la primera o segunda partida con todas perdidas
    """

    responseOne = None
    for persona,partidos in partidosPorPersona.items():
        if partidos==segundaPartida:
            print(persona,'perdio en el segundo partido','\n')
            responseOne = persona
        elif partidos==primeraPartida:
            print(persona,'perdio en el primer partido','\n')

    """
    Por logica se intuye que si una persona tiene el numero minimo de partidos al iniciar en el primero o segundo, perdio 
    dichos partidos, por lo que se puede obtener el nombre de la persona que pierde el segundo partido, resolviendo el primer punto
    """

    if responseOne is not None:
        jsonRespuesta['perdedorSegundoPartido']=responseOne
        jsonRespuesta['partidosPerdidos'] = []
        for i in range(len(partidosPerdidosSegunda)):
            if partidosPerdidosSegunda[i]==1:
                jsonRespuesta['partidosPerdidos'].append(i+1)

    print('La respuesta es:',jsonRespuesta)

    with open('respuesta.json', 'w') as outfile:
        json.dump(jsonRespuesta, outfile, indent=4)

if __name__ == "__main__":
    main()
