import os
from langchain import OpenAI, PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from pathlib import Path
import openai.error
from langchain.output_parsers import PydanticOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic import BaseModel, Field


class RevertCommand(BaseModel):
    action: str = Field(description="The last git action which took place")
    revert_command: str = Field(description="The revert command to undo the last action")


class LanguageModel:
    """
    A helper class for using OpenAI's language model.
    """

    def __init__(self, verbose: bool = True, temperature=0):
        """
        Initializes the Summarizer class with a text splitter and a summarize chain.
         :param verbose: A boolean indicating whether to print verbose output.
        """
        prompt_path = os.path.join(os.path.dirname(__file__), 'prompts/prompt_template.txt')
        summarize_template = PromptTemplate(template=Path(prompt_path).read_text(),
                                            input_variables=["text"])
        self.llm = OpenAI(temperature=temperature)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=20,
            length_function=len,
        )
        self.summarize_chain = load_summarize_chain(llm=self.llm,
                                                    chain_type="map_reduce",
                                                    map_prompt=summarize_template,
                                                    combine_prompt=summarize_template,
                                                    verbose=verbose)
        self.parser = PydanticOutputParser(pydantic_object=RevertCommand)
        prompt_path = os.path.join(os.path.dirname(__file__), 'prompts/undo_template.txt')
        self.undo_template = PromptTemplate(
            template=Path(prompt_path).read_text(),
            input_variables=["reflog"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

    def summarize(self, text: str):
        """
        Summarizes the given text using OpenAI's language model.
         :param text: The text to be summarized.
        :return: The summarized text.
        """
        try:
            texts = self.text_splitter.create_documents([text])
            return self.summarize_chain.run(texts)
        except openai.error.InvalidRequestError as e:
            print(f"Invalid request error: {e}")
        except Exception as e:
            print(f"Error summarizing text: {e}")
        raise RuntimeError("Summarization failed - try to add a single file")

    def get_git_undo(self, reflog: str):
        """
        Returns the last git action and the command to undo it.
        :return: The undo command.
        """
        # TODO explicit maybe? """https://github.blog/2015-06-08-how-to-undo-almost-anything-with-git/"""
        _input = self.undo_template.format_prompt(reflog=reflog)
        output = self.llm(_input.to_string())
        return self.parser.parse(output)
