# Build log (Part B) and AI-use note (Part F)

## Trial lists

I used the trial lists from my Project 2 generator for participants 1–8, using seed 8683. I copied them into `trial_lists/` rather than using the provided canonical lists. The six sample output files were generated using the canonical lists, which I took into account when checking them.

## How the build happened

I first used AI to work through an earlier version of the task. I followed how it put the experiment together because I wanted to understand the process before trying it myself. I then started over with the starter files and spent time building the instructions and basic trial structure in PsychoPy Builder. I saved that version as `ldt_basic.psyexp` (`ce4d807`). From there, I worked through several versions of the full experiment, testing things as I went. I used AI for specific changes and troubleshooting, especially for parts of Q1–Q10 that I was having difficulty implementing, rather than using the earlier attempt as my final project.

During testing, I made changes to the participant setup, practice feedback, timing, response recording, and the break and end screens. I also adjusted how the refresh rate was measured after noticing that the longer SOA was sometimes off. I completed a participant 1 run in Pilot mode and the final runs for participants 3 and 6 in Run mode. I kept the output files as recorded, even though some of my responses in the final runs were too fast to be useful as actual lexical decision data.

Here are the main commits in this repository:

| Commit | What I added |
| --- | --- |
| `fa8729f` | Starting repository and files |
| `ce4d807` | Basic Builder version, `ldt_basic.psyexp` |
| `c71da7c` | My original predictions |
| `7ecb6dd` | Participant 1 Pilot-mode output |
| `2f586eb` | AI-assisted full experiment, `ldt.psyexp` |
| `ab2ba47` | Participant 3 and 6 output files |
| `acfd558`, `d0c74a3` | Initial checker results, then checker updates and tests |
| `a281e3f`, `e7f3136` | Verification report and prediction reconciliation |

I opened, tested, and saved different versions during development, so the files' modification times may not reflect when I first made them. The data files also show that the runs were done before I committed the predictions. The predictions were my own, but I am not presenting that commit as having happened before those runs. I ran the final experiment from the compiled script; I have not documented a separate reopening of the final file in Builder after the AI edits.

## Handoff (only if you used a language model on the experiment file)

- Hash of the `pre-handoff:` commit: There was no single commit with the required prefix and both files together. The basic version was committed as `ce4d807`, and the participant 1 Pilot data as `7ecb6dd`.
- Hash of the first commit after the handoff: `2f586eb` (`Add AI-assisted PsychoPy experiment after multiple test versions`).
- What you asked for: Help extending and fixing the basic Builder version to meet Q1–Q10, including the timing and output columns.

| Change | Kept / changed / reverted | Why |
| --- | --- | --- |
| Participant number selects the matching two-digit trial list | Kept | So each person gets the correct list (Q1). |
| Different F/J instructions for odd and even participants | Kept | The key mapping needs to change with participant number (Q6). |
| Practice feedback, break, and end screens | Kept | These were missing or incomplete in the basic version (Q3–Q4). |
| Timing based on whole frames, including the SOA | Changed during testing | The first refresh-rate approach gave inconsistent long-SOA timings (Q5). |
| Keyboard starting at target onset and keeping the first response | Kept | Responses before the target should not count (Q7). |
| Recording the shown words, onset times, key, RT, accuracy, and timeout | Kept | The data file needs to show what happened on each trial (Q8–Q10). |
| Practice and main loops reading the selected trial list | Kept | Both sections need to follow the file in order (Q1–Q2). |

## AI-use note (Part F)

I used T3 Code, Claude, and Codex during the project. I initially watched AI work through an example of the task, then restarted so I could build and understand the experiment myself. After creating the basic version in Builder, I used AI to help with parts of the full experiment, including some code changes, timing fixes, and debugging. AI also generated an initial version of `check_output.py` and the tests, and helped draft parts of the verification report, reconciliation, and build log. I wrote the original predictions, ran the experiment myself, tested different versions, and reviewed the final files. I corrected an earlier explanation of file A and rewrote sections of the reports to reflect what I found. I did not use simulated responses as my participant data.
