# LongDay

LongDay is a local-first planning tool that turns vagu e goals into realistic days.

Describe what you want to do and how much time you have.
LongDay breaks it down and fits it into your day.

## Philosophy

Planning before tracking
Time as a first-class constraint
Simple, local, transparent

## Project Structure

```
longday
│
├── main.py        # Application entry point
├── config.py      # Global configuration
├── core           # Core data structures and domain logic
│   ├── task.py
│   ├── schedule.py
│   └── allocation.py
├── services       # Main application logic (planning, scheduling, task operations)
├── storage        # File persistence (load/save project data)
├── ui             # User interface components
├── utils          # Shared helper utilities
└── tests          # Unit and integration tests
```

## Status

Early development.
Planning engine first, UI later.
