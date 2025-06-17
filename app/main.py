import gradio as gr

from app.llm import QAAgent
from app.rag import EmbeddingModel

if gr.NO_RELOAD:
    embedding_model = EmbeddingModel()
    embedding_model.load_embeddings()
    retriever = embedding_model.get_retriever()
    agent = QAAgent(retriever=retriever)


def get_response(
    query: str, history: list[tuple[str, str]] = None
) -> tuple[str, list[tuple[str, str]]]:
    """
    Process the user query and return the response from the QA agent.

    Args:
        query (str): The user's question.
        history (list[tuple[str, str]], optional): The conversation history.

    Returns:
        tuple[str, list[tuple[str, str]]]: The response from the QA agent and the updated conversation history.
    """
    if history is None:
        history = []

    answer, sources = agent.answer(query)
    citations = ""
    for i, doc in enumerate(sources):
        title = doc.metadata.get("title", "-")
        link = doc.metadata.get("link", "")
        citations += f"{i+1}. [{title}]({link})\n"
    response = f"{answer}\n\n**Sources:**\n{citations}"
    # history.append(
    #     {"role": "user", "content": query},
    #     {"role": "assistant", "content": response},
    # )
    return response


description = """
    <body>
    <h3>Anveṣaṇā</h3>
    <table style="width: 100%; border: none; border-collapse: collapse;">
    <tr style="border: none;">
        <td width="40%" style="border: none;">
        <div class="column first-column">
            <h3><strong><em>/ənʋeːʂəɳɑː/ · Sanskrit: अन्वेषणा</em></strong></h3>
            <blockquote>
                <p><em>search after, seek for, or inquiry into.<br>Derived from the root verb
                        "anveṣ" (अन्वेष), which means "to search for" or "to seek out".
                        In the context of Vedic texts, Anveṣaṇā refers to the process of searching for
                        knowledge, wisdom, and understanding within these ancient scriptures.</em></p>
            </blockquote>
        </div>
        </td>
        <td width="60%" style="border: none;">
        <div class="column second-column">
            <p>Anvesana is tool that allows you to search through Vedic texts using natural language queries,
                using retrieval-augmented-generation to provide accurate and relevant answers.
                It is designed to help you find information quickly and efficiently, making
                it easier to explore the vast knowledge contained within Vedic literature.</p>
            <p>The following texts are currently supported: </p>
            <ul>
                <li>
                    Charaka Samhita [Ayurveda]
                    <ul>
                        <li>A foundational text of Ayurveda, the ancient Indian system of medicine.
                        Comprised of 8 books and 120 chapters.</li>
                    </ul>
                </li>
            </ul>
        </div>
        </td>
    </tr>
    </table>
    </body>
"""

app = gr.ChatInterface(
    fn=get_response,
    title="Anveṣaṇā: Search through Vedic Texts with ease.",
    description=description,
    type="messages",
    flagging_mode="manual",
    flagging_options=["Like", "Spam", "Inappropriate", "Other"],
    save_history=True,
    examples=[
        ["What is Ayurveda?"],
        ["What is the difference between Ayurveda and modern medicine?"],
        ["What is the Charaka Samhita?"],
        ["What are the main texts of Ayurveda?"],
        ["How does Ayurveda treat insomnia?"],
    ],
    theme="Taithrah/Minimal",
)


if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        # share=True,
    )
