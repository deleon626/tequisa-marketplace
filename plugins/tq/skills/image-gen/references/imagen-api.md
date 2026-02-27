# Imagen API Reference

Google's dedicated image generation API, separate from Gemini's native capabilities.

## Overview

Imagen is Google's specialized text-to-image model. Unlike Nano Banana, Imagen uses a dedicated `generate_images()` endpoint and supports generating multiple images per request.

## Models

| Model ID | Alias | Description |
|----------|-------|-------------|
| `imagen-4.0-generate-001` | standard | Balanced quality and speed |
| `imagen-4.0-ultra-generate-001` | ultra | Highest quality |
| `imagen-4.0-fast-generate-001` | fast | Fastest generation |
| `imagen-3.0-generate-002` | legacy | Previous generation |

## Key Differences from Nano Banana

| Feature | Imagen | Nano Banana |
|---------|--------|-------------|
| Image editing | No | Yes |
| Multi-turn chat | No | Yes |
| Reference images | No | Up to 14 |
| Multiple outputs | 1-4 per call | 1 |
| Thinking mode | No | Yes (Pro) |
| Search grounding | No | Yes (Pro) |
| Person generation control | Yes | No |

## API Usage

### Basic Generation

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_images(
    model="imagen-4.0-generate-001",
    prompt="A serene mountain landscape at sunrise",
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="16:9"
    )
)

# Save image
for generated_image in response.generated_images:
    generated_image.image.save("output.png")
```

### Multiple Images

```python
response = client.models.generate_images(
    model="imagen-4.0-generate-001",
    prompt="Product mockup of a modern smartphone",
    config=types.GenerateImagesConfig(
        number_of_images=4,  # Generate 4 variations
        aspect_ratio="1:1"
    )
)

for i, generated_image in enumerate(response.generated_images):
    generated_image.image.save(f"product_{i+1}.png")
```

### Person Generation Control

```python
response = client.models.generate_images(
    model="imagen-4.0-generate-001",
    prompt="Business meeting in a modern conference room",
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="16:9",
        person_generation="allow_adult"  # Allow adult faces
    )
)
```

## Configuration Options

### GenerateImagesConfig

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `number_of_images` | int | 1 | Images to generate (1-4) |
| `aspect_ratio` | str | "1:1" | Output dimensions |
| `person_generation` | str | "dont_allow" | Person face generation control |
| `output_mime_type` | str | "image/png" | Output format |
| `negative_prompt` | str | None | What to avoid in generation |

### Aspect Ratios

Imagen supports fewer aspect ratios than Nano Banana:

- `1:1` - Square (default)
- `3:4` - Portrait
- `4:3` - Landscape
- `9:16` - Vertical/Stories
- `16:9` - Widescreen

### Person Generation Modes

| Mode | Description |
|------|-------------|
| `dont_allow` | No human faces generated (default, safest) |
| `allow_adult` | Adult faces allowed |
| `allow_all` | All ages allowed |

## Prompt Guidelines

### Token Limit

Imagen prompts are limited to **480 tokens**. Keep prompts concise.

### Language

Imagen works best with **English prompts**. Multi-language support is limited compared to Nano Banana.

### Effective Prompts

```python
# Good - concise and descriptive
"Professional product photo of wireless earbuds on marble surface, soft studio lighting"

# Good - clear style direction
"Minimalist logo design, geometric shapes, blue and white color scheme, vector style"

# Less effective - too vague
"earbuds"

# Less effective - too long/complex
"A highly detailed photograph showing a pair of premium wireless earbuds..."
```

### Negative Prompts

```python
response = client.models.generate_images(
    model="imagen-4.0-generate-001",
    prompt="Modern living room interior",
    config=types.GenerateImagesConfig(
        number_of_images=1,
        negative_prompt="cluttered, messy, dark, low quality"
    )
)
```

## Response Handling

```python
response = client.models.generate_images(...)

# Check for generated images
if response.generated_images:
    for i, gen_image in enumerate(response.generated_images):
        # Access PIL Image
        pil_image = gen_image.image
        pil_image.save(f"output_{i}.png")

        # Or access raw bytes
        # image_bytes = gen_image.image_bytes
```

## Error Handling

```python
try:
    response = client.models.generate_images(...)
except genai.errors.ClientError as e:
    if "SAFETY" in str(e):
        print("Content blocked by safety filters")
    elif "RATE_LIMIT" in str(e):
        print("Rate limited")
    elif "INVALID_ARGUMENT" in str(e):
        print("Invalid configuration")
    else:
        print(f"API error: {e}")
```

## Use Cases

### When to Use Imagen

- **Multiple variations**: Need 4 different options quickly
- **Person control**: Specific requirements for human generation
- **Simple text-to-image**: No editing or reference images needed
- **Fast generation**: Use `fast` model for rapid iteration

### When to Use Nano Banana Instead

- **Image editing**: Modifying existing images
- **Multi-turn refinement**: Iterative improvement through conversation
- **Reference images**: Maintaining style or identity consistency
- **Higher resolution**: Need 4K output
- **Complex reasoning**: Require thinking mode for accurate generation

## Rate Limits

| Model | RPM | Images/min |
|-------|-----|------------|
| Standard | 10 | 40 |
| Ultra | 5 | 20 |
| Fast | 20 | 80 |

## Best Practices

1. **Keep prompts concise**: Stay well under 480 tokens
2. **Use English**: Best results with English prompts
3. **Specify style**: Be explicit about desired aesthetic
4. **Use negative prompts**: Exclude unwanted elements
5. **Generate multiple**: Request 4 images and pick the best
6. **Match model to need**: Fast for iteration, Ultra for final assets

## Limitations

- **No image editing**: Cannot modify existing images
- **No multi-turn**: Each request is independent
- **No reference images**: Cannot provide style or subject references
- **English-centric**: Limited multi-language support
- **Token limit**: 480 tokens maximum for prompts
- **Single resolution**: No 4K option like Nano Banana Pro
