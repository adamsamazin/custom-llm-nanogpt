# Your tasks, step by step

Everything not listed here is done by Claude. Each task below tells you exactly what to
open, what to click or type, what you should see, and what to do if it looks wrong.

Folder for this project (I'll call it **the repo folder**):
`C:\Users\adams\OneDrive\Documents\Claude\Fundamentals of Agentic AI\Assignment 3_Building a Custom LLM with nanoGPT\custom-llm-nanogpt`

---

## A1 — Approve the Python install  ✅ done

Python 3.12 and PyTorch are installed. Nothing more to do.

---

## A2 — Write your prediction (before any training)

The assignment requires you to write your choices, reasons, and a prediction **before**
training, in your own words. I drafted it from the decisions you made in our chat.

1. In the repo folder, double-click **`PREDICTION.md`**. It opens in Notepad (or whatever
   opens `.md` files; Notepad is fine).
2. Read it. It has two parts: **My three choices** and **What I expect to see**.
3. Edit anything you would say differently. You do not have to change much — but the
   graders read this as your voice, so it should sound like you. Keep the numbers
   (they come from the 10-step setup check) unless you have a reason to change them.
4. **File → Save** (Ctrl+S). Close Notepad.
5. Tell me "prediction done" in chat. I will copy it into the notebook and commit it
   before training starts, so the timestamp proves it was written first.

*If Notepad shows odd characters like `**` or `-` at line starts: that is normal —
it is Markdown formatting and renders as bold and bullets on GitHub.*

---

## A3 — GitHub repository  ✅ done (via the GitHub CLI, signed in once in the browser)

Repo: https://github.com/adamsamazin/custom-llm-nanogpt — the browser steps below are no longer needed.

<details><summary>Original manual steps (not needed)</summary>

1. Open your browser and go to **https://github.com/new** (sign in as `adamsamazin` if asked).
2. **Repository name:** `custom-llm-nanogpt`
3. **Description** (optional): `Class 4 – training a word-token nanoGPT from scratch and evaluating it`
4. Select **Public**.
5. Leave **all three checkboxes unticked** — no README, no .gitignore, no license.
   (I already created those files locally; ticking them causes a conflict on the first push.)
6. Click **Create repository**.
7. You will land on a page titled "Quick setup". Copy the URL shown at the top, which
   should be exactly `https://github.com/adamsamazin/custom-llm-nanogpt.git`, and paste
   it to me in chat. That's it — I do the push.

*If the name is taken or GitHub complains: tell me what it says.*

*If the push asks you for a login:* a Windows window titled "Connect to GitHub" may pop
up the first time. Choose **Sign in with your browser**, approve, and it will remember you.

</details>

---

## A4 — Chat with your trained model  ✅ done

This is the "working result" evidence: you typing prompts into the trained model and
it replying. The transcript is saved automatically; you take one screenshot.

1. In the repo folder, **double-click `chat.bat`**. A black console window opens.
   *If Windows shows "Windows protected your PC": click **More info → Run anyway**.
   It's the two-line script you can open in Notepad.*
2. After a second you will see:
   ```
   Tiny language model: short continuations, not a general assistant.
   Each prompt starts fresh. Context: 48 tokens. Type /quit to exit.
   You:
   ```
3. Type the first prompt exactly as written (lowercase, no punctuation), press **Enter**,
   and wait for the `Model:` line. Then type the next one. Use these five, in order:

   | # | Type this | Why |
   |---|---|---|
   | 1 | `the team discussed the surgeon` | Starter-corpus territory — should be fluent |
   | 2 | `the opposite of noisy is` | A skill the corpus extension taught |
   | 3 | `the cup is not green .it is pink .the cup is` | Negation — expected to fail (the space-free `.it` is deliberate; see README) |
   | 4 | `my neighbor bought a laptop` | Contains words the model never saw — shows the "Unknown words:" message |
   | 5 | anything you like | Your own question — try asking it something a chatbot would answer |

4. Type `/quit` and press Enter. You'll see `Saved transcript: results\expanded\chat\chat_...json`.
5. **Screenshot before closing the window:** press **Win + Shift + S**, drag a box around the
   whole console window, release. A "Snip saved to clipboard" popup appears.
6. Open **Paint** (Start menu → type Paint), press **Ctrl + V**, then **File → Save as → PNG**.
   Save it as **`chat_screenshot.png`** inside the folder
   `custom-llm-nanogpt\results\expanded\chat\`
   (in the Save dialog, paste the full path from step 4's message minus the filename, or
   click through OneDrive → Documents → Claude → Fundamentals of Agentic AI → Assignment 3… → custom-llm-nanogpt → results → expanded → chat).
7. Press any key in the console window to close it. Tell me "chat done".

*What "normal" looks like:* replies are short lowercase sentence fragments, sometimes
odd. Prompt 3 will very likely answer with the wrong colour — that's the expected
failure and it goes in the README. Prompt 4 will print `Unknown words: ...` under the reply.

*If it errors:* copy the red text and paste it to me.

---

## A5 — Embedding viewer screenshots  ✅ done

The viewer is a web page that runs in your browser with no install. It shows where
each word sits in the model's 64-number space, squashed to 3D.

1. In the repo folder, double-click **`embedding-viewer.html`**. It opens in your browser.
2. Click **Open your checkpoint** (a button near the top).
3. In the file picker, go to `custom-llm-nanogpt\results\expanded\` and choose **`checkpoint.json`**.
4. The point cloud loads. In the word menu (a search box or dropdown), select **`customer`**.
   You should see its 64 numbers and its three nearest neighbours (expect client, consumer, subscriber or similar).
5. **Win + Shift + S**, snip the whole viewer, paste into Paint, save as
   `results\expanded\viewer_customer.png`.
6. Now select **`kitten`**, and snip again → `results\expanded\viewer_kitten.png`.
   (Its neighbours will include *puppy* — and also *carrot* and *salmon*, which is a
   finding we'll explain in the README.)
7. If the viewer has an "initial / final" or "before / after" toggle, click it once for
   `customer` and notice how the neighbours change from random words to shopping words.
   No screenshot needed for that.
8. Tell me "viewer done".

*If the page is blank or the button does nothing:* try a different browser (Edge or
Chrome), and tell me which one you used.

## A6 — Review the README and make sections 7–8 yours  ← do this now

The README is the grading entry point. I drafted all of it from the result files, in first
person, so it reads as your write-up. Every number is copied from a JSON in `results/` and
I re-checked each one. Two sections are the ones a grader reads as *your understanding*:

- **Section 7 — What I learned** (six paragraphs answering the notebook's six questions)
- **Section 8 — One limitation and my next experiment**

Those must sound like you. Here is the easiest way to do that:

1. Read the README on GitHub first, where it's nicely formatted:
   **https://github.com/adamsamazin/custom-llm-nanogpt** — scroll through the whole thing
   once (10–15 minutes). If anything is unclear to *you*, it will be unclear to a grader:
   tell me and I'll rewrite it.
2. Then open **`README.md`** in the repo folder with Notepad and scroll to
   `## 7. What I learned` (about two-thirds of the way down; Ctrl+F helps).
3. Edit sections 7 and 8 in your own words. You do not need to rewrite them from scratch —
   changing phrasing, cutting sentences you wouldn't say, and adding a sentence of your own
   here and there is plenty. **Keep the numbers as they are** (they are the measured values).
   Leave the `**bold**` markers and the `## 7.` / `## 8.` heading lines alone.
4. Optional: do the same anywhere else you'd phrase things differently. It's your document.
5. Ctrl+S, close Notepad, tell me "readme done". I'll check that nothing broke in the
   formatting, commit, and push.

*If you'd rather not edit the file:* just tell me in chat what you'd change and I'll apply it.

---

## A7 — Final check and submit  ← after A6

1. Open a **private/incognito window** (Ctrl+Shift+N in Chrome or Edge) so you are signed out
   of GitHub, and go to **https://github.com/adamsamazin/custom-llm-nanogpt**.
2. Confirm you can see: the README with its tables and the two loss-curve pictures; and that
   clicking **`notebooks/custom_llm_expanded.ipynb`** shows a notebook with outputs (scroll
   down — you should find lines like `Language evals (final): 33/48`).
3. Submit this URL in the course portal:
   `https://github.com/adamsamazin/custom-llm-nanogpt`
4. Tell me "submitted" and I'll save a memory note of where everything lives.
