import json
from dataclasses import dataclass
from typing import List, Optional

# Import TaskConfig from task_config_var.py
from prompt_config.task_config_vars import IntermediateVars


@dataclass
class DynamicTaskConfigFormatter:
    intermediate_vars: IntermediateVars

    def __init__(self, intermediate_vars):
        self.intermediate_vars = intermediate_vars

    def format_task_config(self, assistant_role_name,phase_prompt):
        # Format the phase_prompt using attributes from intermediate_vars_vars.py
        formatted_phase_prompt = []
        for phase_prompt_line in phase_prompt:
            formatted_line = phase_prompt_line.format(assistant_role=assistant_role_name,
                                                      task=self.intermediate_vars.task,
                                                      modality=self.intermediate_vars.modality,
                                                      language=self.intermediate_vars.language,
                                                      ideas=self.intermediate_vars.ideas,
                                                      gui=self.intermediate_vars.gui,
                                                      codes=self.intermediate_vars.codes,
                                                      unimplemented_file=self.intermediate_vars.unimplemented_file,
                                                      images=self.intermediate_vars.images,
                                                      comments=self.intermediate_vars.comments,
                                                      test_reports=self.intermediate_vars.test_reports,
                                                      error_summary=self.intermediate_vars.error_summary,
                                                      requirements=self.intermediate_vars.requirements)
            formatted_phase_prompt.append(formatted_line)
        return '\n'.join(formatted_phase_prompt)
