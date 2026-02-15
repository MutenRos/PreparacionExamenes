from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

MODEL_ID = "runwayml/stable-diffusion-v1-5"  # example (may require HF access depending on model)
PROMPT = "a cozy modern desk setup, cinematic lighting, ultra detailed, 35mm photo"

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=dtype,
    safety_checker=None,  # optional
)
pipe = pipe.to(device)

img = pipe(
    PROMPT,
    num_inference_steps=30,
    guidance_scale=7.5,
    height=512,
    width=512,
).images[0]

img.save("out.png")
print("Saved out.png")

