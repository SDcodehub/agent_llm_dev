import argparse
from llms.openai_model import ModelType, model_type
from llms.nvidia_model import NvidiaModelType, nvidia_model_type

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
        "--openai_model",
        type=model_type,
        choices=list(ModelType),
        default=ModelType.GPT_3_5_TURBO,
        help="Choose an OpenAI model from available options (default: GPT_3_5_TURBO)",
    )

    parser.add_argument(
        "--nvidia_model",
        type=nvidia_model_type,
        choices=list(NvidiaModelType),
        help="Choose an Nvidia model from available options",
    )

    parser.add_argument(
        "--nvidia_api_key",
        type=str,
        help="API key for Nvidia platform",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    # Extract the enum value from the model arguments
    if args.openai_model:
        args.openai_model = args.openai_model.value
    if args.nvidia_model:
        args.nvidia_model = args.nvidia_model.value

    return args
