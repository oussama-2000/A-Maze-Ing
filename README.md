resource:
https://youtu.be/ioUl1M77hww?si=rY_LKxkN0dleR-Tm




Perfect. You’re asking the **right question at the right time**.
Here is the **exact coding order** you should follow — **step by step**, no skipping, no chaos.

Think of this as your **project roadmap**. If you follow it, you won’t get stuck.

---

# ✅ CODING ORDER (STRICT & SAFE)

## 🔹 STEP 0 — Repo & rules (30 min, once)

**Do this once, together**

* Create repo
* Add `.gitignore`
* Add empty folders
* Decide:

  * `maze[y][x]`
  * `Cell.walls = {N,E,S,W}`
  * Direction constants

👉 **No logic yet**

Commit:

```bash
git commit -m "Project skeleton and shared data model"
```

---

## 🔹 STEP 1 — Cell & grid (FOUNDATION)

📁 `mazegen/generator.py`

### What to code

1. `Cell` class
2. Maze grid initialization
3. Helper methods

### Goals

* You can create an empty maze
* All walls are initially closed
* No generation yet

### Checklist

* [ ] `Cell(walls, visited)`
* [ ] `create_grid(width, height)`
* [ ] `in_bounds(x, y)`
* [ ] `get_cell(x, y)`

👉 **STOP and test here**

---

## 🔹 STEP 2 — Wall carving helpers

### What to code

* `DIRECTIONS`
* `OPPOSITE`
* `carve_passage(current, neighbor, direction)`

### Goals

* Removing a wall works
* Neighbor wall updates correctly

👉 Write a tiny manual test:

* Open E wall
* Check W wall of neighbor

---

## 🔹 STEP 3 — Backtracking maze generation (CORE)

### What to code

* Recursive DFS OR stack-based DFS
* Random unvisited neighbor selection

### Goals

* Entire grid becomes connected
* No crashes
* PERFECT maze achieved

### Checklist

* [ ] Mark visited
* [ ] Random neighbor
* [ ] Backtrack when stuck

👉 **At this point you HAVE a maze**

---

## 🔹 STEP 4 — Shortest path solver (BFS)

### What to code

* BFS from ENTRY to EXIT
* Parent tracking
* Direction reconstruction (`N E S W`)

### Goals

* Correct shortest path
* Works on any maze

👉 Print path length to test

---

## 🔹 STEP 5 — Config file parser (SAFETY FIRST)

📁 `config/parser.py` or similar

### What to code

* Read file
* Parse `KEY=VALUE`
* Validate everything

### Goals

* Bad config → clear error
* No crashes ever

---

## 🔹 STEP 6 — Hex output encoder (FORMAT CRITICAL)

### What to code

* Convert walls → bits → hex
* Write maze rows
* Append entry, exit, path

### Goals

* Validator passes
* Output exactly matches spec

👉 Test with `output_validator.py`

---

## 🔹 STEP 7 — ASCII renderer (VISUAL)

📁 `renderer/ascii.py`

### What to code

* Draw walls
* Draw entry/exit
* Draw solution path
* Colors (optional but nice)

### Goals

* Maze clearly visible
* User interactions work

---

## 🔹 STEP 8 — Main script glue

📁 `a_maze_ing.py`

### What to code

* Read config
* Create generator
* Generate maze
* Solve
* Render / save output

---

## 🔹 STEP 9 — “42” pattern (SPECIAL RULE)

### What to code

* Insert closed cells forming “42”
* Validate size
* Fail gracefully if impossible

---

## 🔹 STEP 10 — Cleanup & README

### What to do

* Makefile
* README explanation
* Final tests
* Merge to `main`

---

# 🧠 WHO DOES WHAT (REMINDER)

| Step | Owner      |
| ---- | ---------- |
| 1–4  | Teammate A |
| 5–8  | Teammate B |
| 9–10 | Both       |

---

# 🚨 MOST IMPORTANT RULE

**Never move to the next step until the current one works.**

This project is a domino chain.
Skip one → everything falls.

---

If you want, next I can:

* Write **Step 1 code with you**
* Review your **first commit**
* Help you debug **DFS backtracking**
* Provide **unit tests per step**

Just say:
👉 **“Let’s code Step 1”** 💻🔥

from dev branch
check here.
