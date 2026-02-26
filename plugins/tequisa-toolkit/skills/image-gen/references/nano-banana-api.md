# Nano Banana (Native) API Reference

Gemini's native image generation capability built directly into the Gemini model family.

## Overview

Nano Banana is Google's native multimodal image generation integrated into Gemini models. It uses `generate_content()` with image response modalities, enabling text-to-image, image editing, and multi-turn conversations.

## Models

| Model ID | Alias | Max Input Images | Resolution | Features |
|----------|-------|------------------|------------|----------|
| `gemini-2.5-flash-image` | flash | 3 | 1K | Fast generation |
| `gemini-3-pro-image-preview` | pro | 14 | 4K | Thinking mode, search grounding |

## API Usage

### Basic Generation

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=["A sunset over mountains"],
    config=types.GenerateContentConfig(
        response_modalities=["Image"],
        image_config=types.ImageConfig(
            aspect_ratio="16:9"
        )
    )
)

# Save image
for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()
        image.save("output.png")
```

### Image Editing

```python
from PIL import Image

source = Image.open("photo.jpg")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=["Change the background to a beach sunset", source],
    config=types.GenerateContentConfig(
        image_config=types.ImageConfig(aspect_ratio="16:9")
    )
)
```

### Multi-Turn Chat

```python
chat = client.chats.create(
    model="gemini-2.5-flash-image",
    config=types.GenerateContentConfig(
        image_config=types.ImageConfig(aspect_ratio="1:1")
    )
)

# First message - generate base image
response = chat.send_message("Create a cozy coffee shop interior")

# Refine iteratively
response = chat.send_message("Add warm morning sunlight")
response = chat.send_message("Make the colors more vibrant")
```

## Configuration Options

### GenerateContentConfig

| Parameter | Type | Description |
|-----------|------|-------------|
| `response_modalities` | list[str] | Set to `["Image"]` for image-only output |
| `image_config` | ImageConfig | Image generation settings |
| `thinking_config` | ThinkingConfig | Thinking mode (Pro only) |
| `tools` | list[Tool] | Search grounding tools |

### ImageConfig

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
| `aspect_ratio` | str | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 | Output dimensions |
| `image_size` | str | 1K, 2K, 4K | Resolution (Pro only) |

### ThinkingConfig (Pro Only)

```python
types.ThinkingConfig(
    thinking_budget=1024  # Token budget for reasoning
)
```

Enables extended reasoning before generation. Useful for complex compositions or when accuracy matters.

### Search Grounding (Pro Only)

```python
config = types.GenerateContentConfig(
    tools=[types.Tool(google_search=types.GoogleSearch())],
    image_config=types.ImageConfig(aspect_ratio="16:9")
)
```

Enables real-time data visualization and fact-grounded imagery.

## Thought Signatures

When thinking mode is enabled, responses include thought process:

```
<thinking>
The user wants a modern office space. I'll consider:
- Natural lighting from large windows
- Minimalist furniture arrangement
- Contemporary color palette (whites, grays, wood tones)
- Plants for biophilic elements
</thinking>

[Image generated]
```

## Multi-Image Input

### Flash Model (up to 3 images)

```python
from PIL import Image

img1 = Image.open("reference_style.jpg")
img2 = Image.open("subject.jpg")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        "Apply the style from the first image to the subject in the second image",
        img1,
        img2
    ]
)
```

### Pro Model (up to 14 images)

```python
# Identity preservation across multiple references
references = [Image.open(f"face_{i}.jpg") for i in range(5)]

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "Create a professional headshot of this person in a studio setting",
        *references
    ],
    config=types.GenerateContentConfig(
        image_config=types.ImageConfig(
            aspect_ratio="3:4",
            image_size="4K"
        )
    )
)
```

## Response Handling

```python
response = client.models.generate_content(...)

for part in response.parts:
    if part.inline_data is not None:
        # Image data
        image = part.as_image()  # PIL Image
        image.save("output.png")
    elif part.text is not None:
        # Text response (if response_modalities includes text)
        print(part.text)
```

## Error Handling

```python
try:
    response = client.models.generate_content(...)
except genai.errors.ClientError as e:
    if "SAFETY" in str(e):
        print("Content blocked by safety filters")
    elif "RATE_LIMIT" in str(e):
        print("Rate limited - try again later")
    else:
        print(f"API error: {e}")
```

## Best Practices

1. **Use response_modalities**: Set `["Image"]` for image-only output to avoid unexpected text
2. **Match aspect ratios**: Use appropriate ratios for use case (16:9 for banners, 9:16 for stories)
3. **Leverage multi-turn**: Refine iteratively rather than rewriting entire prompts
4. **Pro for quality**: Use Pro model for final assets, Flash for rapid iteration
5. **Thinking for accuracy**: Enable thinking mode for technical diagrams or precise compositions

## Limitations

- **Single image output**: Each call produces one image
- **No direct inpainting mask**: Use natural language to describe what to change
- **Text rendering**: May struggle with very small or detailed text
- **Consistency**: Character consistency may vary across separate generations

## Rate Limits

| Model | RPM | TPM |
|-------|-----|-----|
| Flash | 15 | 1M |
| Pro | 2 | 32K |

Check current limits at: https://ai.google.dev/gemini-api/docs/rate-limits
