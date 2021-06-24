import os
import random
import discord
import datetime


from datetime import timedelta
from dotenv import load_dotenv

USUARIOS = ['charliec', 'martilux2580', 'Mister Meme', 'oskiyu']
        
def get_fecha_ultima_pole():
    '''
    Devuelve la fecha de la última pole, en formato datetime.

    La fecha se guarda en el archivo "date.txt" con la siguiente estuctura:

    "dd
    mm
    yyyy"

    '''
    data = open("date.txt","r") 
    
    day = int (data.readline())
    month = int (data.readline())
    year = int(data.readline())

    return datetime.datetime(year,month,day)


def set_fecha_ultima_pole(fecha : datetime.datetime):
    """
    Actualiza la fecha de la última pole en el disco.
    """
    data = open("date.txt", "w")
    data.writelines([str(fecha.day) + "\n", str(fecha.month) + '\n', str(fecha.year) + '\n'])
    data.close()


def get_fecha_ultima_subpole():
    '''
    Devuelve la fecha de la última subpole, en formato datetime.

    La fecha se guarda en el archivo "subdate.txt" con la siguiente estuctura:

    "dd
    mm
    yyyy"

    '''
    data = open("subdate.txt","r") 
    
    day = int (data.readline())
    month = int (data.readline())
    year = int(data.readline())

    return datetime.datetime(year,month,day)


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


def get_puntuacion(nombre : str):
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


def get_all_puntuaciones():
    """
    Devuelve una lista con los nombre sde los usuarios y sus puntuaciones actuales.

    None -> list(tuple(str))
    """
    output = []

    for i in USUARIOS:
        output.append((i, get_puntuacion(i)))

    return output


def set_puntuacion(nombre : str, puntuacion : int):
    """
    Establece la puntuación de un usuario.
    """
    ruta = get_ruta_archivo_puntuacion(nombre)

    if ruta == None:
        raise RuntimeError("No existe puntuación para " + nombre) 

    data = open(ruta, "w")
    data.writelines([str(puntuacion)])
    data.close


def get_puntos_bufo(distancia : float):
    """
    float -> int

    Devuelve los puntos obtenidos por el bufo.
    """
    return int(distancia / 10.0)


# Distancia mínima entre una persona y la siguiente para aplicar el bufo.
MIN_DIFF_FOR_BUFF = 40

PUNTOS_POR_POLE = 2
PUNTOS_POR_SUBPOLE = 1



#Bot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Bienvenido, {member.name}, arriba España!'
    )

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    Frases = [
        'ARRIBA ESPAÑA',
        'martilux gei',
        'oskiyu regei',
        'moha pelota',
        'charlie es el mejor desarrollador de bots',
        'charlie gei',
        'charlie regei',
        'charlie supergei',
        'charlie MEGAgei',
        'charlie MASTERGEI',
        'oskiyu regei',
        'oskiyu superguei',
        'oskiyu MASTERGEI'
    ]

    def calcularDistanciaAnterior(name):
        scores = get_all_puntuaciones()

        for mx in range(len(scores)-1, -1, -1):
            swapped = False
            for i in range(mx):
                if scores[i][1] < scores[i+1][1]:
                    scores[i], scores[i+1] = scores[i+1], scores[i]
                    swapped = True
            if not swapped:
                break

        for i in range(1, len(scores)):
            if scores[i][0] == name:
                return scores[i - 1][1] - scores[i][1]
        
        return 0

    #Funcionalidad de la funcion

    #Frase random
    if message.content.lower() == 'polebot di algo':
        await message.channel.send(random.choice(Frases))
        
    #Bot gei
    elif message.content.lower() == 'polebot eres gei':
            await message.channel.send('Tu si que eres gei, ' + message.author.name + '.')

    #Pole
    elif message.content.lower() == 'pole':
        fecha_ultima_pole = get_fecha_ultima_pole()

        if datetime.datetime.now() > fecha_ultima_pole:
            #Es una pole válida

            #Actualiza la pole en el disco duro
            fecha_ultima_pole = datetime.datetime.now()

            fecha_ultima_pole += timedelta(days = 1)
            fecha_ultima_pole = fecha_ultima_pole.replace(hour = 00, minute = 00, second = 00)

            set_fecha_ultima_pole(fecha_ultima_pole)

            #Lee la puntuación de quien ha hecho la pole
            score = get_puntuacion(message.author.name)

            #Comprueba si se puede aplicar el bufo
            distancia = calcularDistanciaAnterior(message.author.name)
            
            response = ""

            #Puntos del bufo
            if distancia > MIN_DIFF_FOR_BUFF:
                score += get_puntos_bufo(distancia)
                response = message.author.name + ' ha hecho la pole.' + ' ¡Puntos aumentados por ir muy lejos de tu rival!' + ' Puntos obtenidos: '+ str(distancia/10)
            #Puntuación normal
            else:
                score += PUNTOS_POR_POLE
                response = message.author.name + ' ha hecho la pole.' 

            #Actualiza la última pole en disco
            set_puntuacion(message.author.name, score)

            await message.channel.send(response)

    #Subpole
    elif message.content.lower() == 'subpole':
        fecha_ultima_subpole = get_fecha_ultima_subpole()

        if datetime.datetime.now() > fecha_ultima_subpole:
            #Es una pole válida

            #Actualiza la pole en el disco duro
            fecha_ultima_subpole = datetime.datetime.now()

            fecha_ultima_subpole += timedelta(days = 1)
            fecha_ultima_subpole = fecha_ultima_subpole.replace(hour = 00, minute = 00, second = 00)

            set_fecha_ultima_subpole(fecha_ultima_subpole)

            #Lee la puntuación de quien ha hecho la pole
            score = get_puntuacion(message.author.name)
            
            score += PUNTOS_POR_SUBPOLE
            response = message.author.name + ' ha hecho la subpole.' 

            #Actualiza la última pole en disco
            set_puntuacion(message.author.name, score)

            await message.channel.send(response)

    #Ranking actual
    elif message.content.lower() == 'polebot ranking':
        scores = get_all_puntuaciones()

        for mx in range(len(scores)-1, -1, -1):
            swapped = False
            for i in range(mx):
                if scores[i][1] < scores[i+1][1]:
                    scores[i], scores[i+1] = scores[i+1], scores[i]
                    swapped = True
            if not swapped:
                break

        response = 'RANKING:' + '\n'
        
        for i in range(0, len(scores)):
            response += scores[i][0] + str(scores[i][1]) + '\n'
            
        await message.channel.send(response)

    elif message.content.lower() == 'polebot ranking historico':

        data = open("charlie.txt","r")
        score1 = float (data.readline())
        data.close()
        data = open("martilux.txt","r") 
        score2 = float (data.readline())
        data.close()
        data = open("moha.txt","r") 
        score3 = float (data.readline())
        data.close()
        data = open("oskiyu.txt","r") 
        score4 = float (data.readline())
        data.close()
        #TODO: cambiar para la proxima season la forma de los scores
        scores = [['charlie :third_place: : ',score1+95],['martilux :first_place: : ',score2+278],['moha: ' ,score3+70],['oskiyu :second_place: : ',score4+115]]
        for mx in range(len(scores)-1, -1, -1):
            swapped = False
            for i in range(mx):
                if scores[i][1] < scores[i+1][1]:
                    scores[i], scores[i+1] = scores[i+1], scores[i]
                    swapped = True
            if not swapped:
                break
        response = 'RANKING HISTORICO:' + '\n' +scores[0][0]  + str(scores[0][1] ) + '\n' +scores[1][0]  + str(scores[1][1] ) + '\n' +scores[2][0]  + str(scores[2][1] ) + '\n' +scores[3][0]  + str(scores[3][1] )
        await message.channel.send(response)

    #Ranking S1
    elif message.content.lower() == 'polebot ranking season 1':
        response = 'RANKING SEASON 1: ' + '\n' + ':first_place: martilux: 278' + '\n' + ':second_place: oskiyu: 115' + '\n' + ':third_place: charlie: 95' + '\n' + 'moha: 70'
        await message.channel.send(response)    

    #Ayudas
    elif message.content.lower() == 'polebot ayuda':
        response = 'Comandos:'+ '\n' + 'polebot ranking: Muestra el ranking de poles' + '\n' + 'polebot ranking historico: Muestra el ranking historico de poles' + '\n' + 'polebot ranking season 1: Muestra el ranking de poles de la season 1'+ '\n' + 'polebot di algo: El bot dice una frase aleatoria' + '\n' + 'polebot version: La versión del bot' '\n' + 'polebot git: Link al repositorio del polebot. Contribuye al polebot o consulta el código'+ '\n' + 'polebot si o no: ¿Una decisión importante?,deja que polebot decida por ti' + '\n' + "polebot ppt: Una partidita de piedra, papel o tijeras con el polebot" 
        
        await message.channel.send(response)
        
    #Repositorio de git
    elif message.content.lower() == 'polebot git':
        await message.channel.send('https://github.com/cva21/PoleBot')

    #Version
    elif message.content.lower() == 'polebot version':
        response = 'PoleBot Versión Alpha 0.0.3.1 por CharlieC & oskiyu' + '\n' + 'Última actualización : 24/06/2021'
        await message.channel.send(response)    

    #SIono
    elif message.content.lower() == 'polebot si o no':
        await message.channel.send(random.choice(["si","no"]))

    elif message.content.lower() == 'polebot ppt':    
        #create a list of play options
        t = ["piedra", "papel", "tijeras"]
        #assign a random play to the computer
        computer = t[random.randint(0,2)]

        #set player to False
        player = False
       
        response = "Piedra, Papel o Tijeras perro"
        await message.channel.send(response)

        while player == False:
            players = await client.wait_for('message')
            if players.content.lower() == computer:              
                response = "Empate, me has leido la mente cabron" 
                player = True
            elif players.content.lower() == "piedra":
                if computer == "papel":
                    response = "Te jodes, el papel cubre a la piedra gei"
                    player = True     
                else:
                    response = "Pff, romperás mis " + computer + " pero te rompo la cara"  
                    player = True  
            elif players.content.lower() == "papel":
                if computer == "tijeras":
                    response = "JA!, las tijeras cortan el papel pelota"  
                    player = True
                else: 
                    response = "Buah, habia elegido " + computer + " pero eres un puto pelota y lo sabes" 
                    player = True
            elif players.content.lower() == "tijeras":
                if computer == "piedra":
                    response = "TOMA!, la piedra rompe a las tijeras, como lo que yo le rompo a tu novia todas las noches." 
                    player = True
                else:
                    response = "Pff, habré perdido por elegir " + computer + " pero jamás tendrás una gótica culona la que tengo yo"  
                    player = True 
            else:
                response = "cabron, ¿eres retrasado o que?, piedra papel o tijera."
                player = False
                
        #player was set to True, but we want it to be False so the loop continues
            await message.channel.send(response)           
            computer = t[random.randint(0,2)]

client.run(TOKEN)
