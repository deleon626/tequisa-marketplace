---
name: image-gen
description: Generate and edit AI images using Gemini's Nano Banana (Native) and Imagen APIs. Supports text-to-image, image editing, batch generation, and multi-turn conversations. Use for hero banners, product mockups, illustrations, backgrounds, and image editing tasks.
---

# Image Generation

Generate and edit AI images using Google's Gemini APIs. Supports both **Nano Banana** (native multimodal) and **Imagen** (dedicated image generation) APIs.

## Quick Start

```bash
# Generate with Nano Banana (default)
python scripts/generate.py -p "sunset over mountains" -o hero.png

# Generate with Imagen (multiple outputs)
python scripts/generate.py -p "product mockup" --api imagen --count 4 -o product.png

# Edit existing image
python scripts/edit.py edit -i photo.png -p "Add warm lighting" -o edited.png

# Interactive chat for refinement
python scripts/chat.py --model pro
```

## API Comparison

| Feature | Nano Banana | Imagen |
|---------|-------------|--------|
| Text-to-Image | Yes | Yes |
| Image Editing | Yes | **No** |
| Multi-turn Chat | Yes | **No** |
| Reference Images | Up to 14 (Pro) | **No** |
| Multiple outputs/call | 1 | 1-4 |
| Resolution | 1K, 2K, 4K (Pro) | 1K, 2K |
| Thinking Mode | Pro only | No |
| Search Grounding | Pro only | No |
| Person Generation Control | No | **Yes** |

### When to Use Each API

**Use Nano Banana when:**
- Editing existing images
- Refining through conversation
- Using reference images for style/identity
- Needing 4K resolution
- Complex compositions requiring reasoning

**Use Imagen when:**
- Need multiple variations quickly (up to 4)
- Simple text-to-image without editing
- Need person generation control
- Faster batch generation

## Models

### Nano Banana
| Model | Alias | Features |
|-------|-------|----------|
| `gemini-2.5-flash-image` | flash | Fast, up to 3 input images |
| `gemini-3-pro-image-preview` | pro | 4K, 14 inputs, thinking mode, search grounding |

### Imagen
| Model | Alias | Features |
|-------|-------|----------|
| `imagen-4.0-generate-001` | standard | Balanced quality/speed |
| `imagen-4.0-ultra-generate-001` | ultra | Highest quality |
| `imagen-4.0-fast-generate-001` | fast | Fastest generation |
| `imagen-3.0-generate-002` | legacy | Previous generation |

## Configuration

Set `GEMINI_API_KEY` environment variable:

```bash
export GEMINI_API_KEY=your-api-key-here
```

Required packages:
```bash
pip install google-genai Pillow python-dotenv
```

## Scripts Reference

### generate.py - Text-to-Image

Unified generation supporting both APIs.

```bash
# Nano Banana (default)
python scripts/generate.py -p "prompt" -o output.png
python scripts/generate.py -p "city" --model pro --size 4K --thinking

# Imagen
python scripts/generate.py -p "product" --api imagen --model ultra --count 4
python scripts/generate.py -p "meeting" --api imagen --person-gen allow_adult
```

**Arguments:**
| Arg | Description |
|-----|-------------|
| `-p, --prompt` | Image description (required) |
| `-o, --output` | Output path (default: auto-generated) |
| `--output-dir` | Directory for auto outputs (default: ./generated-images) |
| `--api` | nano or imagen (default: nano) |
| `-m, --model` | Model variant |
| `-a, --aspect` | Aspect ratio |
| `-s, --size` | 1K/2K/4K (Nano Pro only) |
| `-n, --count` | Number of images (Imagen only, 1-4) |
| `--person-gen` | Person control (Imagen only) |
| `--with-text` | Include text response (Nano only) |
| `--thinking` | Enable thinking (Nano Pro only) |
| `--grounding` | Enable search (Nano Pro only) |

### edit.py - Image Editing

Edit existing images (Nano Banana only).

```bash
# Generic edit
python scripts/edit.py edit -i input.png -p "instruction" -o output.png

# Specific operations
python scripts/edit.py background -i photo.jpg --new-bg "beach sunset" -o result.jpg
python scripts/edit.py style -i image.png --style "watercolor" -o artistic.png
python scripts/edit.py add -i room.jpg --element "plant" --position "corner" -o room2.jpg
python scripts/edit.py remove -i photo.jpg --element "person in background" -o clean.jpg
python scripts/edit.py recolor -i car.png --target "car" --color "red" -o car_red.png
python scripts/edit.py combine --images img1.png img2.png -p "blend seamlessly" -o merged.png
```

**Subcommands:**
| Command | Description |
|---------|-------------|
| edit | Generic editing with custom prompt |
| background | Replace image background |
| style | Apply artistic style transfer |
| add | Add element to image |
| remove | Remove element from image |
| recolor | Change color of specific element |
| combine | Merge multiple images |

### batch.py - Batch Generation

Generate multiple images from config file.

```bash
python scripts/batch.py -c config.json -o ./output --workers 4
```

**Config format:**
```json
{
    "api": "nano",
    "model": "flash",
    "images": [
        {"name": "hero", "prompt": "...", "aspect": "16:9", "size": "2K"},
        {"name": "about", "prompt": "...", "aspect": "4:3"}
    ]
}
```

### chat.py - Interactive Chat

Multi-turn image refinement (Nano Banana only).

```bash
python scripts/chat.py
python scripts/chat.py --model pro --thinking
```

**Chat commands:**
| Command | Description |
|---------|-------------|
| save [filename] | Save current image |
| aspect \<ratio\> | Set aspect ratio |
| size \<1K\|2K\|4K\> | Set size (Pro only) |
| model \<flash\|pro\> | Switch model |
| thinking on\|off | Toggle thinking |
| status | Show settings |
| history | Show conversation |
| clear | Start fresh |
| help | Show commands |
| quit | Exit |

## Aspect Ratios

**Nano Banana:** 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9

**Imagen:** 1:1, 3:4, 4:3, 9:16, 16:9

## Model Selection Decision Tree

```
Need to edit existing image?
├─ Yes → Nano Banana
└─ No
   ├─ Need multiple variations?
   │  └─ Yes → Imagen (--count 4)
   ├─ Need 4K resolution?
   │  └─ Yes → Nano Banana Pro
   ├─ Need thinking/reasoning?
   │  └─ Yes → Nano Banana Pro
   ├─ Need person generation control?
   │  └─ Yes → Imagen
   └─ Default → Nano Banana Flash (fastest)
```

## Prompting Guide Summary

### SCALS Framework

1. **Subject**: Who/what is the focus
2. **Composition**: Shot framing and angle
3. **Action**: What's happening
4. **Location**: Scene setting
5. **Style**: Overall aesthetic

### Example Prompt

```
"A vintage Porsche 911 photographed from a low angle on a rain-slicked
Tokyo street at night. Headlights on, neon reflections in puddles.
Cinematic mood, film grain, 16:9 aspect ratio."
```

### Key Tips

- Be descriptive but natural (not keyword lists)
- Use photography terms: "f/1.8 bokeh", "golden hour", "soft lighting"
- Specify composition: "negative space on left for text"
- Refine iteratively in chat mode

See `references/prompting-guide.md` for comprehensive strategies.

## Output Directory

**Default behavior:**
- Auto-generates to `./generated-images/{timestamp}_{prompt_slug}.png`
- Creates directory if needed
- Batch outputs use config `name` field

**Recommendations:**
- Quick tests: Use defaults
- Projects: Specify `--output ./assets/images/hero.png`
- Add `generated-images/` to `.gitignore`

## Troubleshooting

### "GEMINI_API_KEY not set"
Export the environment variable or create `.env` file.

### "google-genai not installed"
```bash
pip install google-genai Pillow
```

### "No image generated"
- Check prompt for content policy violations
- Try simpler prompt
- Verify API key is valid

### "Rate limited"
- Wait and retry
- Reduce parallel workers in batch mode
- Check quota at Google AI Studio

### Image quality issues
- Use Pro model for higher quality
- Enable thinking mode for complex scenes
- Be more specific in prompts

## Additional References

- `references/nano-banana-api.md` - Complete Nano Banana API documentation
- `references/imagen-api.md` - Complete Imagen API documentation
- `references/prompting-guide.md` - Comprehensive prompting strategies
- `examples/batch-nano-banana.json` - Batch config example
- `examples/batch-imagen.json` - Batch config example

## External Documentation

- [Gemini Image Generation](https://ai.google.dev/gemini-api/docs/image-generation)
- [Imagen API](https://ai.google.dev/gemini-api/docs/imagen)
- [Prompting Guide](https://dev.to/googleai/nano-banana-pro-prompting-guide-strategies-1h9n)
