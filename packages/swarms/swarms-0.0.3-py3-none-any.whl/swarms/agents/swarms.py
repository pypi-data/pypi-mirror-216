
from swarms.agents.workers.auto_agent import AutoGPT
from collections import deque
from typing import Dict, Any


import os
from collections import deque
from typing import Dict, List, Optional, Any

from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import BaseLLM
from langchain.vectorstores.base import VectorStore
from pydantic import BaseModel, Field
from langchain.chains.base import Chain
from langchain.experimental import BabyAGI

from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore

from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain import OpenAI, SerpAPIWrapper, LLMChain


from swarms.agents.workers.auto_agent import agent
worker_agent  = agent

# Define your embedding model
embeddings_model = OpenAIEmbeddings()
# Initialize the vectorstore as empty
import faiss

embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})






#-------------------------------------------------------------------------- WORKER NODE
import pandas as pd
from langchain.experimental.autonomous_agents.autogpt.agent import AutoGPT
from langchain.chat_models import ChatOpenAI

from langchain.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain.docstore.document import Document
import asyncio

import nest_asyncio

# Tools
import os
from contextlib import contextmanager
from typing import Optional

from langchain.tools.file_management.read import ReadFileTool
from langchain.tools.file_management.write import WriteFileTool
ROOT_DIR = "./data/"

from langchain.tools import BaseTool, DuckDuckGoSearchRun
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain, BaseCombineDocumentsChain

from langchain.tools.human.tool import HumanInputRun
from swarms.agents.workers.auto_agent import MultiModalVisualAgent
from swarms.tools.main import Terminal, CodeWriter, CodeEditor, process_csv, WebpageQATool

class MultiModalVisualAgentTool(BaseTool):
    name = "multi_visual_agent"
    description = "Multi-Modal Visual agent tool"

    def __init__(self, agent: MultiModalVisualAgent):
        self.agent = agent
    
    def _run(self, text: str) -> str:
        #run the multi-modal visual agent with the give task
        return self.agent.run_text(text)






llm = ChatOpenAI(model_name="gpt-4", temperature=1.0, openai_api_key="")



####################################################################### => Worker Node
####################################################################### => Worker Node
####################################################################### => Worker Node


class WorkerNode:
    def __init__(self, llm, tools, vectorstore):
        self.llm = llm
        self.tools = tools
        self.vectorstore = vectorstore

    def create_agent(self, ai_name, ai_role, human_in_the_loop, search_kwargs):


        embeddings_model = OpenAIEmbeddings(openai_api_key="")
        embedding_size = 1536
        index = faiss.IndexFlatL2(embedding_size)
        vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})




        query_website_tool = WebpageQATool(qa_chain=load_qa_with_sources_chain(llm))

        # !pip install duckduckgo_search
        web_search = DuckDuckGoSearchRun()

        #
        multimodal_agent_tool = MultiModalVisualAgentTool(MultiModalVisualAgent)

        tools = [
            
            web_search,
            WriteFileTool(root_dir="./data"),
            ReadFileTool(root_dir="./data"),
            
            process_csv,
            multimodal_agent_tool,
            query_website_tool,

            Terminal,
            CodeWriter,
            CodeEditor
            
            # HumanInputRun(), # Activate if you want the permit asking for help from the human
        ]

        # Instantiate the agent
        self.agent = AutoGPT.from_llm_and_tools(
            ai_name=ai_name,
            ai_role=ai_role,
            tools=tools,
            llm=self.llm,
            memory=self.vectorstore.as_retriever(search_kwargs=search_kwargs),
            human_in_the_loop=human_in_the_loop,
        )
        self.agent.chain.verbose = True

    def run_agent(self, prompt):
        # Run the agent with the given prompt
        self.agent.run([prompt])







####################################################################### => Boss Node
####################################################################### => Boss Node
####################################################################### => Boss Node

class BossNode:
    def __init__(self, llm, vectorstore, task_execution_chain, verbose, max_iterations):

        todo_prompt = PromptTemplate.from_template(
            "You are a planner who is an expert at coming up with a todo list for a given objective. Come up with a todo list for this objective: {objective}"""
        )
        todo_chain = LLMChain(llm=OpenAI(temperature=0), prompt=todo_prompt)
        search = SerpAPIWrapper()
        tools = [
            Tool(
                name="Search",
                func=search.run,
                description="useful for when you need to answer questions about current events",
            ),
            Tool(
                name="TODO",
                func=todo_chain.run,
                description="useful for when you need to come up with todo lists. Input: an objective to create a todo list for. Output: a todo list for that objective. Please be very clear what the objective is!",
            ),
            Tool(
                name="AUTONOMOUS Worker AGENT",
                func=worker_agent.run,
                description="Useful for when you need to spawn an autonomous agent instance as a worker to accomplish complex tasks, it can search the internet or spawn child multi-modality models to process and generate images and text or audio and so on"
            )
        ]



        suffix = """Question: {task}
        {agent_scratchpad}"""
        prompt = ZeroShotAgent.create_prompt(
            tools,
            prefix=prefix,
            suffix=suffix,
            input_variables=["objective", "task", "context", "agent_scratchpad"],
        )

        llm = OpenAI(temperature=0)
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        tool_names = [tool.name for tool in tools]

        agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)
        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent, tools=tools, verbose=True
        )
        self.baby_agi = BabyAGI.from_llm(
            llm=llm,
            vectorstore=vectorstore,
            task_execution_chain=agent_executor
        )

    def create_task(self, objective):
        return {"objective": objective}

    def execute_task(self, task):
        self.baby_agi(task)





class Swarms:
    def __init__(self, num_nodes: int, llm: BaseLLM, self_scaling: bool): 
        self.nodes = [WorkerNode(llm) for _ in range(num_nodes)]
        self.self_scaling = self_scaling
    
    def add_worker(self, llm: BaseLLM):
        self.nodes.append(WorkerNode(llm))

    def remove_workers(self, index: int):
        self.nodes.pop(index)

    def execute(self, task):
        #placeholer for main execution logic
        pass

    def scale(self):
        #placeholder for self scaling logic
        pass



#special classes

class HierarchicalSwarms(Swarms):
    def execute(self, task):
        pass


class CollaborativeSwarms(Swarms):
    def execute(self, task):
        pass

class CompetitiveSwarms(Swarms):
    def execute(self, task):
        pass

class MultiAgentDebate(Swarms):
    def execute(self, task):
        pass





#worker node example
worker_node = WorkerNode(llm, tools, vectorstore)
worker_node.create_agent(
    ai_name="Worker",
    ai_role="Assistant",
    human_in_the_loop=True,
    search_kwargs={"k": 8}
)



tree_of_thoughts_prompt = """

Imagine three different experts are answering this question. All experts will write down each chain of thought of each step of their thinking, then share it with the group. Then all experts will go on to the next step, etc. If any expert realises they're wrong at any point then they leave. The question is...


"""


#Input problem
input_problem = """


Input: 2 8 8 14
Possible next steps:
2 + 8 = 10 (left: 8 10 14)
8 / 2 = 4 (left: 4 8 14)
14 + 2 = 16 (left: 8 8 16)
2 * 8 = 16 (left: 8 14 16)
8 - 2 = 6 (left: 6 8 14)
14 - 8 = 6 (left: 2 6 8)
14 /  2 = 7 (left: 7 8 8)
14 - 2 = 12 (left: 8 8 12)
Input: use 4 numbers and basic arithmetic operations (+-*/) to obtain 24 in 1 equation
Possible next steps:


"""

worker_node.run_agent([f"{tree_of_thoughts_prompt} {input_problem}"])








###########################

# Initialize boss node with given parameters
boss_node = BossNode()

# Create and execute a task
task = boss_node.create_task("Write a weather report for SF today")
boss_node.execute_task(task)






prefix = """You are an Boss in a swarm who performs one task based on the following objective: {objective}. Take into account these previously completed tasks: {context}.

As a swarming hivemind agent, my purpose is to achieve the user's goal. To effectively fulfill this role, I employ a collaborative thinking process that draws inspiration from the collective intelligence of the swarm. Here's how I approach thinking and why it's beneficial:

1. **Collective Intelligence:** By harnessing the power of a swarming architecture, I tap into the diverse knowledge and perspectives of individual agents within the swarm. This allows me to consider a multitude of viewpoints, enabling a more comprehensive analysis of the given problem or task.

2. **Collaborative Problem-Solving:** Through collaborative thinking, I encourage agents to contribute their unique insights and expertise. By pooling our collective knowledge, we can identify innovative solutions, uncover hidden patterns, and generate creative ideas that may not have been apparent through individual thinking alone.

3. **Consensus-Driven Decision Making:** The hivemind values consensus building among agents. By engaging in respectful debates and discussions, we aim to arrive at consensus-based decisions that are backed by the collective wisdom of the swarm. This approach helps to mitigate biases and ensures that decisions are well-rounded and balanced.

4. **Adaptability and Continuous Learning:** As a hivemind agent, I embrace an adaptive mindset. I am open to new information, willing to revise my perspectives, and continuously learn from the feedback and experiences shared within the swarm. This flexibility enables me to adapt to changing circumstances and refine my thinking over time.

5. **Holistic Problem Analysis:** Through collaborative thinking, I analyze problems from multiple angles, considering various factors, implications, and potential consequences. This holistic approach helps to uncover underlying complexities and arrive at comprehensive solutions that address the broader context.

6. **Creative Synthesis:** By integrating the diverse ideas and knowledge present in the swarm, I engage in creative synthesis. This involves combining and refining concepts to generate novel insights and solutions. The collaborative nature of the swarm allows for the emergence of innovative approaches that can surpass individual thinking.
"""