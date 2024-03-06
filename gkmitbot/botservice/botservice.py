import openai
import pandas as pd
import sqlalchemy as sa
import langchain
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain_core import *
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ChatMessageHistory
from .models import *
from langchain.prompts.chat import SystemMessagePromptTemplate 
# Configuration
openai.api_key = "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"

class BotService:
    def __init__(self):
        self.llm = self.get_llm()
        self.tool_list = self.get_tool_list()


    def get_llm(self):
        return ChatOpenAI(model="gpt-3.5-turbo-0125", openai_api_key=openai.api_key)
    
    def get_tool_list(self)->list:
        return [self.get_skill_by_user_input_tool(),self.get_answer_from_llm()]
    
    # Database Connection
    def get_postgres_conn(self):
        db_url = sa.engine.URL.create(drivername='postgresql+psycopg2',
                                     username='postgres',
                                     password='postgres',
                                     host='localhost',
                                     port='5432',
                                     database='gkmit')
        return sa.create_engine(db_url)

    # Database Queries
    def query_db(self,sql_query):
        engine = self.get_postgres_conn()
        with engine.connect() as conn:
            return pd.read_sql(sql_query, conn).to_dict(orient='records')

    # Employee Retrieval
    def get_employee_from_database(self,skill):
        sql_query = f"""SELECT e."First_Name", e."Last_Name" 
                        FROM botservice_emp_skill es 
                        JOIN botservice_employee e ON es."Employee_ID_id" = e."ID" 
                        JOIN botservice_skill s ON es."Skill_ID_id" = s."ID" 
                        WHERE LOWER(s."Skill_Name") = LOWER('{skill}');"""
        return self.query_db(sql_query)

    # Skill List Retrieval
    def get_skills_from_db(self):
        sql_query = """SELECT s."Skill_Name" FROM botservice_skill s;"""
        return self.query_db(sql_query)
    
    # LLM Answer Retrieval
    def get_answer_from_llm(self):
        def answer_from_llm(question):
            llm = self.llm
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You have to answer the question in a friendly manner."),
                ("user", "{input}"),
            ])
            chain = prompt | llm | StrOutputParser()
            response = chain.invoke({"input": question})
            return response
        answer_from_llm_tool = Tool(
            name="ANSWER_FROM_LLM",
            func=answer_from_llm,
            description=
            '''
            First try to use the SKILL_BY_USER_INPUT tool to get the answer. \
            if it returns NULL from the SKILL_BY_USER_INPUT tool,\
            You have to use the ANSWER_FROM_LLM tool to get the answer. \
            You are a helpful chatbot. \
            You will answer the question in a general manner \
            And you don't have to create imaginery characters. \
            The tool will return the answer to the question. \
            ''',
        )
        return answer_from_llm_tool

    # LLM Skill Retrieval
    def get_relevant_skills_from_llm(self,skill):
        llm = self.llm
        stored_skills = self.get_skills_from_db()
        stored_skills = [item['Skill_Name'] for item in stored_skills]
        template = f""" 
                        You have a list of stored_skill as given below: \
                        {stored_skills} \
                        Using the stored_skill, when the user ask about this skill: {skill} \
                        then you have to return the most related skill if it exits in the stored_skill. \
                        other wise just return NULL. \
                        Also return null in case of user asks for non-technical skill.
                    """
        prompt = ChatPromptTemplate.from_messages([
            ("system", template),
            ("user", "{input}"),
        ])
        chain = prompt | llm | StrOutputParser()
        related_skill = chain.invoke({"input": f"which skill is most related to {skill} out of {stored_skills}.? return only one item from the stored_skill list."})
        print(related_skill)
        return related_skill

    # Tool Initialization
    def get_skill_by_user_input_tool(self):
        def skill_by_user_input_search(skill: str):
            if not self.query_db(f"""SELECT * FROM botservice_skill WHERE LOWER("Skill_Name") = LOWER('{skill}');"""):
                new_skill = self.get_relevant_skills_from_llm(skill)
                return self.query_db(f"""SELECT e."First_Name", e."Last_Name",e."Job_Description",s."Skill_Name",s."Skill_Proficiency"
                                         FROM botservice_emp_skill es
                                         JOIN botservice_employee e ON es."Employee_ID_id" = e."ID"
                                         JOIN botservice_skill s ON es."Skill_ID_id" = s."ID"
                                         WHERE LOWER(s."Skill_Name") = LOWER('{new_skill}');""")
            return self.query_db(f"""SELECT e."First_Name", e."Last_Name",e."Job_Description",s."Skill_Name",s."Skill_Proficiency"
                                     FROM botservice_emp_skill es
                                     JOIN botservice_employee e ON es."Employee_ID_id" = e."ID"
                                     JOIN botservice_skill s ON es."Skill_ID_id" = s."ID"
                                     WHERE LOWER(s."Skill_Name") = LOWER('{skill}');""")

        skill_by_user_input_search_tool = Tool(
            name="SKILL_BY_USER_INPUT",
            func=skill_by_user_input_search,
            description=
            '''
            The tool will return the employees with that input skill in a proper human readable format from the database and say employees found. \
            Also don't return any skill if the input skill is a language. \
            And if the skill is matched from the database then go inside the if condition and if it doesn't match then go inside the else condition and figure out the answer from that condition. \
            Important condition is that the it will return only the technical skills and not the soft skills. \
            And if the skill is not found then it will return "No employees with the skills found", and also some resources to learn that skill.
            ''',
        )
        return skill_by_user_input_search_tool
    

    def __create_chat_history(self) -> ChatMessageHistory:
        chat_history = Chat_History.objects.all().values()
        if chat_history == None:
            chat_history = []

        history = ChatMessageHistory()

        for chat in chat_history:
            history.add_user_message(chat['Message'])
            history.add_ai_message(chat['Response'])

        return history

    # Agent Initialization
    def initialize_chat_agent(self):
        tools = self.get_tool_list()
        history = self.__create_chat_history()
        system_template=SystemMessagePromptTemplate.from_template("You are a helpful chatbot. You have to answer the question using the tools provided.Whenever you are unable to answer the question from the SKILL_BY_USER_INPUT tool, you have to use the ANSWER_FROM_LLM tool to get the answer. And whenever use asks about some skill, you have to use the SKILL_BY_USER_INPUT tool to get the answer.")
        agent_kwargs = {
                "system_message": system_template,
                "extra_prompt_messages": history.messages,
            }
        agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent_kwargs=agent_kwargs,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            return_intermediate_steps=True
        )
        return agent

    # Chat Function
    def chat_with_llm(self,input_text: str):
        agent = self.initialize_chat_agent()
        resp = agent.invoke(input_text)
        return resp['output']
