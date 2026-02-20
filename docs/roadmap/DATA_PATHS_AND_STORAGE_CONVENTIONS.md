---



\# 📄 2️⃣ `DATA\_PATHS\_AND\_STORAGE\_CONVENTIONS.md`



```md

\# Data Paths and Storage Conventions



\## Purpose



This document defines how data storage paths are managed across the platform,

with a clear separation between \*\*environment-level directories\*\*

and \*\*tool-level storage logic\*\*.



The objective is to ensure consistency, flexibility, and tool autonomy.



---



\## Layered Responsibility Model



Data paths are handled in two distinct layers:



1\. Global base paths (environment-level)

2\. Tool-specific subpaths (local ownership)



---



\## Global Base Paths (`utils/paths.py`)



\### Role



`utils/paths.py` defines \*\*stable base directories\*\* that represent

logical storage domains (raw, generated, partner data, etc.).



It does \*\*not\*\* contain tool-specific knowledge.



\### Characteristics



\- Environment-dependent

\- Stable and infrequently changed

\- Shared across the entire application

\- Free of business or tool logic



\### Example



```python

DATA\_DIR = BASE\_DIR / "data"

GENERATED\_DIR = DATA\_DIR / "generated"

PARTNER\_DATA\_DIR = GENERATED\_DIR / "partner"






These paths act as mount points, not final storage locations.



Tool-Level Path Ownership (Tabs / Services)

Role



Each tab (tool/service) is responsible for defining how data is organized

under a given base directory.



This includes:



* subfolder creation



* run identifiers



* sharding / numbering



* caching strategies



* Characteristics



* Defined locally in the tab module



* Fully autonomous



* Easy to test and refactor



* Independent of other tools



Example Pattern



from utils.paths import PARTNER\_DATA\_DIR



TAB\_DATA\_DIR = PARTNER\_DATA\_DIR / "svc\_lifecycle"

TAB\_DATA\_DIR.mkdir(parents=True, exist\_ok=True)



RUNS\_DIR = TAB\_DATA\_DIR / "runs"

CACHE\_DIR = TAB\_DATA\_DIR / "cache"





Backwards (Bottom-Up) Path Construction



Paths are intentionally constructed backwards, starting from a stable

base directory and extending downward based on tool needs.



This approach ensures:



no assumptions at the platform level



maximum flexibility at the tool level



minimal coupling between tools



What NOT to Do



Do not define tool-specific paths inside utils/paths.py



Do not store filesystem paths inside UI or orchestration metadata



Do not share subpaths between tools unless explicitly required



Architectural Rule



utils/paths.py defines where data lives.

Each tab defines how its data is structured.



Benefits of This Approach



Clean separation of concerns



Easier testing (temporary directories per tool)



Safe evolution of storage strategies



No accidental coupling between services



Summary



This storage strategy prioritizes tool autonomy and platform stability.

It is a deliberate design choice aligned with the overall modular architecture

of the platform.

