import torch
from PIL import Image
from transformers import ViTFeatureExtractor, ViTForImageClassification


def predict(image, model_path="checkpoint-1900"):
    # Load the pretrained model
    model = ViTForImageClassification.from_pretrained(model_path)
    feature_extractor = ViTFeatureExtractor.from_pretrained(model_path)

    image = feature_extractor(images=image, return_tensors="pt")
    input_ids = image["pixel_values"]

    # Run inference
    with torch.no_grad():
        outputs = model(input_ids)

    # Get predicted class label
    predicted_class_index = torch.argmax(outputs.logits).item()

    actual_names = [
        "Asthma Plant.zip",
        "Avaram.zip",
        "Balloon vine.zip",
        "Bellyache bush (Green).zip",
        "Benghal dayflower.zip",
        "Big Caltrops.zip",
        "Black-Honey Shrub.zip",
        "Bristly Wild Grape.zip",
        "Butterfly Pea.zip",
        "Cape Gooseberry.zip",
        "Common Wireweed.zip",
        "Country Mallow.zip",
        "Crown flower.zip",
        "Green Chireta.zip",
        "Holy Basil.zip",
        "Indian CopperLeaf.zip",
        "Indian Jujube.zip",
        "Indian Sarsaparilla.zip",
        "Indian Stinging Nettle.zip",
        "Indian Thornapple.zip",
        "Indian wormwood.zip",
        "Ivy Gourd.zip",
        "Kokilaksha.zip",
        "Land Caltrops (Bindii).zip",
        "Madagascar Periwinkle.zip",
        "Madras Pea Pumpkin.zip",
        "Malabar Catmint.zip",
        "Mexican Mint.zip",
        "Mexican Prickly Poppy.zip",
        "Mountain Knotgrass.zip",
        "Nalta Jute.zip",
        "Night blooming Cereus.zip",
        "Panicled Foldwing.zip",
        "Prickly Chaff Flower.zip",
        "Punarnava.zip",
        "Purple Fruited Pea Eggplant.zip",
        "Purple Tephrosia.zip",
        "Rosary Pea.zip",
        "Shaggy button weed.zip",
        "Small Water Clover.zip",
        "Spiderwisp.zip",
        "Square Stalked Vine.zip",
        "Stinking Passionflower.zip",
        "Sweet Basil.zip",
        "Sweet flag.zip",
        "Tinnevelly Senna.zip",
        "Trellis Vine.zip",
        "Velvet bean.zip",
        "coatbuttons.zip",
        "heart-leaved moonseed.zip",
    ]

    return {"name": actual_names[predicted_class_index][:-4]}


img_path = "img2.jpg"
image = Image.open(img_path)

print(predict(image))
