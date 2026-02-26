#!/usr/bin/env python3
"""
Multi-turn Image Chat (Nano Banana API Only)

Interactive image generation and refinement through conversation.
Uses Gemini's multi-turn capability to iteratively refine images.

Note: Imagen API does NOT support multi-turn conversations.

Usage:
    python chat.py
    python chat.py --model pro --thinking
    python chat.py --output-dir ./my-images

Commands (during chat):
    save <filename>     Save current image to file
    save                Save with auto-generated name
    aspect <ratio>      Change aspect ratio (e.g., "16:9")
    size <1K|2K|4K>     Change size (Pro only)
    model <flash|pro>   Switch model
    thinking on|off     Toggle thinking mode (Pro only)
    history             Show conversation history
    clear               Start fresh conversation
    help                Show commands
    quit/exit           Exit chat

Example session:
    > Generate a cozy coffee shop interior
    [Image generated]
    > Add warm morning light through the windows
    [Image refined]
    > Make the colors more vibrant
    [Image refined]
    > save coffee_shop.png
    Saved to: coffee_shop.png
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


MODELS = {
    "flash": "gemini-2.5-flash-image",
    "pro": "gemini-3-pro-image-preview"
}

ASPECT_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]
SIZES = ["1K", "2K", "4K"]


class ImageChat:
    """Multi-turn image generation chat session."""

    def __init__(
        self,
        model: str = "flash",
        thinking: bool = False,
        output_dir: str = "./generated-images",
        aspect_ratio: str = "1:1",
        image_size: str = None
    ):
        if not os.environ.get("GEMINI_API_KEY"):
            raise ValueError("GEMINI_API_KEY environment variable not set")

        self.client = genai.Client()
        self.model = model
        self.thinking = thinking
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.aspect_ratio = aspect_ratio
        self.image_size = image_size

        self.chat = None
        self.current_image = None
        self.history = []
        self.image_count = 0

        self._start_chat()

    def _start_chat(self):
        """Initialize or restart the chat session."""
        model_name = MODELS.get(self.model, MODELS["flash"])

        config_kwargs = {}
        image_config_kwargs = {"aspect_ratio": self.aspect_ratio}

        if self.image_size and self.model == "pro":
            image_config_kwargs["image_size"] = self.image_size

        config_kwargs["image_config"] = types.ImageConfig(**image_config_kwargs)

        if self.thinking and self.model == "pro":
            config_kwargs["thinking_config"] = types.ThinkingConfig(thinking_budget=1024)

        config = types.GenerateContentConfig(**config_kwargs)

        self.chat = self.client.chats.create(
            model=model_name,
            config=config
        )
        self.history = []
        self.current_image = None

    def _build_config(self):
        """Build current config for requests."""
        config_kwargs = {}
        image_config_kwargs = {"aspect_ratio": self.aspect_ratio}

        if self.image_size and self.model == "pro":
            image_config_kwargs["image_size"] = self.image_size

        config_kwargs["image_config"] = types.ImageConfig(**image_config_kwargs)

        if self.thinking and self.model == "pro":
            config_kwargs["thinking_config"] = types.ThinkingConfig(thinking_budget=1024)

        return types.GenerateContentConfig(**config_kwargs)

    def send(self, message: str) -> tuple[bool, str]:
        """
        Send a message and get response.

        Returns:
            (success, message) tuple
        """
        try:
            response = self.chat.send_message(message)

            self.history.append({"role": "user", "content": message})

            for part in response.parts:
                if part.inline_data is not None:
                    self.current_image = part.as_image()
                    self.image_count += 1
                    self.history.append({"role": "assistant", "content": "[Image generated]"})
                    return True, "Image generated"
                elif part.text is not None:
                    self.history.append({"role": "assistant", "content": part.text})
                    return True, part.text

            return False, "No response received"

        except Exception as e:
            return False, str(e)

    def save(self, filename: str = None) -> str:
        """Save current image to file."""
        if self.current_image is None:
            raise ValueError("No image to save. Generate an image first.")

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chat_{timestamp}_{self.image_count}.png"

        # Ensure .png extension
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            filename += ".png"

        output_path = self.output_dir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.current_image.save(str(output_path))
        return str(output_path)

    def set_aspect_ratio(self, ratio: str):
        """Change aspect ratio for future generations."""
        if ratio not in ASPECT_RATIOS:
            raise ValueError(f"Invalid ratio. Choose from: {ASPECT_RATIOS}")
        self.aspect_ratio = ratio
        self._start_chat()  # Restart chat with new config

    def set_size(self, size: str):
        """Change image size (Pro model only)."""
        if size not in SIZES:
            raise ValueError(f"Invalid size. Choose from: {SIZES}")
        if self.model != "pro":
            raise ValueError("Size setting only available for Pro model")
        self.image_size = size
        self._start_chat()

    def set_model(self, model: str):
        """Switch model."""
        if model not in MODELS:
            raise ValueError(f"Invalid model. Choose from: {list(MODELS.keys())}")
        self.model = model
        self._start_chat()

    def set_thinking(self, enabled: bool):
        """Toggle thinking mode (Pro only)."""
        if enabled and self.model != "pro":
            raise ValueError("Thinking mode only available for Pro model")
        self.thinking = enabled
        self._start_chat()

    def clear(self):
        """Clear conversation and start fresh."""
        self._start_chat()
        self.current_image = None
        self.image_count = 0

    def get_history(self) -> list:
        """Get conversation history."""
        return self.history.copy()

    def get_status(self) -> dict:
        """Get current session status."""
        return {
            "model": self.model,
            "thinking": self.thinking,
            "aspect_ratio": self.aspect_ratio,
            "image_size": self.image_size,
            "images_generated": self.image_count,
            "has_current_image": self.current_image is not None,
            "history_length": len(self.history)
        }


def print_help():
    """Print available commands."""
    print("""
Commands:
  save [filename]     Save current image (optional filename)
  aspect <ratio>      Set aspect ratio (1:1, 16:9, 9:16, etc.)
  size <1K|2K|4K>     Set image size (Pro model only)
  model <flash|pro>   Switch model
  thinking on|off     Toggle thinking mode (Pro only)
  status              Show current settings
  history             Show conversation history
  clear               Start fresh conversation
  help                Show this help
  quit|exit           Exit chat

Tips:
  - Describe images naturally, like talking to a creative
  - Refine incrementally: "make the sky more blue"
  - Use photography terms: "shallow depth of field", "golden hour"
  - For consistency, reference previous elements: "keep the same style"
""")


def main():
    parser = argparse.ArgumentParser(
        description="Interactive multi-turn image generation chat"
    )
    parser.add_argument(
        "--model", "-m",
        choices=["flash", "pro"],
        default="flash",
        help="Model to use (default: flash)"
    )
    parser.add_argument(
        "--thinking",
        action="store_true",
        help="Enable thinking mode (Pro only)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="./generated-images",
        help="Output directory for saved images"
    )
    parser.add_argument(
        "--aspect", "-a",
        default="1:1",
        help="Initial aspect ratio"
    )
    parser.add_argument(
        "--size", "-s",
        choices=SIZES,
        default=None,
        help="Image size (Pro only)"
    )

    args = parser.parse_args()

    try:
        chat = ImageChat(
            model=args.model,
            thinking=args.thinking,
            output_dir=args.output_dir,
            aspect_ratio=args.aspect,
            image_size=args.size
        )
    except Exception as e:
        print(f"Error initializing chat: {e}")
        sys.exit(1)

    print(f"Image Chat initialized ({args.model} model)")
    print("Type 'help' for commands, 'quit' to exit")
    print("-" * 40)

    while True:
        try:
            user_input = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        # Parse commands
        lower_input = user_input.lower()

        if lower_input in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        elif lower_input == "help":
            print_help()

        elif lower_input == "status":
            status = chat.get_status()
            print(f"Model: {status['model']}")
            print(f"Thinking: {'on' if status['thinking'] else 'off'}")
            print(f"Aspect ratio: {status['aspect_ratio']}")
            print(f"Image size: {status['image_size'] or 'default'}")
            print(f"Images generated: {status['images_generated']}")
            print(f"Has current image: {status['has_current_image']}")

        elif lower_input == "history":
            history = chat.get_history()
            if not history:
                print("No conversation history yet.")
            else:
                for i, entry in enumerate(history):
                    role = "You" if entry["role"] == "user" else "AI"
                    content = entry["content"][:100] + "..." if len(entry["content"]) > 100 else entry["content"]
                    print(f"{i+1}. {role}: {content}")

        elif lower_input == "clear":
            chat.clear()
            print("Conversation cleared. Starting fresh.")

        elif lower_input.startswith("save"):
            parts = user_input.split(maxsplit=1)
            filename = parts[1] if len(parts) > 1 else None
            try:
                path = chat.save(filename)
                print(f"Saved to: {path}")
            except Exception as e:
                print(f"Error saving: {e}")

        elif lower_input.startswith("aspect "):
            ratio = user_input.split(maxsplit=1)[1].strip()
            try:
                chat.set_aspect_ratio(ratio)
                print(f"Aspect ratio set to: {ratio}")
                print("Note: Conversation history preserved, new config applied.")
            except Exception as e:
                print(f"Error: {e}")

        elif lower_input.startswith("size "):
            size = user_input.split(maxsplit=1)[1].strip().upper()
            try:
                chat.set_size(size)
                print(f"Size set to: {size}")
            except Exception as e:
                print(f"Error: {e}")

        elif lower_input.startswith("model "):
            model = user_input.split(maxsplit=1)[1].strip().lower()
            try:
                chat.set_model(model)
                print(f"Switched to {model} model")
                print("Note: Conversation cleared with model change.")
            except Exception as e:
                print(f"Error: {e}")

        elif lower_input.startswith("thinking "):
            setting = user_input.split(maxsplit=1)[1].strip().lower()
            try:
                chat.set_thinking(setting == "on")
                print(f"Thinking mode: {setting}")
            except Exception as e:
                print(f"Error: {e}")

        else:
            # Regular message - send to model
            print("Generating...")
            success, response = chat.send(user_input)
            if success:
                if response == "Image generated":
                    print("[Image generated] Use 'save' to save it.")
                else:
                    print(f"Response: {response}")
            else:
                print(f"Error: {response}")


if __name__ == "__main__":
    main()
