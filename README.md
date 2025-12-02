# Agent-Exam-Cram-The-Active-Recall-Tutor
An interactive multi-agent tutor that uses active recall, fact-verification tools, and automated grading to help you master any subject.

# Agent Exam Cram: The Active Recall Tutor
**Track:** Agents for Good (Education)

## Problem Statement
Students, especially undergraduates often struggle with "passive review" reading notes without retaining information. Effective studying requires "active recall," but finding a study partner to quiz you at midnight during exam season is impossible. Manual flashcards are static and cannot explain *why* an answer is wrong.

## Solution Statement
"Agent Exam Cram" is an intelligent study companion available 24/7. Unlike a standard chatbot, it is a **Multi-Agent System** that acts as both a Tutor and an Evaluator. It uses tool-calling to reference "ground truth" definitions (simulating a textbook lookup) to ensure it grades student answers based on facts, not hallucinations.

## Architecture
This project utilizes a **Multi-Agent Architecture** powered by **Google Gemini 2.5 Flash**.

* **Agent 1: The Tutor (Active)**
    * **Role:** Conducts the interactive quiz loop.
    * **Tools:**
        * `lookup_textbook`: Verifies answers against ground truth (Hallucination prevention).
        * `give_hint`: Provides scaffolding when a student is stuck.
    * **Memory:** Maintains active session context to track the conversation flow.

* **Agent 2: The Evaluator (Passive)**
    * **Role:** Analyzes the full conversation transcript after the session ends.
    * **Task:** Generates a structured "Report Card" with a letter grade and study recommendations.
    * **Concept:** Implements the "Agent-as-a-Judge" pattern to evaluate student performance.

## Value Statement
This agent reduces the cognitive load of planning a study session. By automating the "quizzing" process and providing a final summary grade, it allows students to focus entirely on recall and understanding.
