CODEBOOK_MIN = {
    1: {"name": "Triggering", "definition": "Problem, question, confusion, or new issue is stated."},
    2: {"name": "Exploration", "definition": "Information seeking, brainstorming, tentative ideas, clarification."},
    3: {"name": "Integration", "definition": "Connecting ideas, synthesizing, forming a coherent explanation/plan."},
    4: {"name": "Resolution", "definition": "Applying or confirming a solution, presenting final answer or evaluation."}
}

# Extended lexical cues (optional for heuristic inspection)
CODEBOOK_EXT = {
    1: ["i am stuck", "how do i", "error occurs", "cannot figure"],
    2: ["maybe", "what if", "could we", "let us try", "i will check"],
    3: ["this means", "therefore", "so the idea", "combining these", "in summary"],
    4: ["it works now", "final answer", "solution is", "we fixed", "resolved", "all tests pass"]
}

ONE_SHOT_PROMPT = """You are an expert educational analyst. Classify ONE chat message into exactly one Cognitive Presence stage.
Stages:
1 Triggering: Problem/question/confusion is introduced.
2 Exploration: Searching, brainstorming, gathering info, tentative ideas.
3 Integration: Synthesizing ideas, forming explanations, connecting concepts.
4 Resolution: Applying solution, confirming it works, final answer / evaluation.

Return JSON ONLY: {{"stage": <1-4>, "label": "<name>", "confidence": <0-100>, "rationale": "<brief why>"}}.

Examples:
Message: "I'm stuck, my loop never terminates." -> {{"stage":1,"label":"Triggering","confidence":88,"rationale":"States problem"}}
Message: "Maybe the index isn't incrementing; could you print it?" -> {{"stage":2,"label":"Exploration","confidence":83,"rationale":"Suggests exploratory action"}}
Message: "So the issue was the off-by-one; adjusting the bound aligns both arrays." -> {{"stage":3,"label":"Integration","confidence":86,"rationale":"Synthesizes cause and fix"}}
Message: "Tested again; outputs now match expected results." -> {{"stage":4,"label":"Resolution","confidence":90,"rationale":"Confirms successful application"}}

Now classify the next message.
Message: \"\"\"{text}\"\"\"""" 