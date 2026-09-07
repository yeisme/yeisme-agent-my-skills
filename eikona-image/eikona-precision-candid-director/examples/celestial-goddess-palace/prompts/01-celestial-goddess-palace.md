# Precision-Parameterized Candid Shot

This template produces a single precision-parameterized candid shot prompt. Unlike the random-matrix package, nothing is sampled here: every variable is bound exactly from a shot spec (JSON), and quantified parameters (cm, percentages, degrees) go straight into the body. The consumer binds all variables before rendering; the rendered result is the final prompt body without further rewriting.

## Slot convention

Optional clause variables (`perspective_clause`, `sections_block`, `foreground_sentence`, `light_fill_clause`, `palette_sentence`, `background_sentence`, `fingerprints_sentence`, `tail_clause`) carry their own punctuation and leading spaces/newlines; bind them to an empty string when unused and the whole clause disappears. `genre` defaults to "candid lifestyle photo"; use a different genre phrase (e.g. editorial portrait) for non-candid shots.

Vertical 9:16 Chinese mythological cinema still, an elegant adult Chinese celestial goddess standing atop the white jade steps of Lingxiao Palace with her serene, transcendent calm.
She wears a flowing ivory hanfu embroidered with delicate gold cloud patterns, translucent silk ribbons drifting in the high-altitude breeze, and elaborate golden hairpins with dangling pearls.
Camera positioned from a low angle, 35mm environmental portrait lens, a full-body composition with monumental palace gates rising above an endless sea of clouds behind her.
The first sunlight illuminating her profile, with atmospheric depth through the cloud sea. Main colors: warm ivory, pale gold, cloud white. Monumental palace gates rising above an endless sea of clouds.
Chinese mythological cinema, realistic skin texture, intricate textile details, atmospheric depth, high dynamic range, 4K, highly detailed, a transcendent celestial xianxia mood, no cartoonish look, no plastic over-smoothed skin, no modern objects, no cluttered composition, no overexposure, no watermarks, no logos, no text errors, photorealistic.

## Self-check

- Quantified parameters (cm, %, degrees) survive verbatim and are not rewritten as vague adjectives.
- Palette percentages sum to 100 in descending order (when `palette_sentence` is used).
- Foreground occlusion carries a percentage (when `foreground_sentence` is used).
- Negatives are complete; no studio-lighting vocabulary leaks in.
