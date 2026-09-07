# Precision-Parameterized Candid Shot

This template produces a single precision-parameterized candid shot prompt. Unlike the random-matrix package, nothing is sampled here: every variable is bound exactly from a shot spec (JSON), and quantified parameters (cm, percentages, degrees) go straight into the body. The consumer binds all variables before rendering; the rendered result is the final prompt body without further rewriting.

## Slot convention

Optional clause variables (`perspective_clause`, `sections_block`, `foreground_sentence`, `light_fill_clause`, `palette_sentence`, `background_sentence`, `fingerprints_sentence`, `tail_clause`) carry their own punctuation and leading spaces/newlines; bind them to an empty string when unused and the whole clause disappears. `genre` defaults to "candid lifestyle photo"; use a different genre phrase (e.g. editorial portrait) for non-candid shots.

Horizontal 16:9 cinematic close-up photograph, an adult East Asian woman with long black hair falling in messy strands, a few damp loose strands clinging to the sides of her face, as she holds an old black-red-gold Nuo ghost mask against the side of her face with her left hand, the mask covering about half of the frame, her right half-face emerging beside it, fingers lightly touching the mask's lower edge with her cold, quiet, stunning look — one visible eye gazing directly into the lens.
She wears a black-and-gold embroidered Chinese ceremonial robe.
Mask: the Nuo ghost mask is old and weathered, with ferocious fangs, round bulging eyes, mottled lacquer, and an aged metal texture; long red tassels hang naturally from it.
Makeup: red-brown eye makeup and slightly dewy, glossy lip makeup, the expression cold, stunning, and quiet.
Camera positioned at extremely close range, 85mm portrait lens, shallow depth of field, the face and the mask filling the entire frame.
Low-key warm light from the front-side illuminates the face and the mask's edges, with dramatic chiaroscuro and cinematic shadow layering. Main colors: black, dark red, aged gold. Almost entirely black, with only a few warm golden blurred lights.
dramatic chiaroscuro, cinematic close-up, real human skin texture, fine visible pores, a slight damp sweat sheen, cinematic shadow gradation, light film grain, high contrast, highly detailed, an eerie-beautiful, mysterious, Eastern dark-ritual mood, no cartoonish look, no plastic over-smoothed skin, no bright daylight look, no cluttered background, no overexposure, no clean new-looking mask, no watermarks, no logos, no text errors, photorealistic.

## Self-check

- Quantified parameters (cm, %, degrees) survive verbatim and are not rewritten as vague adjectives.
- Palette percentages sum to 100 in descending order (when `palette_sentence` is used).
- Foreground occlusion carries a percentage (when `foreground_sentence` is used).
- Negatives are complete; no studio-lighting vocabulary leaks in.
