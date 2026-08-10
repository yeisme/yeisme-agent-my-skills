# Critic Panel Rubric

通用 0–4 锚定：

- 0：缺失、冲突或不可验证；
- 1：明显不可用；
- 2：可通过明确修复使用；
- 3：达到当前目标；
- 4：显著提升主题、人物、观众体验或生产可靠性。

聚合：`Σ(weight × median(score)/4) × 100`。先检查 hard gates，再看软分。只在相同 CandidateSet、CanonSnapshot、RubricProfile 和 JudgePanelProfile 内排名。

必须记录：judge role、model ref、model family、correlation cluster、score、evidence refs、coverage、indeterminate、IQR、confidence、blocker、recommendation 和 human review requirement。
