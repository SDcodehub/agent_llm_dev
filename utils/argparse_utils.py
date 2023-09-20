import argparse
from llms.openai_model import ModelType, model_type


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Your App Description")

    parser.add_argument(
        "--app_desc",
        type=str,
        required=True,
        help="A string description for your app",
    )

    parser.add_argument(
        "--app_name",
        type=str,
        required=True,
        help="Name of your app",
    )

    parser.add_argument(
        "--model",
        type=model_type,
        choices=list(ModelType),
        default=ModelType.GPT_3_5_TURBO,
        help="Choose a model from available options (default: GPT_3_5_TURBO)",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    # Extract the enum value from the model argument
    args.model = args.model.value

    return args

