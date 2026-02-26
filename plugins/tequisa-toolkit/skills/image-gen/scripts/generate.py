#!/usr/bin/env python3
"""
Unified Gemini Image Generator

Supports both Nano Banana (Native) and Imagen APIs for text-to-image generation.

Usage:
    # Nano Banana (default)
    python generate.py -p "sunset beach" -o hero.png
    python generate.py -p "city skyline" --api nano --model pro --thinking --size 4K

    # Imagen
    python generate.py -p "product photo" --api imagen --model ultra --count 4
    python generate.py -p "robot" --api imagen --person-gen allow_adult
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai not installed. Run: pip install google-genai Pillow")
    sys.exit(1)


# Model constants
NANO_MODELS = {
    "flash": "gemini-2.5-flash-image",
    "pro": "gemini-3-pro-image-preview"
}

IMAGEN_MODELS = {
    "standard": "imagen-4.0-generate-001",
    "ultra": "imagen-4.0-ultra-generate-001",
    "fast": "imagen-4.0-fast-generate-001",
    "legacy": "imagen-3.0-generate-002"
}

# Aspect ratios
NANO_ASPECT_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]
IMAGEN_ASPECT_RATIOS = ["1:1", "3:4", "4:3", "9:16", "16:9"]

# Sizes (Nano Banana)
SIZES = ["1K", "2K", "4K"]

# Person generation modes (Imagen only)
PERSON_GEN_MODES = ["dont_allow", "allow_adult", "allow_all"]


def slugify(text: str, max_words: int = 3) -> str:
    """Create a slug from text for filenames."""
    words = re.sub(r'[^\w\s]', '', text.lower()).split()[:max_words]
    return '_'.join(words) if words else 'image'


def get_default_output_path(prompt: str, output_dir: str = "./generated-images") -> str:
    """Generate default output path with timestamp and prompt slug."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = slugify(prompt)
    return str(Path(output_dir) / f"{timestamp}_{slug}.png")


def generate_nano_banana(
    prompt: str,
    output_path: str,
    model: str = "flash",
    aspect_ratio: str = "1:1",
    image_size: str = None,
    with_text: bool = False,
    thinking: bool = False,
    grounding: bool = False
) -> list[str]:
    """
    Generate image using Nano Banana (Native) API.

    Returns:
        List of saved image paths (always 1 for Nano Banana)
    """
    client = genai.Client()
    model_name = NANO_MODELS.get(model, NANO_MODELS["flash"])

    # Build config
    config_kwargs = {}

    if not with_text:
        config_kwargs["response_modalities"] = ["Image"]

    # Image config
    image_config_kwargs = {}
    if aspect_ratio:
        image_config_kwargs["aspect_ratio"] = aspect_ratio
    if image_size and model == "pro":
        image_config_kwargs["image_size"] = image_size

    if image_config_kwargs:
        config_kwargs["image_config"] = types.ImageConfig(**image_config_kwargs)

    # Thinking mode (Pro only)
    if thinking and model == "pro":
        config_kwargs["thinking_config"] = types.ThinkingConfig(
            thinking_budget=1024
        )

    # Google Search grounding (Pro only)
    if grounding and model == "pro":
        config_kwargs["tools"] = [types.Tool(google_search=types.GoogleSearch())]

    config = types.GenerateContentConfig(**config_kwargs) if config_kwargs else None

    # Generate
    response = client.models.generate_content(
        model=model_name,
        contents=[prompt],
        config=config
    )

    # Save image
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    saved_paths = []
    for part in response.parts:
        if part.inline_data is not None:
            image = part.as_image()
            image.save(str(output_path))
            saved_paths.append(str(output_path))
        elif part.text is not None and with_text:
            print(f"Model response: {part.text}")

    if not saved_paths:
        raise RuntimeError("No image generated in response")

    return saved_paths


def generate_imagen(
    prompt: str,
    output_path: str,
    model: str = "standard",
    aspect_ratio: str = "1:1",
    image_size: str = None,
    count: int = 1,
    person_gen: str = "dont_allow"
) -> list[str]:
    """
    Generate image(s) using Imagen API.

    Returns:
        List of saved image paths (1-4 depending on count)
    """
    client = genai.Client()
    model_name = IMAGEN_MODELS.get(model, IMAGEN_MODELS["standard"])

    # Build config
    config_kwargs = {
        "number_of_images": min(count, 4),
        "person_generation": person_gen
    }

    if aspect_ratio:
        config_kwargs["aspect_ratio"] = aspect_ratio

    # Imagen uses output_mime_type instead of image_size for some configs
    # but supports 1K and 2K through image_size in some models
    if image_size:
        # Map to Imagen's expected format if needed
        size_map = {"1K": "1024x1024", "2K": "2048x2048"}
        if image_size in size_map and "ultra" in model:
            config_kwargs["image_size"] = size_map[image_size]

    config = types.GenerateImagesConfig(**config_kwargs)

    # Generate
    response = client.models.generate_images(
        model=model_name,
        prompt=prompt,
        config=config
    )

    # Save images
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    saved_paths = []
    base_name = output_path.stem
    extension = output_path.suffix or ".png"

    for i, generated_image in enumerate(response.generated_images):
        if count == 1:
            save_path = output_path
        else:
            save_path = output_path.parent / f"{base_name}_{i+1}{extension}"

        generated_image.image.save(str(save_path))
        saved_paths.append(str(save_path))

    if not saved_paths:
        raise RuntimeError("No images generated in response")

    return saved_paths


def generate_image(
    prompt: str,
    output: str = None,
    output_dir: str = "./generated-images",
    api: str = "nano",
    model: str = None,
    aspect_ratio: str = "1:1",
    image_size: str = None,
    count: int = 1,
    person_gen: str = "dont_allow",
    with_text: bool = False,
    thinking: bool = False,
    grounding: bool = False
) -> list[str]:
    """
    Unified image generation function.

    Args:
        prompt: Text description of the image
        output: Output file path (auto-generated if None)
        output_dir: Directory for auto-generated outputs
        api: "nano" for Nano Banana or "imagen" for Imagen
        model: Model variant (nano: flash/pro, imagen: standard/ultra/fast/legacy)
        aspect_ratio: Output aspect ratio
        image_size: Resolution (1K/2K/4K for Nano Banana Pro)
        count: Number of images (Imagen only, 1-4)
        person_gen: Person generation mode (Imagen only)
        with_text: Include text response (Nano Banana only)
        thinking: Enable thinking mode (Nano Banana Pro only)
        grounding: Enable Google Search grounding (Nano Banana Pro only)

    Returns:
        List of saved image paths
    """
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY environment variable not set")

    # Determine output path
    if output is None:
        output = get_default_output_path(prompt, output_dir)

    if api == "nano":
        model = model or "flash"
        return generate_nano_banana(
            prompt=prompt,
            output_path=output,
            model=model,
            aspect_ratio=aspect_ratio,
            image_size=image_size,
            with_text=with_text,
            thinking=thinking,
            grounding=grounding
        )
    elif api == "imagen":
        model = model or "standard"
        return generate_imagen(
            prompt=prompt,
            output_path=output,
            model=model,
            aspect_ratio=aspect_ratio,
            image_size=image_size,
            count=count,
            person_gen=person_gen
        )
    else:
        raise ValueError(f"Unknown API: {api}. Use 'nano' or 'imagen'.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate AI images using Gemini Nano Banana or Imagen APIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Nano Banana (default)
  python generate.py -p "sunset over mountains" -o hero.png
  python generate.py -p "futuristic city" --model pro --size 4K --thinking

  # Imagen
  python generate.py -p "product mockup" --api imagen --model ultra --count 4
  python generate.py -p "business meeting" --api imagen --person-gen allow_adult
        """
    )

    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Text description of the image to generate"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output file path (default: ./generated-images/{timestamp}_{slug}.png)"
    )
    parser.add_argument(
        "--output-dir",
        default="./generated-images",
        help="Directory for auto-generated outputs (default: ./generated-images)"
    )
    parser.add_argument(
        "--api",
        choices=["nano", "imagen"],
        default="nano",
        help="API to use: nano (Nano Banana) or imagen (default: nano)"
    )
    parser.add_argument(
        "--model", "-m",
        default=None,
        help="Model variant. Nano: flash/pro (default: flash). Imagen: standard/ultra/fast/legacy (default: standard)"
    )
    parser.add_argument(
        "--aspect", "-a",
        default="1:1",
        help=f"Aspect ratio. Nano: {NANO_ASPECT_RATIOS}. Imagen: {IMAGEN_ASPECT_RATIOS}"
    )
    parser.add_argument(
        "--size", "-s",
        choices=SIZES,
        default=None,
        help="Image size for Nano Banana Pro model (1K, 2K, 4K)"
    )
    parser.add_argument(
        "--count", "-n",
        type=int,
        default=1,
        choices=[1, 2, 3, 4],
        help="Number of images to generate (Imagen only, 1-4)"
    )
    parser.add_argument(
        "--person-gen",
        choices=PERSON_GEN_MODES,
        default="dont_allow",
        help="Person generation control (Imagen only)"
    )
    parser.add_argument(
        "--with-text",
        action="store_true",
        help="Include text response with image (Nano Banana only)"
    )
    parser.add_argument(
        "--thinking",
        action="store_true",
        help="Enable thinking mode (Nano Banana Pro only)"
    )
    parser.add_argument(
        "--grounding",
        action="store_true",
        help="Enable Google Search grounding (Nano Banana Pro only)"
    )

    args = parser.parse_args()

    # Validate model choice
    if args.model:
        if args.api == "nano" and args.model not in NANO_MODELS:
            parser.error(f"Invalid model for Nano Banana: {args.model}. Choose from: {list(NANO_MODELS.keys())}")
        elif args.api == "imagen" and args.model not in IMAGEN_MODELS:
            parser.error(f"Invalid model for Imagen: {args.model}. Choose from: {list(IMAGEN_MODELS.keys())}")

    # Validate aspect ratio
    if args.api == "nano" and args.aspect not in NANO_ASPECT_RATIOS:
        parser.error(f"Invalid aspect ratio for Nano Banana: {args.aspect}")
    elif args.api == "imagen" and args.aspect not in IMAGEN_ASPECT_RATIOS:
        parser.error(f"Invalid aspect ratio for Imagen: {args.aspect}")

    try:
        results = generate_image(
            prompt=args.prompt,
            output=args.output,
            output_dir=args.output_dir,
            api=args.api,
            model=args.model,
            aspect_ratio=args.aspect,
            image_size=args.size,
            count=args.count,
            person_gen=args.person_gen,
            with_text=args.with_text,
            thinking=args.thinking,
            grounding=args.grounding
        )

        print(f"Generated {len(results)} image(s):")
        for path in results:
            print(f"  {path}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
