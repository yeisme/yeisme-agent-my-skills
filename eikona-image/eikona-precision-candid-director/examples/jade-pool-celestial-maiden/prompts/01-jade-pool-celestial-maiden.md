# Precision-Parameterized Candid Shot

This template produces a single precision-parameterized candid shot prompt. Unlike the random-matrix package, nothing is sampled here: every variable is bound exactly from a shot spec (JSON), and quantified parameters (cm, percentages, degrees) go straight into the body. The consumer binds all variables before rendering; the rendered result is the final prompt body without further rewriting.

## Slot convention

Optional clause variables (`perspective_clause`, `sections_block`, `foreground_sentence`, `light_fill_clause`, `palette_sentence`, `background_sentence`, `fingerprints_sentence`, `tail_clause`) carry their own punctuation and leading spaces/newlines; bind them to an empty string when unused and the whole clause disappears. `genre` defaults to "candid lifestyle photo"; use a different genre phrase (e.g. editorial portrait) for non-candid shots.

Vertical 2:3 Chinese mythological cinema still, a serene adult Chinese celestial maiden seated beside the turquoise waters of the heavenly Jade Pool, her fingertips gently touching a floating white lotus with a tranquil, otherworldly serenity.
She wears pale mint and blush silk hanfu with delicate lotus embroidery, and jade hair ornaments.
Camera positioned at an intimate close distance beside the water, 85mm portrait lens, shallow depth of field, an intimate cinematic composition, concentric ripples reflecting her face, silver fish visible beneath the clear water. Willow branches cover the foreground frame edges, naturally intruding.
Soft diffused morning light. Main colors: turquoise, pale mint, blush pink, jade white. Distant jade pavilions softened by mist.
realistic skin texture, translucent silk texture, soft diffused light, atmospheric mist, high dynamic range, 4K, highly detailed, a tranquil Chinese mythology mood, no text, no watermarks, no logos, no cartoonish look, no plastic over-smoothed skin, no cluttered composition, no overexposure, no text errors, photorealistic.

## Self-check

- Quantified parameters (cm, %, degrees) survive verbatim and are not rewritten as vague adjectives.
- Palette percentages sum to 100 in descending order (when `palette_sentence` is used).
- Foreground occlusion carries a percentage (when `foreground_sentence` is used).
- Negatives are complete; no studio-lighting vocabulary leaks in.
