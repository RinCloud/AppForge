from pathlib import Path
from typing import Dict
import os

def sumup_json(results: list[Dict]):
    """
    Calculate average values across multiple result dictionaries.
    
    This function takes a dictionary of task results and computes the average
    value for each metric across all tasks. The input should be structured
    with task IDs as keys and dictionaries of metrics as values.
    
    Args:
        results (Dict[int, Dict]): A dictionary where keys are task IDs and values
            are dictionaries containing metric names and their values.
            
    Returns:
        Dict[str, float]: A dictionary with metric names as keys and their
            average values across all tasks as values.
            
    """
    sum_results = {}
    for i in results.keys():
        for j in results[i]:
            if j not in sum_results:
                sum_results[j] = 0
            sum_results[j] += results[i][j]
    for j in results[i]:
        sum_results[j] /= len(results.keys())
    return sum_results

def remove_directory(path: Path):
    """
    Recursively remove a directory and all its contents.
    
    This function safely deletes a directory by first removing all files
    and subdirectories within it, then removing the directory itself.
    It handles nested directory structures recursively.
    
    Args:
        path (Path): The path to the directory to be removed.

    """
    if path.exists() and path.is_dir():
        for child in path.iterdir():
            if child.is_file():
                child.unlink()
            else:
                remove_directory(child)
        path.rmdir()

def compare_folder(folderA:Path, folderB:Path):
    """
    Compare two folders and identify files that differ or are new.
    
    This function recursively compares the contents of two folders and returns
    a dictionary of files that are either new in folderA or have different
    content compared to folderB. Only text files that can be read as UTF-8
    are considered in the comparison.
    
    Args:
        folderA (Path): The source folder to compare (typically newer version).
        folderB (Path): The target folder to compare against (typically baseline).
        
    Returns:
        Dict[str, str]: A dictionary where keys are relative file paths (relative
            to folderA) and values are the file contents from folderA. The dictionary
            includes files that exist in folderA but not in folderB, or files that
            have different content between the two folders.
            
    """
    changed: dict[str, str] = {}
    for root, _dirs, files in os.walk(folderA):
        for name in files:
            p = Path(root) / name
            rel = str(p.relative_to(folderA))
            src_file = folderB / rel

            try:
                new_text = p.read_text(encoding="utf-8")
            except Exception:
                continue

            if not src_file.exists():
                changed[rel] = new_text
            else:
                try:
                    old_text = src_file.read_text(encoding="utf-8")
                except Exception:
                    continue
                if new_text != old_text:
                    changed[rel] = new_text
    return changed
