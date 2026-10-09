file_in = open("lr1.json", "r", encoding="utf-8")
text = file_in.read()
file_in.close()


lexemes = []
i = 0
n = len(text)


while i < n:
    char = text[i]

    
    if char in " \n\r\t":
        i += 1
        continue

    
    if char in "{}[],:":
        lexemes.append(("DEL", 4, char))
        i += 1
        continue

    
    if char == '"':
        j = i + 1

        
        while j < n and text[j] != '"':
            
            if text[j] == "\\":
                j += 1
            j += 1

        
        lexemes.append(("STR", 1, text[i:j + 1]))

        
        i = j + 1
        continue

    
    if char.isdigit() or char == "-":
        j = i + 1

        
        while j < n and (text[j].isdigit() or text[j] in ".eE+-"):
            j += 1

        lexemes.append(("NUM", 2, text[i:j]))
        i = j
        continue

    
    if char.isalpha():
        j = i + 1

        
        while j < n and text[j].isalpha():
            j += 1

        word = text[i:j]

        if word == "true" or word == "false" or word == "null":
            lexemes.append(("KW", 3, word))
        else:
            
            lexemes.append(("ERR", 0, word))

        i = j
        continue

    
    i += 1


file_out = open("lr1_result.txt", "w", encoding="utf-8")

for lexeme_class, lexeme_code, lexeme_text in lexemes:
    file_out.write(lexeme_class + " | " + str(lexeme_code) + " | " + lexeme_text + "\n")

file_out.close()