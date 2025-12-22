import argparse
import os
import shutil
import stat


REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
PAYLOAD_DIR = os.path.join(REPO_ROOT, "payload")

ADD_MARKER_START = "# --- Process Kit Additions (simple-agentic-process-setup) START ---"
ADD_MARKER_END = "# --- Process Kit Additions (simple-agentic-process-setup) END ---"


def _copy_tree(src_dir: str, dst_dir: str, *, overwrite: bool) -> set[str]:
    copied: set[str] = set()
    for root, dirs, files in os.walk(src_dir):
        rel_root = os.path.relpath(root, src_dir)
        dst_root = dst_dir if rel_root == "." else os.path.join(dst_dir, rel_root)
        os.makedirs(dst_root, exist_ok=True)

        for directory in dirs:
            os.makedirs(os.path.join(dst_root, directory), exist_ok=True)

        for filename in files:
            src_path = os.path.join(root, filename)
            dst_path = os.path.join(dst_root, filename)

            os.makedirs(os.path.dirname(dst_path), exist_ok=True)

            if (not overwrite) and os.path.exists(dst_path):
                continue
            shutil.copy2(src_path, dst_path)
            rel_dst = os.path.relpath(dst_path, dst_dir)
            copied.add(rel_dst)

            try:
                src_mode = os.stat(src_path).st_mode
                os.chmod(dst_path, stat.S_IMODE(src_mode))
            except OSError:
                pass

    return copied


def install_payload(target_dir: str) -> None:
    if not os.path.isdir(PAYLOAD_DIR):
        raise RuntimeError(f"Missing payload directory: {PAYLOAD_DIR}")

    os.makedirs(target_dir, exist_ok=True)

    payload_additions_src = os.path.join(PAYLOAD_DIR, "AGENTS-additions.md")
    payload_additions_content: str | None = None
    if os.path.isfile(payload_additions_src):
        with open(payload_additions_src, "r") as f:
            payload_additions_content = f.read().rstrip() + "\n"

    copied = _copy_tree(PAYLOAD_DIR, target_dir, overwrite=False)
    print("Installed: payload/*")

    agents_md_dst = os.path.join(target_dir, "AGENTS.md")
    additions_src = os.path.join(target_dir, "AGENTS-additions.md")

    if not os.path.isfile(additions_src):
        return

    with open(additions_src, "r") as f:
        additions = f.read().rstrip() + "\n"

    wrapped_additions = (
        f"{ADD_MARKER_START}\n" f"{additions}" f"{ADD_MARKER_END}\n"
    )

    applied = False

    if not os.path.isfile(agents_md_dst):
        with open(agents_md_dst, "w") as f:
            f.write(additions)
        print("Created: AGENTS.md from AGENTS-additions.md")
        applied = True
    else:
        with open(agents_md_dst, "r") as f:
            existing = f.read()

        if (ADD_MARKER_START in existing) or (ADD_MARKER_END in existing):
            print("Skipped: AGENTS-additions.md already applied")
            applied = True
        else:
            with open(agents_md_dst, "a") as f:
                if not existing.endswith("\n"):
                    f.write("\n")
                f.write("\n")
                f.write(wrapped_additions)
            print("Appended: AGENTS-additions.md to AGENTS.md")
            applied = True

    if (not applied) or os.path.basename(additions_src) != "AGENTS-additions.md":
        return

    if os.path.isfile(additions_src):
        safe_to_delete = False
        if "AGENTS-additions.md" in copied:
            safe_to_delete = True
        elif (payload_additions_content is not None) and (additions == payload_additions_content):
            safe_to_delete = True

        if safe_to_delete:
            os.remove(additions_src)
            print("Deleted: AGENTS-additions.md (merged into AGENTS.md)")
        else:
            print(
                "Kept: AGENTS-additions.md (differs from kit payload; not auto-deleting)"
            )

    for rel_script in [
        "scripts/run-prompt",
        "scripts/start-topic",
        "scripts/continue-topic",
        "scripts/install-local-exchange",
    ]:
        script_path = os.path.join(target_dir, rel_script)
        if os.path.isfile(script_path):
            os.chmod(script_path, 0o755)
            print(f"Made executable: {rel_script}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install the Process Kit payload into a target project directory."
    )
    parser.add_argument("target", help="Target directory to install into.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow installing into a directory that already contains 'payload/'.",
    )
    parser.add_argument(
        "--keep-additions",
        action="store_true",
        help="Keep AGENTS-additions.md in the target directory after applying.",
    )
    args = parser.parse_args()

    target_dir = os.path.abspath(args.target)
    if (not args.force) and os.path.isdir(os.path.join(target_dir, "payload")):
        raise RuntimeError(
            "Refusing to install into a directory that already contains a 'payload/' folder. "
            "Pick a target project directory (not the kit repo root), or pass --force."
        )

    if args.keep_additions:
        # Install first, then restore the additions file if we delete it.
        install_payload(target_dir)
        # If the file was removed by the installer, put it back from the kit payload.
        payload_additions_src = os.path.join(PAYLOAD_DIR, "AGENTS-additions.md")
        additions_dst = os.path.join(target_dir, "AGENTS-additions.md")
        if os.path.isfile(payload_additions_src) and (not os.path.isfile(additions_dst)):
            shutil.copy2(payload_additions_src, additions_dst)
            print("Restored: AGENTS-additions.md (--keep-additions)")
    else:
        install_payload(target_dir)
    print("\n✅ Process Kit payload installed.")
    print("\nOptional next steps:")
    print("- Local Exchange: ./scripts/run-prompt setup-local-exchange")


if __name__ == "__main__":
    main()
