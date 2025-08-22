PR Content Automation System

An end-to-end automation framework that transforms client briefs (via Email or WhatsApp) into professional, brand-aligned PR content using AI and workflow automation.

🚀 Project Overview

This repository provides the source code and configuration for a scalable PR content automation system, combining:

n8n
: Workflow automation to handle triggers, routing, and integrations

FastAPI
: Backend service for AI-powered content generation

Groq AI: High-performance LLM integration for high-quality writing

Ngrok: Secure tunneling for local development and external access

✨ Features

📩 Multi-channel input (Email + WhatsApp)

📝 Brand voice & style integration via JSON schema

⚡ AI-powered content drafting using Groq

🆔 Automatic task IDs & metadata logging

🔄 Revision workflow for client feedback loops

📂 Organized outputs in structured folders

📂 Repository Structure
File / Folder	Purpose
.env	Stores environment variables (API keys, configs)
api_server.py	FastAPI backend service
brand_voice_schema.json	Defines brand voice/style rules
__init__.py	Package initializer
main_workflow.py	Core automation logic
ngrok.yml	Ngrok tunneling config
requirements.txt	Python dependencies
revision_workflow.py	Feedback & revision handling
test_groq.py	Test script for Groq AI API
⚙️ Setup & Installation

Clone the repository

git clone https://github.com/harjin2005/PR-Content-Creation-with-Automation-AI.git
cd PR-Content-Creation-with-Automation-AI


Create a .env file
Add your API keys and configuration variables (Groq, Ngrok, etc.).

Install dependencies

pip install -r requirements.txt


Start the FastAPI server

python api_server.py


Launch n8n workflows (separate install)

Import the saved workflow JSON (if provided)

Enable webhooks and test triggers

Run Ngrok for local tunneling

ngrok start --config ngrok.yml --all

▶️ Usage

Trigger automation via POST requests to the webhook URL.

Generated PR content will be saved in the outputs/ folder.

For revisions, run the revision workflow to process client feedback.

📜 License

This project is licensed under the MIT License
.

📬 Contact

For demo requests, collaboration, or queries:
📧 harjins2005@gmail.com
