file_in = open("lr2.cpp", "r", encoding="utf-8")
text = file_in.read()
file_in.close()

keywords = {
    "int", "float", "double", "char", "bool", "void", "long", "short",
    "if", "else", "for", "while", "do", "return", "switch", "case",
    "break", "continue", "class", "struct", "public", "private",
    "true", "false", "using", "namespace", "const", "static"
}

two_char_ops = {
    "<<", ">>", "++", "--", "<=", ">=", "==", "!=",
    "&&", "||", "+=", "-=", "*=", "/=", "::"
}

one_char_ops = set("+-*/<>!=&|:")

delimiters = set("{}[]();,.")

lexemes = []

i = 0
n = len(text)

while i < n:
    ch = text[i]

    if ch.isspace():
        i += 1
        continue

    if ch == "/" and i + 1 < n and text[i + 1] == "/":
        i += 2
        while i < n and text[i] != "\n":
            i += 1
        continue

    if ch == "/" and i + 1 < n and text[i + 1] == "*":
        i += 2
        while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
            i += 1
        i += 2
        continue

    if ch == "#":
        j = i
        while j < n and text[j] != "\n":
            j += 1
        lexemes.append(("PRE", 8, text[i:j].strip()))
        i = j
        continue

    if ch == '"':
        j = i + 1
        while j < n and text[j] != '"':
            if text[j] == "\\":
                j += 1
            j += 1
        lexemes.append(("STR", 4, text[i:j + 1]))
        i = j + 1
        continue

    if ch == "'":
        j = i + 1
        while j < n and text[j] != "'":
            if text[j] == "\\":
                j += 1
            j += 1
        lexemes.append(("CHR", 5, text[i:j + 1]))
        i = j + 1
        continue

    if ch.isdigit():
        j = i
        while j < n and (text[j].isdigit() or text[j] == "."):
            j += 1
        lexemes.append(("NUM", 3, text[i:j]))
        i = j
        continue

    if ch.isalpha() or ch == "_":
        j = i
        while j < n and (text[j].isalnum() or text[j] == "_"):
            j += 1

        word = text[i:j]

        if word in keywords:
            lexemes.append(("KW", 1, word))
        else:
            lexemes.append(("ID", 2, word))

        i = j
        continue

    if i + 1 < n and text[i:i + 2] in two_char_ops:
        lexemes.append(("OP", 6, text[i:i + 2]))
        i += 2
        continue

    if ch in one_char_ops:
        lexemes.append(("OP", 6, ch))
        i += 1
        continue

    if ch in delimiters:
        lexemes.append(("DEL", 7, ch))
        i += 1
        continue

    lexemes.append(("ERR", 0, ch))
    i += 1

file_out = open("lr2_result.txt", "w", encoding="utf-8")

for lexeme_class, lexeme_code, lexeme_text in lexemes:
    file_out.write(lexeme_class + " | " + str(lexeme_code) + " | " + lexeme_text + "\n")

file_out.close()