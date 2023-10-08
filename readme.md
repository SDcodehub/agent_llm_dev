# agent_llm_dev - LLM Agents Framework

**agent_llm_dev** is a framework for developing Language Model (LLM) agents, designed to facilitate the creation of conversational AI agents. It is currently focused on software development tasks and includes features for post-processing conversation outputs. Future developments aim to make this framework more generalized for various tasks, incorporate human-in-the-loop capabilities, support long-term and short-term memory, enable self-reflection, and integrate tools like web scraping.

This repository serves as an experimental platform for exploring and experimenting with different concepts related to agent development.

## Usage

To get started with **agent_llm_dev**, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/SDcodehub/agent_llm_dev.git
   ```

2. Create a virtual environment and install all dependencies:

   ```bash
   cd agent_llm_dev
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the main application with custom configurations. You can specify the application description, name, model, and enable debugging:

   ```bash
   python main.py --app_desc "time checking app" --app_name "time_app" --model "GPT_3_5_TURBO" --debug
   ```

4. Modify the configuration settings in the project to suit your experiments and needs.

## Future Steps

The future development roadmap for **agent_llm_dev** includes the following steps:

- Generalize the framework to support various tasks and domains.
- Implement human-in-the-loop capabilities to enhance interaction with users.
- Develop long-term and short-term memory mechanisms for improved context handling.
- Enable self-reflection to enhance the agent's learning and decision-making capabilities.
- Integrate additional tools and functionalities like web scraping for extended use cases.

## Repository

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/SDcodehub/agent_llm_dev)

## Contact

If you have any questions or suggestions, please feel free to reach out to the project maintainer:

- **Sagar Desai**
  - Email: sagardesaee@gmail.com

Feel free to explore, experiment, and contribute to this framework. If you encounter issues or have suggestions, please open an issue on the GitHub repository.
