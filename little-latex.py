import sys
from plex import *
from subprocess import call

PREFACE = """\\documentclass{article}
\\usepackage{amsthm, amssymb, amsmath,verbatim, tikz}
\\usepackage[margin=1in]{geometry}
\\usepackage{enumerate}
\\usetikzlibrary{automata,positioning}
\\title{"""

END_PREFACE = """}
\\date{\\today}
\\author{David Frankl}

\\begin{document}

\\maketitle

\\begin{enumerate}
"""

END_DOC = """\\end{enumerate}
\\end{document}"""

indents = []

def letters(scanner, text):
    print "letters("+str(scanner)+", "+str(text)+")"
    indents.append('enumerate')
    return "letters"

def numbers(scanner, text):
    print "numbers("+str(scanner)+", "+str(text)+")"
    indents.append("enumerate")
    return "numbers"

def items(scanner, text):
    indents.append("itemize")
    return "items"

def end(scanner, text):
    return "end"

lexicon = Lexicon([
    (Str("\\assignment{"), Begin("assignment")),
    State("assignment", [
        (Rep(AnyBut("}")), "assignment"),
        (Str("}"), Begin(""))
    ]),
    (Str("\\letters"), letters),
    (Str("\\numbers"), numbers),
    (Str("\\items"), items),
    (Str("\\end{"), "other"),
    (Str("\\end"), end),
    (AnyChar, "other")
])

if len(sys.argv) < 2:
    print "No filename given"
    sys.exit()

try:
    filename = sys.argv[1]
    f = open(filename, "r")
except:
    print "No Such File: "+filename
    sys.exit()

scanner = Scanner(lexicon, f, filename)

f = open(filename + ".tex", "w")
f.write(PREFACE)

while 1:
    token = scanner.read()

    if token[0] is None:
        break

    print token

    if token[0] == 'letters':
        f.write('\\begin{enumerate}[\\label=a)]')
    elif token[0] == 'numbers':
        f.write('\\begin{enumerate}')
    elif token[0] == 'items':
        f.write('\\begin{itemize}')
    elif token[0] == 'end':
        f.write('\\end{'+indents.pop()+'}\n')
    else:
        f.write(token[1])

    if token[0] == 'assignment':
        f.write(END_PREFACE)

f.write(END_DOC)
f.close()

call(['pdflatex', filename + ".tex"])
call(['rm', filename + '.log', filename + '.tex', filename + '.aux'])
call(['open', filename + '.pdf'])
