import shutil
from pathlib import Path
from typing import Set


def compare_directories(dir1: str, dir2: str):
    """Compare two directories and print differences without modifying files."""
    path1 = Path(dir1)
    path2 = Path(dir2)

    if not path1.exists() or not path1.is_dir():
        print(f"Source directory does not exist or is not a directory: {path1}")
        return

    if not path2.exists():
        print(f"Destination directory does not exist: {path2}")
        return

    files1: Set[Path] = {f.relative_to(path1) for f in path1.rglob("*") if f.is_file()}
    files2: Set[Path] = {f.relative_to(path2) for f in path2.rglob("*") if f.is_file()}

    missing = files1 - files2
    extra = files2 - files1
    common = files1 & files2

    print(f"Missing files to copy ({len(missing)}):")
    for m in sorted(missing):
        print(f"\t{m}")
    print(f"\nExtra files in destination ({len(extra)}):")
    for e in sorted(extra):
        print(f"\t{e}")
    print(f"\nCommon files ({len(common)}):")
    for c in sorted(common):
        print(f"\t{c}")


def sync_directories(dir1: str, dir2: str):
    path1 = Path(dir1)
    path2 = Path(dir2)

    if not path1.exists() or not path1.is_dir():
        print(f"Source directory does not exist or is not a directory: {path1}")
        return

    path2.mkdir(parents=True, exist_ok=True)

    files1: Set[Path] = {f.relative_to(path1) for f in path1.rglob("*") if f.is_file()}
    files2: Set[Path] = {f.relative_to(path2) for f in path2.rglob("*") if f.is_file()}

    missing = files1 - files2
    extra = files2 - files1

    print(f"Missing files to copy ({len(missing)}):")
    for m in sorted(missing):
        print(f"\t{m}")
    print(f"\nExtra files to delete in destination ({len(extra)}):")
    for e in sorted(extra):
        print(f"\t{e}")

    print("\nProceed to copy missing files and delete extra files? (y/n)")
    if input("> ").strip().lower() != "y":
        print("Aborted by user.")
        return

    copied = 0
    copy_failures = 0
    for rel in sorted(missing):
        src = path1 / rel
        dst = path2 / rel
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied += 1
        except Exception as exc:
            copy_failures += 1
            print(f"Failed to copy {src} -> {dst}: {exc}")

    deleted = 0
    delete_failures = 0
    for rel in sorted(extra):
        tgt = path2 / rel
        try:
            if tgt.exists() and (tgt.is_file() or tgt.is_symlink()):
                tgt.unlink()
                deleted += 1
                # try to remove empty parent directories up to path2
                parent = tgt.parent
                while parent != path2 and parent.exists():
                    try:
                        next(parent.iterdir())
                        break  # not empty
                    except StopIteration:
                        try:
                            parent.rmdir()
                            parent = parent.parent
                        except Exception:
                            break
        except Exception as exc:
            delete_failures += 1
            print(f"Failed to delete {tgt}: {exc}")

    print("\nSync complete.")
    print(f"Copied: {copied}, copy failures: {copy_failures}")
    print(f"Deleted: {deleted}, delete failures: {delete_failures}")
