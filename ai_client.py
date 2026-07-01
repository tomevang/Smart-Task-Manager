import anthropic
import json


def get_ai_suggestion(tasks):
    # Build task list string
    task_lines = []
    for task_id, description in tasks.items():
        task_lines.append(f"{task_id}: {description}")
    task_list_string = "\n".join(task_lines)

    # Build full prompt
    prompt = f"""
    You are a task prioritization assistant. Given the following tasks,
    suggest the optimal order to complete them. Return ONLY a JSON array
    of task IDs in priority order. No explanation, just the JSON array.

    Tasks:
    {task_list_string}

    Example response: [1, 2, 3]
    """

    # Automatically use the Anthropic API KEY env variable
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
            ]
    )

    response_text = message.content[0].text

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return []  # return empty list if parsing fails