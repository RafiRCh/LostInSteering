# LostInSteering memory
- Local folder: D:\Cloud Extension\QPAIN\Working paper\LostInSteering (device "Arifs"). Kaggle is blocked from the cloud, so Kaggle work goes through the user's PC. Kaggle account: lynxsilver.
- Run 08 as of Nov 20: notebook_1 (1.5B, 3B, 7B fp16/nf4) is done and pulled to results/08_unified_scale_run/notebook_1_final. 14B (notebook_2) finished Nov 19. The user runs two new notebooks: 0.5B full, and 7B dose with all 6 languages.
- Findings: truth collapse at 7B in all languages, and cosine is high (bn lowest, .73). Opinion is at floor in most cells, and the notebook floor check uses 0.03, not 0.10. The CAA opinion vector is inert, and persona is no better than CAA (null result).
- The user wants the humanizer style for all writing.
- Paper draft (Nov 21): /mnt/project-files/paper/ and D:\...\LostInSteering\paper\. Compile in Overleaf. See paper-draft.
