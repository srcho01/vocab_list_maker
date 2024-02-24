import random
from PIL import Image, ImageDraw, ImageFont

def make_file(files, save_path, format, is_numbering, is_shuffle, is_foreign, is_korean, is_answer):
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            words = f.read().splitlines()
        
        fname = file.split('/')[-1].split('.txt')[0]
        if is_foreign:
            _make_file('foreign', words, save_path, format, fname, is_numbering, is_shuffle, is_answer)
        if is_korean:
            _make_file('korean', words, save_path, format, fname, is_numbering, is_shuffle, is_answer)

    print("finish")
                            
def _make_file(lang, words, path, format, fname, number, shuffle, answer):
    if shuffle:
        random.shuffle(words)
        
    korean = []
    foreign = []
    for text in words:
        start_index = -1
        for i, char in enumerate(text):
            if char >= '가' and char <= '힣':
                start_index = i
                break
            
        korean.append(text[start_index:].strip())
        foreign.append(text[:start_index].strip())
        
    if lang == "foreign":
        if format == 'txt':
            make_text(path, fname, 'foreign', answer, number, foreign, korean)
        elif format == 'jpg':
            make_image(path, fname, 'foreign', answer, number, foreign, korean)
            
    elif lang == "korean":
        if format == 'txt':
            make_text(path, fname, 'korean', answer, number, korean, foreign)
        elif format == 'jpg':
            make_image(path, fname, 'korean', answer, number, korean, foreign)
        
def make_text(path, fname, lang, answer, number, w1, w2):
    output = f"{path}/{fname}_{lang}_test.txt"
    with open(output, 'w', encoding='utf-8') as f:
        for i, word in enumerate(w1):
            if number:
                f.write(f"{i+1}. {word}\n")
            else:
                f.write("word\n")
    
    if answer:
        output = f"{path}/{fname}_{lang}_answer.txt"
        with open(output, 'w', encoding='utf-8') as f:
            for i, word in enumerate(zip(w1, w2)):
                if number:
                    f.write(f"{i+1}. {word[0]} {word[1]}\n")
                else:
                    f.write(f"{word[0]} {word[1]}\n")
                    
def make_image(path, fname, lang, answer, number, w1, w2):
    font_size = 24
    width = font_size * 30
    height = (font_size + 10) * len(w1)
    
    font = ImageFont.truetype("./arialuni.TTF", size=font_size)
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    y_position = 10
    for i, word in enumerate(w1):
        if number:
            draw.text((10, y_position), f"{i+1}. {word}", fill=(0, 0, 0), font=font)
        else:
            draw.text((10, y_position), word, fill=(0, 0, 0), font=font)
        y_position += font_size + 8  # 단어 간격 조절
    
    output = f"{path}/{fname}_{lang}_test.jpg"
    img.save(output)
    
    if answer:
        img = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        y_position = 10
        for i, word in enumerate(zip(w1, w2)):
            if number:
                draw.text((10, y_position), f"{i+1}. {word[0]} {word[1]}", fill=(0, 0, 0), font=font)
            else:
                draw.text((10, y_position), f"{word[0]} {word[1]}", fill=(0, 0, 0), font=font)
            y_position += font_size + 8  # 단어 간격 조절
        
        output = f"{path}/{fname}_{lang}_answer.jpg"
        img.save(output)