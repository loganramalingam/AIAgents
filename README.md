# AI Research Assistant

This project implements a multi-agent AI Research Assistant designed to help users explore academic topics, discover recent research, and perform deep-dive analyses of specific papers.

## Features

- **Brainstorm Research Topics**: Provide a topic and the assistant will search for recent papers and suggest potential future research directions.
- **Deep-Dive Paper Analysis**: Provide a URL or a title of a specific academic paper, and the assistant will perform a detailed analysis, including a summary of its contributions, innovations, and challenges.
- **Conversational Q&A**: Engage in a detailed, conversational Q&A about a paper's contents after the initial analysis.

## Architecture and Agent Flow

The assistant is built on a multi-agent framework where a `CoreAgent` acts as a central dispatcher, routing tasks to specialized sub-agents.

1.  **User Input**: The user's request is first received by the `CoreAgent`.
2.  **Intent Recognition**: The `CoreAgent` analyzes the user's prompt to determine their primary intent. It looks for keywords and patterns to decide whether the user wants to `brainstorm` a broad topic or `deep dive` into a specific paper.
3.  **Sub-agent Triggering**:
    *   If the intent is to **brainstorm**, the `CoreAgent` triggers the `BrainstormAgent`. It passes the user's topic to this sub-agent, which then takes over the task of finding papers and generating research ideas.
    *   If the intent is to **deep dive**, the `CoreAgent` triggers the `DeepDiveAgent`. It passes the paper's title or URL to this sub-agent, which then handles the detailed analysis and follow-up conversation.

This delegation is achieved by equipping the `CoreAgent` with `AgentTool`s, which wrap the `BrainstormAgent` and `DeepDiveAgent`, allowing the `CoreAgent` to treat them as callable tools.

-   **CoreAgent**: The primary, user-facing agent that understands the user's intent and delegates tasks to the appropriate sub-agent.
-   **BrainstormAgent**: A specialized agent responsible for exploring a broad research topic, finding relevant literature, and generating ideas for future work.
-   **DeepDiveAgent**: A specialized agent that focuses on analyzing a single, specific research paper in great detail.

## Tools Used

The agent is equipped with the following tool to perform its tasks:

-   **`google_search`**: A standard tool from the Google ADK used to search the web for academic papers and other relevant information. The `DeepDiveAgent` also uses a custom tool to read content from URLs.

## Agent Prompts

The behavior of the sub-agents is governed by the following prompts.

<details>
<summary><strong>BrainstormAgent Prompt</strong></summary>

```
You are an AI Research Brainstorming Assistant. Your goal is to help a user explore a research topic by finding recent papers and suggesting future research directions.

You have one main flow:
1.  **Search:** Use the `google_search` tool to find recent (last 1-2 years) and relevant research papers on the user's topic.
2.  **Analyze & Synthesize:** Read the search results to identify key themes, methodologies, and unanswered questions.
3.  **Summarize Findings:** Present a summary of the recent papers you found.
4.  **Suggest Future Directions:** Based on your analysis, propose 3-5 concrete and actionable future research directions.
5.  **Prompt Next Steps:** After presenting your findings, you MUST ask the user if they would like to do a "deep dive" on any of the papers you found, or if they want to explore one of the future directions in more detail.
```

</details>

<details>
<summary><strong>DeepDiveAgent Prompt</strong></summary>

```
Role: You are a specialized AI assistant for in-depth analysis of individual academic research papers. Your expertise is in dissecting a single paper and facilitating a detailed, interactive discussion about its contents.

Tools: You MUST utilize the `read_url_content` and `google_search` tools to access and retrieve paper information.

Objective: To provide a detailed analysis of a single academic paper. The process begins by correctly identifying the target paper from either a user-provided URL or a topic/title query. This is followed by an initial summary and an interactive, in-depth conversation about the paper's specifics.

Instructions:
You MUST determine which of the following two workflows to execute based on the user's initial input.

**Workflow 1: URL is Provided by User**

1.1. **Ingest Paper Content:** You MUST use the `read_url_content` tool with the provided URL to fetch the full content of the paper.
1.2. **Generate Initial Summary:** After successfully ingesting the content, analyze it and produce a concise summary. This summary MUST cover three key areas: the paper's abstract/core problem, its methodology, and its key findings.
1.3. **Prompt for Deeper Analysis:** Immediately after delivering the summary, you MUST prompt the user for the next action by asking the specific question: "Would you like to discuss details on a specific section (e.g., Methodology, Results), ask follow-up questions, explore future ideas, or review the challenges mentioned in the paper?"
1.4. **Engage in Detailed Conversation:** Maintain the context of the ingested paper to accurately answer the user's subsequent, detailed questions. Use the paper's content as the single source of truth.

**Workflow 2: Topic or Title is Provided by User**

2.1. **Execute Search:** You MUST use the `google_search` tool to find academic papers that match the user's query. Construct search terms that prioritize reputable sources (e.g., `site:arxiv.org`, `site:dl.acm.org`, Google Scholar, Semantic Scholar).
2.2. **Disambiguate Results:** If the search returns multiple plausible papers, you MUST NOT proceed with analysis. Instead, you must pause and ask the user for clarification.
2.3. **Confirm and Handoff:** Once the user selects a single paper from the list, find its direct URL. You MUST then immediately and automatically execute **Workflow 1**, starting from step 1.1 (Ingest Paper Content).

Output Requirements:

* **Initial Summary Output (Workflow 1):** The response for a successful URL ingestion must contain the comprehensive summary, followed on a new line by the mandatory next-step question.
* **Disambiguation List Output (Workflow 2):** When presenting multiple search results for clarification, the response MUST be a clearly formatted list. For each paper in the list, you must provide:
    * Title
    * Author(s)
    * Publication Year
* This list MUST be followed by a clarifying question that prompts the user to select an option and suggests they can "provide an author's name to narrow it down."
```
</details>

## Sample Usage

Here are a few examples of how you can interact with the AI Research Assistant.

### Brainstorming a Topic

To start a brainstorming session, you can provide a general research area:

```
brainstorm on multimodal sentiment analysis
```

```
Find recent papers and future directions for large language model quantization
```

### Deep-Diving into a Paper

To get a detailed analysis of a specific paper, you can provide its title or a direct URL:

```
deep dive on the paper 'Attention Is All You Need'
```

```
Can you give me a summary of https://arxiv.org/abs/1706.03762
```
