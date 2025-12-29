import argparse
import os
import shutil
import stat


REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
PAYLOAD_DIR = os.path.join(REPO_ROOT, "payload")

ADD_MARKER_START = "# --- Process Kit Additions (repo-agent-pm) START ---"
ADD_MARKER_END = "# --- Process Kit Additions (repo-agent-pm) END ---"


def _copy_tree(
    src_dir: str,
    dst_dir: str,
    *,
    overwrite: bool,
    skip_if_exists: set[str] | None = None,
) -> set[str]:
    copied: set[str] = set()
    skip_if_exists = skip_if_exists or set()
    for root, dirs, files in os.walk(src_dir):
        rel_root = os.path.relpath(root, src_dir)
        dst_root = dst_dir if rel_root == "." else os.path.join(dst_dir, rel_root)
        os.makedirs(dst_root, exist_ok=True)

        for directory in dirs:
            os.makedirs(os.path.join(dst_root, directory), exist_ok=True)

        for filename in files:
            src_path = os.path.join(root, filename)
            dst_path = os.path.join(dst_root, filename)
            rel_dst = os.path.relpath(dst_path, dst_dir)

            os.makedirs(os.path.dirname(dst_path), exist_ok=True)

            if rel_dst in skip_if_exists and os.path.exists(dst_path):
                continue
            if (not overwrite) and os.path.exists(dst_path):
                continue
            shutil.copy2(src_path, dst_path)
            copied.add(rel_dst)

            try:
                src_mode = os.stat(src_path).st_mode
                os.chmod(dst_path, stat.S_IMODE(src_mode))
            except OSError:
                pass

    return copied


def _replace_additions_block(existing: str, wrapped_additions: str) -> str | None:
    if (ADD_MARKER_START not in existing) or (ADD_MARKER_END not in existing):
        return None
    try:
        before, rest = existing.split(ADD_MARKER_START, 1)
        _, after = rest.split(ADD_MARKER_END, 1)
    except ValueError:
        return None
    return f"{before}{wrapped_additions}{after.lstrip()}"


def install_payload(
    target_dir: str,
    *,
    overwrite: bool,
    skip_if_exists: set[str] | None = None,
) -> None:
    if not os.path.isdir(PAYLOAD_DIR):
        raise RuntimeError(f"Missing payload directory: {PAYLOAD_DIR}")

    os.makedirs(target_dir, exist_ok=True)

    payload_additions_src = os.path.join(PAYLOAD_DIR, "AGENTS-additions.md")
    payload_additions_content: str | None = None
    if os.path.isfile(payload_additions_src):
        with open(payload_additions_src, "r") as f:
            payload_additions_content = f.read().rstrip() + "\n"

    copied = _copy_tree(
        PAYLOAD_DIR,
        target_dir,
        overwrite=overwrite,
        skip_if_exists=skip_if_exists,
    )
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
            f.write(wrapped_additions)
        print("Created: AGENTS.md from AGENTS-additions.md")
        applied = True
    else:
        with open(agents_md_dst, "r") as f:
            existing = f.read()

        replaced = _replace_additions_block(existing, wrapped_additions)
        if replaced is not None:
            if replaced != existing:
                with open(agents_md_dst, "w") as f:
                    f.write(replaced)
                print("Updated: AGENTS-additions.md block in AGENTS.md")
            else:
                print("Skipped: AGENTS-additions.md already up to date")
            applied = True
        elif (ADD_MARKER_START in existing) or (ADD_MARKER_END in existing):
            print("Skipped: AGENTS-additions.md has partial markers")
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
        "scripts/setup-exchange.sh",
        "scripts/gitx-wrapper.sh",
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
        "--overwrite",
        action="store_true",
        help="Overwrite existing kit files in the target directory.",
    )
    parser.add_argument(
        "--overwrite-keep-todo",
        action="store_true",
        help="Overwrite existing kit files, except docs/process/TODO.md.",
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

    if args.overwrite and args.overwrite_keep_todo:
        raise RuntimeError("Use only one of --overwrite or --overwrite-keep-todo.")

    overwrite = args.overwrite or args.overwrite_keep_todo
    skip_if_exists = set()
    if args.overwrite_keep_todo:
        skip_if_exists.add("docs/process/TODO.md")

    if args.keep_additions:
        # Install first, then restore the additions file if we delete it.
        install_payload(
            target_dir,
            overwrite=overwrite,
            skip_if_exists=skip_if_exists,
        )
        # If the file was removed by the installer, put it back from the kit payload.
        payload_additions_src = os.path.join(PAYLOAD_DIR, "AGENTS-additions.md")
        additions_dst = os.path.join(target_dir, "AGENTS-additions.md")
        if os.path.isfile(payload_additions_src) and (not os.path.isfile(additions_dst)):
            shutil.copy2(payload_additions_src, additions_dst)
            print("Restored: AGENTS-additions.md (--keep-additions)")
    else:
        install_payload(
            target_dir,
            overwrite=overwrite,
            skip_if_exists=skip_if_exists,
        )
    print("\n✅ repo-agent-pm installed.")
    print("\nWhere to start:")
    print("- Process overview: docs/README.md")
    print("- Guided install (optional): ./scripts/run-prompt installer")
    print("- Local Exchange (optional): docs/process/local-exchange.md")


if __name__ == "__main__":
    main()
