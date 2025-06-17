from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_google_genai import ChatGoogleGenerativeAI


class QAAgent:
    SYSTEM_PROMPT = """
    You are a helpful assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer the question.
    Your responses should be informative and relevant to the input.
    If you don't know the answer, just say that you don't know.
    Question: {input}
    Context: {context}
    Answer:
    """

    def __init__(
        self,
        retriever: VectorStoreRetriever,
        model_name: str = "gemini-2.5-flash-preview-05-20",
    ):
        self.model = ChatGoogleGenerativeAI(model=model_name, temperature=0.3)
        self.retriever = retriever
        self.prompt = PromptTemplate(
            template=self.SYSTEM_PROMPT,
            input_variables=["context", "input"],
        )

        self.qa_chain = create_stuff_documents_chain(llm=self.model, prompt=self.prompt)
        self.retrieval_chain = create_retrieval_chain(
            retriever=self.retriever,
            combine_docs_chain=self.qa_chain,
        )

    def answer(self, query: str) -> tuple[str, list[Document]]:
        """
        Generate an answer to the query using chained context retrieval and LLM response generation.

        Args:
            query (str): The question to be answered.

        Returns:
            tuple: A tuple containing the answer string and a list of source documents.
        """
        response = self.retrieval_chain.invoke({"input": query})
        return response.get("answer", ""), response.get("context", [])
