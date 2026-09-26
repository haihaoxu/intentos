"""Regression tests for distinguishing a manifest path from manifest text.

``parse_manifest`` accepts either a filesystem path or the YAML itself. The two
were told apart with ``Path(source).exists()``, which on POSIX raises
``OSError`` with ``ENAMETOOLONG`` once the string is longer than the
filesystem's name limit — and a manifest is always longer than that. Windows
returns ``False`` instead of raising, so the defect never appeared locally and
only showed up under CI, where it broke every caller that passes YAML text:
the workflow parser, the capability registry, and the ``ask`` resolution path.

These tests pin the contract. ``test_rejects_long_yaml_string`` is the one that
actually fails without the fix, and only on POSIX.
"""

from __future__ import annotations

from pathlib import Path

from core.parser import is_path, parse_manifest

VALID_YAML = """
kind: Capability
metadata:
  name: text_summarize
  version: "1.0.0"
  description: Summarize the input text into a concise summary
spec:
  input:
    text:
      type: string
      description: The text to summarize
  output:
    summary:
      type: string
      description: The generated summary
"""


class TestIsPath:
    def test_rejects_long_yaml_string(self):
        """A manifest is longer than the POSIX name limit; it is not a path."""
        padding = "# padding line\n" * 64
        assert len(VALID_YAML + padding) > 255
        assert is_path(VALID_YAML + padding) is False

    def test_accepts_existing_file(self, tmp_path: Path):
        target = tmp_path / "manifest.yaml"
        target.write_text(VALID_YAML, encoding="utf-8")
        assert is_path(target) is True
        assert is_path(str(target)) is True

    def test_rejects_missing_path(self):
        assert is_path("no/such/manifest.yaml") is False


class TestParseManifestFromString:
    def test_long_yaml_string_parses(self):
        """The full manifest text parses without being mistaken for a path."""
        padding = "# padding line\n" * 64
        manifest, result = parse_manifest(VALID_YAML + padding)
        assert manifest.metadata.name == "text_summarize"
        assert manifest.metadata.version == "1.0.0"

    def test_does_not_raise_on_long_string(self):
        """ENAMETOOLONG must not escape as an OSError on POSIX."""
        long_text = VALID_YAML + "# padding line\n" * 64
        parse_manifest(long_text)
