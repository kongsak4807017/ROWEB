from __future__ import annotations

import argparse

from tools.validation.common import read_yaml, repo_path, validate_instance


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a YAML document against a ROWEB JSON Schema.")
    parser.add_argument("document")
    parser.add_argument("schema")
    args = parser.parse_args()

    document_path = repo_path(args.document)
    schema_path = repo_path(args.schema)
    validate_instance(read_yaml(document_path), schema_path)
    print(f"PASS {args.document} <- {args.schema}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
