# DSA Tutor (small language model)
Fine-tuned Qwen2.5-3B-Instruct that tutors data structures and personalizes answers from a student profile.

## What's here
- Dataset pipeline scripts (extract, merge, coverage, personalization generator)
- gap_seeds.jsonl and personalization_train.jsonl
- course content files (notes_chunks, notes_train, final_train)
- final_train (final dataset)

## Not included
Model weights (3.1 GB) and datasets built from course notes and LeetCode text.

## Limitations
Evaluated on a small sample. Facts and rankings from the 3B model can be wrong, so plans will move into code.
