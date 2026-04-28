# Scripture Insight MCP Server

📖 **A modular MCP server that lets LLMs explore, analyze, and reason over the Bible—combining text retrieval, theology, language analysis, and historical context.**

Think of it as a developer-friendly “Bible intelligence layer” that an AI agent can call into.

## 🧠 Core Concept

The server exposes tools that allow an LLM to:
- **Search scripture:** Find verses based on natural language or keywords.
- **Cross-reference verses:** Discover thematic or contextual links between passages.
- **Analyze themes:** Explore theological concepts like Grace, Salvation, or Covenants.
- **Understand original languages:** Look up Hebrew/Greek words, Strong's numbers, and transliterations.
- **Generate structured theological insights:** Create deep, interpretative reasoning across multiple viewpoints.

## 🛠️ The 10 MCP Tools

### 1. `search_verse`
**Purpose:** Find Bible verses by keyword or phrase.
* **Input:** `{ query: string, translation?: string }`
* **Output:** Matching verses with references.
* *Example:* "faith without works" → James 2:17

### 2. `get_verse`
**Purpose:** Retrieve a specific verse.
* **Input:** `{ book: string, chapter: number, verse: number }`
* **Output:** Exact verse text.

### 3. `get_passage`
**Purpose:** Retrieve a range of verses.
* **Input:** `{ book: string, chapter: number, startVerse: number, endVerse: number }`

### 4. `cross_reference`
**Purpose:** Show related verses.
* **Input:** `{ reference: string }`
* **Output:** Linked verses (based on themes, citations, or study Bible data).
* *Example:* John 3:16 → Romans 5:8, 1 John 4:9

### 5. `topic_lookup`
**Purpose:** Find verses by theological topic.
* **Input:** `{ topic: string }`
* *Examples:* Grace, Salvation, Faith, Covenant

### 6. `original_language_lookup`
**Purpose:** Analyze Hebrew/Greek words.
* **Input:** `{ reference: string, word?: string }`
* **Output:** Original word, Transliteration, Meaning, Strong’s number.

### 7. `character_profile`
**Purpose:** Get structured info about a biblical character.
* **Input:** `{ name: string }`
* **Output:** Key events, Associated verses, Relationships, Timeline summary.
* *Examples:* Moses, David, Paul

### 8. `timeline_event_lookup`
**Purpose:** Place events in the biblical timeline.
* **Input:** `{ event: string }`
* **Output:** Approximate date, Related scriptures, Historical context.

### 9. `summarize_passage`
**Purpose:** Summarize scripture with context.
* **Input:** `{ reference: string, style?: "short" | "detailed" | "devotional" }`

### 10. `theological_analysis`
**Purpose:** Deep reasoning tool (the “AI-heavy” feature).
* **Input:** `{ "reference": "string", "question": "string" }`
* **Output:** Interpretation, Doctrinal themes, Supporting verses, Multiple viewpoints (optional: denominational).
