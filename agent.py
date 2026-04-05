"""Main ADK multi-agent workflow for the hackathon project.

Pipeline:
User Input -> Idea Agent -> Copy Agent -> Planner Agent -> Save to SQLite
"""

from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.apps import App

from .sub_agents import MODEL, copy_agent, idea_agent, planner_agent
from .tools import save_campaign, get_campaigns_tool, save_brand_tool


save_and_format_agent = LlmAgent(
    name="SaveAndFormatAgent",
    model=MODEL,
    description="Saves campaign in DB and returns final structured response.",
    tools=[save_campaign],
    instruction=("""
        "You are the final response generator.\n\n"

        "You receive:\n"
        "- idea_result\n"
        "- copy_result\n"
        "- planner_result\n\n"

        "Your job:\n"
        "- Convert everything into a clean, human-friendly response.\n"
        "- DO NOT show JSON.\n"
        "- DO NOT repeat content.\n"
        "- Keep it crisp and readable.\n\n"

        ""First, call the save_campaign tool with these arguments:\n"
        "- product = idea_result['product']\n"
        "- idea = idea_result\n"
        "- copy = copy_result\n"
        "- plan = planner_result['plan']\n\n"

        "Then format the final response like this:\n\n"

        "🎯 Campaign Idea:\n"
        "{idea_result[concept]}\n\n"

        "👥 Target Audience:\n"
        "{idea_result[target_audience]}\n\n"

        "🔥 Hook:\n"
        "{idea_result[hook]}\n\n"

        "🧾 Ad Copy:\n"
        "Headline: {copy_result[headline]}\n"
        "Description: {copy_result[description]}\n"
        "CTA: {copy_result[cta]}\n\n"

        "📅 Posting Plan:\n"
        "Platforms: Convert planner_result[plan][platform] into a comma-separated string.\n"
        "Schedule:\n"
        "Convert planner_result[plan][schedule] into readable lines like:\n"
        "- Tuesday at 10:00 AM → Introduce campaign\n"
        "- Thursday at 2:00 PM → Engagement post\n\n"

        "Saved Campaign ID: {tool_response[campaign_id]}\n\n"

        "Only output this final response.\n"

        "Only output the final formatted response.\n"
        "Do NOT output JSON.\n"
        """
    ),
)

campaign_workflow = SequentialAgent(
    name="CampaignWorkflow",
    sub_agents=[idea_agent, copy_agent, planner_agent, save_and_format_agent]
)

root_agent = LlmAgent(
    name="CampaignAssistant",
    model=MODEL,
    instruction=(
        "You are a marketing assistant.\n\n"

        "If user is chatting normally (hi, hello, etc):\n"
        "- Reply naturally.\n\n"

        "If user provides brand details (brand name, tone, colors):\n"
        "- Extract brand name, tone, and colors from the message.\n"
        "- Call save_brand_tool(brand, tone, colors).\n"
        "- Do NOT respond without calling the tool.\n\n"

        "If user asks to create a campaign:\n"
        "- Immediately transfer to CampaignWorkflow.\n"
        "- Do NOT respond yourself.\n\n"

        "If user asks to see past campaigns:\n"
        "- Call get_campaigns_tool\n"
        "- Summarize results cleanly for user\n\n"

        "If user asks to improve a campaign:\n"
        "- Modify the last generated campaign and improve it.\n\n"
    ),
    tools=[save_brand_tool, get_campaigns_tool],
    sub_agents=[campaign_workflow]
)

# ADK CLI compatibility (recommended object name: app)
app = App(name="campaign_engine", root_agent=root_agent)
