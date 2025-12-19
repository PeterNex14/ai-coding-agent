import argparse

parser = argparse.ArgumentParser(description="Gabriel's AI Agent Boot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

print(args.user_prompt)
print(args.verbose)
