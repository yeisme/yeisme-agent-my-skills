# Precision-Parameterized Candid Shot

This template produces a single precision-parameterized candid shot prompt. Unlike the random-matrix package, nothing is sampled here: every variable is bound exactly from a shot spec (JSON), and quantified parameters (cm, percentages, degrees) go straight into the body. The consumer binds all variables before rendering; the rendered result is the final prompt body without further rewriting.

## Slot convention

Optional clause variables (`perspective_clause`, `sections_block`, `foreground_sentence`, `light_fill_clause`, `palette_sentence`, `background_sentence`, `fingerprints_sentence`, `tail_clause`) carry their own punctuation and leading spaces/newlines; bind them to an empty string when unused and the whole clause disappears. `genre` defaults to "candid lifestyle photo"; use a different genre phrase (e.g. editorial portrait) for non-candid shots.

Vertical 9:16 ultra-close-up facial portrait photograph, a young adult East Asian woman with long black hair, a few soft loose strands resting naturally across her forehead and the sides of her face, facing the camera directly with a cool, sultry, languid, restrained allure — the quiet confidence of someone who knows she is beautiful, beautiful but never showy — her face from forehead to chin filling the entire frame, cheeks almost touching the frame edges with her half-lidded eyes gazing lazily straight into the lens with slightly lifted outer corners and a subtle fox-eye allure — never an exaggerated seductive smile, never a sweet-girl look.
She wears an understated dark-toned top that stays out of the frame's focus.
Features: a smooth, refined narrow oval face with a small delicate chin, a slim straight nose with a refined tip, and compact well-centered features that keep a soft, delicate East Asian femininity.
Eye makeup: low-saturation powdery gray, grayish violet-pink-brown eyeshadow with a faint lotus-pink wash under the eyes and fine natural aegyo-sal; a thin precise eyeliner extending naturally from the lash roots, visibly elongated and upturned at the outer corners to sculpt a long fox-eye contour; long, clearly separated lashes with a focused, lucid gaze.
Lip makeup: deep rose, berry-rose, cool-toned berry lips — full and refined with a defined cupid's bow, a soft satin sheen, the corners lifted almost imperceptibly; no teeth, no big laugh, the expression restrained yet sultry.
Skin: a cool-toned soft-focus base, translucent and fine, keeping slight real skin texture.
Camera positioned at extremely close range, the features pressed strongly toward the lens, 85mm portrait lens, shallow depth of field, soft focus, the face as the absolute visual center, a frontal straight-on view, the frame nearly filled by the face alone.
Soft low-intensity studio light, frontal and slightly to the side, with delicate shadows and a soft-focus cinematic feel on the face. Main colors: cold gray, powdery gray-pink, lotus pink, berry red. Deeply blurred with all detail suppressed, so only the face, the eyes, the lip color, and a few black loose strands stand out.
cinematic beauty shot, luxury editorial beauty photography, real human skin texture, individual eyelashes, soft focus, moody lighting, high dynamic range, 4K, high detail, a moody, low-key, cold-sultry luxury beauty-editorial mood, no big laugh, no toothy smile, no sweet-girl expression, no childlike youthful look, no exaggerated influencer makeup, no heavy smoky eye, no thick eyeliner, no overdone false lashes, no exaggerated Western high nose, no over-slimmed face, no pointed chin, no over-smoothing, no plastic skin, no oily face, no harsh highlights, no hard light, no overexposure, no shadow cuts across the face, no crossed eyes, no vacant stare, no crooked features, no deformed face, no distorted proportions, no loose hair covering the eyes, no cluttered background, no strongly saturated colors, photorealistic.

## Self-check

- Quantified parameters (cm, %, degrees) survive verbatim and are not rewritten as vague adjectives.
- Palette percentages sum to 100 in descending order (when `palette_sentence` is used).
- Foreground occlusion carries a percentage (when `foreground_sentence` is used).
- Negatives are complete; no studio-lighting vocabulary leaks in.
