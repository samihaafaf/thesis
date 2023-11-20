from pathlib import Path
import random
from PIL import Image


data_path = Path("datasets/")
# image_path = data_path / "datasets"

image_path_list = list(data_path.glob("*/*/*.png"))
random_image_path = random.choice(image_path_list)
image_class = random_image_path.parent.stem
#print(image_class)

#4. Open image
img = Image.open(random_image_path)

#5. Print metadata
print(f"Random image path: {random_image_path}")
print(f"Image class: {image_class}")
print(f"Image height:  {img.height}")
print(f"Image width: {img.width}")
img.show()