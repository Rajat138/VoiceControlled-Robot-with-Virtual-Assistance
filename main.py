import Client
import pywhatkit
import webbrowser
import wikipedia
import virtual_assistant
import datetime


def main():
    ip = "192.168.137.9"
    port = 80
    assistant = virtual_assistant.Assistant()
    run = True
    directions = ['forward', 'reverse', 'left', 'right']

    while run:
        command = assistant.take_command()
        print(command)

        for sw in assistant.stop_words:
            if sw in command:
                print('Bot: Bye, Have a great day')
                assistant.talk('Bye, Have a great day')
                run = False

        if not run:
            break

        command = assistant.remove_useless_words(command)

        for direction in directions:
            if direction in command:
                client = Client.Client(ip, port)
                client.send_msg(direction)

        if 'hello' in command:
            assistant.user_greeting_func(command)
            client = Client.Client(ip, port)
            client.send_msg('hello')

        elif 'coronavirus' in command or 'covid-19' in command:
            print('Bot: ' + assistant.bot_response_func(command))
            assistant.talk(assistant.bot_response_func(command))

        elif 'play' in command:
            song = command.replace('play', '')
            assistant.talk('playing ' + song)
            pywhatkit.playonyt(song)
        elif 'search' in command:
            assistant.talk('sure')
            command = command.replace('search ', '')
            webbrowser.open('https://www.google.co.in/search?q=' + command)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            assistant.talk('Current time is ' + time)
            print('Current time is ' + time)
        elif 'who' in command:
            person = command.replace('who is', '')
            info = wikipedia.summary(person, 1)
            print(info)
            assistant.talk(info)


main()
