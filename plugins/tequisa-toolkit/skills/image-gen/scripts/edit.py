#!/usr/bin/env python3
"""
Gemini Image Editor (Nano Banana API Only)

Edit existing images using Gemini's Nano Banana API.
Supports: adding/removing elements, style transfer, inpainting, background changes.

Note: Imagen API does NOT support image editing. This script uses Nano Banana only.

Usage:
    python edit.py edit -i photo.png -p "Add a sunset background" -o edited.png
    python edit.py background -i logo.png --new-bg "gradient blue to purple" -o logo_v2.png
    python edit.py style -i photo.jpg --style "watercolor painting" -o artistic.png
    python edit.py add -i room.jpg --element "potted plant" --position "corner" -o room_v2.png
    python edit.py remove -i photo.jpg --element "person in background" -o cleaned.png
    python edit.py recolor -i car.png --target "car body" --color "metallic red" -o car_red.png
    python edit.py combine --images img1.png img2.png -p "Blend these seamlessly" -o combined.png
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from google import genai
    from google.genai import types
    from PIL import Image
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install google-genai Pillow")
    sys.exit(1)


# Model constants
MODELS = {
    "flash": "gemini-2.5-flash-image",
    "pro": "gemini-3-pro-image-preview"
}

ASPECT_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]
SIZES = ["1K", "2K", "4K"]


def edit_image(
    input_path: str,
    prompt: str,
    output_path: str,
    model: str = "flash",
    aspect_ratio: str = None,
    image_size: str = None,
    additional_images: list = None,
    thinking: bool = False
) -> str:
    """
    Edit an image using Gemini Nano Banana API.

    Args:
        input_path: Path to the source image
        prompt: Edit instructions
        output_path: Where to save the edited image
        model: "flash" (up to 3 images) or "pro" (up to 14 images, 4K, thinking)
        aspect_ratio: Output aspect ratio (None to match input)
        image_size: Resolution for pro model ("1K", "2K", "4K")
        additional_images: List of additional image paths for composition
        thinking: Enable thinking mode (Pro only)

    Returns:
        Path to the saved image
    """
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY environment variable not set")

    client = genai.Client()
    model_name = MODELS.get(model, MODELS["flash"])

    # Load input image(s)
    source_image = Image.open(input_path)
    contents = [prompt, source_image]

    # Add additional images for composition
    if additional_images:
        max_additional = 13 if model == "pro" else 2  # Pro supports up to 14 total, Flash up to 3
        for i, img_path in enumerate(additional_images[:max_additional]):
            contents.append(Image.open(img_path))

    # Build config
    config_kwargs = {}
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

    config = types.GenerateContentConfig(**config_kwargs) if config_kwargs else None

    # Generate
    response = client.models.generate_content(
        model=model_name,
        contents=contents,
        config=config
    )

    # Save result
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    for part in response.parts:
        if part.inline_data is not None:
            image = part.as_image()
            image.save(str(output_path))
            return str(output_path)
        elif part.text is not None:
            print(f"Model response: {part.text}")

    raise RuntimeError("No image generated in response")


def style_transfer(
    input_path: str,
    style: str,
    output_path: str,
    model: str = "flash",
    thinking: bool = False
) -> str:
    """Apply artistic style transfer to an image."""
    prompt = f"Transform this image into the artistic style of {style}. Preserve the original composition but render all elements in this new style."
    return edit_image(input_path, prompt, output_path, model, thinking=thinking)


def change_background(
    input_path: str,
    new_background: str,
    output_path: str,
    model: str = "flash",
    thinking: bool = False
) -> str:
    """Replace the background of an image."""
    prompt = f"Keep the main subject exactly the same but change the background to {new_background}. Ensure lighting and shadows match naturally."
    return edit_image(input_path, prompt, output_path, model, thinking=thinking)


def add_element(
    input_path: str,
    element: str,
    position: str,
    output_path: str,
    model: str = "flash",
    thinking: bool = False
) -> str:
    """Add an element to an image."""
    prompt = f"Add {element} to the {position} of this image. Make it look natural and match the lighting and style of the original."
    return edit_image(input_path, prompt, output_path, model, thinking=thinking)


def remove_element(
    input_path: str,
    element: str,
    output_path: str,
    model: str = "flash",
    thinking: bool = False
) -> str:
    """Remove an element from an image."""
    prompt = f"Remove {element} from this image. Fill in the area naturally to match the surroundings. Keep everything else exactly the same."
    return edit_image(input_path, prompt, output_path, model, thinking=thinking)


def recolor(
    input_path: str,
    target: str,
    new_color: str,
    output_path: str,
    model: str = "flash",
    thinking: bool = False
) -> str:
    """Change the color of a specific element."""
    prompt = f"Change only the color of {target} to {new_color}. Keep everything else in the image exactly the same, preserving the original style, lighting, and composition."
    return edit_image(input_path, prompt, output_path, model, thinking=thinking)


def combine_images(
    image_paths: list,
    prompt: str,
    output_path: str,
    model: str = "pro",
    aspect_ratio: str = None,
    thinking: bool = False
) -> str:
    """Combine multiple images into a new composition."""
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY environment variable not set")

    client = genai.Client()
    model_name = MODELS.get(model, MODELS["pro"])

    # Load all images
    contents = [prompt]
    max_images = 14 if model == "pro" else 3
    for path in image_paths[:max_images]:
        contents.append(Image.open(path))

    # Build config
    config_kwargs = {}
    if aspect_ratio:
        config_kwargs["image_config"] = types.ImageConfig(aspect_ratio=aspect_ratio)

    if thinking and model == "pro":
        config_kwargs["thinking_config"] = types.ThinkingConfig(
            thinking_budget=1024
        )

    config = types.GenerateContentConfig(**config_kwargs) if config_kwargs else None

    response = client.models.generate_content(
        model=model_name,
        contents=contents,
        config=config
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    for part in response.parts:
        if part.inline_data is not None:
            image = part.as_image()
            image.save(str(output_path))
            return str(output_path)

    raise RuntimeError("No image generated in response")


def main():
    parser = argparse.ArgumentParser(
        description="Edit images using Gemini Nano Banana API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python edit.py edit -i photo.png -p "Make it more vibrant" -o output.png
  python edit.py background -i portrait.jpg --new-bg "sunset beach" -o portrait_sunset.jpg
  python edit.py style -i photo.jpg --style "Van Gogh" -o artistic.png --model pro
  python edit.py combine --images face.png body.png -p "Merge seamlessly" -o merged.png
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Edit command")

    # Common arguments function
    def add_common_args(subparser, require_input=True):
        if require_input:
            subparser.add_argument("--input", "-i", required=True, help="Input image path")
        subparser.add_argument("--output", "-o", required=True, help="Output image path")
        subparser.add_argument("--model", "-m", choices=["flash", "pro"], default="flash",
                              help="Model: flash (fast, up to 3 images) or pro (quality, up to 14 images, 4K)")
        subparser.add_argument("--thinking", action="store_true",
                              help="Enable thinking mode (Pro only)")

    # Generic edit
    edit_parser = subparsers.add_parser("edit", help="Generic image editing")
    add_common_args(edit_parser)
    edit_parser.add_argument("--prompt", "-p", required=True, help="Edit instructions")
    edit_parser.add_argument("--aspect", "-a", choices=ASPECT_RATIOS, help="Output aspect ratio")
    edit_parser.add_argument("--size", "-s", choices=SIZES, help="Image size (Pro only)")
    edit_parser.add_argument("--additional", nargs="+", help="Additional reference images")

    # Style transfer
    style_parser = subparsers.add_parser("style", help="Apply artistic style")
    add_common_args(style_parser)
    style_parser.add_argument("--style", required=True,
                             help="Style description (e.g., 'Van Gogh', 'anime', 'watercolor')")

    # Background change
    bg_parser = subparsers.add_parser("background", help="Change background")
    add_common_args(bg_parser)
    bg_parser.add_argument("--new-bg", required=True, help="New background description")

    # Add element
    add_parser = subparsers.add_parser("add", help="Add element to image")
    add_common_args(add_parser)
    add_parser.add_argument("--element", required=True, help="Element to add")
    add_parser.add_argument("--position", default="center",
                           help="Position (e.g., 'top-left', 'center', 'foreground')")

    # Remove element
    remove_parser = subparsers.add_parser("remove", help="Remove element from image")
    add_common_args(remove_parser)
    remove_parser.add_argument("--element", required=True, help="Element to remove")

    # Recolor
    color_parser = subparsers.add_parser("recolor", help="Change color of element")
    add_common_args(color_parser)
    color_parser.add_argument("--target", required=True, help="Element to recolor")
    color_parser.add_argument("--color", required=True, help="New color")

    # Combine
    combine_parser = subparsers.add_parser("combine", help="Combine multiple images")
    combine_parser.add_argument("--images", nargs="+", required=True, help="Image paths to combine")
    combine_parser.add_argument("--prompt", "-p", required=True, help="How to combine them")
    combine_parser.add_argument("--output", "-o", required=True, help="Output image path")
    combine_parser.add_argument("--model", "-m", choices=["flash", "pro"], default="pro",
                               help="Model (default: pro for combining)")
    combine_parser.add_argument("--aspect", "-a", choices=ASPECT_RATIOS, help="Output aspect ratio")
    combine_parser.add_argument("--thinking", action="store_true", help="Enable thinking mode (Pro only)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "edit":
            result = edit_image(
                args.input, args.prompt, args.output,
                args.model, args.aspect, args.size, args.additional, args.thinking
            )
        elif args.command == "style":
            result = style_transfer(args.input, args.style, args.output, args.model, args.thinking)
        elif args.command == "background":
            result = change_background(args.input, args.new_bg, args.output, args.model, args.thinking)
        elif args.command == "add":
            result = add_element(args.input, args.element, args.position, args.output, args.model, args.thinking)
        elif args.command == "remove":
            result = remove_element(args.input, args.element, args.output, args.model, args.thinking)
        elif args.command == "recolor":
            result = recolor(args.input, args.target, args.color, args.output, args.model, args.thinking)
        elif args.command == "combine":
            result = combine_images(args.images, args.prompt, args.output, args.model, args.aspect, args.thinking)

        print(f"Image saved to: {result}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
