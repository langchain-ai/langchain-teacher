
# LangChain-Teacher

## Description

LangChain-Teacher is designed to facilitate interactive learning of LangChain, allowing users to engage with the LangChain platform through a chat-based learning interface. The app provides two teaching styles: Instructional, which provides step-by-step instructions, and Interactive lesson with questions, which prompts users with questions to assess their understanding.

## Getting Started

This Streamlit app guides users through lessons using a chat-based interface. To get started, follow these steps:

### Prerequisites

- Python 3.10 or higher

### Installation

1. Clone the repository from GitHub or create a GitHub Codespace:
   ```
   git clone https://github.com/hwchase17/langchain-teacher.git
   ```
   Change directory to the langchain-teacher directory
   ```
   cd langchain-teacher
   ```

2. Install the required dependencies listed in `requirements.txt`:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add the following environment variables:

   ```
   OPENAI_API_KEY=
   LANGCHAIN_ENDPOINT=
   LANGCHAIN_API_KEY=
   LANGCHAIN_TRACING_V2=
   LANGCHAIN_PROJECT=
   ```

   An example `.env` file is provided as `.env-example`. If you're not using LangSmith, you only need to set the `OPENAI_API_KEY` variable.

4. Run the Streamlit app using the command:
   ```
   streamlit run lc_main.py
   ```

   If using `dotenv` to manage environment variables, use the following command:
   ```
   dotenv streamlit run lc_main.py
   ```

## Repository Details

- The core of the teaching process is driven by the prompts defined in `get_prompt.py`. This module creates lessons based on the content available in the `lc_guides` folder, where lessons are stored as `.txt` files.

- The `supervisor-model` branch in this repository implements a `SequentialChain` to supervise responses from students and teachers. This approach aims to ensure that questions are on-topic and to detect prompt injections.

## Contributions

There are numerous ways to enhance the teaching style and overall functionality of the app. Contributions and suggestions for improvements are welcome. Feel free to contribute by creating pull requests or raising issues.

## License

This project is licensed under the [MIT License](LICENSE).


