def get_priority(op):
    if op == "+" or op == "-":
        return 1
    if op == "*" or op == "/":
        return 2
    if op == "^":
        return 3
    return 0


f_in = open("lr6.txt", "r")
infix = f_in.read().strip()
f_in.close()

rpn = ""
stack = []

for ch in infix:
    if ch.isdigit():
        rpn = rpn + ch
    elif ch == "(":
        stack.append(ch)
    elif ch == ")":
        while len(stack) > 0 and stack[-1] != "(":
            rpn = rpn + stack.pop()
        if len(stack) > 0:
            stack.pop()
    elif ch in "+-*/^":
        while len(stack) > 0 and stack[-1] != "(":
            top_priority = get_priority(stack[-1])
            current_priority = get_priority(ch)
            if ch == "^":
                if top_priority > current_priority:
                    rpn = rpn + stack.pop()
                else:
                    break
            else:
                if top_priority >= current_priority:
                    rpn = rpn + stack.pop()
                else:
                    break
        stack.append(ch)

while len(stack) > 0:
    rpn = rpn + stack.pop()

stack2 = []

for ch in rpn:
    if ch.isdigit():
        stack2.append(ch)
    elif ch in "+-*/^":
        b = stack2.pop()
        a = stack2.pop()
        stack2.append("(" + a + ch + b + ")")

result = stack2[0]

print("Исходное выражение:", infix)
print("ОПЗ:              ", rpn)
print("Результат:        ", result)