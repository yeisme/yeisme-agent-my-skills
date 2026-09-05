# Precision-Parameterized Candid Shot

This template produces a single precision-parameterized candid shot prompt. Unlike the random-matrix package, nothing is sampled here: every variable is bound exactly from a shot spec (JSON), and quantified parameters (cm, percentages, degrees) go straight into the body. The consumer binds all variables before rendering; the rendered result is the final prompt body without further rewriting.

## Slot convention

Optional clause variables (`perspective_clause`, `foreground_sentence`, `light_fill_clause`, `palette_sentence`, `background_sentence`, `fingerprints_sentence`, `tail_clause`) carry their own punctuation and leading spaces; bind them to an empty string when unused and the whole clause disappears.

Vertical 9:16 candid lifestyle photo, an adult East Asian woman indoors at night, long messy dark hair with wispy bangs, soft pink makeup, slightly flushed cheeks, glossy natural lips bending forward toward the camera, upper body leaning close to the lens, shoulders slightly drawn inward, both knees slightly bent, hands naturally resting near her thighs with large moist eyes looking directly into the camera.
She wears a light gray white lace camisole with thin straps and white mid calf socks.
Camera positioned slightly above eye level and extremely close to her face, 20mm wide angle lens, strong perspective distortion, her face large in the upper center of the frame while her body recedes downward.
Direct on camera flash, bright pale skin highlights, hard compact shadows. Dim ordinary apartment background, dark wooden floor, slightly underexposed surroundings.
Real smartphone flash photography, Japanese Korean late night snapshot aesthetic, natural skin texture, slight grain, subtle motion softness, imperfect framing, giving a spontaneous intimate snapshot feeling, no studio lighting, no beauty filter, photorealistic.

## Self-check

- Quantified parameters (cm, %, degrees) survive verbatim and are not rewritten as vague adjectives.
- Palette percentages sum to 100 in descending order (when `palette_sentence` is used).
- Foreground occlusion carries a percentage (when `foreground_sentence` is used).
- Negatives are complete; no studio-lighting vocabulary leaks in.
