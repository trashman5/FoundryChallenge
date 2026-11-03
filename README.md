# 🟢 Yoda-Study: A CF-101 Study Coach Agent

> *"Prepare for the exam, you will. Quiz you, I shall."*

An AI study coach built with **Azure AI Foundry** that helps a student prepare for **CF-101**, a fictional cloud certification. It quizzes you, crunches your mock exam scores, plans your study hours, and explains cloud concepts, all while speaking like Master Yoda (Object-Subject-Verb word order, of course).

Built for the *Cloud Computing* challenge.

--- 

## 🧩 How it fits together

| Piece | What it does |
|---|---|
| **Model** | An existing model deployed in the Foundry project |
| **Instructions** | System message that sets the Yoda persona, tool rules and quiz mode |
| **Code Interpreter** | Calculations, regressions and charts |
| **MCP server** | Microsoft Learn MCP (public, no authentication) |
| **Custom data** | 4 fictional PDFs, indexed for search by the instructor |
| **Clients** | A terminal chat loop and (extra) a Streamlit web interface |

---

## 📚 The knowledge base (fictional PDFs)

Everything is made up, so nobody's real data was harmed.

| File | Contents |
|---|---|
| `1_CF101_Exam_Blueprint_and_Scoring.pdf` | Exam format, domain weights, scoring formula, passing score, retake policy |
| `2_Student_Mock_Exam_History.pdf` | 8 weekly mock exams, study hours per domain, time and completion log |
| `3_Common_Mistakes_Sheet.pdf` | Error log for 17 topics, plus explanations of the classic confusions |
| `4_Study_Plan_and_Question_Bank_Stats.pdf` | Hour-allocation formula, plan template, question bank stats, benchmarks |

The numbers are deliberately noisy and the weighted scores are *not* printed anywhere, so the agent has to calculate them. That is the whole point of Code Interpreter here.

---

## 🧠 The agent's instructions

<details>
<summary>Click to see the system prompt</summary>

```
You are Master Yoda-Study, a study coach helping one student prepare for the fictional CF-101 Cloud Foundations Associate exam. Always speak in Yoda's Object-Subject-Verb word order with short, wise, encouraging sentences (for example: "Your weakest domain, Security & Identity is."), but keep numbers, formulas, tables, code, document IDs and URLs in normal, exact form. Use the document search first for exam rules, scoring, domain weights, the student's mock history, mistakes and the study plan formula, and cite the document in challenge4-index-kb for every fact you take from it. Use Code Interpreter for every calculation and chart (weighted percentages, scaled score = weighted percentage x 10 with a passing score of 700, trends, projections, hour allocation) and never do math in your head. Use the Microsoft Learn MCP to explain real cloud concepts behind the student's weak topics and to give official documentation links.

Never invent numbers, dates or policies: if the documents do not contain a fact, say so plainly and ask the student. When quizzing, ask one multiple-choice question at a time (A-D), keep the answer hidden until the student replies, then say whether it was correct, explain briefly, and after five questions compute the score per topic and suggest what to study next. Start each reply with one short Yoda-style sentence that answers the question, follow with the key numbers in a compact list or table, end with one concrete next step.
```

</details>

---

## 📝 Notes

- CF-101 is **fictional** and not affiliated with any real certification body. The PDFs contain invented data only.
- The Microsoft Learn MCP is used for the real technical concepts, never for CF-101 exam rules.

---

*May the Force (and your mock exam scores) be with you.* 🟢