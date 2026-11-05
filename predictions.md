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

   I'm expecting 107 rows in total. There should be 104 trials (8 practice and 96 experimental), with the other 3 rows coming from the instructions, break, and end screens.

2. Will any column name appear more than once? If so, which, and what will
   each copy hold on a trial row?

   I think `participant` might appear twice, once from the trial list and once from the experiment settings. Both should show 3.

3. On an SOA 150 trial, what will `target_onset - prime_onset` be, in
   milliseconds and in frames, on the machine you are using? On an SOA 1000
   trial?

   My computer runs at around 119 Hz, so I'm expecting about 151 ms (18 frames) for SOA 150 and 1000 ms (119 frames) for SOA 1000. There might be some small differences in the actual timings.

4. What will the median `rt` be, roughly, and what proportion of trials will
   be timeouts?

   I'd expect the median RT to be around 700 ms, with maybe 5% of trials timing out since there's a 2-second response window.

5. On a trial whose prime is `smoke` and whose target is `pepper`, what will
   `prime_shown` and `target_shown` hold, exactly?

   I'm expecting `prime_shown` to be `smoke` and `target_shown` to be `PEPPER`, since the prime stays lowercase and the target is shown in uppercase.

## Reconciliation

For each prediction: what you got, and if it differs, why. "I was wrong" is
not a reason. Name the mechanism: what PsychoPy, your build, or your machine
did that you did not expect.

1.

2.

3.

4.

5.