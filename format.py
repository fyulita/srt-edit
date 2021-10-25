def clearFormat(line):
    # Clear bold letters
    b = line.find("<b>")
    if b == -1:
        b = line.find("{b}")
    if b != -1:
        b_end = line.find("</b>")
        if b_end == -1:
            b_end = line.find("{/b}")
        line = line[:b] + line[b + 3:b_end] + line[b_end + 4:]

    # Clear italics
    i = line.find("<i>")
    if i == -1:
        i = line.find("{i}")
    if i != -1:
        i_end = line.find("</i>")
        if i_end == -1:
            i_end = line.find("{/i}")
        line = line[:i] + line[i + 3:i_end] + line[i_end + 4:]
        
    # Clear underlines
    u = line.find("<u>")
    if u == -1:
        u = line.find("{u}")
    if u != -1:
        u_end = line.find("</u>")
        if u_end == -1:
            u_end = line.find("{/u}")
        line = line[:u] + line[u + 3:u_end] + line[u_end + 4:]

    # Clear font opening
    f = line.find("<font")
    if f == -1:
        f = line.find("{font")
    if f != -1:
        f_end = line.find(">")
        if f_end == -1:
            f_end = line.find("}")
        line = line[:f] + line[f_end + 1:]

    # Clear font closing
    fc = line.find("</font>")
    if fc == -1:
        fc = line.find("{/font}")
    if fc != -1:
        line = line[:fc] + line[fc + 7:]

    # Clear positioning
    p = line.find("</a")
    if p == -1:
        p = line.find("{/a")
    if p != -1:
        p_end = line.find(">")
        if p_end == -1:
            p_end = line.find("}")
        line = line[:p] + line[p_end + 1:]
    
    return line


def formatting(file):
    reader = open(file, "r")
    lines = reader.readlines()
    writer = open(file[:-13] + ".srt", "w")
    
    line_counter = 0
    while line_counter < len(lines):
        # Write sequence number
        writer.write(lines[line_counter])
        line_counter += 1
    
        # Now times
        writer.write(lines[line_counter])
        line_counter += 1
    
        # Now we are in the dialogue part. We want to clear formatting.
        while line_counter < len(lines) and not lines[line_counter][:-1].isdigit():
            new_line = clearFormat(lines[line_counter])
            writer.write(new_line)

            line_counter += 1
    
    reader.close()
    writer.close()
