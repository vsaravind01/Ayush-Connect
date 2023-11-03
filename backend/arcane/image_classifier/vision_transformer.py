import os
from pathlib import Path
from typing import List

import torch
from PIL import Image
from transformers import ViTForImageClassification, ViTImageProcessor


class VisionTransformer:
    def __init__(self, model_path: str = "model_checkpoints/checkpoint-1900"):
        self.model_path = model_path
        self.model = ViTForImageClassification.from_pretrained(model_path)
        self.feature_extractor = ViTImageProcessor.from_pretrained(model_path)
        self.actual_names = [
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

    def predict_top_k(self, image_path: Path, k: int = 5) -> List:
        """
        Predict top k classes for an image

        Parameters
        ----------
        **image_path** : (Path) Path to the image to be predicted
        **k** : (int) Number of classes to be predicted

        Returns
        -------
        **top_k_results** : (List) List of top k predictions with class name and probability

        Raises
        ------
        **FileNotFoundError** : If image is not found at the given path
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")

        search_image = Image.open(image_path)
        search_image = self.feature_extractor(images=search_image, return_tensors="pt")
        input_ids = search_image["pixel_values"]

        # Run inference
        with torch.no_grad():
            outputs = self.model(input_ids)

        predicted_class_indices = torch.topk(outputs.logits, k=k, dim=1).indices[0]
        predicted_class_probabilities = torch.topk(outputs.logits, k=k, dim=1).values[0]

        top_k_class_names = [
            self.actual_names[index][:-4] for index in predicted_class_indices
        ]

        top_k_class_probabilities = [
            probability.item() for probability in predicted_class_probabilities
        ]
        top_k_results = [
            {"name": name, "probability": probability}
            for name, probability in zip(top_k_class_names, top_k_class_probabilities)
        ]

        return top_k_results
