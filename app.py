import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, tool
from langchain_groq import ChatGroq
from utils import convert_raw_json_to_csv

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')

search_tool = SerperDevTool(n_results=10)

researcher = Agent(
    role = "Senior researcher",
    goal = "Gather information on top 100 tools used in scientific research.",
    backstory = """Skilled in finding and analyzing data, with a focus on scientific research
      tools.""",
    verbose = False,
    allow_delegation = False,
    tools = [search_tool],
    llm = ChatGroq(model_name="llama-3.1-70b-versatile", temperature=0.7)
)
exporter = Agent(
    role = "data exporter",
    goal = "clean and export the data to a json file.",
    backstory = """you are expert in data analysis, with a focus on processing and structuring
      data for further use.""",
    verbose = True,
    allow_delegation = True,
    llm = ChatGroq(model_name="llama-3.1-70b-versatile", temperature=0.7)
)

task1 = Task(
    description = "Use available tools to gather information on top 100 tools used in scientific research. Search websites, directories. it's okay if one source has a list of tools use the list but make sure to complete 100 tool",
    expected_output = "A list of top 100 tools used in scientific research, including tool names, descriptions, functionalities out put should be json.",
    agent = researcher
)

task2 = Task(
    description = "Take the list of top 100 tools used in scientific research and process it into a structured format and output a json file",
    expected_output = "A formatted json containing tool names, descriptions,  functionalities, price, link, ready for further analysis.",
    agent = exporter,
    context =[task1]
)

crew = Crew(
    agents = [researcher, exporter],
    tasks = [task1, task2],
    verbose = 1
)

final = crew.kickoff()

convert_raw_json_to_csv(final.raw)