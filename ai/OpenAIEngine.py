import os
from langchain.chains import LLMChain
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from cryptography.fernet import Fernet


class CollegeAIEngine:    
    @staticmethod
    def get_openai_answer(user_input):
        encrypted_app_token = 'gAAAAABlOLQoLplaL2-lfD1T4VkBXnkKxq1XK_VlVHiEm7MaftNJmZ4f-7rQlUws-NIMHjpWOMtevkwB5NX7f4kqknvrVtwH3ccAsOHB_Yg9dzksRxh5yVuuIXRD3hov8yU6BSXwd-HLTnBRLX5ARDOqzxJoK6M15A=='

        crypto_key = os.getenv("CRYPTO_KEY")
        if crypto_key is None:
            raise ValueError("CRYPTO_KEY environment variable is not set.")
        
        cipher_suite = Fernet(crypto_key)
        api_key = cipher_suite.decrypt(encrypted_app_token).decode()
        os.environ["OPENAI_API_KEY"] = api_key
        
        summary_template = """
            {user_input}, answer using information only about colleges in United States of America
        """

        summary_prompt_template = PromptTemplate(
            input_variables=["user_input"], template=summary_template
        )

        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k", api_key=api_key)

        chain = LLMChain(llm=llm, prompt=summary_prompt_template)
        
        response = chain.run(user_input=user_input)
        
        return response

# Example usage:
# result = CollegeAIEngine.get_openai_answer(user_input="Your question here.")
# print(result)
