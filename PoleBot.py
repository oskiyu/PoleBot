import os
import random
import discord
import datetime


from datetime import timedelta
from dotenv import load_dotenv

USUARIOS = ['charliec', 'martilux2580', 'Mister Meme', 'oskiyu']
       

def read_lineas_archivo(path : str):
    '''
    str -> list(str)

    Devuelve el contenido del archivo como una lista de strings.
    Cada string es una línea del archivo.
    '''
    output = []

    with open(path, 'r') as file:
        for linea in file:
            output.append(linea)

    return output


def read_fecha_ultima_pole():
    '''
    Devuelve la fecha de la última pole, en formato datetime.

    La fecha se guarda en el archivo "date.txt" con la siguiente estuctura:

    "dd
    mm
    yyyy"

    '''
    data = read_lineas_archivo("date.txt") 
    
    day = int(data[0])
    month = int (data[1])
    year = int(data[2])

    return datetime.datetime(year,month,day)


def set_fecha_ultima_pole(fecha : datetime.datetime):
    """
    Actualiza la fecha de la última pole en el disco.
    """
    data = open("date.txt", "w")
    data.writelines([str(fecha.day) + "\n", str(fecha.month) + '\n', str(fecha.year) + '\n'])
    data.close()


def read_fecha_ultima_subpole():
    '''
    Devuelve la fecha de la última subpole, en formato datetime.

    La fecha se guarda en el archivo "subdate.txt" con la siguiente estuctura:

    "dd
    mm
    yyyy"

    '''
    data = read_lineas_archivo("subdate.txt") 
    
    day = int(data[0])
    month = int (data[1])
    year = int(data[2])

    return datetime.datetime(year, month, day)


def set_fecha_ultima_subpole(fecha : datetime.datetime):
    """
    Actualiza la fecha de la última pole en el disco.
    """
    data = open("subdate.txt", "w")
    data.writelines([str(fecha.day) + "\n", str(fecha.month) + '\n', str(fecha.year) + '\n'])
    data.close()


def get_ruta_archivo_puntuacion(nombre_usuario : str):
    """
    str -> str

    Devuelve la ruta del archivo en la que se guarda la puntuación del jugador dado.
    """
    if nombre_usuario == "charliec":
        return "charlie.txt"

    if nombre_usuario == "Mister Meme":  
        return "moha.txt"

    if nombre_usuario == "martilux2580":  
        return "martilux.txt"

    if nombre_usuario == "oskiyu": 
        return "oskiyu.txt"

    return None


def read_puntuacion(nombre : str):
    """
    Devuelve la puntuación de un usuario.
    """
    ruta = get_ruta_archivo_puntuacion(nombre)

    if ruta == None:
        raise RuntimeError("No existe puntuación para " + nombre) 

    data = open(ruta, "r")
    output = int(data.readline())
    data.close

    return output


def read_all_puntuaciones():
    """
    Devuelve una lista con los nombres de los usuarios y sus puntuaciones actuales.

    None -> list(tuple(str, int))
    """
    output = []

    for i in USUARIOS:
        output.append((i, read_puntuacion(i)))

    return output


def read_all_puntuaciones_ordenadas():
    """
    Devuelve una lista con los nombres de los usuarios y sus puntuaciones actuales, ordenados.

    None -> list(tuple(str, int))
    """
    output = read_all_puntuaciones()

    for mx in range(len(output) - 1, -1, -1):
            swapped = False

            for i in range(mx):

                if output[i][1] < output[i + 1][1]:
                    output[i], output[i + 1] = output[i + 1], output[i]
                    swapped = True

            if not swapped:
                break

    return output


def read_ranking_season_1():
    '''
    None -> list(tuple(str, int))

    Devuelve las puntuaciones de la season 1.
    '''
    data = read_lineas_archivo("ranking s1.txt")

    output = []

    for i in range(0, len(data), 2):
        output.append((data[i], int(data[i + 1])))

    return output


def read_distancia_al_anterior(usuario : str):
    '''
    Devuelve la distancia del usuario con el usuario que va delante suya.
    '''
    scores = read_all_puntuaciones_ordenadas()

    for i in range(1, len(scores)):
        if scores[i][0] == usuario:
            return scores[i - 1][1] - scores[i][1]
        
    return 0


def set_puntuacion(nombre : str, puntuacion : int):
    """
    Establece la puntuación de un usuario.
    """
    ruta = get_ruta_archivo_puntuacion(nombre)

    if ruta == None:
        raise Exception("No existe puntuación para " + nombre) 

    data = open(ruta, "w")
    data.writelines([str(puntuacion)])
    data.close

    reload()


def get_puntos_bufo(distancia : int):
    """
    int -> int

    Devuelve los puntos obtenidos por el bufo.
    """
    return int(distancia / 10.0)


def get_medalla(posicion : int):
    '''
    int -> str

    Devueve una medalla que indica la posición en el ranking.
    El primero es el 1, 2, 3... (no empieza por 0).
    '''
    if posicion == 0:
        return ":first_place:"
        
    if posicion == 0:
        return ":second_place:"
        
    if posicion == 0:
        return ":third_place:"
    
    return " "


# Distancia mínima entre una persona y la siguiente para aplicar el bufo.
MIN_DIFF_FOR_BUFF = 40

PUNTOS_POR_POLE = 2
PUNTOS_POR_SUBPOLE = 1


#Sistema de cache

frases = None
ayuda_comandos = None

puntuaciones = None

ranking_season_1 = None
ranking_historico = None

def reload():
    '''
    Recarga los archivos frases.txt, comandos_help.txy
    y todas las puntuaciones.
    '''

    #Para poder asignar valores a las variables globales,
    # en vez de que se creen variables locales con el '='.
    global frases
    global ayuda_comandos
    global puntuaciones
    global ranking_season_1
    global ranking_historico

    frases = read_lineas_archivo("frases.txt")
    ayuda_comandos = read_lineas_archivo("comandos_help.txt")

    puntuaciones = read_all_puntuaciones_ordenadas()

    ranking_season_1 = read_ranking_season_1()

    #Historico:
    ranking_historico = []

    #SUuar puntuaciones de la primera temporada
    for i in range(len(puntuaciones)):
        for j in range(len(ranking_season_1)):

            #Si los nombres son iguales, se suman los puntos
            if ranking_season_1[j][0].find(puntuaciones[i][0]) != -1:
                ranking_historico.append((puntuaciones[i][0], puntuaciones[i][1] + ranking_season_1[i][1]))

    #Reordenar
    for mx in range(len(ranking_historico) - 1, -1, -1):
        swapped = False

        for i in range(mx):
            if ranking_historico[i][1] < ranking_historico[i + 1][1]:
                ranking_historico[i], ranking_historico[i + 1] = ranking_historico[i + 1], ranking_historico[i]
                swapped = True

        if not swapped:
             break
    

#Bot

reload()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Bot('/')


#Comandos:

@client.command(
    name = "polebot reload",
    help = "Recarga los datos de PoleBot: ayuda, frases y rankings.",
    brief = "Recarga el PoleBot."
)
async def cmd_reload(context):
    '''
    Recarga las frases, los comandos y los rankings
    '''
    reload()


@client.command(
    name = "polebot di algo",
    help = "El bot dice una frase aleatoria.",
    brief = "El bot dice una frase aleatoria."
)
async def cmd_frases(context):
    '''
    Frases random
    '''
    await context.channel.send(random.choice(frases))


@client.command(
    name = "pole",
    help = "Reclama la pole.",
    brief = "Reclama la pole."
)
async def cmd_pole(context):
    '''
    Pole.
    '''
    fecha_ultima_pole = read_fecha_ultima_pole()

    if datetime.datetime.now() > fecha_ultima_pole:
        #Es una pole válida

        #Actualiza la pole en el disco duro
        fecha_ultima_pole = datetime.datetime.now()

        fecha_ultima_pole += timedelta(days = 1)
        fecha_ultima_pole = fecha_ultima_pole.replace(hour = 00, minute = 00, second = 00)

        set_fecha_ultima_pole(fecha_ultima_pole)

        #Lee la puntuación de quien ha hecho la pole
        score = read_puntuacion(context.message.author.name)

        #Comprueba si se puede aplicar el bufo
        distancia = read_distancia_al_anterior(context.message.author.name)
            
        response = ""

        #Puntos del bufo
        if distancia > MIN_DIFF_FOR_BUFF:
            score += get_puntos_bufo(distancia)
            response = context.message.author.name + ' ha hecho la pole.' + ' ¡Puntos aumentados por ir muy lejos de tu rival!' + ' Puntos obtenidos: '+ str(distancia/10)
        #Puntuación normal
        else:
            score += PUNTOS_POR_POLE
            response = context.message.author.name + ' ha hecho la pole.' 

        #Actualiza la última pole en disco
        set_puntuacion(context.message.author.name, score)
          
        await context.channel.send(response)
    

@client.command(
    name = "subpole",
    help = "Reclama la subpole.",
    brief = "Reclama la subpole."
)
async def cmd_subpole(context):
    '''
    Subpole.
    '''
    fecha_ultima_subpole = read_fecha_ultima_subpole()

    if datetime.datetime.now() > fecha_ultima_subpole:
        #Es una pole válida

        #Actualiza la pole en el disco duro
        fecha_ultima_subpole = datetime.datetime.now()

        fecha_ultima_subpole += timedelta(days = 1)
        fecha_ultima_subpole = fecha_ultima_subpole.replace(hour = 00, minute = 00, second = 00)

        set_fecha_ultima_subpole(fecha_ultima_subpole)

        #Lee la puntuación de quien ha hecho la pole
        score = read_puntuacion(context.message.author.name)
            
        score += PUNTOS_POR_SUBPOLE
        response = context.message.author.name + ' ha hecho la subpole.' 

        #Actualiza la última pole en disco
        set_puntuacion(context.message.author.name, score)

        await context.channel.send(response)


@client.command(
    name = "polebot ranking",
    help = "Muestra el ranking de la temporada actual.",
    brief = "Ranking actual."
)
async def cmd_ranking(context):
    '''
    Muestra el ranking actual.
    '''
    response = 'RANKING:' + '\n'
        
    for i in range(0, len(puntuaciones)):
        response += puntuaciones[i][0] + ": " + str(puntuaciones[i][1]) + '\n'
            
    await context.channel.send(response)


@client.command(
    name = "polebot ranking historico",
    help = "Muestra el ranking de todas las temporadas.",
    brief = "Ranking historico."
)
async def cmd_ranking_historico(context):
    '''
    Muestra el ranking historico.
    '''
    response = 'RANKING HISTORICO: \n'
        
    for i in range(len(ranking_historico)):
        response += ranking_historico[i][0] + ": " + str(ranking_historico[i][1]) + '\n'
         
    await context.channel.send(response)


@client.command(
    name = "polebot ranking season 1",
    help = "Muestra el ranking de la primera temporada.",
    brief = "Ranking S1."
)
async def cmd_ranking_s1(context):
    response = 'RANKING SEASON 1: \n'

    for i in range(0, len(ranking_season_1)):
        response += ranking_season_1[i][0] + ": " + ranking_season_1[i][1]

    await context.channel.send(response)  


@client.command(
    name = "polebot ayuda",
    help = "Muestra ayuda de los comandos.",
    brief = "Help."
)
async def cmd_ayuda(context):
    response = ""

    for i in ayuda_comandos:
        response += i + '\n'
        
    await context.channel.send(response)

    
@client.command(
    name = "polebot git",
    help = "Muestra el repositorio open-source de PoleBot..",
    brief = "PoleBot en GitHub."
)
async def cmd_git(context):
    await context.channel.send('https://github.com/cva21/PoleBot')


@client.command(
    name = "polebot version",
    help = "Muestra la versión de PoleBot.",
    brief = "Versión de PoleBot.."
)
async def cmd_version(context):
    response = 'PoleBot Versión Alpha 0.0.4.0 por CharlieC & oskiyu' + '\n' + 'Última actualización : 28/06/2021'
    await context.channel.send(response)    

    
@client.command(
    name = "polebot si o no",
    help = "PoleBot decide por ti.",
    brief = "Kys PoleBot."
)
async def cmd_siono(context):
    await context.channel.send(random.choice(["si","no"]))


@client.command(
    name = "polebot ppt",
    help = "Juega a piedra, papel o tijeras con PoleBot.",
    brief = "Kys PoleBot x2."
)
async def cmd_ppt(context, seleccion_player : str):
    
    CHOICES = ["piedra", "papel", "tijeras"]
        
    seleccion_polebot = random.choice(CHOICES)

    respone = ""

    if seleccion_player == seleccion_polebot:              
        response = "Empate, me has leido la mente cabron"
            
    elif seleccion_player == "piedra":
        if seleccion_polebot == "papel":
            response = "Te jodes, el papel cubre a la piedra gei"
        
        else:
            response = "Pff, romperás mis " + seleccion_polebot + " pero te rompo la cara"

    elif seleccion_player == "papel":
        if seleccion_polebot == "tijeras":
            response = "JA!, las tijeras cortan el papel pelota"  
        
        else: 
            response = "Buah, habia elegido " + seleccion_polebot + " pero eres un puto pelota y lo sabes" 

    elif seleccion_player == "tijeras":
        if seleccion_polebot == "piedra":
                response = "TOMA!, la piedra rompe a las tijeras, como lo que yo le rompo a tu novia todas las noches." 
                
        else:
           response = "Pff, habré perdido por elegir " + seleccion_polebot + " pero jamás tendrás una gótica culona la que tengo yo"  
                    
    else:
        response = "cabron, ¿eres retrasado o que?, piedra papel o tijera."
                
    await context.channel.send(response)


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Bienvenido, {member.name}, arriba España!'
    )


client.run(TOKEN)
