from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings


class GrammarCorrectionAgent:
    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL_NAME, api_key=settings.OPENAI_API_KEY
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a grammar correction agent.Do not chnage the tone of the sentence,follow the ceratin guidelines provided",
                ),
                (
                    "human",
                    "Correct the grammar and spelling mistakes in the following text: {text}",
                ),
            ]
        )

    async def run(
        self,
        issues: list,
        guidelines: list,
        text: str,
    ):
        try:
            prompt_text = self.prompt.format(text=text)

            for issue in issues:
                prompt_text += f"\nIssue: {issue[0]}"
            for guideline in guidelines:
                prompt_text += f"\nGuideline: {guideline}"

            prompt = ChatPromptTemplate.from_messages([("human", prompt_text)])
            chain = prompt | self.llm

            response = chain.invoke(input={"text": text})
            corrected_text = response.content

            return corrected_text

        except Exception as e:
            raise e


async def main():
    agent = GrammarCorrectionAgent(doc_id=1)
    issues = [
        {"message": "The verb “do” seems to be incorrect."},
        {"message": "Add a space after a period."},
    ]
    guidelines = [
        "Aim for Flesch Reading Ease >= 60.",
        "Keep average sentence length <= 20 words.",
        "Avoid grammar and spelling mistakes.",
        "Prefer active voice and clear phrasing.",
    ]
    text = "Human had do everything.Human can live human.Human can fly."

    corrected_text = await agent.run(issues=issues, guidelines=guidelines, text=text)
    print(corrected_text)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
