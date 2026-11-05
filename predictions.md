# Predictions and reconciliation (Part D)

Fill in **Predictions** before your first complete run, and commit this file
with a message that starts `predictions:`. Do not edit the Predictions
section after that commit; the history is how it is read. Then run the
experiment and fill in **Reconciliation**.

You are graded on the reconciliation, not on being right.

## Predictions

Answer for your own build, as participant 3.

1. How many rows will the output file have? How many of them will be trials?
   What will the other rows be?

2. Will any column name appear more than once? If so, which, and what will
   each copy hold on a trial row?

3. On an SOA 150 trial, what will `target_onset - prime_onset` be, in
   milliseconds and in frames, on the machine you are using? On an SOA 1000
   trial?

4. What will the median `rt` be, roughly, and what proportion of trials will
   be timeouts?

5. On a trial whose prime is `smoke` and whose target is `pepper`, what will
   `prime_shown` and `target_shown` hold, exactly?

### My answers

These answers are my own and were written outside this repository. They are
committed here before the first complete run of any build in this repository.
An earlier attempt at this task, kept in a separate repository, had already
been run as participants 3 and 6 before this commit, so they are not
predictions made before I had ever run the task. See `build_log.md`.

**1. How many rows will the output file have? How many will be trials? What will the other rows be?**

I'm expecting 107 rows in total. There should be 104 trials (8 practice and 96 experimental), with the other 3 rows coming from the instructions, break, and end screens.

**2. Will any column name appear more than once? If so, which, and what will each copy hold?**

I think `participant` might appear twice, once from the trial list and once from the experiment settings. Both should show 3.

**3. On an SOA 150 trial, what will `target_onset - prime_onset` be? What about an SOA 1000 trial?**

My computer runs at around 119 Hz, so I'm expecting about 151 ms (18 frames) for SOA 150 and 1000 ms (119 frames) for SOA 1000. There might be some small differences in the actual timings.

**4. What will the median RT be, roughly, and what proportion of trials will be timeouts?**

I'd expect the median RT to be around 700 ms, with maybe 5% of trials timing out since there's a 2-second response window.

**5. On a trial whose prime is `smoke` and target is `pepper`, what will `prime_shown` and `target_shown` hold?**

I'm expecting `prime_shown` to be `smoke` and `target_shown` to be `PEPPER`, since the prime stays lowercase and the target is shown in uppercase.

## Reconciliation

For each prediction: what you got, and if it differs, why. "I was wrong" is
not a reason. Name the mechanism: what PsychoPy, your build, or your machine
did that you did not expect.

I compared my predictions with the final Participant 3 run (`data/3_ldt_2026-11-04_21h45.27.117.csv`). I also checked Participant 6 where it was useful. I wasn't paying full attention during parts of these runs, which affected my responses.

1. **Number of rows:** This matched what I predicted. The file has 107 rows: 104 trials (8 practice and 96 experimental), plus one each for the instructions, break, and end screens. PsychoPy creates a new row after each trial and after those separate screens. Feedback and the blank interval are recorded with their trial, rather than as separate rows. Participant 3 also has two extra columns, `target_text.stopped` and `trial_key.stopped`, because a trial timed out; Participant 6 had no timeouts.

2. **Repeated column:** I was right that `participant` appears twice and both columns show 3, but my explanation was wrong. PsychoPy ends up writing the participant number from the startup dialog into both columns, rather than keeping separate numbers from the dialog and trial list. This means the two columns alone cannot tell us whether the right trial list was loaded. That is also why the provided file C can show participant 7 even though its trials came from participant 1's list.

3. **SOA timing:** The 150 ms SOA was close to my prediction, with a median of **150.67 ms**, or about **18 frames**. The 1000 ms SOA was slightly longer at **1004.40 ms**, or about **120 frames**, instead of the 119 I expected. PsychoPy measured the refresh rate at **119.58 Hz** and rounded it to **120 Hz** when calculating frames. Since the display was running a little below 120 Hz, those 120 frames took slightly more than a second. The frame counts are inferred from the timing because the output does not record them directly. I didn't see evidence of dropped frames in these final runs. I also had the external monitor unplugged this time, although I can't say for certain whether that explains the timing problems I saw in an earlier version.

4. **Reaction time and timeouts:** I predicted about **700 ms** and **5% timeouts**, but the median RT was **505 ms**, with only **1 timeout out of 104 trials (0.96%)**. Practice was slower at **876 ms**, while the experimental trials had a median of **494 ms**. Toward the end, I was responding much faster and wasn't always reading the targets properly. There were **9 responses under 100 ms**, and I often alternated between F and J. Because my trial list alternates word and nonword targets so often, this still gave me about **91% accuracy**. So the faster RT mostly reflects how I responded during the run, not better lexical decision performance. Responding quickly also made timeouts less likely.

5. **Prime and target text:** My prediction about the formatting was correct, but the exact `smoke`–`pepper` pair wasn't in Participant 3's list. Across its 104 trials, `prime_shown` matched the lowercase prime and `target_shown` matched the uppercase target. For example, `pebble` and `FRUNT` were recorded correctly. Participant 6 had `smoke` and `FIRE`, which were also recorded correctly. Based on that, a `smoke`–`pepper` trial should record `smoke` and `PEPPER`. These values came from the PsychoPy text components, rather than just copying the input list.
