# Predictions (Part A)

These are my predictions before any new A6 checks or runs. I used my A5 reports and build code, without reopening the six provided datasets. My A5 report already describes some problems beyond Q1 and Q2, so those predictions reflect what I already knew. For my own build, the baseline is `ef6c471` (`Start Assignment 6`), on the same laptop as A5.

These answers were drafted with AI help from my previous work. Once reviewed and committed with `predictions-a6:`, I will leave them unchanged and put the reconciliation in `a6_report.md`.

## The six provided files

Each cell predicts the file-only verdict. I have split the verdicts where different parts may get different results. PASS here means the recorded evidence should meet that part of the requirement, not that the file proves what physically appeared on the display.

| Property | A | B | C | D | E | F |
| --- | --- | --- | --- | --- | --- | --- |
| Q3 | PASS sequence; UNDETERMINED screen content | PASS sequence; UNDETERMINED screen content | PASS sequence; UNDETERMINED screen content | PASS sequence; UNDETERMINED screen content | PASS sequence; UNDETERMINED screen content | PASS sequence; UNDETERMINED screen content |
| Q4 | PASS recorded timing; UNDETERMINED feedback text | PASS recorded timing; UNDETERMINED feedback text | PASS recorded timing; UNDETERMINED feedback text | PASS recorded timing; UNDETERMINED feedback text | PASS recorded timing; UNDETERMINED feedback text | FAIL response window; PASS fixation, prime and SOA; UNDETERMINED feedback text |
| Q5 | PASS recorded frame counts; UNDETERMINED other refresh rates | PASS recorded frame counts; UNDETERMINED other refresh rates | PASS recorded frame counts; UNDETERMINED other refresh rates | PASS recorded frame counts; UNDETERMINED other refresh rates | PASS recorded frame counts; UNDETERMINED other refresh rates | PASS fixed visual frame counts; UNDETERMINED other refresh rates |
| Q6 | UNDETERMINED instructions | UNDETERMINED instructions | UNDETERMINED instructions | UNDETERMINED instructions | UNDETERMINED instructions | UNDETERMINED instructions |
| Q7 | PASS recorded keyboard onset; UNDETERMINED first-key/buffer handling | PASS recorded keyboard onset; UNDETERMINED first-key/buffer handling | PASS recorded keyboard onset; UNDETERMINED first-key/buffer handling | PASS recorded keyboard onset; UNDETERMINED first-key/buffer handling | PASS recorded keyboard onset; UNDETERMINED first-key/buffer handling | FAIL recorded keyboard onset; UNDETERMINED first-key/buffer handling |
| Q8 | PASS recorded text | PASS recorded text | PASS recorded text | FAIL prime; PASS target | PASS recorded text | PASS recorded text |
| Q9 | PASS onset values; UNDETERMINED how captured | PASS onset values; UNDETERMINED how captured | PASS onset values; UNDETERMINED how captured | PASS onset values; UNDETERMINED how captured | PASS onset values; UNDETERMINED how captured | PASS onset values; UNDETERMINED how captured |
| Q10 | FAIL accuracy; PASS key, RT and timeout consistency | PASS recorded responses | PASS recorded responses | PASS recorded responses | PASS recorded responses | FAIL target-relative RT and timeout; PASS key coding |

For Q3, sequence means the practice, break and experimental sections, rather than the trial-list order already checked in Q2. For Q5, the fixed visual events should use the required frame counts at the simulated 60 Hz, even in F, where the response window looks wrong based on my A5 report. For Q8, I am predicting agreement between the recorded shown text and the intended text; proving that those values came from the displayed components needs the build.

**1. Which parts will be UNDETERMINED for every file?**

The exact instructions and screen content in Q3/Q6, and the feedback wording in Q4, should stay UNDETERMINED if they were not saved. Screen names and timestamps do not establish the words shown. I would need the build or a recording of a run to settle those parts.

For Q5, one 60 Hz file cannot show whether the build calculates frames correctly at other refresh rates. For Q7, a saved response does not prove that earlier keys were cleared or that the first eligible key was kept. Those need the code or a controlled test. For Q8/Q9, matching text and onset values can pass consistency checks, but the build is needed to establish that they came from the actual text components and flip timestamps. Physical display timing would still need hardware.

**2. How many files that passed Q1 and Q2 will fail something else?**

My prediction is **three: A, D and F**. My A5 report describes incorrect accuracy in A, the literal word `prime` in D, and a keyboard window starting before the target in F. B should pass the parts the file can settle. C and E already failed A5 checks, but my prediction is that neither has additional Q3–Q10 failures.

## Your own build

**3. Expected refresh rate and frame counts**

On the same laptop, `frameRate` should be about **119.6 Hz**, close to the 119.58 Hz recorded in my A5 report. That rounds to **120 Hz**, or about **8.33 ms per frame** for Q5. That gives these frame counts:

| Event | Intended duration | Frames at 120 Hz |
| --- | --- | --- |
| Fixation | 500 ms | 60 |
| Prime | 150 ms | 18 |
| Prime to target, SOA 150 | 150 ms | 18 |
| Prime to target, SOA 1000 | 1000 ms | 120 |
| ITI | 500 ms | 60 |
| Feedback | 1000 ms | 120 |
| End screen | 2000 ms | 240 |

The SOA is measured from prime onset to target onset, not from prime offset. At a measured rate slightly below 120 Hz, the durations in milliseconds should be slightly longer than the nominal values, even without dropped frames.

**4. Expected failures in my A5 build**

My prediction is a **Q3 failure in the break screen**: its text is set to disappear after one second, while the space-key component can keep waiting. That would leave a blank screen if I wait before pressing space. This is the part I am least sure of, and it needs checking against the full presentation specification and an actual run.

The other Q3–Q10 requirements should pass. The build uses frame counts, starts the keyboard with the target, and records the displayed text and onset times. I am less confident about exactly what gets saved when a response ends the trial, especially the target's offset and responses near the two-second limit. My low accuracy in A5 is not itself evidence that the build scored responses incorrectly.

**5. Expected dropped frames**

My prediction is **0 dropped intervals for participant 7** with nothing else open, and **10 for participant 8** with a muted browser video playing. These are estimates, not measurements. The extra load will probably cause occasional delays rather than a problem on every trial.

Most of the delays in run 8 will probably fall during the long SOA interval and target period, since those take up most of the recorded time. There may also be one or two around prime or target onset. I2 counts intervals longer than 1.5 frames, not the number of missing refreshes inside each interval. At 120 Hz, that threshold is **12.5 ms**. Delays during feedback, the ITI or separate screens should not contribute to this total because they are outside I1's recording window.

**6. What happens if a frame is dropped during the prime?**

The prime should stay on screen **longer**, and the SOA on that trial should get **longer too**. My build schedules both prime duration and target onset by frame number. If a refresh is missed while the prime is visible, the old image stays up until the next flip; the build does not shorten the later blank interval to catch up. A single missed refresh at 120 Hz would add roughly **8.33 ms** to both durations.

**7. What can software timestamps establish?**

Software timestamps should verify these three things, assuming they really are recorded on the relevant flips and use compatible clocks:

- The fixation duration from its onset and offset (Q4/Q5).
- The prime duration from its onset and offset (Q4/Q5).
- The prime-to-target SOA from the two onset times (Q4/Q9).

They can only **bound the screen change after a response** (Q4/Q7): the change must wait for a flip. With no dropped frames or extra processing delay, that should take up to about one frame, or 8.33 ms at 120 Hz, from detecting the response to changing the screen. A dropped frame would widen that bound.

They cannot establish **when the pixels physically changed luminance**, including the physical prime-to-target interval. That needs a photodiode and external timing equipment. A flip timestamp alone does not measure the display's response delay.
