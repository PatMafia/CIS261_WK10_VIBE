# CIS261_WK10_VIBE

## Student Record Manager

Run the program with:

```bash
python VIBE.py
```

The program adds students with exactly three test scores, calculates the average
and letter grade, displays a formatted table, reports class statistics, and
searches by name without regard to case. Records are loaded from and saved to
`student_grades.txt`. Press **ESC** from the menu to save and exit.

Each saved record uses this pipe-delimited format:

```text
name|id|test1|test2|test3|average|grade
```

Letter grades use these ranges:

- A: 90-100
- B: 80-89
- C: 70-79
- D: 60-69
- F: below 60