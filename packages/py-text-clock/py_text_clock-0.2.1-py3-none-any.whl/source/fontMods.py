from .mylogger import logger

# 0   ITLISASTHTEN
# 1   ACFIFTEENDCO
# 2   TWENTYXFIVEW
# 3   THIRTYFTENOS
# 4   MINUTESETOUR
# 5   PASTORUFOURT
# 6   SEVENXTWELVE
# 7   NINEDIVECTWO
# 8   EIGHTFELEVEN
# 9   SIXTHREEONEG
# 10  TENSEZO'CLOCK

class TimeFonts:

    PURPLE      = '\033[95m'
    CYAN        = '\033[96m'
    DARKCYAN    = '\033[36m'
    BLUE        = '\033[94m'
    GREEN       = '\033[92m'
    YELLOW      = '\033[93m'
    RED         = '\033[91m'
    BOLD        = '\033[1m'
    UNDERLINE   = '\033[4m'
    END         = '\033[0m'    

    #          0   1   2   3   4   5   6    7   8   9   10  11  12
    line0 =  ["I","T","L","I","S","A","S", "T","H","T","E","N"," "]
    line1 =  ["A","C","F","I","F","T","E", "E","N","D","C","O"," "]
    line2 =  ["T","W","E","N","T","Y","X", "F","I","V","E","W"," "]
    line3 =  ["T","H","I","R","T","Y","F", "T","E","N","O","S"," "]
    line4 =  ["M","I","N","U","T","E","S", "E","T","O","U","R"," "]
    line5 =  ["P","A","S","T","O","R","U", "F","O","U","R","T"," "]
    line6 =  ["S","E","V","E","N","X","T", "W","E","L","V","E"," "]
    line7 =  ["N","I","N","E","D","I","V", "E","C","T","W","O"," "]
    line8 =  ["E","I","G","H","T","F","E", "L","E","V","E","N"," "]
    line9 =  ["S","I","X","T","H","R","E", "E","O","N","E","G"," "]
    line10 = ["T","E","N","S","E","Z","O'","C","L","O","C","K"," "]

    all_lines = [line0,line1,line2,line3,line4,line5,line6,line7,line8,line9,line10,]
    
    time_key_maps = {
        'it'        : [0,   0,  2],
        'is'        : [0,   3,  5],
        'one'       : [9,   8,  11],
        'two'       : [7,   9,  -1],
        'three'     : [9,   3,  8],
        'four'      : [5,   7,  11],
        'five'      : [2,   7,  11],
        'six'       : [9,   0,  3],
        'seven'     : [6,   0,  5],
        'nine'      : [7,   0,  4],
        'ten'       : [0,   9,  12],
        'TEN'       : [10,  0,  3],
        'eleven'    : [8,   6,  12],
        'twelve'    : [6,   6,  12],
        'fifteen'   : [1,   2,  9],
        'quarter'   : [1,   2,  9],
        'twenty'    : [2,   0,  6],
        'thirty'    : [3,   0,  6],
        'half'      : [3,   0,  6],
        'minutes'   : [4,   0,  7],
        'past'      : [5,   0,  4],
        'to'        : [4,   8,  10],
        "o'clock"   : [10,  6,  12]

        
    }

    def __init__(self,time_sentence) -> None:
        self.time_sentence = time_sentence
        # self.time_sentence = "it is ten minutes to twelve"
        # self.time_sentence = "it is ten o'clock"
        # self.time_sentence = "it is five minutes past zero"
        # self.time_sentence = "it is zero o'clock"
        self.get_word_locations()

    def get_word_locations(self):
        logger.debug(f'Showing matrix for "{self.time_sentence}"')
        
        # from the time as sentence, take each word
        logger.debug(self.time_sentence.split(' '))
        self.word_locations = []
        for each_word in self.time_sentence.split(' '):


            # corner case
            if each_word == 'quarter': each_word = 'fifteen'
            if each_word == 'half': each_word = 'thirty'
            if each_word == 'zero': each_word = 'twelve'

            logger.debug(f'Checking word "{each_word}" in one {["".join(s) for s in self.all_lines]}')
            

            # check that word in each line
            for each_line in self.all_lines:

                if each_word.lower() in ''.join(each_line).lower():

                    logger.debug(f'MATCH found for "{each_word.upper()}" in {"".join(each_line).upper()}')
                    word_location = self.time_key_maps.get(each_word.lower())

                    if word_location is not None:
                        logger.debug(f'Appending location of "{each_word.lower()}":{word_location}')
                        self.word_locations.append(word_location)

                    # if match is found break
                    break
            logger.debug(f'--------------------------------------')
    
    def clean_locations(self,locations):

        logger.debug(f'Attempting to clean {locations}')
        # Group the inner lists by their first element using a dictionary
        temp_dict = {}
        for inner_list in locations:
            key = inner_list[0]
            value = inner_list[1:]
            if key not in temp_dict:
                temp_dict[key] = []
            temp_dict[key].append(value)

        # Convert the dictionary to the desired format
        new_list = []
        for key, value in temp_dict.items():
            new_list.append([key] + value)

        # remove duplicates
        new_list = [[x[0]] + list(set(map(tuple, x[1:]))) for x in new_list]

        #sort the words
        new_list = [[x[0]] + sorted(x[1:], key=lambda y: y[0]) for x in new_list]
        logger.debug(f'Cleaned locations {new_list}')
        return new_list


    def show(self):
        
        # self.word_locations = [[0, 0, 2], [0, 3, 5], [0,   9,  12], [10, 0, 3], [4, 0, 7], [4, 8, 10], [10, 0, 3]]
        # self.word_locations = [[0, 0, 2], [0, 3, 5], [3,   0,  6],[5, 0, 4], [8, 6, 12]]
        # [[0, [0, 2], [3, 5]], [10, [0, 3], [0, 3]], [4, [0, 7], [8, 10]]]
        locations = self.clean_locations(self.word_locations)

        for line_no,line in enumerate(self.all_lines):
            # logger.debug(f'line #{line_no}: {line}')
            if line_no not in [s[0] for s in locations]:
                logger.debug(f'Line {line_no} not required {locations}')
                print(" ".join(line))
            else:
                for word_loc in locations:
                    if word_loc[0] == line_no:
                        logger.debug(f'{word_loc}')
                        words = word_loc[1:]
                        if len(words)==2:
                            logger.debug(f'Two words {words}')
                            print(self.CYAN + self.BOLD + 
                                    " ".join(line[words[0][0]:words[0][1]]) + self.END + " " +  
                                    " ".join(line[words[0][1]:words[1][0]]) + " " + 
                                    self.CYAN + self.BOLD + 
                                    " ".join(line[words[1][0]:words[1][1]]) + " " +  self.END + 
                                    " ".join(line[words[1][1]:])
                                    )
                        elif len(words)==3:
                            logger.debug(f'Three words {words}')
                            print(self.CYAN + self.BOLD + 
                                    " ".join(line[words[0][0]:words[0][1]]) + self.END + " " +  
                                    " ".join(line[words[0][1]:words[1][0]]) + " " + 
                                    self.CYAN + self.BOLD + 
                                    " ".join(line[words[1][0]:words[1][1]]) + " " +  self.END + 
                                    " ".join(line[words[1][1]:words[2][0]]) + " " +
                                    self.CYAN + self.BOLD +
                                    " ".join(line[words[2][0]:words[2][1]]) +                                 
                                     self.END )
                        else:
                            # if the word is beginning after few positions
                            if words[0][0] != 0:
                                print(" ".join(line[0:words[0][0]]),end=' ')

                            print(self.CYAN + self.BOLD +
                                    " ".join(line[words[0][0]:words[0][1]]) + 
                                    " " +  
                                    self.END + 
                                    " ".join(line[words[0][1]:])
                                    )

        

                        
            