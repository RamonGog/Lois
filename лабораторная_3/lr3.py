import os

def skip_spaces(state):
    while state['pos'] < len(state['text']):
        ch = state['text'][state['pos']]
        if ch in ' \t\r':
            state['pos'] += 1
        elif ch == '\n':
            state['pos'] += 1
            state['line'] += 1  
        else:
            break

def get_ch(state):
    if state['pos'] < len(state['text']):
        return state['text'][state['pos']]
    return None

def next_ch(state):
    state['pos'] += 1


def parse_value(state):
    skip_spaces(state)
    ch = get_ch(state)
    
    if ch == '{':
        parse_object(state)
    elif ch == '[':
        parse_array(state)
    elif ch == '"':
        parse_string(state)
    elif ch is not None and (ch.isdigit() or ch == '-'):
        parse_number(state)
    elif ch is not None and ch.isalpha():
        parse_constant(state)
    else:
        
        raise ValueError(f"символ '{ch}' там, где ожидалось значение") 

def parse_object(state):
    next_ch(state) 
    skip_spaces(state)
    
    if get_ch(state) == '}':
        next_ch(state)
        return
        
    while True:
        skip_spaces(state)
        if get_ch(state) != '"':
            raise ValueError("Ключ объекта должен быть строкой в двойных кавычках")
            
        parse_string(state)
        skip_spaces(state)
        
        if get_ch(state) != ':':
            raise ValueError(f"После ключа ожидался символ ':', но обнаружен '{get_ch(state)}'")
        next_ch(state) 
        
        parse_value(state)
        skip_spaces(state)
        
        ch = get_ch(state)
        if ch == '}':
            next_ch(state)
            break
        elif ch == ',':
            next_ch(state)
            skip_spaces(state)
            if get_ch(state) == '}':
                raise ValueError("Лишняя запятая в конце объекта перед закрывающей скобкой '}'")
        else:
            raise ValueError(f"В объекте пропущена запятая или закрывающая скобка '}}', найден символ '{ch}'")

def parse_array(state):
    next_ch(state)
    skip_spaces(state)
    
    if get_ch(state) == ']':
        next_ch(state)
        return
        
    while True:
        parse_value(state)
        skip_spaces(state)
        
        ch = get_ch(state)
        if ch == ']':
            next_ch(state)
            break
        elif ch == ',':
            next_ch(state)
            skip_spaces(state)
            if get_ch(state) == ']':
                raise ValueError("Лишняя запятая в конце массива перед закрывающей скобкой ']'")
        else:
            raise ValueError(f"В массиве пропущена запятая или закрывающая скобка ']', найден символ '{ch}'")

def parse_string(state):
    next_ch(state) 
    while state['pos'] < len(state['text']):
        ch = get_ch(state)
        if ch == '"':
            next_ch(state)
            return
        elif ch == '\\':
            next_ch(state)
        next_ch(state)
    raise ValueError("Незакрытая строка (пропущена закрывающая кавычка)")

def parse_number(state):
    if get_ch(state) == '-':
        next_ch(state)
    while state['pos'] < len(state['text']) and (get_ch(state).isdigit() or get_ch(state) == '.'):
        next_ch(state)

def parse_constant(state):
    start = state['pos']

    while state['pos'] < len(state['text']) and get_ch(state).isalpha():
        next_ch(state)

    word = state['text'][start:state['pos']]

    if word not in ("true", "false", "null"):
        raise ValueError(f"Недопустимая константа '{word}'. Разрешены только true, false, null")

script_dir = os.path.dirname(os.path.abspath(__file__))

for file_num in range(1, 6):
    file_name = f"lr3.{file_num}.json"
    file_path = os.path.join(script_dir, file_name)
    
    print(f"\n проверка файла: {file_name} ")
    
    if not os.path.exists(file_path):
        print(f" Файл {file_name} не найден!")
        continue
        
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
        f.seek(0)
        lines = f.readlines()

    state = {'text': raw_text, 'pos': 0, 'line': 1}
    
    try:
        parse_value(state)
        skip_spaces(state)
        if state['pos'] < len(state['text']):
            raise ValueError("лишний текст после закрытия основного JSON объекта")
        print(f" Файл {file_name} полностью валиден")
        
    except ValueError as e:
        error_line = state['line']
        
        print(f"ОШИБКА СИНТАКСИСА: {e}")
        print(f"ошибка: {error_line}")
        
        err_idx = error_line - 1
        start = max(0, err_idx - 2)
        end = min(len(lines), err_idx + 3)
        
        for i in range(start, end):
            if i == err_idx:
                print(f"---> {i + 1}: {lines[i]}", end="")
            else:
                print(f"     {i + 1}: {lines[i]}", end="")
