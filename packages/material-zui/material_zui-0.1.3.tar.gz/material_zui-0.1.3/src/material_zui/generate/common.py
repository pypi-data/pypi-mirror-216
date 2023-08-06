import os
from langchain import PromptTemplate, HuggingFaceHub, LLMChain, HuggingFacePipeline

from material_zui.bing_ai.bing_ai import ZuiBingAi


class ZuiGen:
    def __init__(self, token: str, cookie_dir_path: str) -> None:
        self.token = os.environ['HUGGINGFACEHUB_API_TOKEN'] = token
        self.bing_ai = ZuiBingAi(cookie_dir_path)

    def gen_title(self, topic: str) -> str:
        prompt = topic
        # data = self.bing_ai.query(prompt)
        data = self.bing_ai.query(
            'Write seven subheadings for the blog article with the title yoga; the titles should be catchy and 60 characters max.')
        # print(data.response)
        # print(data.full_texts)
        print(data.texts)
        print(data.last_text)
        return ''

    def gen_titles(self, topics: list[str]) -> list[str]:
        return []

    def test(self):
        template = """
        Question: {question}
        Answer: """

        prompt = PromptTemplate(
            template=template,
            input_variables=['question']
        )
        question = "Which NFL team won the Super Bowl in the 2010 season?"

        # initialize Hub LLM
        hub_llm = HuggingFaceHub(
            # repo_id='google/flan-t5-xl',
            repo_id='OpenAssistant/oasst-sft-6-llama-30b-xor',
            model_kwargs={'temperature': 1e-10}
        )

        # create prompt template > LLM chain
        llm_chain = LLMChain(
            prompt=prompt,
            llm=hub_llm
        )

        # ask the user question about NFL 2010
        print(llm_chain.run(question))

    def ask(self, ask: str) -> str:
        template = """Question: {query}
        Answer: Let's think step by step."""
        prompt = PromptTemplate(template=template, input_variables=["query"])
        llm = HuggingFaceHub(repo_id="google/flan-t5-xxl",
                             model_kwargs={"temperature": 0.1})  # type: ignore
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        # query = "When was America discovered?"
        # query = "What the nodejs latest version?"
        return llm_chain.run(ask)
