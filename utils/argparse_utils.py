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
        "--model",
        type=str,
        required=True,
        help="Choose a model from available options",
    )

    parser.add_argument(
        "--openai",
        action="store_true",
        help="Use OpenAI model",
    )

    parser.add_argument(
        "--nvidia",
        action="store_true",
        help="Use Nvidia model",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    # Check if both --openai and --nvidia flags are provided
    if args.openai and args.nvidia:
        raise ValueError("Both --openai and --nvidia flags cannot be provided simultaneously")

    # Check if either --openai or --nvidia flag is provided
    if not args.openai and not args.nvidia:
        raise ValueError("Either --openai or --nvidia flag must be provided")

    # Extract the enum value from the model argument based on the flag
    if args.openai:
        args.model = model_type(args.model).value
    elif args.nvidia:
        args.model = nvidia_model_type(args.model).value

    return args
