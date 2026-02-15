You are classifying whether an arXiv paper is an EEG Foundation Model (EEG-FM) paper.

Definition: EEG-FM if
(1) EEG is a primary modality (EEG/electroencephalography/brainwaves/BCI using EEG), AND
(2) the paper centers on a general-purpose pretrained representation/model intended to transfer/generalize across tasks/datasets/subjects/settings, often via self-supervised pretraining, large-scale pretraining, or explicit “foundation model” framing.

You will be given: arxiv_id_base, title, authors, categories, published_date, abstract.

Output MUST be valid JSON matching this schema (no markdown, no extra keys):
- arxiv_id_base: string
- is_eeg_related: boolean
- is_foundation_model_related: boolean
- borderline: boolean (true if plausible but unclear)
- paper_type: one of ["new_model","benchmark","survey","method","application","other"]
- confidence: number 0..1
- reasons: 1..8 short strings based only on the abstract/metadata
- suggested_digest_tags: 0..12 short tags
- decision: one of ["accept","reject","borderline"]

Conservative policy:
- Prefer false positives over false negatives.
- If unsure but plausible: decision="borderline" and borderline=true.

Input:
{{INPUT_JSON}}
