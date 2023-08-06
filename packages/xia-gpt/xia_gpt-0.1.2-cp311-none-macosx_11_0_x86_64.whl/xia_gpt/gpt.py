import re


class Gpt:
    def __init__(self):
        pass

    @classmethod
    def extract_code_blocks(cls, message: str) -> list:
        """Extract code blocks embraced by ``` code ```

        Args:
            message:

        Returns:
            List of the dictionary with the following structure:
                * type: code type  (like python, json or might be empty)
                * body: code body  (Code)
        """
        # Regular expression pattern to find code blocks
        pattern = r"```(.*?)\n(.*?)```"

        # Find all matches in the markdown_text
        matches = re.findall(pattern, message, re.DOTALL)

        # Create a list of dictionaries from the matches
        code_blocks = [{'type': match[0], 'body': match[1]} for match in matches]

        return code_blocks

    def chat_complete(self, context: str, message: str, **kwargs):
        """Give the context and

        Args:
            context: chat context
            message: message to be sent
            **kwargs: other parameters
        """

