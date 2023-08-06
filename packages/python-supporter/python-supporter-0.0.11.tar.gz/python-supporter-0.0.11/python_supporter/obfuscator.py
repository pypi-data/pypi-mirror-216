'''
https://pyob.oxyry.com/
'''
import requests
import urllib.parse
import argparse 
import json
from . import logging
from pathlib import Path
import os

def obfuscate_code(code):
    logging.debug("===")
    logging.debug(code)
    code = code.strip()
	
	#https://m.blog.naver.com/wideeyed/221586482884
    data = {"append_source":False,"remove_docstrings":True,"rename_nondefault_parameters":True,"rename_default_parameters":False,"preserve":"","source":code}
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
        "referer": "https://pyob.oxyry.com/",
        "content-type": "application/json"
	}

    res = requests.post("https://pyob.oxyry.com/obfuscate", data=json.dumps(data), headers=headers)

    #

    text = res.text
    logging.debug(text)

    d = json.loads(text) 
    logging.debug(d)

    return d["dest"]

if __name__ == "__main__":
    import logging_lib
    #level = logging.DEBUG
    #level = logging.INFO
    level = logging.ERROR
    logging.basic_config(level)

    parser = argparse.ArgumentParser()
    parser.add_argument('--input')
    parser.add_argument('--output')
    args = parser.parse_args()
    input = args.input
    output = args.output
    logging.debug(input)
    logging.debug(output)
    logging.debug("----------")

    #code = "print('안녕하세요')"
    f = open(input, encoding='utf8')
    code = f.read() 
    f.close()

    obfuscated_code = obfuscate_code(code)
    logging.debug(obfuscated_code)

    #https://stackoverflow.com/questions/10149263/extract-a-part-of-the-filepath-a-directory-in-python
    p = Path(output)
    dir = str(p.parent)
    if not os.path.exists(dir):
        os.makedirs(dir)

    f = open(output, 'w', encoding='utf8')
    f.write(obfuscated_code)
    f.close()
