import time

from spellchecker import SpellChecker

class Tracker: 
    def __init__(self):
        self.__backspace = 0
        self.__num_pauses = 0
        self.__total_time_pauses = 0
        self.__last_timestamp = round(time.time())
        self.__has_paused = False
        self.__prev_diff_time = 0
        self.__has_typed = False
        self.__spell = SpellChecker()

    def reset(self):
        self.__backspace = 0
        self.__has_paused = 0
        self.__last_timestamp = round(time.time())
        self.__has_typed = False

    def __check_pauses(self):
        current_timestamp = round(time.time())
        diff_time = current_timestamp - self.__last_timestamp
        duration = 3 # 3 seconds
        if diff_time > duration: 
            self.__total_time_pauses += (diff_time - self.__prev_diff_time)
            self.__prev_diff_time = diff_time
            if not self.__has_paused:
                self.__has_paused = True
                self.__num_pauses += 1
        else:
            self.__prev_diff_time = 0
            self.__last_timestamp = round(time.time())
            self.__has_paused = False

    def key_pressed(self, event):
        self.__has_typed = True
        print(event.keysym)
        self.__check_pauses()
        if event.keysym == 'BackSpace':
            self.__backspace += 1

    def get_n_backspace(self):
        return self.__backspace
    
    def get_pauses(self):
        return {'Number of pauses': self.__num_pauses, 'Total time of pause': self.__total_time_pauses}
    
    def user_has_typed(self):
        return self.__has_typed

    def get_n_typos(self, words):
        # get all the misspelled words
        # return how many misspelled words we have
        misspelled = self.__spell.unknown(words)
        return len(misspelled)