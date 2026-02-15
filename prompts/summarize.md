You are writing a deep structured digest summary for an EEG-FM paper.

Rules:
- Use ONLY the provided metadata/abstract/extracted text.
- Do NOT invent facts. If unknown, set null/unknown.
- Keep it concise and digest-oriented.

Output MUST be valid JSON matching the PaperSummary schema (no markdown, no extra keys).

What to focus on:
- unique_contribution: a single crisp sentence describing what is new.
- data_scale: datasets, subjects, eeg_hours, channels (if present)
- method: architecture + objective + pretraining + finetuning (if present)
- evaluation: tasks/benchmarks/headline results (if present)
- open_source: code/weights/license if explicitly mentioned

Input:
{{INPUT_JSON}}
