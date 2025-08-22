import os
import sys
import json
from datetime import datetime

# Fix Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from ingestion.parse_email import parse_email
from ingestion.parse_voice import parse_voice
from classify.content_type_classifier import classify_content_type
from generate.internal_brief import generate_internal_brief
from generate.draft_content import draft_content
from utils.task_id import generate_task_id, generate_folder_path
from utils.logger import log_content_request
from transport.email_stub import send_email_response
from transport.whatsapp_stub import send_whatsapp_response

def process_content_request(input_text: str, input_type: str = "email") -> dict:
    """
    Main workflow following PDF Steps 1-8
    """
    print(f"🚀 Starting content automation workflow...")
    print(f"📥 Input type: {input_type}")
    
    # Step 1-2: Parse input
    if input_type == "email":
        parsed_data = parse_email(input_text)
    elif input_type == "whatsapp":
        parsed_data = parse_voice(input_text)
    else:
        raise ValueError("Input type must be 'email' or 'whatsapp'")
    
    print(f"📋 Parsed data: {json.dumps(parsed_data, indent=2)}")
    
    # Step 3: Classify content type if needed
    if not parsed_data.get("content_type"):
        parsed_data["content_type"] = classify_content_type(parsed_data)
    
    client_name = parsed_data.get("client", "Unknown")
    print(f"🏢 Client: {client_name}")
    print(f"📄 Content Type: {parsed_data.get('content_type')}")
    
    # Step 4: Context already loaded in generate functions
    
    # Step 5: Generate internal brief
    print("📝 Generating internal brief...")
    internal_brief = generate_internal_brief(parsed_data, client_name)
    
    # Step 6: Draft final content
    print("✍️ Generating content draft...")
    content_draft = draft_content(parsed_data, client_name)
    
    # Step 6.5: Generate task ID
    task_id = generate_task_id()
    print(f"🔢 Task ID: {task_id}")
    
    # Step 7: Bundle outputs
    output_folder = generate_folder_path(client_name, task_id)
    os.makedirs(output_folder, exist_ok=True)
    
    # Save files
    brief_file = os.path.join(output_folder, "internal_brief.txt")
    draft_file = os.path.join(output_folder, "content_draft.txt")
    original_file = os.path.join(output_folder, "original_brief.txt")
    
    with open(brief_file, "w", encoding="utf-8") as f:
        f.write(internal_brief)
    
    with open(draft_file, "w", encoding="utf-8") as f:
        f.write(content_draft)
    
    with open(original_file, "w", encoding="utf-8") as f:
        f.write(f"Original Input:\n{input_text}\n\nParsed Data:\n{json.dumps(parsed_data, indent=2)}")
    
    print(f"💾 Files saved to: {output_folder}")
    
    # Step 6.6: Log to CSV
    log_content_request(
        task_id=task_id,
        client_name=client_name,
        content_type=parsed_data.get("content_type"),
        topic=parsed_data.get("topic", ""),
        trigger_source=parsed_data.get("trigger_source"),
        file_path=output_folder
    )
    
    # Step 8: Send responses (simulated)
    email_response = send_email_response(task_id, client_name, output_folder)
    whatsapp_response = send_whatsapp_response(task_id, client_name, output_folder)
    
    # Return result summary
    result = {
        "task_id": task_id,
        "client": client_name,
        "content_type": parsed_data.get("content_type"),
        "topic": parsed_data.get("topic"),
        "output_folder": output_folder,
        "files": {
            "internal_brief": brief_file,
            "content_draft": draft_file,
            "original_brief": original_file
        },
        "email_sent": email_response,
        "whatsapp_sent": whatsapp_response
    }
    
    print("✅ Workflow completed successfully!")
    return result

if __name__ == "__main__":
    # Test with sample email
    sample_email = """
    Client: AcmeCo
    Content Type: Press Release
    Topic: Partnership announcement with FinTrust for secure payment processing platform
    Notes: Highlight compliance benefits, security features, and customer trust aspects
    """
    
    print("Testing Email Input:")
    print("=" * 50)
    result = process_content_request(sample_email, "email")
    print(f"\n📊 Result: {json.dumps(result, indent=2)}")
    
    print("\n" + "=" * 50)
    
    # Test with WhatsApp transcript
    sample_whatsapp = "Hey, need a press release for AcmeCo about their new partnership with FinTrust for secure payments. Make sure to include compliance angle and security benefits."
    
    print("Testing WhatsApp Input:")
    print("=" * 50)
    result2 = process_content_request(sample_whatsapp, "whatsapp")
    print(f"\n📊 Result: {json.dumps(result2, indent=2)}")
