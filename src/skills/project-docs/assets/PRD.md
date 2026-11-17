# Product Requirements Document

- **Status:** [Draft or ready for use; identify proposals and open decisions below]
- **Scope:** [Product, version, or project boundary]
- **Owner:** [Known accountable role, or decision needed]
- **Evidence:** [Links to approved requirements and relevant implemented behavior]

> Template examples describe a fictional personal task app, Taskboard. They demonstrate specificity; they are proposals, not facts or approved requirements for the selected repository. Replace them with the project's decisions. Use each **Minimum** note as an authoring checklist and remove it once covered.

## 01 Product Overview

- **Product name:** Taskboard (example)
- **Tagline:** Know what needs doing today.
- **Description:** A personal task list for people who want to capture and finish small commitments without managing a full project workspace. The first version works in one browser and saves tasks locally.

**Minimum:** name the product, its main user, and the value it provides in a short description.

## 02 Problem

**Example hypothesis:** freelancers track small tasks across notes and messages and lose sight of their next action. Validate this with the owner or user research before treating it as established evidence.

**Minimum:** describe one specific problem, identify who experiences it, and link supporting evidence or mark the assumption.

## 03 Goal

**Example proposed goal:** a first-time user can add and complete a task within 60 seconds of opening the app.

**Minimum:** define at least one measurable user outcome and its owner-approved target, or name the decision needed.

## 04 Target Users

| User | Need | Example context |
|---|---|---|
| Freelancer | Capture a small commitment quickly | Adds a task between client calls |
| Student | See and finish a short daily list | Checks tasks on a small-screen device |

**Minimum:** identify the primary user group, its need, and any access/platform constraints that change the product.

## 05 Core Features (Version 1)

| Feature | User outcome | State and evidence |
|---|---|---|
| Add task | Save a nonempty task title and see it in the list | Proposal in this fictional example |
| Complete task | Mark a task complete and undo that choice | Proposal in this fictional example |
| Retain tasks | See the same tasks after refreshing the browser | Proposal in this fictional example |

**Minimum:** connect each core feature to a user outcome and distinguish implemented, approved, proposed, and undecided scope with source evidence.

## 06 Out of Scope (for now)

**Example exclusions:**

- Team workspaces and shared lists.
- Cross-device synchronization and accounts.
- Recurring tasks, attachments, and chat.

**Minimum:** state the boundaries that could otherwise lead to unrequested work. Explain any dependency on a later version.

## 07 Success Metrics

| Metric | Target | Measurement and evidence |
|---|---|---|
| Time to first completed task | Proposed: 60 seconds or less | Observe a first-use task; owner must confirm the target |
| Independent first-use completion | Proposed: at least 9 of 10 trial users | A small moderated trial; record sample and limitations |

**Minimum:** give a target, measurement method, and decision/evidence source for each metric. Example targets are not measured results.

## 08 Key Journeys and Acceptance Criteria

| Journey / trigger | Observable acceptance criterion | Relevant edge or failure case |
|---|---|---|
| Open the app with no tasks | An empty-state message and Add task action are available | The action is reachable by keyboard |
| Enter a title and submit | Exactly one task appears and the entry field is ready for another task | Blank/whitespace titles show a linked validation message and add nothing |
| Toggle a task's completion | The task's state changes and can be reversed | State is conveyed through more than colour |
| Refresh after adding a task | Saved tasks and completion states are restored | Storage failure produces a useful message without claiming that saving succeeded |

**Minimum:** provide acceptance criteria for every core journey, including applicable empty, validation, failure, and accessibility behavior. These examples remain proposed until confirmed.

## 09 Constraints and Dependencies

**Example proposal:** single-user browser storage, no server account, and no sensitive-data use case in version one. The owner must confirm supported browsers, accessibility expectations, and data-loss/recovery expectations. Link the agreed technical choices to architecture and UI rules to the design system.

**Minimum:** record constraints that affect acceptance and link their owners; mark unconfirmed constraints as questions.

## 10 Open Decisions

| Question | Impact | Owner or next evidence |
|---|---|---|
| Should deleting a task be part of version one? | Adds a destructive action and recovery expectations | Product owner; confirm desired scope |
| What happens when local storage is unavailable? | Retention and user feedback | Product/engineering owner; choose supported fallback |

**Minimum:** resolve or explicitly retain material questions before describing the document as ready for use. State "None" when no questions remain.
