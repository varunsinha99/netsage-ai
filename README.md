# NetSage AI: AI-Assisted Network Troubleshooter (with Human Review)

Cisco AICTE Virtual Internship (AI track), Project 2: *Applied AI + Network Troubleshooting*.

NetSage AI reads a symptom, a topology note and show-command output from a Cisco-style lab network, then suggests a likely root cause, confidence, evidence, next command and fix steps as structured JSON. **A human reviews every diagnosis** (Accepted / Edited / Rejected). A separate deterministic Python checker validates common config mistakes without using any AI.

## Repository layout

| Path | What it is |
|---|---|
| `data/cases.csv` | 30 troubleshooting cases: symptom, topology note, show output, expected fault, OSI layer, concept tag, severity |
| `data/comparison.csv` | AI root cause vs expected fault per case (yes / partial) |
| `prompts/diagnose_prompt.md` | System prompt, user template, 3 worked examples (JSON output) |
| `ai_outputs/diagnoses.json` | AI diagnosis for each of the 30 cases |
| `checker/checker.py` | Rule-based checker: duplicate IP, mask mismatch, gateway mismatch, interface down, missing VLAN, missing route |
| `checker/checker_output.txt` | Sample output of the checker |
| `review/review_log.csv` | Human review status and note per case (24 Accepted, 5 Edited, 1 Rejected) |
| `dashboard/NetSage_AI_Dashboard.xlsx` | Cases by fault type and severity, AI vs human outcome |

## Coverage

30 cases: VLAN (4), Gateway (4), DHCP (4), DNS (4), Routing (4), ACL (4), NAT (3), Wireless (3).

## Run the checker

```bash
python3 checker/checker.py
```

## Methodology


- AI outputs in `ai_outputs/diagnoses.json` were generated using <model name> via <how you ran it>.
- Each case was run with the prompt in `prompts/diagnose_prompt.md`. <Outputs were / were not edited manually.>
- Human review (Accepted / Edited / Rejected) was done by me and logged in `review/review_log.csv`.

## Known limitations (work in progress)

Being upfront about what is not done yet:

- Worked examples in the prompt overlap with test cases (GW-01, VLAN-03); they need to be replaced with separate examples to avoid inflating agreement.
- Several `evidence` fields quote only a header line instead of the line that proves the fault.
- `fix_steps` and `next_command` are fairly generic across cases.
- The checker currently runs on a sample dictionary, not yet on parsed show output from the 30 cases.
- Dashboard values are static, not generated from the CSV files.
- Demo video and Packet Tracer topology files are not included yet.

## Planned next steps

1. Re-run all 30 cases with a fresh AI run and unedited raw outputs, with separate worked examples.
2. Write a detailed Responsible AI log (AI answer, human correction, why, lesson).
3. Add a parser so the checker runs on the actual cases, and compare checker vs AI.
4. Generate the dashboard from CSV with a script.
5. Add the demo video and Packet Tracer files.
