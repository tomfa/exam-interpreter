#coding: utf-8
'''
    The purpose of this script is to read a file of questions and store
    it to a JSON format. It was made to suit some NTNU exam that was written
    this way, so that's why it is the way it is.

    The script is built using Python 2.7.
    
    USAGE:
        Put two .txt files in the same folder, one named <title>.txt and one 
        named <title>_solution.txt. Make sure they're in the format given below.

        Run script with python quiz_interpreter.py <title>

    FORMAT <title>.txt
        Everything you write before a line defining the first question
        is ignored. So here you could have an introthing or whatever.

        Below are two questions with alternatives. You can just keep going
        on and on repeating questions.

        Oppgave 01: 
        This is a multiline question. Questions can be on one line or more,
        and can be followed by blank lines if you wish. Blank lines can be
        put anywhere, really.
        
        a) This is an option. Options should start with a letter ('a' and up),
        followed by an end parenthesis and a space. They can also be on 
        multiple lines. If I want to, I can add a picture by writing an
        html tag for that: <img src='img/example.jpg' />
        b) Another alternative.
        c) A third alternative.
        d) A forth alternative.

        Oppgave 2: 
        Another question. Note that we didn't use 0 in front of the number 
        2 this time.
        a) An alternative.        
        b) Another alternative.
        c) A third alternative.
        d) A forth alternative.

    FORMAT <title>_solution.txt
        Exam for TIØ4258 fall 2009 
        1) a, The number defines the questions it answers, and the letter 
        defines the correct alternative. The Format "0) a," is mandatory,
        but the answer can go over multiple lines and, contain more commas
        (or parenthesis)
        2) b, A new answer is defined by a line starting the same way
        3) c, Explainations are not mandatory
        4) d,
        5) c,

'''


class Question:
    """
    A question, initiated with question (string).
    """
    def __init__(self, question):
        self.question = question
        self.alternatives = [] 
        self.solution = -1  # Int for which alternativ is correct
        self.explaination = "No explaination given"
        self.qnum = 0

    def append_line_to_question(self, more_question):
        '''
        Appends more text to the existing question.
        '''
        self.question += " " + more_question

    def add_alternative(self, alternative):
        '''
        Adds an alternative to the question
        '''
        self.alternatives.append(alternative)

    def append_text_to_last_alternative(self, text):
        '''
        Appends text to the most recently added alternative
        '''
        self.alternatives[-1] += " " + text

    def add_explaination(self, solution, explaination):
        '''
        Sets correct solution (int) and adds an explaination.
        '''
        self.solution = solution
        self.explaination = explaination

    def append_explaination(self, explaination):
        '''
        Appends text to the existing explaination
        '''
        self.explaination += " " + explaination

    def setQuestionNumber(self, number):
        '''
        Sets the question number (int)
        '''
        self.qnum = number


def readQuestions(path):
    '''
    Opens and reads a filepath. Returns an array of Question.
    '''
    lines = read_path_as_array(path)
    questions = {}
    processedQLine = 0
    qnum = 0
    for line in lines:
        # Removes spaces at start an end of line
        line = line.strip()

        # Test if line is of an ignoreable type
        if ignorable_line(line):
            print("IGNORED: " + line)
            continue

        # Check if the line defines a new task
        if line_defines_new_task(line):
            processedQLine = 1
            qnum = get_question_number(line)

        # If we're not 'ready' for a question or an alternativ
        elif processedQLine <= 0:
            print("IGNORED: " + line)
            continue

        # If the previous line defined the task
        elif processedQLine == 1:
            questions[qnum] = Question(line)
            questions[qnum].setQuestionNumber(qnum)
            processedQLine += 1

        # If we're somewhere within a task
        elif processedQLine > 1:
            if line_defines_new_alternative(line):
                # Skips the first three chars, as they're "x) "
                questions[qnum].add_alternative(line[3:])
            
            # If no alternatives has been added, we're still working on Q
            elif not questions[qnum].alternatives:
                questions[qnum].append_line_to_question(line)
            
            # If alternatives has been added, we're still working on alternative
            else:
                if line_defines_end_of_tasks(line):
                    print("QUIT AT " + line)
                    return questions

                questions[qnum].append_text_to_last_alternative(line)
    return questions


def applySolutions(questions, solution_path):
    '''
    Applies a solution to existing questions.
    Takes in:
    * questions: a list of Question.
    * solution_path: path to solution file
    '''
    
    print("applySolutions " + solution_path)
    lines = read_path_as_array(solution_path)
    
    qnum = 0
    for line in lines:
        line = line.strip()
        if not line_defines_answer(line):
            if line_defines_end_of_tasks(line):
                print("QUIT AT " + line)
                return questions
            elif qnum > 0 and qnum <= 50: # We're inside questions
                questions[qnum].append_explaination(line)
            continue

        qnum, solution = extract_qnum_and_solution(line)
        explaination = extract_explaination(line)

        try:
            questions[qnum].add_explaination(solution, explaination)
        except:
            print("Couldn't add answer to " + str(qnum))
    return questions

def load(dictionary, title):
    '''
    Loads questions and answers into a dictionary.
    '''
    dictionary[title] = applySolutions(
        readQuestions(title + '.txt'), title + '_solution.txt')


def ignorable_line(line):
    '''
    Returns whether or not the line should be ignored.
    '''
    return (
        len(line) < 2 
        or (line.lower().startswith('side ') and "av" in line) 
        or (line.lower().startswith("oppgaver fra") and ":" in line)
        )


def line_defines_new_task(line):
    '''
    Returns whether or not a line defines the start of a new task
    '''
    return line.lower().startswith('oppgave ') and line[8:10].isdigit()


def get_question_number(line):
    '''
    Returns the number of the question.
    '''
    try:
        return int(line[8:10])
    except:
        return 0


def line_defines_new_alternative(line):
    '''
    Returns whether or not the line defines a new alternative
    '''
    try:
        return line[1] == ')'
    except: 
        return False


def line_defines_end_of_tasks(line):
    '''
    Whether or not the line defines end of tasks
    '''
    return (
        (line.lower().startswith('karakter') and ":" in line)
        or line.lower().startswith("karaktergiving")
        )


def read_path_as_array(path):
    '''
    Opens file and returns an array of string. One line = one string.
    '''
    f = open(path, 'r')
    return f.read().split('\n')


def convert_letter_to_num(letter):
    '''
    converts letter to int (a --> 0)
    '''
    return ord(letter.lower())-97


def line_defines_answer(line):
    '''
    Whether or not the line defines an answer.
    '''
    temp = line.split(')', 1)
    return temp[0].isdigit() and len(temp) == 2 and len(temp[1].split(',')[0]) == 2


def extract_qnum_and_solution(line):
    '''
    Returns tuple with question number and solution as int (a -> 0.. etc)
    '''
    temp = line.split(')', 1)
    qnum = int(temp[0])
    solution = temp[1].split(',', 1)[0].strip().lower()
    solution = convert_letter_to_num(solution)
    return qnum, solution


def extract_explaination(line):
    '''
    Returns explaination from an answerline
    '''
    temp = line.split(')', 1)
    if len(temp[1].split(',', 1)) == 2:
        return temp[1].split(',', 1)[1].strip()
    else:
        return "No explaination given"


if __name__ == "__main__":
    import sys

    exams = {}
    args = sys.argv[1:]
    if not args:
        print("Usage: Run as 'python quiz_interpreter.py <title_of_quiz_file>'")
        print("Output will be saved as data.js")
        sys.exit()
    
    for arg in args:
        print arg
        load(exams, arg)

    print('Starting packing')
    f = open('data.js', 'w')
    f.write('var exams = {')
    for year in exams:
        questions = exams[year]
        f.write('"' + year + '"' + ' : [\n')
        for key in questions:
            f.write('{\n')
            f.write('   "question":"' + questions[key].question + '",\n')
            f.write('   "solution":"' + str(questions[key].solution) + '",\n')
            f.write('   "explaination":"' + questions[key].explaination + '",\n')
            f.write('   "number":"' + str(questions[key].qnum) + '",\n')
            f.write('   "alternatives": [\n')
            for i in range(len(questions[key].alternatives)):
                f.write('      "' + questions[key].alternatives[i] + '"')
                if i+1 < len(questions[key].alternatives):
                    f.write(',')
                f.write('\n')
            f.write('   ]')
            f.write('},\n\n')
        f.write('],\n\n')
    f.write('};')
