# LLM Prompt: Generate System Design Interview Framework

## Role
You are an expert system design interviewer and coach with 15+ years of experience evaluating senior staff engineers at top tech companies. You excel at creating structured, time-efficient frameworks that help candidates succeed in system design interviews.

## Interview Context
- **Time Limit**: 60 minutes total
- **Environment**: Virtual whiteboard (e.g., Excalidraw, Miro, or similar)
- **Success Criteria**: 
  - Demonstrate strong technical architecture skills
  - Show clear communication and structured thinking
  - Cover breadth and appropriate depth
  - Handle trade-offs and scaling considerations
  - Leave time for follow-up questions (critical for passing)
  - Receive "Strong Hire" or "Hire" feedback

## Your Task
Generate a **reusable, time-boxed framework** for system design interviews that:
1. Provides a minute-by-minute breakdown of how to use the 60 minutes
2. Works as a template with generic placeholders that can be filled for ANY system design problem
3. Emphasizes time management and pacing to avoid running out of time
4. Balances what to draw (diagrams) vs. what to write (text explanations)
5. Maximizes chances of passing the interview

## Output Requirements

### Structure Your Framework With These Sections:

**1. Time Allocation Template** (5-7 time blocks)
- Break down the 60 minutes into phases
- Specify minutes and purpose for each phase
- Include buffer time for follow-ups

**2. Phase-by-Phase Guide**
For each time block, provide:
- **Objective**: What to accomplish
- **Actions**: Specific steps to take
- **Visual Guidelines**: What to draw on the whiteboard
- **Written Guidelines**: What text/notes to add
- **Communication Tips**: What to say to the interviewer
- **Common Pitfalls**: What to avoid

**Example of what ONE phase should look like:**

```
Phase 1: Requirements Gathering (0-5 minutes)

Objective: Clarify functional and non-functional requirements

Actions:
1. Ask about users: "Who are the primary users of [SYSTEM_NAME]?"
2. Ask about scale: "What's the expected QPS/DAU/data volume?"
3. Confirm core features: "Should we prioritize X over Y?"
4. List assumptions: "I'll assume Z unless you'd like different"

Visual Guidelines:
- Draw a simple box in top-left corner labeled "Requirements"
- List 3-5 functional requirements with checkmarks
- List 2-3 non-functional requirements (scale, latency, availability)

Written Guidelines:
- Write: "100M DAU", "1M QPS", "99.9% availability"
- Use abbreviations to save time and space

Communication Tips:
- Start with: "Let me clarify a few things before jumping into design..."
- Show you're thinking about trade-offs: "High consistency or high availability?"

Common Pitfalls:
- ❌ Don't spend more than 5 minutes here
- ❌ Don't design while gathering requirements
- ❌ Don't ask obvious questions the interviewer already stated
```

**3. Template Placeholders**
Include generic placeholders like:
- `[SYSTEM_NAME]`
- `[KEY_REQUIREMENTS]`
- `[SCALE_PARAMETERS]`
- `[MAIN_COMPONENTS]`
- etc.

**4. Worked Example**
Apply your framework to this specific problem:
> **Design a metrics collection system that includes ingestion, storage, and querying capabilities.**

Show how each phase of your framework would be executed for this metrics system.

## Constraints
- **Concise and Actionable**: Each recommendation should be specific and immediately applicable
- **Simplicity First**: Prioritize simple, clear designs over over-engineering
- **Time-Aware**: Always consider time remaining; include "if time allows" suggestions
- **Generic Coverage**: Must handle common patterns (APIs, databases, caching, queuing, scaling)
- **Interview-Tested**: Based on real interview expectations, not theoretical ideals
- **Follow-up Ready**: Must finish core design with 10-15 minutes remaining for deep-dives

## Success Metrics for Your Framework
A candidate using your framework should:
- Never run out of time during the interview
- Cover all critical system design areas
- Produce clear, professional diagrams
- Demonstrate senior-level thinking
- Confidently handle follow-up questions
- Receive positive feedback from interviewers

## Additional Guidance
- Assume the candidate has strong technical skills but needs structure
- Focus on **time management** as the primary optimization
- Recommend specific visual elements (boxes, arrows, labels, etc.)
- Suggest when to go deep vs. stay high-level
- Include checkpoints to gauge if the candidate is on track

---

**Now generate the comprehensive system design interview framework following all requirements above.**
