from utils.logger import lookup_task, log_revision
from generate.revise_content import apply_feedback
from utils.llm_client import llm
import os

def process_revision_request(feedback_text: str) -> dict:
    """
    PDF Auto Feedback Implementation Steps 1-6
    """
    print("🔄 Starting revision workflow...")
    
    # Step 1-2: Parse feedback and extract task code
    task_code = extract_task_code(feedback_text)
    if not task_code:
        return {"error": "Task code not found in feedback"}
    
    print(f"🔍 Task code: {task_code}")
    
    # Step 3: Retrieve original content
    original_task = lookup_task(task_code)
    if not original_task:
        return {"error": f"Task {task_code} not found in logs"}
    
    print(f"📂 Original task found: {original_task['client_name']}")
    
    # Load original content
    original_file = os.path.join(original_task['file_path'], "content_draft.txt")
    if not os.path.exists(original_file):
        return {"error": f"Original content file not found: {original_file}"}
    
    with open(original_file, "r", encoding="utf-8") as f:
        original_content = f.read()
    
    # Step 4: Apply feedback using LLM
    print("✏️ Applying feedback...")
    revised_content = apply_feedback_with_llm(original_content, feedback_text, original_task)
    
    # Save revised content
    revised_file = os.path.join(original_task['file_path'], f"content_draft_revised_{task_code}.txt")
    with open(revised_file, "w", encoding="utf-8") as f:
        f.write(revised_content)
    
    print(f"💾 Revised content saved: {revised_file}")
    
    # Step 6: Update log
    log_revision(
        task_id=task_code,
        client_name=original_task['client_name'],
        content_type=original_task['content_type'],
        feedback_summary=feedback_text[:100]
    )
    
    # Step 5: Simulate delivery
    delivery_response = f"""
📧 REVISION DELIVERED:
To: Client Servicing Team  
Subject: REVISED: [{task_code}]

Your feedback has been applied to {original_task['client_name']} content.

Changes made:
- {feedback_text[:200]}...

Revised file: {revised_file}

Task ID: {task_code}
"""
    
    print(delivery_response)
    
    return {
        "success": True,
        "task_code": task_code,
        "client": original_task['client_name'],
        "revised_file": revised_file,
        "feedback_applied": feedback_text[:100]
    }

def extract_task_code(text: str) -> str:
    """Extract 6-character task code from feedback text"""
    import re
    # Look for 6-character alphanumeric codes
    matches = re.findall(r'\b[A-Z0-9]{6}\b', text.upper())
    return matches[0] if matches else None

def apply_feedback_with_llm(original_content: str, feedback: str, task_info: dict) -> str:
    """Use LLM to apply feedback while preserving brand voice"""
    
    system_prompt = f"""
You are revising content for {task_info['client_name']}. 
Apply the requested feedback while maintaining:
- Professional tone and brand voice
- Original structure and format
- Factual accuracy
- Compliance requirements

Make minimal changes - only what's specifically requested in the feedback.
"""
    
    revision_prompt = f"""
Original content:
{original_content}

Feedback to apply:
{feedback}

Please revise the content according to the feedback while preserving the professional tone and structure.
"""
    
    revised_content = llm.generate_content(revision_prompt, system_prompt)
    return revised_content

if __name__ == "__main__":
    sample_feedback = """
    Task: VNH01C  # ✅ Use real task ID
    Please shorten the introduction paragraph and add a quote from the CEO about customer security.
    """

    
    result = process_revision_request(sample_feedback)
    print(f"Revision result: {result}")
