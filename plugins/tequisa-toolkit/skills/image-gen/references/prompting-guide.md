# Gemini Image Generation Prompting Guide

Strategies for effective prompts with Nano Banana and Imagen APIs.

## Core Principles

### 1. Edit Conversationally
Make incremental adjustments rather than regenerating from scratch.

```
# Good - iterative refinement
"Create a coffee shop interior"
→ "Add warm morning light through the windows"
→ "Make the wood tones richer"
→ "Add a few customers at tables"

# Less effective - starting over each time
"Create a coffee shop interior with warm morning light, rich wood tones, and customers"
```

### 2. Use Natural Language
Write prompts like you're talking to a creative collaborator, not a search engine.

```
# Good - natural and descriptive
"A cozy reading nook by a rain-streaked window, soft lamp light, someone curled up with a book"

# Less effective - keyword stuffing
"reading nook, window, rain, lamp, book, cozy, warm, person, indoor, comfortable"
```

### 3. Be Descriptive
Explicitly describe subjects, materials, lighting, and mood.

```
# Good - specific details
"A ceramic coffee mug with a matte sage green glaze, steam rising, on a weathered oak table, soft morning backlight"

# Less effective - vague
"A coffee cup on a table"
```

### 4. Provide Context
Explain the purpose or audience when relevant.

```
# Good - context helps
"Hero banner for a sustainable fashion brand: flowing organic cotton fabrics in earth tones, natural studio lighting, eco-luxury aesthetic, 16:9"

# Also good
"Product shot for an e-commerce listing: minimalist wireless earbuds, white background, soft shadows, professional product photography"
```

## The SCALS Framework

Structure prompts using these five elements:

### Subject
Who or what is the main focus?

```
"A golden retriever puppy"
"An Art Deco skyscraper"
"A vintage espresso machine"
```

### Composition
How is the shot framed?

```
"Close-up portrait"
"Wide establishing shot"
"Low angle looking up"
"Bird's eye view"
"Rule of thirds, subject on left"
```

### Action
What's happening in the scene?

```
"Running through autumn leaves"
"Steam rising from the cup"
"Sunlight filtering through clouds"
"People walking on a busy street"
```

### Location
Where is the scene set?

```
"In a sunlit greenhouse"
"On a foggy San Francisco street"
"Inside a minimalist Japanese interior"
"Against a gradient studio backdrop"
```

### Style
What's the overall aesthetic?

```
"Photorealistic, editorial photography"
"3D render, Pixar style"
"Watercolor illustration"
"Film noir, high contrast"
"Flat vector illustration"
```

### Complete SCALS Example

```
Subject: A vintage Porsche 911
Composition: Low angle, three-quarter front view
Action: Parked, headlights on, slight motion blur in background
Location: Rain-slicked Tokyo street at night
Style: Cinematic, moody, neon reflections, film grain

→ "A vintage Porsche 911 photographed from a low angle, three-quarter front view, parked on a rain-slicked Tokyo street at night. Headlights on, neon signs reflecting in the wet pavement, slight motion blur in the background suggesting city life. Cinematic mood, film grain, moody lighting."
```

## Advanced Controls

### Camera Settings

```
# Depth of field
"Shallow depth of field, f/1.8, blurred background"
"Deep focus, everything sharp, f/11"

# Focal length
"Wide angle lens, 24mm, expansive view"
"Telephoto compression, 200mm, flattened perspective"
"Macro lens, extreme close-up, fine details visible"

# Motion
"Motion blur suggesting speed"
"Frozen action, high shutter speed"
"Long exposure, light trails"
```

### Lighting

```
# Natural light
"Golden hour, warm side lighting"
"Overcast day, soft diffused light"
"Harsh midday sun, strong shadows"
"Blue hour, twilight atmosphere"

# Studio lighting
"Rembrandt lighting, dramatic shadows"
"High key, bright and airy"
"Low key, moody with dark tones"
"Rim lighting, silhouette effect"
"Softbox lighting, even illumination"

# Color temperature
"Warm tungsten light"
"Cool daylight balanced"
"Mixed lighting, warm/cool contrast"
```

### Color and Mood

```
# Color schemes
"Monochromatic blue palette"
"Complementary orange and teal"
"Muted earth tones"
"Vibrant saturated colors"
"Desaturated, faded vintage look"

# Mood keywords
"Serene and peaceful"
"Energetic and dynamic"
"Mysterious and atmospheric"
"Warm and inviting"
"Clean and professional"
```

### Aspect Ratio in Prompts

```
"9:16 vertical composition for Instagram stories"
"16:9 widescreen banner layout"
"1:1 square format, centered subject"
"Ultrawide 21:9 cinematic panorama"
```

## 7 Key Techniques

### 1. Text Rendering
Gemini excels at generating sharp, legible text in images.

```
"Poster design with bold text saying 'SUMMER SALE' in white sans-serif font, beach background"

"Business card mockup with 'John Smith, CEO' in elegant serif typography"

"Neon sign reading 'OPEN' in pink cursive script against brick wall"
```

### 2. Real-World Knowledge
Leverage Gemini's understanding for accuracy.

```
"The Eiffel Tower at sunset, accurate architectural details"

"A correctly anatomically proportioned human hand holding a pen"

"Map of Europe with accurate country borders, illustrated style"
```

### 3. Translation/Localization
Generate text in multiple languages.

```
"Japanese restaurant menu board with '本日のランチ' (today's lunch) in brush calligraphy"

"Street sign in French: 'Rue de la Paix'"

"Arabic calligraphy spelling 'Welcome'"
```

### 4. Studio-Quality Edits
Professional photography controls.

```
"Product photo with studio lighting setup: key light at 45 degrees, fill light opposite, white seamless background"

"Portrait with cinematic color grading, lifted shadows, crushed blacks, teal highlights"

"Food photography, overhead shot, natural window light with white bounce card"
```

### 5. Resize with Precision
Control output dimensions.

```
"4K resolution, ultra-detailed hero image"
"Web-optimized 1K thumbnail"
"2K social media asset"
```

### 6. Image Blending
Combine multiple reference images (Nano Banana).

```
# With reference images provided:
"Blend the architectural style from image 1 with the color palette from image 2"

"Place the person from image 1 into the background scene from image 2, matching lighting"

"Create a composite using elements from all three reference images"
```

### 7. Brand Consistency
Maintain visual identity.

```
"Apply the brand's signature coral (#FF6B6B) and navy (#1A365D) color scheme"

"Modern tech startup aesthetic: clean lines, generous whitespace, sans-serif typography"

"Vintage Americana style: warm sepia tones, distressed textures, retro typography"
```

## Nano Banana Pro Capabilities

### Identity Locking
Maintain consistent faces across scenarios.

```
# With multiple reference images of the same person:
"Generate a professional headshot maintaining the exact facial features from the reference images"

"Create different expressions and angles while keeping the same identity"
```

### Semantic Editing
Intelligent object manipulation.

```
"Remove the person in the background, fill naturally"
"Change the season from summer to autumn"
"Colorize this black and white photo with realistic colors"
```

### Dimensional Translation
Convert between 2D and 3D representations.

```
"Convert this floor plan into a 3D interior render"
"Transform this wireframe sketch into a polished UI design"
"Turn this side-view car sketch into a three-quarter perspective render"
```

### Layout Control
Work from sketches or wireframes.

```
"Transform this rough wireframe into a polished website hero section"
"Use this layout sketch as a guide for the final composition"
```

### Google Search Integration (Pro)
Real-time data for visualizations.

```
# With search grounding enabled:
"Create an infographic showing current population statistics for major cities"
"Generate a chart visualizing recent stock market trends"
```

## Common Pitfalls

### Too Vague
```
# Bad
"A dog"

# Better
"A golden retriever puppy sitting in autumn leaves, warm afternoon light, shallow depth of field"
```

### Conflicting Instructions
```
# Bad - contradictory
"Minimalist design with lots of intricate details"

# Better - coherent
"Minimalist design with a single focal point of intricate detail"
```

### Over-Specification
```
# Bad - too prescriptive
"Exactly 3 trees, 2 birds, 1 cloud, 47 blades of grass"

# Better - descriptive intent
"A peaceful meadow with scattered trees, birds in flight"
```

### Keyword Lists
```
# Bad
"sunset, beach, palm tree, ocean, waves, sand, tropical, paradise"

# Better
"A tropical beach at sunset with palm trees silhouetted against an orange sky, gentle waves lapping at the shore"
```

## Current Limitations

1. **Small text/fine details**: Very small text or intricate patterns may not render perfectly
2. **Factual accuracy**: Verify details in diagrams, infographics, and data visualizations
3. **Multi-language nuances**: Grammar and cultural context may vary
4. **Complex compositions**: Multi-element scenes may produce artifacts
5. **Character consistency**: Identity may drift across separate generations (use reference images)
6. **Hands and text**: Common AI image generation challenges still apply

## Quick Reference

### Essential Modifiers

| Category | Examples |
|----------|----------|
| Quality | 4K, high resolution, detailed, professional |
| Lighting | golden hour, studio lighting, dramatic shadows |
| Style | photorealistic, illustration, 3D render, watercolor |
| Mood | serene, energetic, mysterious, warm |
| Composition | close-up, wide shot, centered, rule of thirds |

### Photography Terms Cheat Sheet

| Term | Effect |
|------|--------|
| f/1.8 | Shallow depth, blurry background |
| f/11 | Deep focus, everything sharp |
| Golden hour | Warm, soft lighting |
| High key | Bright, minimal shadows |
| Low key | Dark, dramatic shadows |
| Bokeh | Blurred light points |
| Rim light | Edge lighting, silhouette |
