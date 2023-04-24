def count_lines(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Remove blank lines and import statements
    lines = [line.strip() for line in lines if line.strip() and not (line.strip().startswith('import') or line.strip().startswith('from ') and line.strip().endswith(' import *'))]

    # Remove method signatures
    new_lines = []
    for i, line in enumerate(lines):
        if i > 0 and line.startswith('def '):
            j = i
            while j < len(lines) and not lines[j].strip().endswith(':'):
                j += 1
            lines = lines[:i] + lines[j+1:]
        else:
            new_lines.append(line)

    return len(new_lines)
