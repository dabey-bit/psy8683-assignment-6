# Verification report (Part C)

## Your own runs

Paste your checker's output for participants 3 and 6. 

```
Scope: Q1-Q2 only. Q3-Q10 deferred to Project 6.

data\3_ldt_2026-11-04_21h45.27.117.csv
Q1 PASS Participant 3: all 104 recorded trial records match trials_p03.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 PILOT Filename ldt.psyexp, dialog entry format, and actual relative-path loading cannot be established from output alone; inspect Builder and pilot.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.

data\6_ldt_2026-11-04_21h49.55.148.csv
Q1 PASS Participant 6: all 104 recorded trial records match trials_p06.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 PILOT Filename ldt.psyexp, dialog entry format, and actual relative-path loading cannot be established from output alone; inspect Builder and pilot.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.
```

For each property marked PILOT, say how you established it: what you watched
for, and what would have counted as a failure.

For any FAIL: what was wrong, what you changed, and the commit that fixed it.
If you fixed it, rerun and paste the new output too.

**PILOT (Q1).** I checked that `ldt.psyexp` was in the main project folder and that entering 3 or 6 selected the matching trial list. Both runs loaded and recorded the correct 104 trials. I also checked the setup code for the participant entry: it is meant to reject `03` and accept a plain integer. I did not test `03` during a run, and these runs were started from the compiled script rather than by reopening the file in Builder, so the Builder-opening part still needs to be checked. A failure would be the wrong list loading, an invalid participant entry being accepted, or the file not opening and compiling in Builder.

**FAILs and fixes.** There were no Q1 or Q2 FAILs on either final run, so I did not need to make a Q1/Q2 fix or rerun after these checks. Earlier versions were tested and changed during development; I discuss those changes in `build_log.md`.

The checks only establish that the right trials were recorded. They do not prove that my responses were good. My median RT was about 0.505 s for participant 3 and 0.122 s for participant 6, with accuracy of 91.3% and 52.9%, respectively. I was not consistently attending to the task, especially for participant 6, so I would not treat these as good behavioral data. They are still useful for checking what the experiment saved.

## The six provided files

Each of `provided/output_files/file_A.csv` … `file_F.csv` came from a
different build of this task, run by a different participant (the number is
in the file). They were generated from the lists in
`provided/canonical_trial_lists/`. Some builds may be broken and some may
not; do not assume a count in either direction.

For each file, answer three things. Two or three sentences each.

### file_A

- Verdicts (paste your checker's output, or summarize it):
  Q1 PASS, Q1 PILOT, Q2 PASS. All 104 recorded trials match participant 3's list in order. Outside Q1 and Q2, `accuracy` is 0 on every row even though 97 of 103 recorded responses match the correct keys.
- What the person who built it most likely did in Builder:
  They probably set the keyboard's correct answer to `$correct_response`, which contains `word` or `nonword`, instead of `f` or `j`. That would make every response count as wrong.
- What a researcher analyzing this file, without your checker, would have
  concluded:
  They could think the participant scored 0% and exclude the data, even though the recorded keys show about 93% accuracy (97/104). Any analysis using only trials marked correct would also have no rows. This issue needs a Q10 check; Q1 and Q2 do not detect it.

### file_B

- Verdicts:
  Q1 PASS, Q1 PILOT, Q2 PASS. I did not find another issue in my manual inspection. The recorded keys, displayed words, SOAs, and response timing looked consistent with the specification.
- What the person who built it most likely did in Builder:
  It looks like this one was set up correctly.
- What a researcher analyzing this file would have concluded:
  They would report around 96% accuracy and RTs around 600 ms, which is supported by what I could check. This is not proof that everything passed Q3–Q10, since those automated checks are for Project 6.

### file_C

- Verdicts:
  Q1 FAIL, Q1 PILOT, Q2 FAIL. The file says participant 7, but all 104 trials match participant 1's list rather than participant 7's.
- What the person who built it most likely did in Builder:
  They likely left `trial_lists/trials_p01.csv` as a fixed file in the Conditions field instead of selecting a file based on the participant number.
- What a researcher analyzing this file would have concluded:
  The researcher could treat it as participant 7 data, since both participant columns say 7 and the accuracy looks reasonable. But participant 7 never received the planned list, so the counterbalancing would be wrong.

### file_D

- Verdicts:
  Q1 PASS, Q1 PILOT, Q2 PASS. The trial-list data match, but `prime_shown` contains the literal text `prime` on all 104 trials.
- What the person who built it most likely did in Builder:
  They probably entered `prime` in the Text component instead of `$prime`.
- What a researcher analyzing this file would have concluded:
  They could assume the intended primes were displayed because the `prime` column looks correct. If the screen actually showed `prime` each time, the intended priming manipulation did not happen. Q8 would catch this.

### file_E

- Verdicts:
  Q1 PASS, Q1 PILOT, Q2 FAIL. All 104 trials are present, but they were run in a different order. The practice sequence begins 2, 3, 6, 7, 1, 4, 8, 5.
- What the person who built it most likely did in Builder:
  They likely left the practice and main loops on `random` rather than `sequential`.
- What a researcher analyzing this file would have concluded:
  They could assume the planned order had run, particularly if they later sorted by `trial_index`. Any analyses depending on trial order or previous-trial effects could then be misleading.

### file_F

- Verdicts:
  Q1 PASS, Q1 PILOT, Q2 PASS. Outside Q1–Q2, the keyboard began listening before the target: about 650 ms early for SOA 150 and 1500 ms early for SOA 1000.
- What the person who built it most likely did in Builder:
  They probably started the Keyboard component at the beginning of the trial routine, instead of at target onset.
- What a researcher analyzing this file would have concluded:
  They could report a large SOA effect on RT: medians were 1.289 s at SOA 150 and 1.947 s at SOA 1000. But those RTs included time before the target, and the keyboard stopped too early on longer-SOA trials, producing 50 false timeouts out of 52. Q1 and Q2 would not detect this timing problem.

## Your first checker on the six files

Run your first working checker on the six files before you look at them by
hand, and commit that output (paste it here too). Then:

The output below is from the first checker. I saved it unchanged in `verification/first_checker_provided.txt`. My earlier work records it in commit `3b2ea30` from a previous repository attempt; that earlier commit should be kept available as evidence of when the checker was run.

```text
Scope: Q1-Q2 only. Q3-Q10 deferred to Project 6.

provided/output_files\file_A.csv
Q1 PASS Participant 3: all 104 recorded trial records match trials_p03.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 PILOT Filename ldt.psyexp, dialog entry format, and actual relative-path loading cannot be established from output alone; inspect Builder and pilot.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.

provided/output_files\file_B.csv
Q1 PASS Participant 4: all 104 recorded trial records match trials_p04.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 PILOT Filename ldt.psyexp, dialog entry format, and actual relative-path loading cannot be established from output alone; inspect Builder and pilot.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.

provided/output_files\file_C.csv
Q1 FAIL Participant 7: 104/104 trial records do not match trials_p07.csv; first at CSV line 3, phase='practice', index='1', item='PW4'.
Q1 PILOT Filename ldt.psyexp, dialog entry format, and actual relative-path loading cannot be established from output alone; inspect Builder and pilot.
Q2 FAIL 104/104 trial records; missing=104, extra/changed=104; first sequence mismatch at trial position 1.

provided/output_files\file_D.csv
Q1 PASS Participant 2: all 104 recorded trial records match trials_p02.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 PILOT Filename ldt.psyexp, dialog entry format, and actual relative-path loading cannot be established from output alone; inspect Builder and pilot.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.

provided/output_files\file_E.csv
Q1 PASS Participant 5: all 104 recorded trial records match trials_p05.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 PILOT Filename ldt.psyexp, dialog entry format, and actual relative-path loading cannot be established from output alone; inspect Builder and pilot.
Q2 FAIL 104/104 trial records; missing=0, extra/changed=0; first sequence mismatch at trial position 1.

provided/output_files\file_F.csv
Q1 PASS Participant 8: all 104 recorded trial records match trials_p08.csv across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.
Q1 PILOT Filename ldt.psyexp, dialog entry format, and actual relative-path loading cannot be established from output alone; inspect Builder and pilot.
Q2 PASS 104/104 trial records, each reference row once and in file order; 3 nontrial rows excluded. This verifies recorded rows, not independent screen observation.
```

- If it got a verdict wrong, in either direction, say which, what your check
  was actually testing, and what you changed. The fix belongs in its own
  commit.
- If it got all six right, say for each file which of your checks could have
  failed on it, and whether it did.

The first checker did not get any **Q1 or Q2** verdict wrong, so I did not need to change those verdicts. It is limited to Q1 and Q2, though, and that is why files A, D and F can still pass while having problems with other properties.

| File | What the checker could have caught | What happened |
| --- | --- | --- |
| A | Wrong participant list (Q1) or missing/reordered trials (Q2) | Neither failed; the problem is accuracy coding (Q10). |
| B | Wrong list or order (Q1/Q2) | Neither failed; no problem found in my inspection. |
| C | Wrong participant list (Q1) and mismatch in the expected sequence (Q2) | Both failed, correctly. |
| D | Wrong list or order (Q1/Q2) | Neither failed; the displayed prime was wrong (Q8). |
| E | Missing, repeated or reordered trials (Q2) | Q2 failed at the first trial, correctly; Q1 passed because the rows belonged to the right list. |
| F | Wrong list or order (Q1/Q2) | Neither failed; the problem is keyboard timing (Q7/Q4). |

I also ran nine tests in `test_check_output.py` using deliberately incorrect trial data. They checked that the checker could fail on missing, repeated, reordered, changed, or wrong-list trials, rather than just printing PASS. All nine tests passed. My earlier interpretation of file A as possibly having reversed accuracy coding was wrong: `accuracy` was zero for every trial, which is different from simply reversing the keys. That correction did not change the Q1/Q2 checker results.
