# Precision-Parameterized Candid Shot

This template produces a single precision-parameterized candid shot prompt. Unlike the random-matrix package, nothing is sampled here: every variable is bound exactly from a shot spec (JSON), and quantified parameters (cm, percentages, degrees) go straight into the body. The consumer binds all variables before rendering; the rendered result is the final prompt body without further rewriting.

## Slot convention

Optional clause variables (`perspective_clause`, `sections_block`, `foreground_sentence`, `light_fill_clause`, `palette_sentence`, `background_sentence`, `fingerprints_sentence`, `tail_clause`) carry their own punctuation and leading spaces/newlines; bind them to an empty string when unused and the whole clause disappears. `genre` defaults to "candid lifestyle photo"; use a different genre phrase (e.g. editorial portrait) for non-candid shots.

Vertical 9:16 vintage digital camera snapshot, an adult East Asian woman with long messy black hair and wispy bangs at a nighttime Chinese Nuo opera ritual festival, positioned close beside a weathered black-red-gold Nuo mask hung with red ribbons with her direct piercing gaze and softly parted lips.
She wears a deep red sleeveless embroidered ceremonial dress.
Camera positioned for a close over-the-shoulder portrait beside the mask, 50mm lens, a tight close-up from behind the shoulder line, the weathered Nuo mask immediately beside her, the torch-lit ritual crowd blurred far behind.
Torchlight glowing behind her with a subtle direct on-camera flash on the face, warm orange rim light separating her from the deep shadows. Main colors: dark red, aged gold, warm orange, deep shadow black. Drifting smoke, blurred ritual crowds, deep impenetrable shadows.
vintage digital camera snapshot aesthetic, real human skin texture, shallow depth of field, subtle grain, high dynamic range, 4K, ultra detailed, an eerie, sensual folk-horror mood, no cartoonish look, no plastic over-smoothed skin, no stiff pose, no overexposure, no cluttered composition, no watermarks, no logos, no text errors, photorealistic.

## Self-check

- Quantified parameters (cm, %, degrees) survive verbatim and are not rewritten as vague adjectives.
- Palette percentages sum to 100 in descending order (when `palette_sentence` is used).
- Foreground occlusion carries a percentage (when `foreground_sentence` is used).
- Negatives are complete; no studio-lighting vocabulary leaks in.
