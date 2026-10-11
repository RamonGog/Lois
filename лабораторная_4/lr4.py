file_in = open("lr4.json", "r", encoding="utf-8")
text = file_in.read()
file_in.close()

out = ""
indent = 0
in_string = False
escape = False
tab = "    "

for ch in text:

    if in_string:
        out = out + ch

        if escape:
            escape = False
        elif ch == "\\":
            escape = True
        elif ch == '"':
            in_string = False

        continue

    if ch == '"':
        in_string = True
        out = out + ch

    elif ch == "{" or ch == "[":
        out = out + ch
        indent = indent + 1
        out = out + "\n" + tab * indent

    elif ch == "}" or ch == "]":
        indent = indent - 1
        out = out + "\n" + tab * indent
        out = out + ch

    elif ch == ",":
        out = out + ch
        out = out + "\n" + tab * indent

    elif ch == ":":
        out = out + ": "

    elif ch == " " or ch == "\n" or ch == "\t" or ch == "\r":
        continue

    else:
        out = out + ch

file_out = open("lr4output.json", "w", encoding="utf-8")
file_out.write(out)
file_out.close()