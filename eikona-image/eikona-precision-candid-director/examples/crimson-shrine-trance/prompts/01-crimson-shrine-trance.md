# Precision-Parameterized Candid Shot

This template produces a single precision-parameterized candid shot prompt. Unlike the random-matrix package, nothing is sampled here: every variable is bound exactly from a shot spec (JSON), and quantified parameters (cm, percentages, degrees) go straight into the body. The consumer binds all variables before rendering; the rendered result is the final prompt body without further rewriting.

## Slot convention

Optional clause variables (`perspective_clause`, `sections_block`, `foreground_sentence`, `light_fill_clause`, `palette_sentence`, `background_sentence`, `fingerprints_sentence`, `tail_clause`) carry their own punctuation and leading spaces/newlines; bind them to an empty string when unused and the whole clause disappears. `genre` defaults to "candid lifestyle photo"; use a different genre phrase (e.g. editorial portrait) for non-candid shots.

Vertical 9:16 photorealistic cinematic portrait, an adult East Asian woman with long messy black hair, wet loose strands framing her face, soft smoky eye makeup, flushed skin, and glossy lips, as she leans slightly forward while tilting her head far back, chin raised, neck elongated, eyes looking upward, lips softly parted with a dreamy trance-like softness.
She wears a deep red and black embroidered camisole dress with ornate traditional patterns and thin straps, delicate red metallic hair ornaments trailing behind her hair.
Setting: she is surrounded by burning red candles, dark carved wood, hanging crimson fabric, antique ritual objects, and traditional masks.
Camera positioned at close range, a tight vertical composition, 50mm lens, shallow depth of field, dramatic chiaroscuro, her face and upper body dominating the frame. A blurred painted ritual mask and a large glowing candle cover the lower-left and lower-right foreground.
Warm candlelight illuminates her face and shoulders from the side, a strong orange rim light outlines her hair, with deep black shadows behind and red and gold reflections throughout the scene. Main colors: deep red, crimson, black, warm gold. The dark ancient ritual shrine interior sinking into deep black shadows.
realistic skin texture, individual hair strands, subtle film grain, dramatic chiaroscuro, highly detailed, a sensual, mysterious Chinese ritual fantasy mood, no cartoonish look, no plastic over-smoothed skin, no harsh daylight, no overexposure, no cluttered composition, no watermarks, no logos, no text errors, photorealistic.

## Self-check

- Quantified parameters (cm, %, degrees) survive verbatim and are not rewritten as vague adjectives.
- Palette percentages sum to 100 in descending order (when `palette_sentence` is used).
- Foreground occlusion carries a percentage (when `foreground_sentence` is used).
- Negatives are complete; no studio-lighting vocabulary leaks in.
