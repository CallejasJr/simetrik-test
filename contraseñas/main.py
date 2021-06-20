import pandas as pd

def validation(allV,pw):
    """
    Funcion para validar si una lista de keylogs se encuentran dentro de la contraseña que se le pase.

    Se itera por cada keylog en la lista allV, y se valida si los digitos se encuentren dentro de la contraseña pw

    allV: Lista
    pw: String

    Si todas las keylogs se encuentran en la contraseña, retorna True, en caso de que al menos una falle, retorna False
    junto con la keylog que no se encuentra dentro de la contraseña
    """
    for key in allV:
        pos = []
        for letra in key:
            pos.append(pw.index(letra))
        
        tamPos = len(pos)
        if tamPos>0:
            for i in range(tamPos-1):
                if pos[i]>pos[i+1]:
                    return False, key
    return True, ''

def changePos(value,pos1,pos2):
    """
    Funcion para cambiar de posición los caracteres de un String.

    value: string
    pos1: int
    pos2: int
    """

    newValue = ''
    for i in range(len(value)):
        if i==pos2:
            newValue+=value[pos1]
        elif i==pos1:
            newValue+=value[pos2]
        else:
            newValue+=value[i]
    return newValue

def checkPattern(key,pw, allV):
    """
    Función para validar si un keylog se encuentra dentro de la contraseña que se le pase.

    En caso de que no se encuentre ningún dígito de la contraseña, retorna un vector notFound con los dígitos que no están 
    para que se agregen, si los dígitos se encuentran, pero no cumplen el patrón, intentará hacer cambios en la posición de los digítos
    para que se cumpla el patrón sin necesidad de agregarlos. En caso que después de 5 intentos de movimientos entre digitos no se logre ajustar la contraseña para aceptar el keylog actual
    junto con los anteriores, se agregarán los dígitos de la keylog actual al final de la contraseña.

    key: string
    pw: string
    allV: lista

    retorna pos, un entero para la cantidad e dígitos que se encuentran en la contraseña, una lista notFound para pasar los digitos faltantes que se deben agregar,
    y una contraseña pw, newpwd en caso de ser ajustada para aceptar nuevos patrones
    """
    pos = []
    notFound = []
    newpw = pw
    lenAllV = len(allV)
    responseValidation = True

    for letra in key:
        try:
            pos.append(pw.index(letra))
        except Exception as error:
            if str(error)=='substring not found':
                notFound.append(letra)
    
    tamPos = len(pos)
    if tamPos>0:
        for i in range(tamPos-1):
            if pos[i]>pos[i+1]:
                newpw = changePos(newpw,pos[i],pos[i+1])
    
        for i in range(5):
            if lenAllV>0:
                responseValidation, k = validation(allV,newpw)
                if responseValidation:
                    break
                else:
                    p,n,newpw = checkPattern(k,newpw,[])

    if responseValidation:
        return tamPos, notFound, newpw
    else:
        return tamPos, [i for i in key], pw

def main():
    # Se lee el archivo txt con las keylogs con pandas
    df = pd.read_csv('keylog.txt',encoding='utf-8')
    df['contraseñas'] = df['contraseñas'].astype('str')


    pw = ''
    validations = []
    for contras in df['contraseñas']:
        print('------'*5)
        print('pw actual:',pw)
        print('buscando keylog:',contras)
        posiciones, notF, pw = checkPattern(contras,pw,validations)
        lenContras = len(contras)
        lenNumNoEncontrados = len(notF)
        if lenNumNoEncontrados==lenContras:
            print(contras,'No encontrado en PW')
            pw += contras
            validations.append(contras)
        elif lenNumNoEncontrados>0:
            for digito in notF:
                print('agregando digito no encontrado',digito)
                pw+=digito
            posiciones, notF, pw = checkPattern(contras,pw,validations)
        elif posiciones == lenContras:
            print('Keylog OK')
            validations.append(contras)

    print('------'*5) 
    print('\n\nLa contraseña más corta para todas las secuencias es:',pw)

if __name__ == "__main__":
    main()