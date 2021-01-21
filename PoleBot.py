import os
import random
import discord
import datetime


from datetime import timedelta
from dotenv import load_dotenv

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
    def calcularRanking(name):
        """interpreta el nombre del usuario"""
        if name == "charliec":
            return "charlie.txt"
        if name == "Mister Man":  
            return "moha.txt"
        if name == "martilux2580":  
            return "martilux.txt"
        if name == "oskiyu": 
            return "oskiyu.txt"
    
        
    if message.content.lower() == 'polebot di algo':
        response = random.choice(Frases)
        await message.channel.send(response)
    if message.content.lower() == 'polebot eres gei':
            response = 'Tu si que eres gei, ' + message.author.name + '.'
            await message.channel.send(response)
    if message.content.lower() == 'pole':
        data = open("date.txt","r") 
        day = int (data.readline())
        month = int (data.readline())
        year = int(data.readline())
        data.close()
        data = open("date.txt","w") 
        LastPoleDate = datetime.datetime(year,month,day)
        if datetime.datetime.now() > LastPoleDate:
            LastPoleDate = datetime.datetime.now()
            LastPoleDate = LastPoleDate + timedelta(days=1)
            LastPoleDate = LastPoleDate.replace(hour=00, minute=00,second=00)
            L = [str(LastPoleDate.day)+"\n", str(LastPoleDate.month)+'\n', str(LastPoleDate.year)+'\n'] 
            data.writelines(L)
            data.close()
            data = open(calcularRanking(message.author.name),"r")
            score = int (data.readline())
            score = score+2
            data.close()
            data = open(calcularRanking(message.author.name),"w")
            data.write(str(score))
            response = message.author.name + ' ha hecho la pole.' 

            await message.channel.send(response)
        else:
            L = [str(LastPoleDate.day)+"\n", str(LastPoleDate.month)+'\n', str(LastPoleDate.year)+'\n'] 
            data.writelines(L)
            data.close()
    if message.content.lower() == 'subpole':
        data = open("subdate.txt","r") 
        day = int (data.readline())
        month = int (data.readline())
        year = int(data.readline())
        data.close()
        data = open("subdate.txt","w") 
        LastPoleDate = datetime.datetime(year,month,day)
        if datetime.datetime.now() > LastPoleDate:
            LastPoleDate = datetime.datetime.now()
            LastPoleDate = LastPoleDate + timedelta(days=1)
            LastPoleDate = LastPoleDate.replace(hour=00, minute=00,second=00)
            L = [str(LastPoleDate.day)+"\n", str(LastPoleDate.month)+'\n', str(LastPoleDate.year)+'\n'] 
            data.writelines(L)
            response = message.author.name + ' ha hecho la subpole.' 
            data.close()
            data = open(calcularRanking(message.author.name),"r")
            score = int (data.readline())
            score = score+1
            data.close()
            data = open(calcularRanking(message.author.name),"w")
            data.write(str(score))
            await message.channel.send(response)
        else:
            L = [str(LastPoleDate.day)+"\n", str(LastPoleDate.month)+'\n', str(LastPoleDate.year)+'\n'] 
            data.writelines(L)
            data.close()
    if message.content.lower() == 'polebot ranking':

        data = open("charlie.txt","r")
        score1 = int (data.readline())
        data.close()
        data = open("martilux.txt","r") 
        score2 = int (data.readline())
        data.close()
        data = open("moha.txt","r") 
        score3 = int (data.readline())
        data.close()
        data = open("oskiyu.txt","r") 
        score4 = int (data.readline())
        data.close()
        scores = [['charlie: ',score1],['martilux: ',score2],['moha: ' ,score3],['oskiyu: ',score4]]
        for mx in range(len(scores)-1, -1, -1):
            swapped = False
            for i in range(mx):
                if scores[i][1] < scores[i+1][1]:
                    scores[i], scores[i+1] = scores[i+1], scores[i]
                    swapped = True
            if not swapped:
                break
        response = scores[0][0]  + str(scores[0][1] ) + '\n' +scores[1][0]  + str(scores[1][1] ) + '\n' +scores[2][0]  + str(scores[2][1] ) + '\n' +scores[3][0]  + str(scores[3][1] )
        await message.channel.send(response)
    if message.content.lower() == 'polebot ayuda':
        response = 'Comandos:'+ '\n' + 'polebot ranking: Muestra el ranking de poles' + '\n' + 'polebot di algo: El bot dice una frase aleatoria' + '\n' + 'polebot version: La versión del bot' '\n' + 'polebot git: Link al repositorio del polebot. Contribuye al polebot o consulta el código'+ '\n' + 'polebot si o no: ¿Una decisión importante?,deja que polebot decida por ti' + '\n' + "polebot ppt: Una partidita de piedra, papel o tijeras con el polebot" 
        await message.channel.send(response)
    if message.content.lower() == 'polebot git':
        response = 'https://github.com/cva21/PoleBot'
        await message.channel.send(response)
    if message.content.lower() == 'polebot version':
        response = 'PoleBot Versión Alpha 0.0.2 por CharlieC' + '\n' + 'Última actualización : 16/01/2021'
        await message.channel.send(response)    
    if message.content.lower() == 'polebot si o no':
        respuestas = ["si","no"]
        response = random.choice(respuestas)
        await message.channel.send(response)
    if message.content.lower() == 'polebot ppt':    
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
