#!/usr/bin/env python3

import json
import os
import re
from pathlib import Path
from collections import defaultdict

# Define the root directory
ROOT_DIR = Path(__file__).parent

# Regex pattern to find {id_firmware_version} comparisons
# Matches patterns like: {id_firmware_version} >= 2, {id_firmware_version} <= 1, etc.
FIRMWARE_PATTERN = r"\{id_firmware_version\}\s*([><=!]+)\s*(\d+)"


def extract_firmware_values(file_path):
    """
    Extract all firmware version values from a JSON file.
    Returns a list of tuples: (operator, value)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # Read the file as text to find all patterns
            content = f.read()

        # Find all matches
        matches = re.findall(FIRMWARE_PATTERN, content)
        return matches
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []


def get_highest_value(matches):
    """
    Extract the highest value from the comparisons.
    For example, if we have >= 2 and <= 1, returns 2.
    """
    if not matches:
        return None

    values = [int(value) for _, value in matches]
    return max(values) if values else None


def main():
    # Dictionary to store results
    results = defaultdict(list)

    # Walk through all directories
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".json"):
                file_path = Path(root) / file

                # Extract firmware version values
                matches = extract_firmware_values(file_path)

                if matches:
                    highest_value = get_highest_value(matches)
                    # Get relative path
                    rel_path = file_path.relative_to(ROOT_DIR)

                    results[str(rel_path)] = {
                        "matches": matches,
                        "highest_value": highest_value,
                        "count": len(matches),
                    }

    # Print results in simple format
    print("Board | Highest Firmware Version\n" + "-" * 60)

    for file_path in sorted(results.keys()):
        data = results[file_path]
        highest = data["highest_value"]
        print(f"{file_path} | {highest}")


if __name__ == "__main__":
    main()
