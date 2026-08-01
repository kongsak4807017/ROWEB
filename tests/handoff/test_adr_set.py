from pathlib import Path

ADR_ROOT = Path("docs/adr")
EXPECTED = {
    "ADR-020-client-product-strategy.md",
    "ADR-021-rathena-authority.md",
    "ADR-022-dual-client-contract-boundary.md",
    "ADR-023-engine-neutral-asset-catalog.md",
    "ADR-024-reference-source-and-license-policy.md",
    "ADR-025-unity-start-gate.md",
}
REQUIRED_HEADINGS = {
    "## Context",
    "## Decision",
    "## Alternatives considered",
    "## Consequences",
    "## Reversal conditions",
    "## Evidence",
    "## Owner",
}


def test_required_adr_files_exist() -> None:
    actual = {path.name for path in ADR_ROOT.glob("ADR-*.md")}
    assert EXPECTED <= actual


def test_required_adr_sections_exist() -> None:
    for filename in EXPECTED:
        content = (ADR_ROOT / filename).read_text(encoding="utf-8")
        missing = REQUIRED_HEADINGS - set(content.splitlines())
        assert not missing, f"{filename} missing headings: {sorted(missing)}"
        assert "Status: Accepted" in content
        assert "Date: 2026-08-01" in content
