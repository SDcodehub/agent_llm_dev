from dataclasses import dataclass
from typing import List, Optional

# DemandAnalysis ->modality -> <INFO> PowerPoint
# LanguageChoose-> language -> <INFO> Python
# Coding -> codes ->       "FILENAME",
#       "```LANGUAGE",
#       "'''",
#       "DOCSTRING",
#       "'''",
#       "CODE",
#       "```",
# ArtDesign -> images ->
# "button_1.png: The button with the number \"1\" on it.",
# "button_multiply.png: The button with the multiplication symbol (\"*\") on it.
# ArtIntegration -> gui ->
# "FILENAME",
# "```LANGUAGE",
# "'''",
# "DOCSTRING",
# "'''",
# "CODE",
# "```",
# CodeComplete -> unimplemented_file
# CodeReviewComment -> comments
# CodeReviewModification
# test_reports
# TestErrorSummary -> error_summary
# TestModification ->
# EnvironmentDoc ->



@dataclass
class IntermediateVars:
    task: Optional[str] = None
    modality: Optional[str] = None
    language: Optional[str] = None
    ideas: Optional[str] = None
    gui: Optional[str] = None
    codes: Optional[str] = None
    unimplemented_file: Optional[str] = None
    images: Optional[str] = None
    comments: Optional[str] = None
    test_reports: Optional[str] = None
    error_summary: Optional[str] = None
    requirements: Optional[str] = None
