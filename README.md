# ATLS TALKHAND

## What this is

ATLS TALKHAND is a two-part desktop project for recognizing fingerspelled letters from Mexican Sign Language (LSM) through a webcam. One half is a Python script that reads hand landmarks with MediaPipe and classifies vowel handshapes using geometry, no trained classifier involved. The other half is a .NET 7 WinForms application that hosts the actual lesson/practice screens the user sees. I built this as a student project at ITZ, and the repo still carries the seams from how it was actually built rather than a cleaned-up final version.

## Why I built it

LSM learning material for beginners tends to be static: PDFs, posters, maybe a YouTube video. I wanted something that would tell you, live, whether your hand was actually forming the letter correctly instead of you just guessing from a picture. Fingerspelling is a reasonable place to start because the handshapes for vowels are distinct enough to be told apart from finger angles alone, without needing a trained model or a labeled dataset.

## How it actually works

The recognition side lives in `ATLS/Funciones/`:

- `normalizacionCords.py` defines `obtenerAngulos(results, width, height)`. For each hand MediaPipe finds, it pulls three landmarks per finger (tip, PIP, MCP for the four main fingers; TIP/IP/MCP plus wrist for the thumb), turns them into pixel coordinates, and computes the three side lengths of the triangle they form with `np.linalg.norm`. From there it applies the law of cosines to get the joint angle in degrees for each of the six measured joints (pinky, ring, middle, index, thumb-outer, thumb-inner). If the denominator would be zero or the ratio falls outside `[-1, 1]`, it just defaults the angle to 0 instead of letting `acos` blow up. One thing I didn't notice until re-reading this code: the `return` sits inside the `for hand_landmarks in results.multi_hand_landmarks` loop, so even though `app.py` configures `max_num_hands=2`, this function only ever hands back the first hand it sees.
- `condicionales.py` takes the resulting 6-value angle list, converted into a binary "finger up/down" vector, and matches it against hardcoded patterns for A, E, I, O and U (e.g. `[1, 1, 0, 0, 0, 0]` reads as "A"). Each `obtenerX` function also writes a boolean flag for that letter into `ATLS/info.json`, which is how the recognition state gets out of the Python process. There's a `# abecedario` comment right before the end of `condicionalesLetras`, which is basically me leaving a note to myself that this was meant to grow into the full alphabet. It didn't get there.
- The main loop that ties this together (`app.py`) captures frames with `cv2.VideoCapture(0)`, runs them through `mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.75)`, and thresholds the six angles into the finger vector: thumb-outer counts as "up" above 125°, thumb-inner above 150°, and the other four fingers above 90°. It also has an attempt at detecting a moving "J" by tracking the frame-to-frame delta in the pinky's y-position and firing if it jumps more than 30 pixels. That branch never fully worked, more on that below.
- The Python side gets frozen into a standalone executable with cx_Freeze (that's what `ATLS/general/` and `ATLS/general/a/` are — a bundled Python 3.8 runtime plus OpenCV and MediaPipe), so the recognition script can run on a machine without a separate Python install.
- The `.NET 7` WinForms app (`ATLS TALKHAND.exe`, namespace `ATLS_TALKHAND`, five forms) is the part the user actually navigates. It reads `info.json` with Newtonsoft.Json to know what letter the Python side is currently seeing and embeds IronPython so the two runtimes can talk without a network socket or a proper IPC layer between them, just a shared file getting overwritten every frame.

## Stack, and why each piece is there

- **OpenCV (`opencv-python`)** for grabbing webcam frames and drawing the letter overlay and bounding box directly on the frame. Nothing fancier than that.
- **MediaPipe Hands** because I needed hand landmarks and had no interest in training a landmark detector myself. It's a pretrained model, I just consume its output.
- **NumPy** for `linalg.norm` on the landmark coordinates, which is all the vector math the angle calculation needs.
- **.NET 7 + WinForms** for the desktop shell, because it's the GUI stack I had actually been taught to use for a Windows desktop app at the time, not something picked for technical merit over Python's GUI options.
- **IronPython / IronPython.StdLib** embedded in the .NET app, so the WinForms side can host Python without shelling out to a separate process (in principle, `IronPython.Wpf.dll` is also pulled in as a dependency here even though the app is WinForms and never touches WPF, it's a leftover from the IronPython package set, not something I use).
- **Newtonsoft.Json** on the .NET side to parse `info.json`.
- **cx_Freeze** to package the Python recognition script as a standalone `.exe` so it doesn't need Python installed separately on whatever machine runs it.

## Running it

This only really runs on Windows, given WinForms and the bundled `python38.dll`/`python3.dll`.

1. Clone the repo.
2. You need a webcam.
3. To run the frozen build as-is: launch `ATLS/general/app.exe` for the recognition window, and `ATLS/ATLS TALKHAND.exe` for the lesson UI (needs the .NET 7 desktop runtime installed, not ".NET Framework 7.0" like the very first version of this README said, since ".NET Framework" and modern ".NET" are different products and version 7 only exists for the latter).
4. To work on the Python side from source: install `opencv-python`, `mediapipe`, and `numpy`, then import the functions in `ATLS/Funciones/`. Fair warning, the original `app.py` that wired `normalizacionCords` and `condicionales` together into a webcam loop isn't in this repo anymore, it got removed in the commit that added the frozen build. You can pull it back out of git history (commit `1004723`) if you want the original loop instead of writing a new one from scratch.

## What didn't go well

A few things, honestly:

- The repo has close to 130 MB of committed binaries: two near-duplicate cx_Freeze builds (`ATLS/general/` and `ATLS/general/a/`), each with a full bundled Python 3.8 stdlib plus OpenCV and MediaPipe `.pyd` files. That should have been a build step and a `.gitignore` entry, or shipped as a GitHub release, not checked into version control.
- The `.NET`/WinForms side (the five forms behind `ATLS TALKHAND.exe`) never actually had its `.cs`/`.resx` source committed, only the compiled `.dll`/`.exe`/`.pdb`. So this repository can't actually rebuild that half of the app; it can only run the binary that's already there.
- `app.py`, the actual entry point tying the recognition modules together, got deleted from the tree in the same commit that added the frozen build. What's left in `Funciones/` is real and works, but it's not a complete, runnable program on its own anymore.
- Only the five vowels are recognized. The "J" attempt in `app.py` (motion-based, tracking the pinky's vertical movement) has a bug: `cv2.rectangle(frame, (0, 0), (100, 100), (0, 0, ), -1)` passes a 2-value tuple where OpenCV expects a 3-value BGR color, so that branch would error out if it ever actually triggered. That's probably part of why it never made it into `condicionales.py` with the rest of the letters.
- There's no dataset and no accuracy numbers anywhere, the angle thresholds (90°, 125°, 150°) were picked by testing in front of my own webcam, not measured against labeled examples. That means it's sensitive to hand size, distance from the camera, and lighting in ways I never quantified. If I did this again I'd log a few hundred labeled frames per letter first and fit something small on top of the same MediaPipe landmarks, instead of hand-picking degree cutoffs.
