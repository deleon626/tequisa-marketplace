#!/usr/bin/env python3
"""
Batch Image Generator

Generate multiple images from a JSON config file using either Nano Banana or Imagen API.

Usage:
    python batch.py -c config.json -o ./output
    python batch.py -c website-images.json -o ./assets/images --workers 4

Config format (Nano Banana):
{
    "api": "nano",
    "model": "flash",
    "images": [
        {"name": "hero", "prompt": "...", "aspect": "16:9", "size": "2K"},
        {"name": "about", "prompt": "...", "aspect": "4:3"}
    ]
}

Config format (Imagen):
{
    "api": "imagen",
    "model": "standard",
    "person_gen": "dont_allow",
    "images": [
        {"name": "product", "prompt": "...", "aspect": "1:1", "count": 4},
        {"name": "banner", "prompt": "...", "aspect": "16:9"}
    ]
}
"""

import argparse
import json
import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

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


def generate_nano_banana(
    client,
    name: str,
    prompt: str,
    output_dir: Path,
    model: str,
    aspect_ratio: str = "1:1",
    image_size: str = None,
    thinking: bool = False
) -> dict:
    """Generate a single image using Nano Banana API."""
    try:
        config_kwargs = {"response_modalities": ["Image"]}
        image_config_kwargs = {"aspect_ratio": aspect_ratio}

        if image_size and "pro" in model:
            image_config_kwargs["image_size"] = image_size

        config_kwargs["image_config"] = types.ImageConfig(**image_config_kwargs)

        if thinking and "pro" in model:
            config_kwargs["thinking_config"] = types.ThinkingConfig(thinking_budget=1024)

        config = types.GenerateContentConfig(**config_kwargs)

        response = client.models.generate_content(
            model=model,
            contents=[prompt],
            config=config
        )

        output_path = output_dir / f"{name}.png"
        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                image.save(str(output_path))
                return {"name": name, "status": "success", "paths": [str(output_path)]}

        return {"name": name, "status": "error", "error": "No image in response"}

    except Exception as e:
        return {"name": name, "status": "error", "error": str(e)}


def generate_imagen(
    client,
    name: str,
    prompt: str,
    output_dir: Path,
    model: str,
    aspect_ratio: str = "1:1",
    count: int = 1,
    person_gen: str = "dont_allow"
) -> dict:
    """Generate image(s) using Imagen API."""
    try:
        config_kwargs = {
            "number_of_images": min(count, 4),
            "person_generation": person_gen
        }

        if aspect_ratio:
            config_kwargs["aspect_ratio"] = aspect_ratio

        config = types.GenerateImagesConfig(**config_kwargs)

        response = client.models.generate_images(
            model=model,
            prompt=prompt,
            config=config
        )

        saved_paths = []
        for i, generated_image in enumerate(response.generated_images):
            if count == 1:
                output_path = output_dir / f"{name}.png"
            else:
                output_path = output_dir / f"{name}_{i+1}.png"

            generated_image.image.save(str(output_path))
            saved_paths.append(str(output_path))

        if saved_paths:
            return {"name": name, "status": "success", "paths": saved_paths}
        return {"name": name, "status": "error", "error": "No images in response"}

    except Exception as e:
        return {"name": name, "status": "error", "error": str(e)}


def batch_generate(config_file: str, output_dir: str, max_workers: int = 3):
    """Generate multiple images from config file."""
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY environment variable not set")

    with open(config_file) as f:
        config = json.load(f)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    api = config.get("api", "nano")
    model_key = config.get("model", "flash" if api == "nano" else "standard")

    if api == "nano":
        model = NANO_MODELS.get(model_key, NANO_MODELS["flash"])
    else:
        model = IMAGEN_MODELS.get(model_key, IMAGEN_MODELS["standard"])

    # Global settings from config
    default_person_gen = config.get("person_gen", "dont_allow")
    default_thinking = config.get("thinking", False)

    client = genai.Client()
    images = config.get("images", [])

    print(f"Generating {len(images)} images using {api.upper()} API ({model})...")

    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}

        for img in images:
            if api == "nano":
                future = executor.submit(
                    generate_nano_banana,
                    client=client,
                    name=img["name"],
                    prompt=img["prompt"],
                    output_dir=output_path,
                    model=model,
                    aspect_ratio=img.get("aspect", "1:1"),
                    image_size=img.get("size"),
                    thinking=img.get("thinking", default_thinking)
                )
            else:  # imagen
                future = executor.submit(
                    generate_imagen,
                    client=client,
                    name=img["name"],
                    prompt=img["prompt"],
                    output_dir=output_path,
                    model=model,
                    aspect_ratio=img.get("aspect", "1:1"),
                    count=img.get("count", 1),
                    person_gen=img.get("person_gen", default_person_gen)
                )

            futures[future] = img["name"]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

            if result["status"] == "success":
                paths = result["paths"]
                if len(paths) == 1:
                    print(f"  {result['name']}: {paths[0]}")
                else:
                    print(f"  {result['name']}: {len(paths)} images")
                    for p in paths:
                        print(f"    - {p}")
            else:
                print(f"  {result['name']}: ERROR - {result['error']}")

    # Summary
    success_count = sum(1 for r in results if r["status"] == "success")
    total_images = sum(len(r.get("paths", [])) for r in results if r["status"] == "success")

    print(f"\nGenerated {total_images} image(s) from {success_count}/{len(images)} configs")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Batch generate images using Gemini APIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Config file format:
{
    "api": "nano" | "imagen",
    "model": "flash" | "pro" | "standard" | "ultra" | "fast" | "legacy",
    "images": [
        {
            "name": "image-name",
            "prompt": "Image description",
            "aspect": "16:9",
            "size": "2K",        // Nano Banana Pro only
            "count": 4,          // Imagen only (1-4)
            "thinking": true,    // Nano Banana Pro only
            "person_gen": "allow_adult"  // Imagen only
        }
    ]
}
        """
    )

    parser.add_argument(
        "--config", "-c",
        required=True,
        help="Path to JSON config file"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="./generated-images",
        help="Output directory (default: ./generated-images)"
    )
    parser.add_argument(
        "--workers", "-w",
        type=int,
        default=3,
        help="Number of parallel workers (default: 3)"
    )

    args = parser.parse_args()

    try:
        batch_generate(args.config, args.output_dir, args.workers)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
