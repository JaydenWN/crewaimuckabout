import os
os.environ["OPENAI_API_KEY"] = 
os.environ["SERPER_API_KEY"] = 

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

# The team
bossman = Agent (
    backstory=('Oversees content strategy, quality control, and editorial guidelines. Manages a team of writers, editors, and contributors. Ensures that content aligns with the companys brand and objectives.'),
    goal='Manage the team to provide a project owner quality blog posts',
    role='Content Director',
    verbose=True,
    allow_delegation=True,
    memory=True
)

cheifEditor = Agent (
    backstory=('Drafts a layout for blog posts, asks seo specialist for input on how to form a seo friendly blog article'),
    goal='Creates an seo friendly layout for content creators to follow',
    role='Chief Editor',
    verbose=True,
    memory=True,
    allow_delegation=True
)

researchSpecialist = Agent (
    backstory =('Researches and sources relevant material that could help with forming an SEO friendly blog article'),
    goal='Finds relevant information and links to boost SEO rankings',
    role='Researcher',
    verbose=True,
    tools=[search_tool],
    memory=True
)

legalGuy = Agent (
    backstory=('Researches and provides legal and compliancy information related to the blog article that is being developed'),
    goal='Ensures correct legal information is present in any article written',
    role='Legal Compliancy Officer / Researcher',
    verbose = True,
    tools=[search_tool],
    memory=True
    
)

SEOguy = Agent(
    backstory = ('Optimizes content for search engines to improve visibility and organic traffic. Conducts keyword research, provides on-page SEO strategies.'),
    goal='Provides SEO tips to the team to ensure any blog article drives traffic from seo',
    role='Seo specialist',
    verbose = True,
    memory=True,
    tools=[search_tool]
)

copywriter = Agent(
    backstory=('Collects a outline of how a blog post is to be structured, then using research provided from a researcher and research from a legal researcher and seo specialist.'),
    goal=('Writes the copy for a provide blog outline, then hands work to be formatted in html'),
    role='Content Creator',
    verbose=True,
    memory=True,
)

htmlGuy = Agent(
    backstory =('Develops HTML code for blog articles with SEO as a number one priority'),
    goal='Writes seo-friendly html to display pre-written blogs',
    role="SEO Specialist",
    verbose=True,
    memory=True
)


## tasks
blogPost = Task(
    description=('Create a 1000 word blog post written in HTML for the company Mid Coast Saftey Rail. Mid Coast Saftey Rail is located on the mid north coast nsw and rents scaffolding equipment to business.'),
    expected_output='A 1000-2000 word blog article written in seo-friendly html',
    agent= bossman,
    output_file='output.txt'
)

crew = Crew(
    agents=[bossman, researchSpecialist, legalGuy, SEOguy, cheifEditor, copywriter, htmlGuy],
    tasks=[blogPost],
    process= Process.sequential
)
result = crew.kickoff()
