# Precision-Parameterized Candid Shot

This template produces a single precision-parameterized candid shot prompt. Unlike the random-matrix package, nothing is sampled here: every variable is bound exactly from a shot spec (JSON), and quantified parameters (cm, percentages, degrees) go straight into the body. The consumer binds all variables before rendering; the rendered result is the final prompt body without further rewriting.

## Slot convention

Optional clause variables (`perspective_clause`, `foreground_sentence`, `light_fill_clause`, `palette_sentence`, `background_sentence`, `fingerprints_sentence`, `tail_clause`) carry their own punctuation and leading spaces; bind them to an empty string when unused and the whole clause disappears.

Vertical 9:16 candid lifestyle photo, an adult East Asian woman with long slightly messy black hair lying on her stomach across a rumpled bed at night, turning her head back toward the camera with soft moist eyes and slightly parted lips.
She wears a white floral lace camisole and light gray lounge shorts.
Camera height about 55 cm from the mattress, 35mm lens, subject occupies about 68% of the frame, cropped from upper thighs upward. A blurred notebook and laptop cover about 15% of the lower foreground.
Warm bedside lamp from frame left at about 45 degrees, cool city window light from frame right. Main colors: 40% warm cream, 25% dark brown-black, 20% cool blue-gray, 15% skin tone. Scene fingerprints: city lights outside the large window, photo collage on the wall, plush toy near the pillow.
Natural skin texture, shallow depth of field, subtle film grain, realistic candid photography, intimate lived-in bedroom atmosphere, no collage, no split screen.

## Self-check

- Quantified parameters (cm, %, degrees) survive verbatim and are not rewritten as vague adjectives.
- Palette percentages sum to 100 in descending order (when `palette_sentence` is used).
- Foreground occlusion carries a percentage (when `foreground_sentence` is used).
- Negatives are complete; no studio-lighting vocabulary leaks in.
