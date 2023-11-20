#!/usr/bin/env python3

from PIL import Image, ImageDraw
import math
import pandas as pd


class SequenceEncoder:
    def __init__(self, width=512, height=512, seq=None, radius=15, point_size=2):
        self.width = width
        self.height = height
        self.seq = seq
        self.amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
        self.uniform_angle = 18  # 360/len(amino_acids)
        self.radius = radius
        self.x = self.width//2
        self.y = self.height//2
        self.point_size = point_size

        self.colors = {
                'A': (255, 0, 0),
                'C': (255, 255, 0),
                'D': (0, 234, 255),
                'E': (170, 0, 255), 
                'F': (255, 127, 0), 
                'G': (191, 255, 0), 
                'H': (0, 149, 255), 
                'I': (255, 0, 170), 
                'K': (237, 185, 185), 
                'L': (185, 215, 237), 
                'M': (231, 233, 185), 
                'N': (220, 185, 237), 
                'P': (185, 237, 224), 
                'Q': (143, 35, 35), 
                'R': (35, 98, 143), 
                'S': (143, 106, 35), 
                'T': (107, 35, 143), 
                'V': (115, 115, 155), 
                'W': (204, 204, 204), 
                'Y': (0, 64, 255)
                }

        if seq:
            self.image = Image.new("RGB", (width, height), "black")
            self.draw = ImageDraw.Draw(self.image)
            self.createImage()
        else:
            print("error")


    def drawEllipse(self, x, y, color):
        self.draw.ellipse((x - self.point_size, y - self.point_size, x + self.point_size, y + self.point_size), fill=color)
    

    def createImage(self):
        for char in self.seq:
            if char in ['X', 'J', 'B', 'Z']:
                pass
            else:
                angle_degrees = self.amino_acids.index(char) * self.uniform_angle
                self.x += int(self.radius * math.cos(math.radians(angle_degrees)))
                self.y -= int(self.radius * math.sin(math.radians(angle_degrees)))
                self.drawEllipse(self.x, self. y, self.colors[char])
    

    def save(self, name=None):
        if self.seq and name:
            # self.image = self.image.resize((256, 256))
            self.image.save(name+'.png')
            # self.image.show()
            self.image.close()
        else:
            print("error")


if __name__ == "__main__":
    # SequenceEncoder(seq=seq).save("wow")
    df = pd.read_csv('./test_input.csv')
    for i in df.iterrows():
        SequenceEncoder(seq=i[1]['sequence']).save(i[1]['accession'])
    


