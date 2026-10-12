import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.checkout = self.root / "checkout"
        (self.checkout / "references").mkdir(parents=True)
        for name in ("SKILL.md", "install.py", "references/catalog.md"):
            shutil.copy2(REPO / name, self.checkout / name)
        shutil.copytree(REPO / "third_party", self.checkout / "third_party")
        self.home = self.root / "home"
        self.home.mkdir()

    def cli(self, *args, ok=True):
        result = subprocess.run(
            [sys.executable, str(self.checkout / "install.py"), "--home", str(self.home), *args],
            capture_output=True, text=True, timeout=20,
        )
        if ok:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def test_dry_run_install_verify_and_idempotence(self):
        self.cli("--dry-run")
        self.assertEqual(list(self.home.iterdir()), [])
        self.cli()
        self.cli("--verify")
        self.cli()
        for dirname in (".skills", ".hermes/skills", ".codex/skills", ".claude/skills", ".cursor/skills", ".gemini/skills", ".config/opencode/skills", ".opencode/skills", ".openclaude/skills", ".grok/skills", ".zcode/skills", ".agents/skills"):
            self.assertEqual((self.home / dirname / "motion-skill-workflow/SKILL.md").read_bytes(), (self.checkout / "SKILL.md").read_bytes())

    def test_official_bundle_installs_only_selected_markdown(self):
        names = ("motion-skill-workflow", "lottiefiles-motion-design", "gsap-core")
        args = ("--tools", "codex,gemini-antigravity", "--skills", ",".join(names))
        self.cli(*args)
        self.cli(*args, "--verify")
        for tool in (".codex/skills", ".gemini/skills"):
            for name in names:
                dest = self.home / tool / name
                self.assertTrue((dest / "SKILL.md").is_file())
                if name != "motion-skill-workflow":
                    self.assertTrue(all(p.suffix == ".md" for p in dest.rglob("*") if p.is_file()))

    def test_existing_other_skill_is_never_overwritten(self):
        dest = self.home / ".claude/skills/motion-skill-workflow"
        dest.mkdir(parents=True)
        (dest / "SKILL.md").write_text("user-owned\n")
        output = self.cli("--tools", "claude", ok=False)
        self.assertIn("CONFLICT", output)
        self.assertEqual((dest / "SKILL.md").read_text(), "user-owned\n")

    def test_managed_copy_update_and_local_edit_protection(self):
        args = ("--tools", "claude", "--mode", "copy")
        self.cli(*args)
        dest = self.home / ".claude/skills/motion-skill-workflow"
        (self.checkout / "SKILL.md").write_text("updated\n")
        self.assertIn("STALE", self.cli(*args, "--verify", ok=False))
        self.cli(*args)
        self.assertEqual((dest / "SKILL.md").read_text(), "updated\n")
        (dest / "SKILL.md").write_text("local edit\n")
        self.assertIn("CONFLICT", self.cli(*args, ok=False))
        self.assertEqual((dest / "SKILL.md").read_text(), "local edit\n")

    def test_managed_copy_rejects_symlinked_file_and_marker(self):
        args = ("--tools", "claude", "--mode", "copy")
        self.cli(*args)
        dest = self.home / ".claude/skills/motion-skill-workflow"
        external = self.root / "outside.md"
        shutil.copy2(dest / "SKILL.md", external)
        (dest / "SKILL.md").unlink()
        try:
            (dest / "SKILL.md").symlink_to(external)
        except OSError as error:
            self.skipTest(f"symlink unavailable: {error}")
        (self.checkout / "SKILL.md").write_text("changed\n")
        self.assertIn("CONFLICT", self.cli(*args, ok=False))
        self.assertEqual(external.read_bytes(), (REPO / "SKILL.md").read_bytes())
        (dest / "SKILL.md").unlink()
        shutil.copy2(external, dest / "SKILL.md")
        marker = dest / ".motion-skill-workflow-install.json"
        other_marker = self.root / "other-marker.json"
        shutil.copy2(marker, other_marker)
        marker.unlink()
        marker.symlink_to(other_marker)
        self.assertIn("CONFLICT", self.cli(*args, ok=False))
        self.assertTrue(marker.is_symlink())

    def test_broken_destination_symlink_is_preserved(self):
        dest = self.home / ".codex/skills/motion-skill-workflow"
        dest.parent.mkdir(parents=True)
        try:
            dest.symlink_to(self.root / "missing", target_is_directory=True)
        except OSError as error:
            self.skipTest(f"symlink unavailable: {error}")
        self.assertIn("CONFLICT", self.cli("--tools", "codex", ok=False))
        self.assertTrue(dest.is_symlink())


if __name__ == "__main__":
    unittest.main()
