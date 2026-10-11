def get_priority(op):
    if op == "+" or op == "-":
        return 1
    if op == "*" or op == "/":
        return 2
    return 0


for i in range(1, 6):
    in_name = "lr5." + str(i) + ".txt"
    out_name = "lr5." + str(i) + "_output.txt"

    try:
        f_in = open(in_name, "r")
        text = f_in.read().strip()
        f_in.close()
    except FileNotFoundError:
        print("Файл " + in_name + " не найден")
        continue

    out = ""
    stack = []

    for ch in text:
        if ch.isdigit():
            out = out + ch

        elif ch in "+-*/":
            while len(stack) > 0 and get_priority(stack[-1]) >= get_priority(ch):
                out = out + stack.pop()
            stack.append(ch)

    while len(stack) > 0:
        out = out + stack.pop()

    f_out = open(out_name, "w")
    f_out.write(out)
    f_out.close()

    print("Готово: " + out_name)