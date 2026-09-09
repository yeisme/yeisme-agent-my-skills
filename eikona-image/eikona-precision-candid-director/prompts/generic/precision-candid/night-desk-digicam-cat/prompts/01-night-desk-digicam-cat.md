# Precision-Parameterized Candid Shot

This template produces a single precision-parameterized candid shot prompt. Unlike the random-matrix package, nothing is sampled here: every variable is bound exactly from a shot spec (JSON), and quantified parameters (cm, percentages, degrees) go straight into the body. The consumer binds all variables before rendering; the rendered result is the final prompt body without further rewriting.

## Slot convention

Optional clause variables (`perspective_clause`, `sections_block`, `foreground_sentence`, `light_fill_clause`, `palette_sentence`, `background_sentence`, `fingerprints_sentence`, `tail_clause`) carry their own punctuation and leading spaces/newlines; bind them to an empty string when unused and the whole clause disappears. `genre` defaults to "candid lifestyle photo"; use a different genre phrase (e.g. editorial portrait) for non-candid shots.

Vertical 3:4 candid lifestyle photo, a young adult woman with extremely long natural black hair, messy wispy bangs and slightly tousled strands as she sits beside a small cluttered desk in a cozy bedroom at night, looking softly toward the camera, one hand resting near her lips with a quiet, dreamy, detached expression.
She wears an oversized cream vintage knitted sweater draped loosely off one shoulder, its extra long sleeves covering part of her hands, with a subtle dark knitted pattern.
Camera positioned at close distance at her eye level, 35mm equivalent lens, slight wide angle, subject sits on the right side of the frame occupying about 55% of the width, cropped at the waist. An open silver laptop cover about 20% of the lower-left foreground.
Dim warm ambient room lighting, slightly underexposed overall with soft shadows. Main colors: 30% warm gray beige, 25% cream, 20% muted brown, 15% dark charcoal, 10% silver gray. Warm gray beige bedroom walls with small photos and everyday objects, and a white cat lying on the back of the chair behind her, looking at the camera. Scene fingerprints: a white cat lying on the chair back staring into the camera, small photos and everyday clutter on the wall and desk, the faint glow of the open laptop screen.
old compact digital camera snapshot with early 2000s digicam aesthetic, high ISO grain and subtle film grain, slight softness and imperfect focus, slightly underexposed with soft shadows, muted low saturation and low contrast with slightly faded colors, natural skin texture, an intimate lived-in atmosphere, cozy Japanese lifestyle photography, candid and unposed, no studio lighting, no professional fashion shoot, no overly perfect skin, no plastic skin, no heavy makeup, no HDR, no oversaturated colors, no strong orange lighting, no dramatic cinematic lighting, no luxury bedroom, no perfectly clean room, no sharp commercial photography, no exaggerated bokeh, no anime, no illustration, no doll face, no distorted hands, no extra fingers, no deformed cat, no overexposed skin, photorealistic.

## Self-check

- Quantified parameters (cm, %, degrees) survive verbatim and are not rewritten as vague adjectives.
- Palette percentages sum to 100 in descending order (when `palette_sentence` is used).
- Foreground occlusion carries a percentage (when `foreground_sentence` is used).
- Negatives are complete; no studio-lighting vocabulary leaks in.
