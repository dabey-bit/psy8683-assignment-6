# Data dictionary (Part D)

Based on the completed, instrumented run 7 CSV (run 8 has the same 86 columns). It contains **104 trial rows** (8 practice, 96 experimental) plus one row each for instructions, break, and the end screen. Columns are listed in **saved order**; adjacent related columns share a description.

**Rows:** T = all trials; P = practice; E = experimental; I = instructions; B = break; Z = end; All = all 107 rows; — = blank. **Timing:** values marked *flip* refer to PsychoPy refresh timestamps. Routine start/end times are **not** flip timestamps. RTs and key-hold durations are also not flips.

| # | Column(s), in CSV order | Source | Meaning and units | Rows |
| ---: | --- | --- | --- | :---: |
| 1 | `participant` | List / dialog | Participant ID (integer); also repeated at column 78. | All |
| 2 | `phase` | Trial list | Practice or experimental phase. | T |
| 3 | `trial_index` | Trial list | Trial number within the phase (1–8 or 1–96). | T |
| 4 | `item_id` | Trial list | Stimulus/item identifier (text). | T |
| 5–6 | `target`, `prime` | Trial list | Target and prime, before display formatting (lowercase text). | T |
| 7 | `relatedness` | Trial list | Prime–target relationship: `related`, `unrelated`, or `none`. | T |
| 8 | `soa` | Trial list | Prime-to-target SOA: 150 or 1000 **ms**. | T |
| 9 | `correct_response` | Trial list | Correct category: `word` or `nonword` (not a key). | T |
| 10 | `seed` | Trial list | Trial-list random seed (8683). | T |
| 11–13 | `thisN`, `thisTrialN`, `thisRepN` | PsychoPy | Current loop’s overall/trial/repetition counters (zero-based). | T |
| 14–16 | `trial_key.keys`, `trial_key.rt`, `trial_key.duration` | PsychoPy keyboard | Response key (`f`/`j`/blank), target-relative RT (**s**), key-hold duration (**s** or `None`). | T |
| 17–20 | `practice_loop.thisRepN`, `practice_loop.thisTrialN`, `practice_loop.thisN`, `practice_loop.thisIndex` | PsychoPy loop | Practice repetition, trial number, overall number, and input-row index (zero-based). | P |
| 21–24 | `main_loop.thisRepN`, `main_loop.thisTrialN`, `main_loop.thisN`, `main_loop.thisIndex` | PsychoPy loop | Same four counters for the experimental loop (zero-based). | E |
| 25 | `thisRow.t` | PsychoPy | Timestamp on the first fixation **flip**, **s**. | T |
| 26 | `notes` | PsychoPy | Unused notes field (empty). | — |
| 27 | `piloting` | PsychoPy | Pilot-mode flag (`False`), stored on the instructions row. | I |
| 28 | `instructions.started` | PsychoPy | Instructions **routine start**, **s**; *not* a display flip. | I |
| 29–30 | `instructions_text.started`, `instructions_key.started` | PsychoPy | **Flip** showing the instructions text and starting the SPACE keyboard, **s**. | I |
| 31 | `instructions.stopped` | PsychoPy | Instructions **routine end**, **s**; *not* a display flip. | I |
| 32–34 | `instructions_key.keys`, `instructions_key.rt`, `instructions_key.duration` | PsychoPy keyboard | Instructions continue key (`space`), RT (**s**), hold duration (**s** or `None`). | I |
| 35 | `ldt_trial.started` | PsychoPy | Trial **routine start**, **s**; *not* a display flip. | T |
| 36–37 | `fixation_text.started`, `fixation_text.stopped` | PsychoPy | Fixation **appearance / disappearance flips**, **s**, respectively. | T |
| 38–39 | `prime_text.started`, `prime_text.stopped` | PsychoPy | Prime **appearance / disappearance flips**, **s**. | T |
| 40 | `target_text.started` | PsychoPy | **Flip** when the target appears, **s**. | T |
| 41 | `trial_key.started` | PsychoPy keyboard | **Flip** when the response keyboard starts listening, **s**. | T |
| 42 | `ldt_trial.stopped` | PsychoPy | Trial **routine end**, **s**; *not* a display flip. | T |
| 43–45 | `practice_loop.trial_key.keys`, `practice_loop.trial_key.rt`, `practice_loop.trial_key.duration` | PsychoPy loop | Practice-loop copy of response key, RT (**s**), and hold duration (**s** or `None`). | P |
| 46–47 | `prime_shown`, `target_shown` | Custom (`trial_record`) | Prime text read from the stimulus object (lowercase); target text read from its object (uppercase). | T |
| 48–49 | `prime_onset`, `target_onset` | Custom (`trial_record`) | Prime and target **onset flips** from `.tStartRefresh`, **s**. | T |
| 50–51 | `key`, `rt` | Custom (`trial_record`) | Accepted key (`f`/`j`/empty) and target-relative RT (**s**, empty on timeout). | T |
| 52–53 | `accuracy`, `timeout` | Custom (`trial_record`) | Accuracy (1 correct, 0 wrong/timeout) and timeout (1 no timely key, 0 otherwise). | T |
| 54 | `dropped_frames` | Custom (`a6_frame_recording`) | Per-trial number of intervals longer than 1.5 frames (I2); integer. | T |
| 55 | `feedback.started` | PsychoPy | Feedback **routine start**, **s**; *not* a display flip. | P |
| 56–57 | `feedback_text.started`, `feedback_text.stopped` | PsychoPy | Feedback text **appearance / disappearance flips**, **s**. | P |
| 58 | `feedback.stopped` | PsychoPy | Feedback **routine end**, **s**; *not* a display flip. | P |
| 59 | `iti.started` | PsychoPy | ITI **routine start**, **s**; *not* a display flip. | T |
| 60–61 | `iti_blank.started`, `iti_blank.stopped` | PsychoPy | Blank ITI component **start / stop flips**, **s**. | T |
| 62 | `iti.stopped` | PsychoPy | ITI **routine end**, **s**; *not* a display flip. | T |
| 63 | `break_screen.started` | PsychoPy | Break **routine start**, **s**; *not* a display flip. | B |
| 64–65 | `break_text.started`, `break_key.started` | PsychoPy | **Flip** showing break text and starting SPACE keyboard, **s**. | B |
| 66 | `break_text.stopped` | PsychoPy | **Flip** removing break text, **s**; in runs 7/8 the text stopped after ~1 s (later fixed). | B |
| 67 | `break_screen.stopped` | PsychoPy | Break **routine end** after SPACE, **s**; *not* a display flip. | B |
| 68–70 | `break_key.keys`, `break_key.rt`, `break_key.duration` | PsychoPy keyboard | Break continue key (`space`), RT (**s**), hold duration (**s** or `None`). | B |
| 71–73 | `main_loop.trial_key.keys`, `main_loop.trial_key.rt`, `main_loop.trial_key.duration` | PsychoPy loop | Experimental-loop copy of response key, RT (**s**), and hold duration (**s** or `None`). | E |
| 74 | `end_screen.started` | PsychoPy | End-screen **routine start**, **s**; *not* a display flip. | Z |
| 75–76 | `end_text.started`, `end_text.stopped` | PsychoPy | End message **appearance / disappearance flips**, **s**. | Z |
| 77 | `end_screen.stopped` | PsychoPy | End-screen **routine end**, **s**; *not* a display flip. | Z |
| 78 | `participant` | PsychoPy / dialog | Second `participant` field, from session metadata (integer/text ID). | All |
| 79 | `session` | Startup dialog | Session label (e.g. `a6run7`). | All |
| 80 | `date` | PsychoPy | Session date/time string; *not* a display flip. | All |
| 81 | `expName` | PsychoPy | Experiment name (`ldt`). | All |
| 82 | `expVersion` | PsychoPy | Experiment version; unset/empty. | — |
| 83 | `psychopyVersion` | PsychoPy | Software version (`2026.2.4`). | All |
| 84 | `frameRate` | PsychoPy | Measured refresh rate (**Hz**); rounded to whole Hz for frame scheduling. | All |
| 85 | `expStart` | PsychoPy | Experiment start date/time string; *not* a display flip. | All |
| 86 | *(empty header)* | CSV export | Unnamed trailing empty column. | — |

## Frame-interval log (I1)

The matching `data/<participant>_ldt_<timestamp>_frameIntervals.log` saves **one interval in seconds per line**, in order, from fixation onset to the final target flip on every trial. It excludes instructions, feedback, ITIs, break, and end screens. The log has no trial labels; `dropped_frames` in the CSV supplies each trial’s I2 count.

An interval is counted as dropped if it exceeds **1.5 × (1 / rounded frameRate)** seconds (**25 ms at 60 Hz**). The totals agree in both official runs: **run 7: 2**, **run 8: 10**. The earlier A5 runs (3 and 6) do not have I1 logs or the I2 column.

**CSV details:** `participant` appears twice (columns 1 and 78), so handle duplicate headers when parsing. The last column is unnamed and empty. A keyboard `.duration` value of `None` means PsychoPy did not record key-release duration, not that it was zero.
