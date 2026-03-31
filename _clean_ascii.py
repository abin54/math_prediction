import sys

def clean_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple replacement map for the common ones I used
    replacements = {
        '\u2550': '=',
        '\u2500': '-',
        '\u26a0': '!',
        '\u2605': '*',
        '\u2502': '|',
        '\u2212': '-',
        '\u25b6': '>',
        '★': '*',
        '─': '-',
        '═': '=',
        '⚠': '!',
        '>>>': '>>>' # just in case
    }
    
    new_content = ""
    for char in content:
        if ord(char) > 127:
            new_content += replacements.get(char, '?')
        else:
            new_content += char
            
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)

clean_file('swarm_predictor.py')
clean_file('predict_today.py')
print("Files cleaned of non-ASCII characters.")
