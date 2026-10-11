def get_priority(op):
    if op == "+" or op == "-":
        return 1
    if op == "*" or op == "/":
        return 2
    if op == "^":
        return 3
    return 0

f_in = open("lr6.txt", "r")
text = f_in.read().strip()
f_in.close()

out = ""
stack = []

for ch in text:
    if ch.isdigit():
        out = out + ch
        
    elif ch == "(":
        stack.append(ch)
        
    elif ch == ")":
        while len(stack) > 0 and stack[-1] != "(":
            out = out + stack.pop()
        if len(stack) > 0:
            stack.pop()
            
    elif ch in "+-*/^":
        while len(stack) > 0 and stack[-1] != "(":
            top_priority = get_priority(stack[-1])
            current_priority = get_priority(ch)
            
            if ch == "^":
                if top_priority > current_priority:
                    out = out + stack.pop()
                else:
                    break
            else:
                if top_priority >= current_priority:
                    out = out + stack.pop()
                else:
                    break
                    
        stack.append(ch)

while len(stack) > 0:
    out = out + stack.pop()

f_out = open("lr6_output.txt", "w")
f_out.write(out)
f_out.close()

print("Результат записан в lr6_output.txt: " + out)