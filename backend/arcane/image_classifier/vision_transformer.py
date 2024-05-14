import os
from pathlib import Path
from typing import List

import torch
from PIL import Image
from transformers import ViTForImageClassification, ViTImageProcessor


class VisionTransformer:
    """Vision Transformer class to predict top k classes for an image.

    Attributes
    ----------
    **model_path** : (str) Path to the model checkpoint
    **model** : (ViTForImageClassification) Vision Transformer model
    **feature_extractor** : (ViTImageProcessor) Feature extractor for the model
    **actual_names** : (List) List of actual class names

    Methods
    -------
    **predict_top_k(image_path: Path, k: int = 5) -> List** : Predict top k classes for an image

    Raises
    ------
    **FileNotFoundError** : If image is not found at the given path

    Example
    -------
    >>> from arcane.image_classifier import VisionTransformer
    >>> vision_transformer = VisionTransformer(model_path="path/to/model_checkpoint")
    >>> image_path = Path("path/to/image.jpg")
    >>> top_k_results = vision_transformer.predict_top_k(image_path, k=5)
    >>> print(top_k_results)
    """

    def __init__(self, model_path: str = "model_checkpoints/checkpoint-1900"):
        self.model_path = model_path
        self.model = ViTForImageClassification.from_pretrained(model_path)
        self.feature_extractor = ViTImageProcessor.from_pretrained(model_path)
        self.actual_names = [
            "Asthma Plant",
            "Avaram",
            "Balloon vine",
            "Bellyache bush (Green)",
            "Benghal dayflower",
            "Big Caltrops",
            "Black-Honey Shrub",
            "Bristly Wild Grape",
            "Butterfly Pea",
            "Cape Gooseberry",
            "Common Wireweed",
            "Country Mallow",
            "Crown flower",
            "Green Chireta",
            "Holy Basil",
            "Indian CopperLeaf",
            "Indian Jujube",
            "Indian Sarsaparilla",
            "Indian Stinging Nettle",
            "Indian Thornapple",
            "Indian wormwood",
            "Ivy Gourd",
            "Kokilaksha",
            "Land Caltrops (Bindii)",
            "Madagascar Periwinkle",
            "Madras Pea Pumpkin",
            "Malabar Catmint",
            "Mexican Mint",
            "Mexican Prickly Poppy",
            "Mountain Knotgrass",
            "Nalta Jute",
            "Night blooming Cereus",
            "Panicled Foldwing",
            "Prickly Chaff Flower",
            "Punarnava",
            "Purple Fruited Pea Eggplant",
            "Purple Tephrosia",
            "Rosary Pea",
            "Shaggy button weed",
            "Small Water Clover",
            "Spiderwisp",
            "Square Stalked Vine",
            "Stinking Passionflower",
            "Sweet Basil",
            "Sweet flag",
            "Tinnevelly Senna",
            "Trellis Vine",
            "Velvet bean",
            "coatbuttons",
            "heart-leaved moonseed",
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

        probs = torch.nn.functional.softmax(outputs.logits, dim=1)

        top_p, top_class = probs.topk(k, dim=1)
        top_k_results = [
            {"class": self.actual_names[class_idx], "probability": prob.item()}
            for class_idx, prob in zip(top_class[0], top_p[0])
        ]

        return top_k_results
