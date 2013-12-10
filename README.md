exam-interpreter
================

Script to extract questions + answers (from NTNU exams) and save as JSON-structure.

The purpose of this script is to read a file of questions and store it to a JSON format. It was made to suit some NTNU exam that was written this way, so that's why it is the way it is.

The script is built using Python 2.7.

## Usage
Put two .txt files in the same folder, one named filename.txt and one 
named filename_solution.txt. Make sure they're in the format given in the next section.

```
python quiz_interpreter.py filename
```
Note: filename (relative path if all files are in the same folder) can be replace with path to the file.

A data.js file will then be created, containing the quiz.

### HTML/JS shell presenting the quiz
The [Tekled repository](https://github.com/tomfa/tekled) contains a simple HTML/JS 'shell' to present the quiz. 
Replace js/data.js to replace the questions with yours.

## Format

The repository contains example files showing example input files and the generated data.js file. In addition, it's explained to some extent below.

### FORMAT title.txt
```
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
```
### FORMAT title_solution.txt
```
        Exam for TIØ4258 fall 2009 
        1) a, The number defines the questions it answers, and the letter 
        defines the correct alternative. The Format "1) a," is mandatory,
        but the answer can go over multiple lines and, contain more commas 
        (or parenthesis).
        2) b, A new answer is defined by a line starting the same way
        3) c, Explainations are not mandatory
        4) d,
        5) c,
```


