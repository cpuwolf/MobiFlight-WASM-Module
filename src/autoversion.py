# update version string in the project
import argparse
import os
import re

def update_version(new_version):
    # Use the script's location as the base path
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Definitions using explicit group references ${1} to prevent digit collision
    targets = [
        {
            "path": os.path.join(base_dir, "PackageDefinitions", "mobiflight-event-module.xml"),
            "pattern": r'(<AssetPackage Version=")([^"]+)',
            "repl": rf'\g<1>{new_version}'
        },
        {
            "path": os.path.join(base_dir, "PackagesExport", "mobiflight-event-module", "manifest.json"),
            "pattern": r'("package_version":\s*")([^"]+)',
            "repl": rf'\g<1>{new_version}'
        },
        {
            "path": os.path.join(base_dir, "PackagesExport", "mobiflight-event-module", "manifest.json"),
            "pattern": r'("LastUpdate":\s*"VERSION\s+)([^ ]+)',
            "repl": rf'\g<1>{new_version}'
        },
        {
            "path": os.path.join(base_dir, "Sources", "Code", "Module.cpp"),
            "pattern": r'(const char\*\s+version\s*=\s*")([^"]+)',
            "repl": rf'\g<1>{new_version}'
        }
    ]

    for target in targets:
        file_path = target["path"]
        if not os.path.exists(file_path):
            print(f"[-] File not found: {file_path}")
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Using \g<1> instead of \1 ensures digit-safety
            new_content, count = re.subn(target["pattern"], target["repl"], content)

            if count > 0:
                with open(file_path, 'w', encoding='utf-8', newline='') as f:
                    f.write(new_content)
                print(f"[+] Updated {count} occurrence(s) in: {os.path.relpath(file_path, base_dir)}")
            else:
                print(f"[!] No pattern match in: {os.path.relpath(file_path, base_dir)}")

        except Exception as e:
            print(f"[X] Error processing {file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update MobiFlight WASM Module version info.")
    parser.add_argument("version", help="New version string (e.g., 1.0.2)")
    
    args = parser.parse_args()
    update_version(args.version)