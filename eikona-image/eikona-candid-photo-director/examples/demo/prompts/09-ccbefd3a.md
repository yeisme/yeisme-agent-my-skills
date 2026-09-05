# Candid Lifestyle Portrait (Random Matrix)

This template produces a single summer candid-portrait prompt ready for direct delivery to an image model. Each of the 12 picture dimensions is bound to exactly one value before rendering; the rendered result is the final prompt body and must not be rewritten. Dimension pools, compatibility constraints, and in-batch dedup belong to the consumer-side sampler (the Eikona candid-photo director skill); this template only defines the single-image body structure.

## Goal

Realistic candid lifestyle photography, 9:16 vertical, modern East Asian summer portrait, strong photographic texture, clean frame, clear large-shape relationships, explicit spatial layering.

## Subject

一个极具镜头感的韩国 INS 网红，皮肤白皙，身材夸张, wearing 纯欲风.

## Frame

老式火车车厢. 经过镜头时被偶然捕捉, 轻轻眯眼.
半身环境人像, 85mm压缩人像, 隔着植物侧拍, 极端留白.
Foreground: 树叶. The foreground must intrude naturally into the frame and form a clear occlusion; do not show every element in full.
Light: 傍晚低角度逆光. Palette: 雨后灰蓝+湿润绿色. Keep at most 3-4 major color blocks; avoid a multicolored frame.
Photography state: 自然抓拍.

## Avoid

No studio portrait look, no commercial studio shoot, no standard influencer posing, no subject staring into the lens, no conventional centered portrait, no complex props, no cluttered background, no over-smoothing, no plastic skin.

## Self-check

- The foreground value actually intrudes and occludes rather than being displayed completely.
- Camera position, composition, and foreground are compatible with the scene category (e.g. lotus-leaf camera angles only with lotus scenes).
- The palette value keeps at most 4 major color blocks.
- The subject does not look into the lens (unless `expression` explicitly requires it).
