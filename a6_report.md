# Verification report and timing audit (Part C)

I compared my A5 runs (3 and 6), the instrumented runs (7 and 8), and the six provided files using the checker and PsychoPy logs. **PASS** means the recorded evidence supports a check, **PILOT** means I checked the build, and **UNDETERMINED** means the evidence cannot settle it. A timestamp is evidence about a software flip, not necessarily when the pixels changed on screen.

## 1. My Assignment 5 build: Q3–Q10

**Runs 3 and 6 had 104 trials each** (8 practice, 96 experimental). Their recorded fixation, prime, SOA, responses, saved text, and onset times passed. I also checked the A5 build at `ef6c471` for the parts a CSV cannot show: participant list loading (Q1); screen sequence and feedback (Q3); the fixation, stimulus case and blank screens (Q4); frame calculations (Q5); key mapping and Escape (Q6); clearing earlier keys and storing the first response (Q7); and the source of saved text, timestamps and accuracy (Q8–Q10). These are **PILOT** findings from code inspection, not extra CSV evidence. A wrong mapping, early keyboard start, hardcoded stimulus, or incorrect scoring would have failed the corresponding check.

**I did find one Q3 bug.** The break waited for SPACE, but the message disappeared after about a second. The A5 and A6 run logs confirmed it. I removed the text timeout in `1f2dea1` (`fix: keep break prompt visible until SPACE`). The corrected file compiles and still waits for SPACE. **Runs 7 and 8 were collected before this fix**, so I kept them for timing but am not claiming they tested the new screen visually.

A few **ITIs were longer than expected** in the A5 runs: 2/104 in run 3 and 1/104 in run 6. They stay UNDETERMINED because there was no I1 interval log to explain those flips. Run 6 also had no timeout trial to test the full target deadline. I1/I2 were not yet part of the A5 build, so they are not retrospectively graded as failures. I did not rerun 3 or 6.

<details>
<summary>Own runs 3, 6, 7 and 8 — full, unchanged checker output (click to expand)</summary>

```text
Scope: software evidence for Q1-Q10 and I1-I2.

data\3_ldt_2026-11-04_21h45.27.117.csv
Q1 PASS Participant 3: all 104 recorded trial records match trials_p03.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 UNDETERMINED Inspect the Builder file and test the dialog and relative-path loading to settle the remaining Q1 requirements.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.
Q3 PASS Phase sequence: 104 trials with 8 practice and 96 experimental. Expected 8 practice followed by 96 experimental.
Q3 PASS instructions: instructions_text.started is recorded in the expected row (CSV line 2).
Q3 PASS instructions: recorded ending key 'space'.
Q3 PASS break: break_text.started is recorded in the expected row (CSV line 11).
Q3 PASS break: recorded ending key 'space'.
Q3 PASS end: end_text.started is recorded in the expected row (CSV line 108).
Q3 PASS Feedback placement: all 104 rows matched.
Q3 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q3 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q3 UNDETERMINED Need the build or an observed run to establish the instruction and feedback wording and the actual screen transitions.
Q4 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence.
Q4 UNDETERMINED ITI: 102/104 matched, 0 lack timestamps, 2 have unexplained elapsed-time deviations. First at CSV line 31: 70 elapsed frame periods (586.750 ms), expected 60. Need the actual flip counts to distinguish delays from a frame setting error.
Q4 PASS Presentation order: all 104 rows matched.
Q4 PASS Target through response or timeout: all 104 rows matched.
Q4 UNDETERMINED Inspect the build or watch a run to confirm the fixation cross, stimulus case, and blank SOA and ITI screens. Physical timing requires a photodiode.
Q5 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence.
Q5 UNDETERMINED ITI: 102/104 matched, 0 lack timestamps, 2 have unexplained elapsed-time deviations. First at CSV line 31: 70 elapsed frame periods (586.750 ms), expected 60. Need the actual flip counts to distinguish delays from a frame setting error.
Q5 PASS Timeout target: 1 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q5 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q5 UNDETERMINED One recorded refresh rate cannot establish the Builder conversion rule at other rates. Inspect the frame expressions and refresh-rate source.
Q6 PASS Accepted response keys: all 103 rows matched.
Q6 UNDETERMINED Need the instructions and keyboard configuration or a controlled run to confirm displayed mapping, ignored keys and Escape.
Q7 PASS Keyboard synchronization: all 104 rows matched.
Q7 PASS Recorded RT reference: all 103 rows matched.
Q7 UNDETERMINED Need Builder or a controlled run to verify buffer clearing and first-key storage. Physical stimulus-to-key latency needs external measurement.
Q8 PASS prime text: all 104 rows matched.
Q8 PASS target text: all 104 rows matched.
Q8 UNDETERMINED Need Builder code to confirm the saved strings came from the stimulus objects at trial end.
Q9 PASS Custom onsets versus automatic flip stamps: all 104 rows matched.
Q9 UNDETERMINED Need build code to establish how the timestamps were captured. Measuring physical light onset requires hardware.
Q10 PASS Recorded response and timeout coding: all 104 rows matched.
Q10 PASS All ten recorded trial-list values match a row in trials_p03.csv.
Q10 UNDETERMINED Saved response codes cannot show unrecorded presses or establish the physical two-second deadline without reference timing evidence.
I1 UNDETERMINED No instrumentation log or column. Run the instrumented build and retain its matching log.
I2 UNDETERMINED No dropped_frames column or matching log. Run the instrumented build and retain both outputs.
Q1 PILOT Source at ef6c471: ldt.psyexp setup validates a plain positive integer, formats trial_lists/trials_p%02d.csv, and both loops use trialListFile.
Q3 PILOT Source at ef6c471: SPACE ends the instructions and break routines. Practice alone includes feedback, set to Correct, Incorrect or Too slow from the recorded outcome.
Q4 PILOT Source at ef6c471: Builder defines +, the prime and uppercase target, leaves the long SOA gap undrawn, and uses a blank ITI after feedback in practice.
Q5 PILOT Source at ef6c471: Setup measures the refresh rate and rounds it to whole Hz; msToFrames rounds to whole frames and targetStartFrame uses that conversion for SOA.
Q6 PILOT Source at ef6c471: The displayed and scoring mappings both use wordKey/nonwordKey from participant parity. Trial keyboard accepts f/j and Enable Escape is on.
Q7 PILOT Source at ef6c471: Target and keyboard share targetStartFrame. The keyboard is refresh-synchronized, discards previous events and stores the first key.
Q8 PILOT Source at ef6c471: trial_record End Routine reads prime_text.text and target_text.text directly from the stimulus objects.
Q9 PILOT Source at ef6c471: trial_record End Routine saves prime_text.tStartRefresh and target_text.tStartRefresh.
Q10 PILOT Source at ef6c471: trial_record treats RT >= 2 s as late and computes accuracy against the expected key for the recorded category.
Q3 NOTE The break text stops after 1 s while the routine continues waiting for SPACE.

data\6_ldt_2026-11-04_21h49.55.148.csv
Q1 PASS Participant 6: all 104 recorded trial records match trials_p06.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 UNDETERMINED Inspect the Builder file and test the dialog and relative-path loading to settle the remaining Q1 requirements.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.
Q3 PASS Phase sequence: 104 trials with 8 practice and 96 experimental. Expected 8 practice followed by 96 experimental.
Q3 PASS instructions: instructions_text.started is recorded in the expected row (CSV line 2).
Q3 PASS instructions: recorded ending key 'space'.
Q3 PASS break: break_text.started is recorded in the expected row (CSV line 11).
Q3 PASS break: recorded ending key 'space'.
Q3 PASS end: end_text.started is recorded in the expected row (CSV line 108).
Q3 PASS Feedback placement: all 104 rows matched.
Q3 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q3 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q3 UNDETERMINED Need the build or an observed run to establish the instruction and feedback wording and the actual screen transitions.
Q4 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence.
Q4 UNDETERMINED ITI: 103/104 matched, 0 lack timestamps, 1 have unexplained elapsed-time deviations. First at CSV line 29: 70 elapsed frame periods (585.033 ms), expected 60. Need the actual flip counts to distinguish delays from a frame setting error.
Q4 PASS Presentation order: all 104 rows matched.
Q4 PASS Target through response or timeout: all 104 rows matched.
Q4 UNDETERMINED Inspect the build or watch a run to confirm the fixation cross, stimulus case, and blank SOA and ITI screens. Physical timing requires a photodiode.
Q5 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence.
Q5 UNDETERMINED ITI: 103/104 matched, 0 lack timestamps, 1 have unexplained elapsed-time deviations. First at CSV line 29: 70 elapsed frame periods (585.033 ms), expected 60. Need the actual flip counts to distinguish delays from a frame setting error.
Q5 UNDETERMINED Timeout target: no timeout trials; need a run that reaches the deadline.
Q5 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q5 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q5 UNDETERMINED One recorded refresh rate cannot establish the Builder conversion rule at other rates. Inspect the frame expressions and refresh-rate source.
Q6 PASS Accepted response keys: all 104 rows matched.
Q6 UNDETERMINED Need the instructions and keyboard configuration or a controlled run to confirm displayed mapping, ignored keys and Escape.
Q7 PASS Keyboard synchronization: all 104 rows matched.
Q7 PASS Recorded RT reference: all 104 rows matched.
Q7 UNDETERMINED Need Builder or a controlled run to verify buffer clearing and first-key storage. Physical stimulus-to-key latency needs external measurement.
Q8 PASS prime text: all 104 rows matched.
Q8 PASS target text: all 104 rows matched.
Q8 UNDETERMINED Need Builder code to confirm the saved strings came from the stimulus objects at trial end.
Q9 PASS Custom onsets versus automatic flip stamps: all 104 rows matched.
Q9 UNDETERMINED Need build code to establish how the timestamps were captured. Measuring physical light onset requires hardware.
Q10 PASS Recorded response and timeout coding: all 104 rows matched.
Q10 PASS All ten recorded trial-list values match a row in trials_p06.csv.
Q10 UNDETERMINED Saved response codes cannot show unrecorded presses or establish the physical two-second deadline without reference timing evidence.
I1 UNDETERMINED No instrumentation log or column. Run the instrumented build and retain its matching log.
I2 UNDETERMINED No dropped_frames column or matching log. Run the instrumented build and retain both outputs.
Q1 PILOT Source at ef6c471: ldt.psyexp setup validates a plain positive integer, formats trial_lists/trials_p%02d.csv, and both loops use trialListFile.
Q3 PILOT Source at ef6c471: SPACE ends the instructions and break routines. Practice alone includes feedback, set to Correct, Incorrect or Too slow from the recorded outcome.
Q4 PILOT Source at ef6c471: Builder defines +, the prime and uppercase target, leaves the long SOA gap undrawn, and uses a blank ITI after feedback in practice.
Q5 PILOT Source at ef6c471: Setup measures the refresh rate and rounds it to whole Hz; msToFrames rounds to whole frames and targetStartFrame uses that conversion for SOA.
Q6 PILOT Source at ef6c471: The displayed and scoring mappings both use wordKey/nonwordKey from participant parity. Trial keyboard accepts f/j and Enable Escape is on.
Q7 PILOT Source at ef6c471: Target and keyboard share targetStartFrame. The keyboard is refresh-synchronized, discards previous events and stores the first key.
Q8 PILOT Source at ef6c471: trial_record End Routine reads prime_text.text and target_text.text directly from the stimulus objects.
Q9 PILOT Source at ef6c471: trial_record End Routine saves prime_text.tStartRefresh and target_text.tStartRefresh.
Q10 PILOT Source at ef6c471: trial_record treats RT >= 2 s as late and computes accuracy against the expected key for the recorded category.
Q3 NOTE The break text stops after 1 s while the routine continues waiting for SPACE.
Scope: software evidence for Q1-Q10 and I1-I2.

data/7_ldt_2026-11-18_14h42.14.252.csv
Q1 PASS Participant 7: all 104 recorded trial records match trials_p07.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 UNDETERMINED Inspect the Builder file and test the dialog and relative-path loading to settle the remaining Q1 requirements.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.
Q3 PASS Phase sequence: 104 trials with 8 practice and 96 experimental. Expected 8 practice followed by 96 experimental.
Q3 PASS instructions: instructions_text.started is recorded in the expected row (CSV line 2).
Q3 PASS instructions: recorded ending key 'space'.
Q3 PASS break: break_text.started is recorded in the expected row (CSV line 11).
Q3 PASS break: recorded ending key 'space'.
Q3 PASS end: end_text.started is recorded in the expected row (CSV line 108).
Q3 PASS Feedback placement: all 104 rows matched.
Q3 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q3 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q3 UNDETERMINED Need the build or an observed run to establish the instruction and feedback wording and the actual screen transitions.
Q4 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence. 104 checked against logged flips; 3 had elapsed-time deviations despite the correct count.
Q4 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence. 104 checked against logged flips; 0 had elapsed-time deviations despite the correct count.
Q4 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence. 104 checked against logged flips; 0 had elapsed-time deviations despite the correct count.
Q4 UNDETERMINED ITI: 103/104 matched, 0 lack timestamps, 1 have unexplained elapsed-time deviations. First at CSV line 32: 38 elapsed frame periods (633.934 ms), expected 30. Need the actual flip counts to distinguish delays from a frame setting error.
Q4 PASS Presentation order: all 104 rows matched.
Q4 PASS Target through response or timeout: all 104 rows matched.
Q4 UNDETERMINED Inspect the build or watch a run to confirm the fixation cross, stimulus case, and blank SOA and ITI screens. Physical timing requires a photodiode.
Q5 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence. 104 checked against logged flips; 3 had elapsed-time deviations despite the correct count.
Q5 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence. 104 checked against logged flips; 0 had elapsed-time deviations despite the correct count.
Q5 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence. 104 checked against logged flips; 0 had elapsed-time deviations despite the correct count.
Q5 UNDETERMINED ITI: 103/104 matched, 0 lack timestamps, 1 have unexplained elapsed-time deviations. First at CSV line 32: 38 elapsed frame periods (633.934 ms), expected 30. Need the actual flip counts to distinguish delays from a frame setting error.
Q5 UNDETERMINED Timeout target: no timeout trials; need a run that reaches the deadline.
Q5 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q5 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q5 UNDETERMINED One recorded refresh rate cannot establish the Builder conversion rule at other rates. Inspect the frame expressions and refresh-rate source.
Q6 PASS Accepted response keys: all 104 rows matched.
Q6 UNDETERMINED Need the instructions and keyboard configuration or a controlled run to confirm displayed mapping, ignored keys and Escape.
Q7 PASS Keyboard synchronization: all 104 rows matched.
Q7 PASS Recorded RT reference: all 104 rows matched.
Q7 UNDETERMINED Need Builder or a controlled run to verify buffer clearing and first-key storage. Physical stimulus-to-key latency needs external measurement.
Q8 PASS prime text: all 104 rows matched.
Q8 PASS target text: all 104 rows matched.
Q8 UNDETERMINED Need Builder code to confirm the saved strings came from the stimulus objects at trial end.
Q9 PASS Custom onsets versus automatic flip stamps: all 104 rows matched.
Q9 UNDETERMINED Need build code to establish how the timestamps were captured. Measuring physical light onset requires hardware.
Q10 PASS Recorded response and timeout coding: all 104 rows matched.
Q10 PASS All ten recorded trial-list values match a row in trials_p07.csv.
Q10 UNDETERMINED Saved response codes cannot show unrecorded presses or establish the physical two-second deadline without reference timing evidence.
I1 PASS 10169 positive, finite intervals, one per line in 7_ldt_2026-11-18_14h42.14.252_frameIntervals.log.
I1 PASS All intervals align with the fixation, prime and target timestamps for 104 trials and end about one flip before feedback or ITI. No extra intervals outside those windows.
I2 PASS 104 trial counts sum to 2; the log has 2 intervals strictly above 25 ms.
I2 PASS Per-trial dropped_frames values agree with a timestamp-aligned partition of the log.
Q1 PILOT Source at 9b1a2a0: ldt.psyexp setup validates a plain positive integer, formats trial_lists/trials_p%02d.csv, and both loops use trialListFile.
Q3 PILOT Source at 9b1a2a0: SPACE ends the instructions and break routines. Practice alone includes feedback, set to Correct, Incorrect or Too slow from the recorded outcome.
Q4 PILOT Source at 9b1a2a0: Builder defines +, the prime and uppercase target, leaves the long SOA gap undrawn, and uses a blank ITI after feedback in practice.
Q5 PILOT Source at 9b1a2a0: Setup measures the refresh rate and rounds it to whole Hz; msToFrames rounds to whole frames and targetStartFrame uses that conversion for SOA.
Q6 PILOT Source at 9b1a2a0: The displayed and scoring mappings both use wordKey/nonwordKey from participant parity. Trial keyboard accepts f/j and Enable Escape is on.
Q7 PILOT Source at 9b1a2a0: Target and keyboard share targetStartFrame. The keyboard is refresh-synchronized, discards previous events and stores the first key.
Q8 PILOT Source at 9b1a2a0: trial_record End Routine reads prime_text.text and target_text.text directly from the stimulus objects.
Q9 PILOT Source at 9b1a2a0: trial_record End Routine saves prime_text.tStartRefresh and target_text.tStartRefresh.
Q10 PILOT Source at 9b1a2a0: trial_record treats RT >= 2 s as late and computes accuracy against the expected key for the recorded category.
Q3 NOTE The break text stops after 1 s while the routine continues waiting for SPACE.

data/8_ldt_2026-11-18_14h53.25.766.csv
Q1 PASS Participant 8: all 104 recorded trial records match trials_p08.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 UNDETERMINED Inspect the Builder file and test the dialog and relative-path loading to settle the remaining Q1 requirements.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.
Q3 PASS Phase sequence: 104 trials with 8 practice and 96 experimental. Expected 8 practice followed by 96 experimental.
Q3 PASS instructions: instructions_text.started is recorded in the expected row (CSV line 2).
Q3 PASS instructions: recorded ending key 'space'.
Q3 PASS break: break_text.started is recorded in the expected row (CSV line 11).
Q3 PASS break: recorded ending key 'space'.
Q3 PASS end: end_text.started is recorded in the expected row (CSV line 108).
Q3 PASS Feedback placement: all 104 rows matched.
Q3 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q3 UNDETERMINED End screen: 0/1 matched, 0 lack timestamps, 1 have unexplained elapsed-time deviations. First at CSV line 108: 123 elapsed frame periods (2054.768 ms), expected 120. Need the actual flip counts to distinguish delays from a frame setting error.
Q3 UNDETERMINED Need the build or an observed run to establish the instruction and feedback wording and the actual screen transitions.
Q4 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence. 104 checked against logged flips; 5 had elapsed-time deviations despite the correct count.
Q4 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence. 104 checked against logged flips; 1 had elapsed-time deviations despite the correct count.
Q4 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence. 104 checked against logged flips; 1 had elapsed-time deviations despite the correct count.
Q4 UNDETERMINED ITI: 101/104 matched, 0 lack timestamps, 3 have unexplained elapsed-time deviations. First at CSV line 31: 34 elapsed frame periods (574.838 ms), expected 30. Need the actual flip counts to distinguish delays from a frame setting error.
Q4 PASS Presentation order: all 104 rows matched.
Q4 UNDETERMINED Target through response or timeout: 103/104 assessable rows matched. Need the target offset, response time or event-level interval evidence.
Q4 UNDETERMINED Inspect the build or watch a run to confirm the fixation cross, stimulus case, and blank SOA and ITI screens. Physical timing requires a photodiode.
Q5 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence. 104 checked against logged flips; 5 had elapsed-time deviations despite the correct count.
Q5 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence. 104 checked against logged flips; 1 had elapsed-time deviations despite the correct count.
Q5 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence. 104 checked against logged flips; 1 had elapsed-time deviations despite the correct count.
Q5 UNDETERMINED ITI: 101/104 matched, 0 lack timestamps, 3 have unexplained elapsed-time deviations. First at CSV line 31: 34 elapsed frame periods (574.838 ms), expected 30. Need the actual flip counts to distinguish delays from a frame setting error.
Q5 UNDETERMINED Timeout target: no timeout trials; need a run that reaches the deadline.
Q5 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q5 UNDETERMINED End screen: 0/1 matched, 0 lack timestamps, 1 have unexplained elapsed-time deviations. First at CSV line 108: 123 elapsed frame periods (2054.768 ms), expected 120. Need the actual flip counts to distinguish delays from a frame setting error.
Q5 UNDETERMINED One recorded refresh rate cannot establish the Builder conversion rule at other rates. Inspect the frame expressions and refresh-rate source.
Q6 PASS Accepted response keys: all 104 rows matched.
Q6 UNDETERMINED Need the instructions and keyboard configuration or a controlled run to confirm displayed mapping, ignored keys and Escape.
Q7 PASS Keyboard synchronization: all 104 rows matched.
Q7 PASS Recorded RT reference: all 104 rows matched.
Q7 UNDETERMINED Need Builder or a controlled run to verify buffer clearing and first-key storage. Physical stimulus-to-key latency needs external measurement.
Q8 PASS prime text: all 104 rows matched.
Q8 PASS target text: all 104 rows matched.
Q8 UNDETERMINED Need Builder code to confirm the saved strings came from the stimulus objects at trial end.
Q9 PASS Custom onsets versus automatic flip stamps: all 104 rows matched.
Q9 UNDETERMINED Need build code to establish how the timestamps were captured. Measuring physical light onset requires hardware.
Q10 PASS Recorded response and timeout coding: all 104 rows matched.
Q10 PASS All ten recorded trial-list values match a row in trials_p08.csv.
Q10 UNDETERMINED Saved response codes cannot show unrecorded presses or establish the physical two-second deadline without reference timing evidence.
I1 PASS 10568 positive, finite intervals, one per line in 8_ldt_2026-11-18_14h53.25.766_frameIntervals.log.
I1 PASS All intervals align with the fixation, prime and target timestamps for 104 trials and end about one flip before feedback or ITI. No extra intervals outside those windows.
I2 PASS 104 trial counts sum to 10; the log has 10 intervals strictly above 25 ms.
I2 PASS Per-trial dropped_frames values agree with a timestamp-aligned partition of the log.
Q1 PILOT Source at 9b1a2a0: ldt.psyexp setup validates a plain positive integer, formats trial_lists/trials_p%02d.csv, and both loops use trialListFile.
Q3 PILOT Source at 9b1a2a0: SPACE ends the instructions and break routines. Practice alone includes feedback, set to Correct, Incorrect or Too slow from the recorded outcome.
Q4 PILOT Source at 9b1a2a0: Builder defines +, the prime and uppercase target, leaves the long SOA gap undrawn, and uses a blank ITI after feedback in practice.
Q5 PILOT Source at 9b1a2a0: Setup measures the refresh rate and rounds it to whole Hz; msToFrames rounds to whole frames and targetStartFrame uses that conversion for SOA.
Q6 PILOT Source at 9b1a2a0: The displayed and scoring mappings both use wordKey/nonwordKey from participant parity. Trial keyboard accepts f/j and Enable Escape is on.
Q7 PILOT Source at 9b1a2a0: Target and keyboard share targetStartFrame. The keyboard is refresh-synchronized, discards previous events and stores the first key.
Q8 PILOT Source at 9b1a2a0: trial_record End Routine reads prime_text.text and target_text.text directly from the stimulus objects.
Q9 PILOT Source at 9b1a2a0: trial_record End Routine saves prime_text.tStartRefresh and target_text.tStartRefresh.
Q10 PILOT Source at 9b1a2a0: trial_record treats RT >= 2 s as late and computes accuracy against the expected key for the recorded category.
Q3 NOTE The break text stops after 1 s while the routine continues waiting for SPACE.
```

</details>

## 2. Timing audit

| Setup | Run 7 — quiet | Run 8 — muted video |
| --- | --- | --- |
| Machine | ASUS ROG Zephyrus G14, Windows; AMD Radeon 780M | Same |
| Display | 2880 × 1800, OS set to 60 Hz | Same |
| PsychoPy | 2026.2.4, full screen | Same |
| Measured `frameRate` | 60.027 Hz | 59.961 Hz |
| Other load | No unnecessary apps open | Muted video playing in browser |

At 60 Hz, a frame is about **16.667 ms**. Q5 asks for the correct **number of frames**, which is not always the same as a perfect elapsed duration if a flip runs late. The table gives programmed/verified counts for the recorded trial windows; values for ITI, feedback and the end screen are **elapsed-time equivalents** from timestamps, because I1 does not record those screens.

| Event | Expected at 60 Hz | Run 7 | Run 8 |
| --- | ---: | --- | --- |
| Fixation, 500 ms | 30 | 30 flips on **104/104**; elapsed equivalents 29 (2), 30 (101), 31 (1) | 30 flips on **104/104**; elapsed equivalents 29 (3), 30 (100), 31 (1) |
| Prime, 150 ms | 9 | 9 flips on **104/104** | 9 flips on **104/104** |
| Prime → target: SOA 150 | 9 | 9 on 52/52 | 9 on 52/52 |
| Prime → target: SOA 1000 | 60 | 60 on 52/52 | 60 on 52/52 |
| ITI, 500 ms | 30 | equivalents 30 (103), 38 (1) | equivalents 30 (100), 31 (3), 34 (1) |
| Practice feedback, 1000 ms | 60 | 60 on 8/8 | 60 on 8/8 |
| End screen, 2000 ms | 120 | equivalent 120 | equivalent 123 (~2.055 s) |
| Dropped intervals (I2) | — | **2** | **10** |
| Longest logged interval | — | **55.172 ms** | **63.531 ms** |

The fixation, prime and SOA **flip counts were correct** even where their elapsed time varied. Run 8 had more such timing variation; that does not mean the frame settings were wrong. Run 7 had one ITI of about **634 ms**, and run 8 had three ITIs flagged as long, one ~**35 ms** delay after a response before target offset, and a **2.055 s** end screen. Those later flips fall **outside I1**, so even a trial with `dropped_frames = 0` cannot rule out a delay there. The code requests the right durations, but I cannot identify the cause from these logs.

**I1 and I2 agree.** Run 7 logged **10,169** intervals (median **16.667 ms**); run 8 logged **10,568** (median **16.675 ms**). Each interval is on its own line, and all 104 fixation-to-last-target windows align. The CSV totals (2 and 10) equal the numbers over the **25 ms** threshold, including per-trial counts. Run 8 had 33 unusually short intervals (< half a frame), compared with 4 in run 7. The video run had five times as many dropped intervals, but with one run per condition I cannot say the video caused it.

### What the timing evidence actually tells me

**Verified from software timestamps (Q4/Q5/Q7/Q9/Q10):** The recorded fixation/prime/SOA timing and flip counts agree with the settings; keyboard starts at the target; onset fields match the automatic PsychoPy stamps; and keys, RTs, timeouts and accuracy are internally consistent. This assumes the logged timestamps refer to the intended screen flips and use compatible clocks.

**Bounded, not fully verified:** The build converts milliseconds into whole frames using the rounded startup refresh rate. A response can remove a target only at a later flip, normally around one refresh later, but delays can be longer (as in run 8). A missed flip can also lengthen elapsed prime/SOA timing without changing the scheduled frame count. I checked this conversion in the code, not by running the build on four different displays:

| Refresh rate | 60 Hz | 75 Hz | 120 Hz | 144 Hz |
| --- | ---: | ---: | ---: | ---: |
| Fixation / ITI (500 ms) | 30 | 38 | 60 | 72 |
| Prime / SOA 150 (150 ms) | 9 | 11 | 18 | 22 |
| SOA 1000 / feedback (1000 ms) | 60 | 75 | 120 | 144 |
| Target timeout / end (2000 ms) | 120 | 150 | 240 | 288 |

**Not testable without hardware:** The exact moment a stimulus physically lights up, display lag/scan-out, and physical light-to-key latency. A photodiode and external timing/response equipment would be needed; the software logs cannot establish those parts of Q4, Q5, Q7, Q9 or Q10.

## 3. The six provided files

| File | Final failures | Likely Builder issue (inference) | What someone might conclude without checking |
| --- | --- | --- | --- |
| **A** | **Q10**: 97 accuracy values wrong | Correct answer set to category (`word`) rather than key (`f`/`j`) | Participant was unusually inaccurate, even though responses mostly used the right keys. |
| **B** | None in recorded checks | No detectable setup error | Data look usable, but unseen display/input behavior is still an assumption. |
| **C** | **Q1, Q2, Q10**: wrong participant list (same underlying issue) | Conditions file likely hardcoded to participant 1 | Treats participant-1 items as participant 7's stimuli. |
| **D** | **Q8**: `prime_shown` is literally `prime` on all 104 trials | Literal text or wrong variable handling | Assumes the intended primes were shown because the input `prime` column looks right. |
| **E** | **Q2**: correct items, wrong order | Loop probably set to random rather than sequential | Misses possible order/carryover problems. |
| **F** | **Q4, Q7, Q10**: response clock starts before target | Keyboard component/clock starts too early | Misreads inflated RTs and false timeouts as an SOA effect. |

For F, the keyboard started roughly **650 ms early** on SOA-150 and **1,500 ms early** on SOA-1000 trials. For C, the Q10 failure is the *same wrong copied input list* that Q1/Q2 already caught, not a separate scoring problem. For D, the file cannot tell whether the screen displayed `prime` or only saved it incorrectly.

**Still UNDETERMINED in all six:** Exact instructions/feedback and key mapping shown on screen (Q3/Q6), blank displays (Q4), whether earlier keys were ignored and the first key retained (Q7), whether saved text/timestamps came from the actual stimulus objects/flip callbacks (Q8/Q9), and behavior at other refresh rates (Q5). We would need their Builder files or controlled runs. Physical light timing needs hardware. These files also lack I1/I2 instrumentation; that is missing evidence, not an A6 failure of those older builds.

<details>
<summary>Final checker on files A–F — full, unchanged checker output (click to expand)</summary>

```text
Scope: software evidence for Q1-Q10 and I1-I2.

provided/output_files\file_A.csv
Q1 PASS Participant 3: all 104 recorded trial records match trials_p03.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 UNDETERMINED Inspect the Builder file and test the dialog and relative-path loading to settle the remaining Q1 requirements.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.
Q3 PASS Phase sequence: 104 trials with 8 practice and 96 experimental. Expected 8 practice followed by 96 experimental.
Q3 PASS instructions: instr_text_stim.started is recorded in the expected row (CSV line 2).
Q3 PASS instructions: recorded ending key 'space'.
Q3 PASS break: break_text.started is recorded in the expected row (CSV line 11).
Q3 PASS break: recorded ending key 'space'.
Q3 PASS end: end_text.started is recorded in the expected row (CSV line 108).
Q3 PASS Feedback placement: all 104 rows matched.
Q3 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q3 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q3 UNDETERMINED Need the build or an observed run to establish the instruction and feedback wording and the actual screen transitions.
Q4 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS ITI: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS Presentation order: all 104 rows matched.
Q4 PASS Target through response or timeout: all 104 rows matched.
Q4 UNDETERMINED Inspect the build or watch a run to confirm the fixation cross, stimulus case, and blank SOA and ITI screens. Physical timing requires a photodiode.
Q5 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS ITI: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Timeout target: 1 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q5 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q5 UNDETERMINED One recorded refresh rate cannot establish the Builder conversion rule at other rates. Inspect the frame expressions and refresh-rate source.
Q6 PASS Accepted response keys: all 103 rows matched.
Q6 UNDETERMINED Need the instructions and keyboard configuration or a controlled run to confirm displayed mapping, ignored keys and Escape.
Q7 PASS Keyboard synchronization: all 104 rows matched.
Q7 PASS Recorded RT reference: all 103 rows matched.
Q7 UNDETERMINED Need Builder or a controlled run to verify buffer clearing and first-key storage. Physical stimulus-to-key latency needs external measurement.
Q8 PASS prime text: all 104 rows matched.
Q8 PASS target text: all 104 rows matched.
Q8 UNDETERMINED Need Builder code to confirm the saved strings came from the stimulus objects at trial end.
Q9 PASS Custom onsets versus automatic flip stamps: all 104 rows matched.
Q9 UNDETERMINED Need build code to establish how the timestamps were captured. Measuring physical light onset requires hardware.
Q10 FAIL Recorded response and timeout coding: 97 inconsistent rows, first at CSV line 3: accuracy 0 for 'f'; correct key is 'f'
Q10 PASS All ten recorded trial-list values match a row in trials_p03.csv.
Q10 UNDETERMINED Saved response codes cannot show unrecorded presses or establish the physical two-second deadline without reference timing evidence.
I1 UNDETERMINED No instrumentation log or column. Run the instrumented build and retain its matching log.
I2 UNDETERMINED No dropped_frames column or matching log. Run the instrumented build and retain both outputs.

provided/output_files\file_B.csv
Q1 PASS Participant 4: all 104 recorded trial records match trials_p04.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 UNDETERMINED Inspect the Builder file and test the dialog and relative-path loading to settle the remaining Q1 requirements.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.
Q3 PASS Phase sequence: 104 trials with 8 practice and 96 experimental. Expected 8 practice followed by 96 experimental.
Q3 PASS instructions: instr_text_stim.started is recorded in the expected row (CSV line 2).
Q3 PASS instructions: recorded ending key 'space'.
Q3 PASS break: break_text.started is recorded in the expected row (CSV line 11).
Q3 PASS break: recorded ending key 'space'.
Q3 PASS end: end_text.started is recorded in the expected row (CSV line 108).
Q3 PASS Feedback placement: all 104 rows matched.
Q3 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q3 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q3 UNDETERMINED Need the build or an observed run to establish the instruction and feedback wording and the actual screen transitions.
Q4 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS ITI: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS Presentation order: all 104 rows matched.
Q4 PASS Target through response or timeout: all 104 rows matched.
Q4 UNDETERMINED Inspect the build or watch a run to confirm the fixation cross, stimulus case, and blank SOA and ITI screens. Physical timing requires a photodiode.
Q5 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS ITI: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Timeout target: 2 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q5 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q5 UNDETERMINED One recorded refresh rate cannot establish the Builder conversion rule at other rates. Inspect the frame expressions and refresh-rate source.
Q6 PASS Accepted response keys: all 102 rows matched.
Q6 UNDETERMINED Need the instructions and keyboard configuration or a controlled run to confirm displayed mapping, ignored keys and Escape.
Q7 PASS Keyboard synchronization: all 104 rows matched.
Q7 PASS Recorded RT reference: all 102 rows matched.
Q7 UNDETERMINED Need Builder or a controlled run to verify buffer clearing and first-key storage. Physical stimulus-to-key latency needs external measurement.
Q8 PASS prime text: all 104 rows matched.
Q8 PASS target text: all 104 rows matched.
Q8 UNDETERMINED Need Builder code to confirm the saved strings came from the stimulus objects at trial end.
Q9 PASS Custom onsets versus automatic flip stamps: all 104 rows matched.
Q9 UNDETERMINED Need build code to establish how the timestamps were captured. Measuring physical light onset requires hardware.
Q10 PASS Recorded response and timeout coding: all 104 rows matched.
Q10 PASS All ten recorded trial-list values match a row in trials_p04.csv.
Q10 UNDETERMINED Saved response codes cannot show unrecorded presses or establish the physical two-second deadline without reference timing evidence.
I1 UNDETERMINED No instrumentation log or column. Run the instrumented build and retain its matching log.
I2 UNDETERMINED No dropped_frames column or matching log. Run the instrumented build and retain both outputs.

provided/output_files\file_C.csv
Q1 FAIL Participant 7: 104/104 trial records do not match trials_p07.csv; first at CSV line 3, phase='practice', index='1', item='PW4'.
Q1 UNDETERMINED Inspect the Builder file and test the dialog and relative-path loading to settle the remaining Q1 requirements.
Q2 FAIL 104/104 trial records; missing=104, extra/changed=104; first sequence mismatch at trial position 1.
Q3 PASS Phase sequence: 104 trials with 8 practice and 96 experimental. Expected 8 practice followed by 96 experimental.
Q3 PASS instructions: instr_text_stim.started is recorded in the expected row (CSV line 2).
Q3 PASS instructions: recorded ending key 'space'.
Q3 PASS break: break_text.started is recorded in the expected row (CSV line 11).
Q3 PASS break: recorded ending key 'space'.
Q3 PASS end: end_text.started is recorded in the expected row (CSV line 108).
Q3 PASS Feedback placement: all 104 rows matched.
Q3 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q3 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q3 UNDETERMINED Need the build or an observed run to establish the instruction and feedback wording and the actual screen transitions.
Q4 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS ITI: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS Presentation order: all 104 rows matched.
Q4 PASS Target through response or timeout: all 104 rows matched.
Q4 UNDETERMINED Inspect the build or watch a run to confirm the fixation cross, stimulus case, and blank SOA and ITI screens. Physical timing requires a photodiode.
Q5 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS ITI: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Timeout target: 2 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q5 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q5 UNDETERMINED One recorded refresh rate cannot establish the Builder conversion rule at other rates. Inspect the frame expressions and refresh-rate source.
Q6 PASS Accepted response keys: all 102 rows matched.
Q6 UNDETERMINED Need the instructions and keyboard configuration or a controlled run to confirm displayed mapping, ignored keys and Escape.
Q7 PASS Keyboard synchronization: all 104 rows matched.
Q7 PASS Recorded RT reference: all 102 rows matched.
Q7 UNDETERMINED Need Builder or a controlled run to verify buffer clearing and first-key storage. Physical stimulus-to-key latency needs external measurement.
Q8 PASS prime text: all 104 rows matched.
Q8 PASS target text: all 104 rows matched.
Q8 UNDETERMINED Need Builder code to confirm the saved strings came from the stimulus objects at trial end.
Q9 PASS Custom onsets versus automatic flip stamps: all 104 rows matched.
Q9 UNDETERMINED Need build code to establish how the timestamps were captured. Measuring physical light onset requires hardware.
Q10 PASS Recorded response and timeout coding: all 104 rows matched.
Q10 FAIL 104 trial rows differ from trials_p07.csv, first at CSV line 3.
Q10 UNDETERMINED Saved response codes cannot show unrecorded presses or establish the physical two-second deadline without reference timing evidence.
I1 UNDETERMINED No instrumentation log or column. Run the instrumented build and retain its matching log.
I2 UNDETERMINED No dropped_frames column or matching log. Run the instrumented build and retain both outputs.

provided/output_files\file_D.csv
Q1 PASS Participant 2: all 104 recorded trial records match trials_p02.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 UNDETERMINED Inspect the Builder file and test the dialog and relative-path loading to settle the remaining Q1 requirements.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.
Q3 PASS Phase sequence: 104 trials with 8 practice and 96 experimental. Expected 8 practice followed by 96 experimental.
Q3 PASS instructions: instr_text_stim.started is recorded in the expected row (CSV line 2).
Q3 PASS instructions: recorded ending key 'space'.
Q3 PASS break: break_text.started is recorded in the expected row (CSV line 11).
Q3 PASS break: recorded ending key 'space'.
Q3 PASS end: end_text.started is recorded in the expected row (CSV line 108).
Q3 PASS Feedback placement: all 104 rows matched.
Q3 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q3 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q3 UNDETERMINED Need the build or an observed run to establish the instruction and feedback wording and the actual screen transitions.
Q4 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS ITI: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS Presentation order: all 104 rows matched.
Q4 PASS Target through response or timeout: all 104 rows matched.
Q4 UNDETERMINED Inspect the build or watch a run to confirm the fixation cross, stimulus case, and blank SOA and ITI screens. Physical timing requires a photodiode.
Q5 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS ITI: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Timeout target: 4 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q5 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q5 UNDETERMINED One recorded refresh rate cannot establish the Builder conversion rule at other rates. Inspect the frame expressions and refresh-rate source.
Q6 PASS Accepted response keys: all 100 rows matched.
Q6 UNDETERMINED Need the instructions and keyboard configuration or a controlled run to confirm displayed mapping, ignored keys and Escape.
Q7 PASS Keyboard synchronization: all 104 rows matched.
Q7 PASS Recorded RT reference: all 100 rows matched.
Q7 UNDETERMINED Need Builder or a controlled run to verify buffer clearing and first-key storage. Physical stimulus-to-key latency needs external measurement.
Q8 FAIL prime text: 104 inconsistent rows, first at CSV line 3: saved 'prime', expected 'gravel'
Q8 PASS target text: all 104 rows matched.
Q8 UNDETERMINED Need Builder code to confirm the saved strings came from the stimulus objects at trial end.
Q9 PASS Custom onsets versus automatic flip stamps: all 104 rows matched.
Q9 UNDETERMINED Need build code to establish how the timestamps were captured. Measuring physical light onset requires hardware.
Q10 PASS Recorded response and timeout coding: all 104 rows matched.
Q10 PASS All ten recorded trial-list values match a row in trials_p02.csv.
Q10 UNDETERMINED Saved response codes cannot show unrecorded presses or establish the physical two-second deadline without reference timing evidence.
I1 UNDETERMINED No instrumentation log or column. Run the instrumented build and retain its matching log.
I2 UNDETERMINED No dropped_frames column or matching log. Run the instrumented build and retain both outputs.

provided/output_files\file_E.csv
Q1 PASS Participant 5: all 104 recorded trial records match trials_p05.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 UNDETERMINED Inspect the Builder file and test the dialog and relative-path loading to settle the remaining Q1 requirements.
Q2 FAIL 104/104 trial records; missing=0, extra/changed=0; first sequence mismatch at trial position 1.
Q3 PASS Phase sequence: 104 trials with 8 practice and 96 experimental. Expected 8 practice followed by 96 experimental.
Q3 PASS instructions: instr_text_stim.started is recorded in the expected row (CSV line 2).
Q3 PASS instructions: recorded ending key 'space'.
Q3 PASS break: break_text.started is recorded in the expected row (CSV line 11).
Q3 PASS break: recorded ending key 'space'.
Q3 PASS end: end_text.started is recorded in the expected row (CSV line 108).
Q3 PASS Feedback placement: all 104 rows matched.
Q3 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q3 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q3 UNDETERMINED Need the build or an observed run to establish the instruction and feedback wording and the actual screen transitions.
Q4 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS ITI: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS Presentation order: all 104 rows matched.
Q4 PASS Target through response or timeout: all 104 rows matched.
Q4 UNDETERMINED Inspect the build or watch a run to confirm the fixation cross, stimulus case, and blank SOA and ITI screens. Physical timing requires a photodiode.
Q5 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS ITI: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Timeout target: 1 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q5 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q5 UNDETERMINED One recorded refresh rate cannot establish the Builder conversion rule at other rates. Inspect the frame expressions and refresh-rate source.
Q6 PASS Accepted response keys: all 103 rows matched.
Q6 UNDETERMINED Need the instructions and keyboard configuration or a controlled run to confirm displayed mapping, ignored keys and Escape.
Q7 PASS Keyboard synchronization: all 104 rows matched.
Q7 PASS Recorded RT reference: all 103 rows matched.
Q7 UNDETERMINED Need Builder or a controlled run to verify buffer clearing and first-key storage. Physical stimulus-to-key latency needs external measurement.
Q8 PASS prime text: all 104 rows matched.
Q8 PASS target text: all 104 rows matched.
Q8 UNDETERMINED Need Builder code to confirm the saved strings came from the stimulus objects at trial end.
Q9 PASS Custom onsets versus automatic flip stamps: all 104 rows matched.
Q9 UNDETERMINED Need build code to establish how the timestamps were captured. Measuring physical light onset requires hardware.
Q10 PASS Recorded response and timeout coding: all 104 rows matched.
Q10 PASS All ten recorded trial-list values match a row in trials_p05.csv.
Q10 UNDETERMINED Saved response codes cannot show unrecorded presses or establish the physical two-second deadline without reference timing evidence.
I1 UNDETERMINED No instrumentation log or column. Run the instrumented build and retain its matching log.
I2 UNDETERMINED No dropped_frames column or matching log. Run the instrumented build and retain both outputs.

provided/output_files\file_F.csv
Q1 PASS Participant 8: all 104 recorded trial records match trials_p08.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 UNDETERMINED Inspect the Builder file and test the dialog and relative-path loading to settle the remaining Q1 requirements.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.
Q3 PASS Phase sequence: 104 trials with 8 practice and 96 experimental. Expected 8 practice followed by 96 experimental.
Q3 PASS instructions: instr_text_stim.started is recorded in the expected row (CSV line 2).
Q3 PASS instructions: recorded ending key 'space'.
Q3 PASS break: break_text.started is recorded in the expected row (CSV line 11).
Q3 PASS break: recorded ending key 'space'.
Q3 PASS end: end_text.started is recorded in the expected row (CSV line 108).
Q3 PASS Feedback placement: all 104 rows matched.
Q3 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q3 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q3 UNDETERMINED Need the build or an observed run to establish the instruction and feedback wording and the actual screen transitions.
Q4 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS ITI: 104 durations agree with the rounded frame counts in the software evidence.
Q4 PASS Presentation order: all 104 rows matched.
Q4 FAIL Target through response or timeout: 104 inconsistent rows, first at CSV line 3: response window is not synchronized to target onset
Q4 UNDETERMINED Inspect the build or watch a run to confirm the fixation cross, stimulus case, and blank SOA and ITI screens. Physical timing requires a photodiode.
Q5 PASS Fixation: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Prime: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS SOA: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS ITI: 104 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Timeout target: 50 durations agree with the rounded frame counts in the software evidence.
Q5 PASS Feedback: 8 durations agree with the rounded frame counts in the software evidence.
Q5 PASS End screen: 1 durations agree with the rounded frame counts in the software evidence.
Q5 UNDETERMINED One recorded refresh rate cannot establish the Builder conversion rule at other rates. Inspect the frame expressions and refresh-rate source.
Q6 PASS Accepted response keys: all 54 rows matched.
Q6 UNDETERMINED Need the instructions and keyboard configuration or a controlled run to confirm displayed mapping, ignored keys and Escape.
Q7 FAIL Keyboard synchronization: 104 inconsistent rows, first at CSV line 3: keyboard minus target onset is -650.000 ms
Q7 FAIL Recorded RT reference: 54 inconsistent rows, first at CSV line 3: keyboard minus target onset is -650.000 ms
Q7 UNDETERMINED Need Builder or a controlled run to verify buffer clearing and first-key storage. Physical stimulus-to-key latency needs external measurement.
Q8 PASS prime text: all 104 rows matched.
Q8 PASS target text: all 104 rows matched.
Q8 UNDETERMINED Need Builder code to confirm the saved strings came from the stimulus objects at trial end.
Q9 PASS Custom onsets versus automatic flip stamps: all 104 rows matched.
Q9 UNDETERMINED Need build code to establish how the timestamps were captured. Measuring physical light onset requires hardware.
Q10 FAIL Recorded response and timeout coding: 104 inconsistent rows, first at CSV line 3: keyboard times are referenced to a different onset, so the saved RT or timeout is not target-relative
Q10 PASS All ten recorded trial-list values match a row in trials_p08.csv.
Q10 UNDETERMINED Saved response codes cannot show unrecorded presses or establish the physical two-second deadline without reference timing evidence.
I1 UNDETERMINED No instrumentation log or column. Run the instrumented build and retain its matching log.
I2 UNDETERMINED No dropped_frames column or matching log. Run the instrumented build and retain both outputs.
```

</details>

### First checker and what changed

I committed the **first working output before inspecting the six files again for A6** as `9a07bf1` (`first-run: save initial A6 checker output for six provided files`). I had already seen some issues during A5, which I disclosed in my predictions. The first checker incorrectly flagged **A's Q6** using its bad accuracy values as evidence of the displayed key mapping. The correction separated **Q6 key acceptance** from **Q10 accuracy scoring**, and improved component-name matching, response handling and flip-count checks (`8087076`, followed by tests/final outputs in `58565fc`). The 17 negative-control/tests passed. The first-run output is preserved below rather than replaced.

In A5, **Q1/Q2** already caught **C** (wrong list) and **E** (wrong order), but could not detect **A** (bad accuracy), **D** (bad recorded prime), or **F** (keyboard/RT reference). These need Q10, Q8, and Q4/Q7/Q10 respectively; the nearest A5 checks only confirmed the input list/order. B never failed an observable test.

<details>
<summary>First working checker on files A–F — full, unchanged checker output (click to expand)</summary>

```text
Scope: software evidence for Q1-Q10 and I1-I2.

provided/output_files\file_A.csv
Q1 PASS Participant 3: all 104 recorded trial records match trials_p03.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 UNDETERMINED Inspect the Builder file and test the dialog and relative-path loading to settle the remaining Q1 requirements.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.
Q3 PASS Phase sequence: 104 trials with 8 practice and 96 experimental. Expected 8 practice followed by 96 experimental.
Q3 PASS instructions: instructions.started is recorded in the expected row (CSV line 2).
Q3 PASS instructions: recorded ending key 'space'.
Q3 PASS break: break_text.started is recorded in the expected row (CSV line 11).
Q3 PASS break: recorded ending key 'space'.
Q3 PASS end: end_text.started is recorded in the expected row (CSV line 108).
Q3 PASS Feedback placement: all 104 rows matched.
Q3 PASS Feedback: 8 durations agree with the rounded frame counts in the software timestamps.
Q3 PASS End screen: 1 durations agree with the rounded frame counts in the software timestamps.
Q3 UNDETERMINED Need the build or an observed run to establish the instruction and feedback wording and the actual screen transitions.
Q4 PASS Fixation: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS Prime: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS SOA: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS ITI: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS Target through response or timeout: all 104 rows matched.
Q4 UNDETERMINED Inspect the build or watch a run to confirm the fixation cross, stimulus case, and blank SOA and ITI screens. Physical timing requires a photodiode.
Q5 PASS Fixation: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Prime: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS SOA: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS ITI: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Timeout target: 1 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Feedback: 8 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS End screen: 1 durations agree with the rounded frame counts in the software timestamps.
Q5 UNDETERMINED One recorded refresh rate cannot establish the Builder conversion rule at other rates. Inspect the frame expressions and refresh-rate source.
Q6 FAIL Recorded key mapping: 97 inconsistent rows, first at CSV line 3: 'f' scored '0' under the participant mapping (correct key 'f')
Q6 UNDETERMINED Need the instructions and keyboard configuration or a controlled run to confirm displayed mapping, ignored keys and Escape.
Q7 PASS Keyboard synchronization: all 104 rows matched.
Q7 PASS Recorded RT reference: all 103 rows matched.
Q7 UNDETERMINED Need Builder or a controlled run to verify buffer clearing and first-key storage. Physical stimulus-to-key latency needs external measurement.
Q8 PASS prime text: all 104 rows matched.
Q8 PASS target text: all 104 rows matched.
Q8 UNDETERMINED Need Builder code to confirm the saved strings came from the stimulus objects at trial end.
Q9 PASS Custom onsets versus automatic flip stamps: all 104 rows matched.
Q9 UNDETERMINED Need build code to establish how the timestamps were captured. Measuring physical light onset requires hardware.
Q10 FAIL Recorded response and timeout coding: 97 inconsistent rows, first at CSV line 3: accuracy 0 for 'f'; correct key is 'f'
Q10 PASS All ten recorded trial-list values match a row in trials_p03.csv.
Q10 UNDETERMINED Saved response codes cannot show unrecorded presses or establish the physical two-second deadline without reference timing evidence.
I1 UNDETERMINED No instrumentation log or column. Run the instrumented build and retain its matching log.
I2 UNDETERMINED No dropped_frames column or matching log. Run the instrumented build and retain both outputs.

provided/output_files\file_B.csv
Q1 PASS Participant 4: all 104 recorded trial records match trials_p04.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 UNDETERMINED Inspect the Builder file and test the dialog and relative-path loading to settle the remaining Q1 requirements.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.
Q3 PASS Phase sequence: 104 trials with 8 practice and 96 experimental. Expected 8 practice followed by 96 experimental.
Q3 PASS instructions: instructions.started is recorded in the expected row (CSV line 2).
Q3 PASS instructions: recorded ending key 'space'.
Q3 PASS break: break_text.started is recorded in the expected row (CSV line 11).
Q3 PASS break: recorded ending key 'space'.
Q3 PASS end: end_text.started is recorded in the expected row (CSV line 108).
Q3 PASS Feedback placement: all 104 rows matched.
Q3 PASS Feedback: 8 durations agree with the rounded frame counts in the software timestamps.
Q3 PASS End screen: 1 durations agree with the rounded frame counts in the software timestamps.
Q3 UNDETERMINED Need the build or an observed run to establish the instruction and feedback wording and the actual screen transitions.
Q4 PASS Fixation: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS Prime: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS SOA: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS ITI: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS Target through response or timeout: all 104 rows matched.
Q4 UNDETERMINED Inspect the build or watch a run to confirm the fixation cross, stimulus case, and blank SOA and ITI screens. Physical timing requires a photodiode.
Q5 PASS Fixation: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Prime: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS SOA: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS ITI: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Timeout target: 2 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Feedback: 8 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS End screen: 1 durations agree with the rounded frame counts in the software timestamps.
Q5 UNDETERMINED One recorded refresh rate cannot establish the Builder conversion rule at other rates. Inspect the frame expressions and refresh-rate source.
Q6 PASS Recorded key mapping: all 102 rows matched.
Q6 UNDETERMINED Need the instructions and keyboard configuration or a controlled run to confirm displayed mapping, ignored keys and Escape.
Q7 PASS Keyboard synchronization: all 104 rows matched.
Q7 PASS Recorded RT reference: all 102 rows matched.
Q7 UNDETERMINED Need Builder or a controlled run to verify buffer clearing and first-key storage. Physical stimulus-to-key latency needs external measurement.
Q8 PASS prime text: all 104 rows matched.
Q8 PASS target text: all 104 rows matched.
Q8 UNDETERMINED Need Builder code to confirm the saved strings came from the stimulus objects at trial end.
Q9 PASS Custom onsets versus automatic flip stamps: all 104 rows matched.
Q9 UNDETERMINED Need build code to establish how the timestamps were captured. Measuring physical light onset requires hardware.
Q10 PASS Recorded response and timeout coding: all 104 rows matched.
Q10 PASS All ten recorded trial-list values match a row in trials_p04.csv.
Q10 UNDETERMINED Saved response codes cannot show unrecorded presses or establish the physical two-second deadline without reference timing evidence.
I1 UNDETERMINED No instrumentation log or column. Run the instrumented build and retain its matching log.
I2 UNDETERMINED No dropped_frames column or matching log. Run the instrumented build and retain both outputs.

provided/output_files\file_C.csv
Q1 FAIL Participant 7: 104/104 trial records do not match trials_p07.csv; first at CSV line 3, phase='practice', index='1', item='PW4'.
Q1 UNDETERMINED Inspect the Builder file and test the dialog and relative-path loading to settle the remaining Q1 requirements.
Q2 FAIL 104/104 trial records; missing=104, extra/changed=104; first sequence mismatch at trial position 1.
Q3 PASS Phase sequence: 104 trials with 8 practice and 96 experimental. Expected 8 practice followed by 96 experimental.
Q3 PASS instructions: instructions.started is recorded in the expected row (CSV line 2).
Q3 PASS instructions: recorded ending key 'space'.
Q3 PASS break: break_text.started is recorded in the expected row (CSV line 11).
Q3 PASS break: recorded ending key 'space'.
Q3 PASS end: end_text.started is recorded in the expected row (CSV line 108).
Q3 PASS Feedback placement: all 104 rows matched.
Q3 PASS Feedback: 8 durations agree with the rounded frame counts in the software timestamps.
Q3 PASS End screen: 1 durations agree with the rounded frame counts in the software timestamps.
Q3 UNDETERMINED Need the build or an observed run to establish the instruction and feedback wording and the actual screen transitions.
Q4 PASS Fixation: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS Prime: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS SOA: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS ITI: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS Target through response or timeout: all 104 rows matched.
Q4 UNDETERMINED Inspect the build or watch a run to confirm the fixation cross, stimulus case, and blank SOA and ITI screens. Physical timing requires a photodiode.
Q5 PASS Fixation: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Prime: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS SOA: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS ITI: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Timeout target: 2 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Feedback: 8 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS End screen: 1 durations agree with the rounded frame counts in the software timestamps.
Q5 UNDETERMINED One recorded refresh rate cannot establish the Builder conversion rule at other rates. Inspect the frame expressions and refresh-rate source.
Q6 PASS Recorded key mapping: all 102 rows matched.
Q6 UNDETERMINED Need the instructions and keyboard configuration or a controlled run to confirm displayed mapping, ignored keys and Escape.
Q7 PASS Keyboard synchronization: all 104 rows matched.
Q7 PASS Recorded RT reference: all 102 rows matched.
Q7 UNDETERMINED Need Builder or a controlled run to verify buffer clearing and first-key storage. Physical stimulus-to-key latency needs external measurement.
Q8 PASS prime text: all 104 rows matched.
Q8 PASS target text: all 104 rows matched.
Q8 UNDETERMINED Need Builder code to confirm the saved strings came from the stimulus objects at trial end.
Q9 PASS Custom onsets versus automatic flip stamps: all 104 rows matched.
Q9 UNDETERMINED Need build code to establish how the timestamps were captured. Measuring physical light onset requires hardware.
Q10 PASS Recorded response and timeout coding: all 104 rows matched.
Q10 FAIL 104 trial rows differ from trials_p07.csv, first at CSV line 3.
Q10 UNDETERMINED Saved response codes cannot show unrecorded presses or establish the physical two-second deadline without reference timing evidence.
I1 UNDETERMINED No instrumentation log or column. Run the instrumented build and retain its matching log.
I2 UNDETERMINED No dropped_frames column or matching log. Run the instrumented build and retain both outputs.

provided/output_files\file_D.csv
Q1 PASS Participant 2: all 104 recorded trial records match trials_p02.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 UNDETERMINED Inspect the Builder file and test the dialog and relative-path loading to settle the remaining Q1 requirements.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.
Q3 PASS Phase sequence: 104 trials with 8 practice and 96 experimental. Expected 8 practice followed by 96 experimental.
Q3 PASS instructions: instructions.started is recorded in the expected row (CSV line 2).
Q3 PASS instructions: recorded ending key 'space'.
Q3 PASS break: break_text.started is recorded in the expected row (CSV line 11).
Q3 PASS break: recorded ending key 'space'.
Q3 PASS end: end_text.started is recorded in the expected row (CSV line 108).
Q3 PASS Feedback placement: all 104 rows matched.
Q3 PASS Feedback: 8 durations agree with the rounded frame counts in the software timestamps.
Q3 PASS End screen: 1 durations agree with the rounded frame counts in the software timestamps.
Q3 UNDETERMINED Need the build or an observed run to establish the instruction and feedback wording and the actual screen transitions.
Q4 PASS Fixation: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS Prime: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS SOA: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS ITI: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS Target through response or timeout: all 104 rows matched.
Q4 UNDETERMINED Inspect the build or watch a run to confirm the fixation cross, stimulus case, and blank SOA and ITI screens. Physical timing requires a photodiode.
Q5 PASS Fixation: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Prime: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS SOA: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS ITI: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Timeout target: 4 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Feedback: 8 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS End screen: 1 durations agree with the rounded frame counts in the software timestamps.
Q5 UNDETERMINED One recorded refresh rate cannot establish the Builder conversion rule at other rates. Inspect the frame expressions and refresh-rate source.
Q6 PASS Recorded key mapping: all 100 rows matched.
Q6 UNDETERMINED Need the instructions and keyboard configuration or a controlled run to confirm displayed mapping, ignored keys and Escape.
Q7 PASS Keyboard synchronization: all 104 rows matched.
Q7 PASS Recorded RT reference: all 100 rows matched.
Q7 UNDETERMINED Need Builder or a controlled run to verify buffer clearing and first-key storage. Physical stimulus-to-key latency needs external measurement.
Q8 FAIL prime text: 104 inconsistent rows, first at CSV line 3: saved 'prime', expected 'gravel'
Q8 PASS target text: all 104 rows matched.
Q8 UNDETERMINED Need Builder code to confirm the saved strings came from the stimulus objects at trial end.
Q9 PASS Custom onsets versus automatic flip stamps: all 104 rows matched.
Q9 UNDETERMINED Need build code to establish how the timestamps were captured. Measuring physical light onset requires hardware.
Q10 PASS Recorded response and timeout coding: all 104 rows matched.
Q10 PASS All ten recorded trial-list values match a row in trials_p02.csv.
Q10 UNDETERMINED Saved response codes cannot show unrecorded presses or establish the physical two-second deadline without reference timing evidence.
I1 UNDETERMINED No instrumentation log or column. Run the instrumented build and retain its matching log.
I2 UNDETERMINED No dropped_frames column or matching log. Run the instrumented build and retain both outputs.

provided/output_files\file_E.csv
Q1 PASS Participant 5: all 104 recorded trial records match trials_p05.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 UNDETERMINED Inspect the Builder file and test the dialog and relative-path loading to settle the remaining Q1 requirements.
Q2 FAIL 104/104 trial records; missing=0, extra/changed=0; first sequence mismatch at trial position 1.
Q3 PASS Phase sequence: 104 trials with 8 practice and 96 experimental. Expected 8 practice followed by 96 experimental.
Q3 PASS instructions: instructions.started is recorded in the expected row (CSV line 2).
Q3 PASS instructions: recorded ending key 'space'.
Q3 PASS break: break_text.started is recorded in the expected row (CSV line 11).
Q3 PASS break: recorded ending key 'space'.
Q3 PASS end: end_text.started is recorded in the expected row (CSV line 108).
Q3 PASS Feedback placement: all 104 rows matched.
Q3 PASS Feedback: 8 durations agree with the rounded frame counts in the software timestamps.
Q3 PASS End screen: 1 durations agree with the rounded frame counts in the software timestamps.
Q3 UNDETERMINED Need the build or an observed run to establish the instruction and feedback wording and the actual screen transitions.
Q4 PASS Fixation: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS Prime: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS SOA: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS ITI: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS Target through response or timeout: all 104 rows matched.
Q4 UNDETERMINED Inspect the build or watch a run to confirm the fixation cross, stimulus case, and blank SOA and ITI screens. Physical timing requires a photodiode.
Q5 PASS Fixation: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Prime: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS SOA: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS ITI: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Timeout target: 1 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Feedback: 8 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS End screen: 1 durations agree with the rounded frame counts in the software timestamps.
Q5 UNDETERMINED One recorded refresh rate cannot establish the Builder conversion rule at other rates. Inspect the frame expressions and refresh-rate source.
Q6 PASS Recorded key mapping: all 103 rows matched.
Q6 UNDETERMINED Need the instructions and keyboard configuration or a controlled run to confirm displayed mapping, ignored keys and Escape.
Q7 PASS Keyboard synchronization: all 104 rows matched.
Q7 PASS Recorded RT reference: all 103 rows matched.
Q7 UNDETERMINED Need Builder or a controlled run to verify buffer clearing and first-key storage. Physical stimulus-to-key latency needs external measurement.
Q8 PASS prime text: all 104 rows matched.
Q8 PASS target text: all 104 rows matched.
Q8 UNDETERMINED Need Builder code to confirm the saved strings came from the stimulus objects at trial end.
Q9 PASS Custom onsets versus automatic flip stamps: all 104 rows matched.
Q9 UNDETERMINED Need build code to establish how the timestamps were captured. Measuring physical light onset requires hardware.
Q10 PASS Recorded response and timeout coding: all 104 rows matched.
Q10 PASS All ten recorded trial-list values match a row in trials_p05.csv.
Q10 UNDETERMINED Saved response codes cannot show unrecorded presses or establish the physical two-second deadline without reference timing evidence.
I1 UNDETERMINED No instrumentation log or column. Run the instrumented build and retain its matching log.
I2 UNDETERMINED No dropped_frames column or matching log. Run the instrumented build and retain both outputs.

provided/output_files\file_F.csv
Q1 PASS Participant 8: all 104 recorded trial records match trials_p08.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 UNDETERMINED Inspect the Builder file and test the dialog and relative-path loading to settle the remaining Q1 requirements.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.
Q3 PASS Phase sequence: 104 trials with 8 practice and 96 experimental. Expected 8 practice followed by 96 experimental.
Q3 PASS instructions: instructions.started is recorded in the expected row (CSV line 2).
Q3 PASS instructions: recorded ending key 'space'.
Q3 PASS break: break_text.started is recorded in the expected row (CSV line 11).
Q3 PASS break: recorded ending key 'space'.
Q3 PASS end: end_text.started is recorded in the expected row (CSV line 108).
Q3 PASS Feedback placement: all 104 rows matched.
Q3 PASS Feedback: 8 durations agree with the rounded frame counts in the software timestamps.
Q3 PASS End screen: 1 durations agree with the rounded frame counts in the software timestamps.
Q3 UNDETERMINED Need the build or an observed run to establish the instruction and feedback wording and the actual screen transitions.
Q4 PASS Fixation: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS Prime: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS SOA: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 PASS ITI: 104 durations agree with the rounded frame counts in the software timestamps.
Q4 FAIL Target through response or timeout: 104 inconsistent rows, first at CSV line 3: response window is not synchronized to target onset
Q4 UNDETERMINED Inspect the build or watch a run to confirm the fixation cross, stimulus case, and blank SOA and ITI screens. Physical timing requires a photodiode.
Q5 PASS Fixation: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Prime: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS SOA: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS ITI: 104 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Timeout target: 50 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS Feedback: 8 durations agree with the rounded frame counts in the software timestamps.
Q5 PASS End screen: 1 durations agree with the rounded frame counts in the software timestamps.
Q5 UNDETERMINED One recorded refresh rate cannot establish the Builder conversion rule at other rates. Inspect the frame expressions and refresh-rate source.
Q6 PASS Recorded key mapping: all 54 rows matched.
Q6 UNDETERMINED Need the instructions and keyboard configuration or a controlled run to confirm displayed mapping, ignored keys and Escape.
Q7 FAIL Keyboard synchronization: 104 inconsistent rows, first at CSV line 3: keyboard minus target onset is -650.000 ms
Q7 FAIL Recorded RT reference: 54 inconsistent rows, first at CSV line 3: keyboard minus target onset is -650.000 ms
Q7 UNDETERMINED Need Builder or a controlled run to verify buffer clearing and first-key storage. Physical stimulus-to-key latency needs external measurement.
Q8 PASS prime text: all 104 rows matched.
Q8 PASS target text: all 104 rows matched.
Q8 UNDETERMINED Need Builder code to confirm the saved strings came from the stimulus objects at trial end.
Q9 PASS Custom onsets versus automatic flip stamps: all 104 rows matched.
Q9 UNDETERMINED Need build code to establish how the timestamps were captured. Measuring physical light onset requires hardware.
Q10 FAIL Recorded response and timeout coding: 104 inconsistent rows, first at CSV line 3: keyboard times are referenced to a different onset, so the saved RT or timeout is not target-relative
Q10 PASS All ten recorded trial-list values match a row in trials_p08.csv.
Q10 UNDETERMINED Saved response codes cannot show unrecorded presses or establish the physical two-second deadline without reference timing evidence.
I1 UNDETERMINED No instrumentation log or column. Run the instrumented build and retain its matching log.
I2 UNDETERMINED No dropped_frames column or matching log. Run the instrumented build and retain both outputs.
```

</details>

## 4. Prediction reconciliation

I left my committed `a6_predictions.md` unchanged. Here is what matched and what differed.

**Provided-file table (Q3–Q10).** Q3–Q5 and Q7–Q9 largely matched my predictions: the files supported recorded sequences/timing, F failed the early response window (Q4/Q7), and D failed saved prime text (Q8). The unresolved screen wording, buffer handling, source of timestamps, other refresh rates, and physical timing stayed UNDETERMINED. **Q6** differed in the first checker because I initially used inaccurate `accuracy` fields to infer key mapping for A; that was corrected to a Q10 problem. **Q10** also failed on C, which I had not predicted as a new property failure: the checker correctly applies Q10's requirement to preserve the ten trial-list columns, so C's wrong list fails it too. This does not mean its response scoring was separately wrong.

| Prediction | What happened and why |
| --- | --- |
| **1. UNDETERMINED evidence** | As expected: a CSV cannot prove exact instructions, screen blanks, ignored keys, component-source values, other-rate behavior, or physical onset. |
| **2. Three extra failures after Q1/Q2** | **Correct: A, D, F.** B had no detectable new failure; C and E already failed Q1/Q2. |
| **3. ~120 Hz refresh** | **Changed:** A5 was near 120 Hz, but I manually set the laptop to **60 Hz** for A6. PsychoPy measured ~60 Hz and correctly used 30/9/60-frame timings instead of 60/18/120. |
| **4. Break prompt disappears** | **Confirmed:** text stopped after ~1 s even while the routine waited for SPACE. Fixed in `1f2dea1`, after runs 7/8. Other suspected timing differences remain unexplained, not silently marked PASS. |
| **5. Dropped intervals: 0 vs 10** | **Actually 2 vs 10.** A quiet computer can still have delayed flips. At 60 Hz the cutoff is **25 ms**, not the 12.5 ms I expected for 120 Hz. The logs support the totals, not a precise causal explanation or location for every delay. |
| **6. Dropped frame during prime** | The frame-based schedule still uses the right number of flips, but one missed refresh can add roughly **16.7 ms** of elapsed time at 60 Hz (not my predicted 8.3 ms at 120 Hz). |
| **7. What software can establish** | As expected, software supports the timing and onset consistency checks, but cannot verify actual light onset. My predicted ~one-frame response-to-offset delay was **not a guaranteed bound**; run 8 had a transition around **35 ms**. |

**Overall:** My files had no final definite failure in their recorded response/stimulus fields, but examining the build caught a real break-screen bug. The provided files show why correct trial lists alone are not enough: accuracy, recorded primes and response timing can still be wrong. I have kept the unresolved timing and hardware questions as uncertainties rather than calling them PASS.
