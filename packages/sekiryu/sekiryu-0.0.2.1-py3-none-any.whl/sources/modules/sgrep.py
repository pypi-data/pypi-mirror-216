import subprocess, xmlrpc.client, os, re

def find_vulnerabilities(input):
    GREEN = '\033[32m'
    print("Performing analysis with Semgrep")
    proxy = xmlrpc.client.ServerProxy('http://localhost:13337')
    # Step 1: Store the pseudo code source dictionary in the "buffer" variable
    buffer = proxy.rec_decomp()

    filename = input
    regex_pattern = r"\.[^.]+$"
    stripped_filename = re.sub(regex_pattern, "", filename)
    filename = str(stripped_filename)+"_pcode.c"

    # Step 2: Execute Semgrep with the desired rules
    current_script_path = os.path.abspath(__file__)
    current_script_dir = os.path.dirname(current_script_path)
    rules_folder = os.path.join(current_script_dir, "rules_sgrep")  # Specify the subfolder containing your rules

    subprocess.run(["semgrep", "--config", str(rules_folder), str(filename)], capture_output=False, text=True)
