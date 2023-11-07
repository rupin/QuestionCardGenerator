from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import textwrap
import math
import os

# Load the template image

font =ImageFont.truetype("arial.ttf", 50)

# Load the Excel file
excel_file = "questions.xlsx"
df = pd.read_excel(excel_file)

df.replace('',0)

# Function to draw wrapped text on the image
def draw_wrapped_text(draw, text, position, font, max_width):
    if(text=="" or text==None or pd.isnull(text)):
        return
    lines = textwrap.wrap(text, width=max_width)  # Adjust the width as needed
    offset=0
    if(len(lines)==1):
        offset=40   

    y = position[1]
    for line in lines:
        draw.text((position[0], y+offset), line, fill="black", font=font)
        y += font.getsize(line)[1]

# Iterate through rows in the Excel file
optionsArray=['A', 'B', 'C', 'D']
for index, row in df.iterrows():  
   
    
    question = row['Question']
    options = [row[f'Option {optionsArray[i]}'] for i in range(0, 4)]

    # Define positions for text on the template
    
    question_position = (132, 170)
    #shift=40
    option_position=[(136, 742), (136, 981), (136, 1220), (136, 1459)] #A,B,C,D
    options_text_positions = [(277, 745), (277, 988), (277, 1227), (277, 1466)] # where options are placed
    optionsCount=0
    for i, option in enumerate(options):
        if(str(option)!="nan"):
            optionsCount=optionsCount+1
            
    template_path = "templates/"+str(optionsCount)+"Options.png"
    if(not os.path.exists(template_path)):
        continue
    template = Image.open(template_path)
    draw = ImageDraw.Draw(template)
    
    draw_wrapped_text(draw, question, question_position, font, max_width=35)

    for i, option in enumerate(options):
        if(str(option)!="nan"):
            draw_wrapped_text(draw, f"{chr(65 + i)}", option_position[i], font, max_width=980)
            draw_wrapped_text(draw, f"{option}", options_text_positions[i], font, max_width=30)
        #continue
    # Save the image with overlayed text
    output_path = f"output_question_{index + 1}.png"
    template.save(output_path)

print("Images generated successfully!")
