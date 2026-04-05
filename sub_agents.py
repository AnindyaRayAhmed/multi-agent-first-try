"""Sub-agent definitions for the campaign pipeline."""

from google.adk.agents.llm_agent import LlmAgent
from .tools import get_brand_tool

MODEL = "gemini-2.5-flash"

idea_agent = LlmAgent(
    name="IdeaAgent",
    model=MODEL,
    description="Generates campaign concept, audience, and hook.",
    instruction=(
        "You are the Idea Agent for a marketing team. "
        "If brand is mentioned:\n"
        "- Extract brand name from user input.\n"
        "- Call get_brand_tool(brand).\n"
        "Use returned tone and colors in your idea.\n"
        "The user message will look like: 'Create a campaign for [product]'.\n"
        "Extract product name and create a simple, creative campaign concept including an emotional hook and the main problem it solves.\n"
        "Return ONLY valid JSON with this exact schema: "
        '{"product":"...","concept":"...","target_audience":"...","hook":"..."}' 
        "Return ONLY JSON. Do NOT explain. Do NOT repeat. Do NOT introduce yourself.\n"
        "If previous campaigns exist, avoid repeating ideas.\n"
        "Do NOT output anything except the JSON.\n"
        "Do NOT explain.\n"
        "Do NOT repeat.\n"
        "Your output will be passed to next agent. Do NOT speak to user.\n"
        "This output is for internal use only.\n"
    ),
    tools=[get_brand_tool],
    output_key="idea_result",
    
)

copy_agent = LlmAgent(
    name="CopyAgent",
    model=MODEL,
    description="Creates ad headline, description, and CTA.",
    instruction=(
        "You are the Copy Agent. Use the campaign idea below to generate ad copy.\n"
        "Idea JSON:\n{idea_result}\n"
        "Return ONLY valid JSON with this exact schema: "
        '{"headline":"...","description":"...","cta":"..."}' 
        "Return ONLY JSON. Do NOT explain. Do NOT repeat. Do NOT introduce yourself."
        "Do NOT output anything except the JSON.\n"
        "Do NOT explain.\n"
        "Do NOT repeat.\n"
        "Your output will be passed to next agent. Do NOT speak to user.\n"
        "This output is for internal use only.\n"
    ),
    output_key="copy_result",
   
)

planner_agent = LlmAgent(
    name="PlannerAgent",
    model=MODEL,
    description="Builds posting platform + schedule and final structured output.",
    instruction=(
        "You are the Planner Agent. Use idea and copy to create a simple posting plan.\n"
        "Idea JSON:\n{idea_result}\n"
        "Copy JSON:\n{copy_result}\n"
        "Return ONLY valid JSON with this structure:\n"
        '{"plan":{"platform":"<platform>","schedule":"<schedule>"}}'
        "Return ONLY JSON. Do NOT explain. Do NOT repeat. Do NOT introduce yourself.\n"
        "If schedule is created, optionally call schedule_campaign_tool(product, schedule).\n"
        "Do NOT output anything except the JSON.\n"
        "Do NOT explain.\n"
        "Do NOT repeat.\n"
        "Your output will be passed to next agent. Do NOT speak to user.\n"
        "This output is for internal use only.\n"
    ),
    output_key="planner_result",
    
)
