f_in = open("lr7.txt", "r")
text = f_in.read().strip()
f_in.close()

stack = []

for ch in text:
    
    if ch.isdigit():
        stack.append(int(ch))
        
    elif ch in "+-*/^":
        b = stack.pop()
        a = stack.pop()
        
        if ch == "+":
            res = a + b
        elif ch == "-":
            res = a - b
        elif ch == "*":
            res = a * b
        elif ch == "/":
            res = a / b
        elif ch == "^":
            res = a ** b
            
        stack.append(res)

print("Результат:", stack[0])