import Libraries as lib

class Assistant:
    def __init__(self):
        self.listener = lib.sr.Recognizer()
        self.engine = lib.pyttsx3.init()

        self.useless_words = ['please', 'can', 'you', 'assistant', 'tell',
                              'something']
        self.bot_greeting = ['hi', 'hello']
        self.user_greeting = ['hi', 'hello', 'howdy']
        self.stop_words = ['bye', 'stop', 'quit', 'see you later']

        article = lib.Article('https://en.wikipedia.org/wiki/COVID-19')
        article.download()
        article.parse()
        article.nlp()
        text = article.text

        self.sentence_list = lib.nltk.sent_tokenize(text)

    def talk(self, text):
        self.engine.setProperty('voice', 'voices[0].id')
        self.engine.say(text)
        self.engine.runAndWait()

    def take_command(self):
        try:
            with lib.sr.Microphone() as source:
                print('listening...')
                voice = self.listener.listen(source)
                command = self.listener.recognize_google(voice)
                command = command.lower()
        except:
            pass
        return command

    def remove_useless_words(self, command):
        for useless in self.useless_words:
            if useless in command:
                command = command.replace(useless, '')
        return command

    def user_greeting_func(self, command):
        for greetings in self.user_greeting:
            if greetings in command:
                temp = lib.random.choice(self.bot_greeting)
                print('Bot: ' + temp)
                self.talk(temp)

    def index_sort(self, list_var):
        length = len(list_var)
        list_index = list(range(0, length))

        x = list_var
        for i in range(length):
            for j in range(length):
                if x[list_index[i]] > x[list_index[j]]:
                    temp = list_index[i]
                    list_index[i] = list_index[j]
                    list_index[j] = temp
        return list_index

    def bot_response_func(self, user_input):
        user_input = user_input.lower()
        self.sentence_list.append(user_input)
        bot_response = ''
        cm = lib.CountVectorizer().fit_transform(self.sentence_list)
        similarity_scores = lib.cosine_similarity(cm[-1], cm)
        similarity_scores_list = similarity_scores.flatten()
        index = self.index_sort(similarity_scores_list)
        index = index[1:]
        response_flag = 0
        j = 0

        for i in range(len(index)):
            if similarity_scores_list[index[i]] > 0.0:
                bot_response = bot_response + ' ' + self.sentence_list[index[i]]
                response_flag = 1
                j = j + 1
            if j > 2:
                break

        if response_flag == 0:
            bot_response = bot_response + ' ' + "sorry, I didn't understand your query."

        self.sentence_list.remove(user_input)

        return bot_response
