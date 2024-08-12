import discord
import os

intents = discord.Intents.default()
intents.message_content = True

# arquivo onde as tarefas vão ficar salvas
FILENAME = "tarefas.txt"

bot = discord.Client(intents=intents)
tarefas = []

def adicionar_tarefas(tarefa):
    with open(FILENAME, "a") as file:
        file.write(tarefa + "\n")
    tarefas.append(tarefa)

def iniciar_lista_de_tarefas():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            for line in file:
                tarefas.append(line.strip())

@bot.event
async def on_ready():
    iniciar_lista_de_tarefas()
    print(f'Fizemos login como {bot.user}')

@bot.event
async def on_message(message):
    global tarefas
    if message.channel.id != 40028922 or message.author.bot or message.author == bot.user:
        return

    # Dividindo a mensagem em partes
    command_parts = message.content.split(maxsplit=2)

    # Verificando o comando e subcomando
    if len(command_parts) >= 2 and command_parts[0] == '!tarefas':
        subcommand = command_parts[1]

        if subcommand == 'adicionar':
            if len(command_parts) == 3:
                adicionar_tarefa = command_parts[2].strip()
                if adicionar_tarefa:
                    adicionar_tarefas(adicionar_tarefa)
                    await message.channel.send(f'Tarefa -> {adicionar_tarefa} <- adicionada!')
                else:
                    await message.channel.send('Nenhuma tarefa adicionada')
            else:
                await message.channel.send('Faltando descrição da tarefa')

        elif subcommand == 'remover':
            if tarefas:
                try:
                    remover_tarefa = int(command_parts[2].strip())
                    tarefa_removida = tarefas.pop(remover_tarefa)
                    with open(FILENAME, "w") as file:
                        for tarefa in tarefas:
                            file.write(tarefa + "\n")
                    await message.channel.send(f'Tarefa -> {tarefa_removida} <- removida!')
                except (IndexError, ValueError):
                    await message.channel.send('Índice inválido!')
            else:
                await message.channel.send('Não tem tarefas!')

        elif subcommand == 'listar':
            tarefa_listar = '\n'.join(tarefas)
            if tarefa_listar:
                await message.channel.send(f'Suas tarefas são:\n{tarefa_listar}')
            else:
                await message.channel.send('Nenhuma tarefa para listar!')

    if command_parts[0] == '!juntar':
        junta_string = ' '.join(command_parts[1:])
        if junta_string:
            await message.channel.send(f'{junta_string}')
        else:
            await message.channel.send('Nenhuma string para juntar!')

#executando token do bot
bot.run('Token_do_bot')
