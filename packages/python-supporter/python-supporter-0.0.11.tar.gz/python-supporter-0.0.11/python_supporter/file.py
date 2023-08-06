def read_file(file):
    try:
        with open(file, encoding="utf8") as f:
            text = f.read()
    except:
        text = ""
    return text

def write_file(file, text):
    with open(file, "w", encoding="utf8") as f:
        f.write(text)
