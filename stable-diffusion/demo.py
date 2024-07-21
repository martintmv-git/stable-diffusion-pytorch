# demo.py demonstrates how to use the pipeline to generate images from text prompts or input images.

import model_loader
import pipeline
from PIL import Image
from pathlib import Path
from transformers import CLIPTokenizer
import torch

DEVICE = "cpu"

# Configure device preferences here, I'm using MPS for Apple Silicon GPU:
ALLOW_CUDA = False
ALLOW_MPS = True

if torch.cuda.is_available() and ALLOW_CUDA:
    DEVICE = "cuda"
elif torch.backends.mps.is_available() and ALLOW_MPS:
    DEVICE = "mps"
print(f"Using device: {DEVICE}")

tokenizer = CLIPTokenizer("../data/tokenizer_vocab.json", merges_file="../data/tokenizer_merges.txt")
model_file = "../data/v1-5-pruned-emaonly.ckpt"
models = model_loader.preload_models_from_standard_weights(model_file, DEVICE)

# TEXT TO IMAGE

prompt = "A small dog on the floor, highly detailed, ultra sharp, cinematic, 100mm lens, 8k resolution."
uncond_prompt = "" 
do_cfg = True
cfg_scale = 8  # min: 1, max: 14

# IMAGE TO IMAGE

input_image = None
image_path = "../img/dog.jpg"
# input_image = Image.open(image_path)
# Higher values means more noise will be added to the input image, so the result will be further from the input image.
# Lower values means less noise is added to the input image, so output will be closer to the input image.
strength = 0.9

# SAMPLER

sampler = "ddpm"
num_inference_steps = 50
seed = 42

output_image = pipeline.generate(
    prompt=prompt,
    uncond_prompt=uncond_prompt,
    input_image=input_image,
    strength=strength,
    do_cfg=do_cfg,
    cfg_scale=cfg_scale,
    sampler_name=sampler,
    n_inference_steps=num_inference_steps,
    seed=seed,
    models=models,
    device=DEVICE,
    idle_device="cpu",
    tokenizer=tokenizer,
)

# Combine the input image and the output image into a single image.
output_image = Image.fromarray(output_image)

# Create the output directory if it doesn't exist
output_dir = Path("../img/results/demo")
output_dir.mkdir(parents=True, exist_ok=True)

# Determine the output filename
file_index = 1
while (output_dir / f"o{file_index}.png").exists():
    file_index += 1
output_file = output_dir / f"o{file_index}.png"

# Save the output image
output_image.save(output_file)
print(f"Saved output image to {output_file}")