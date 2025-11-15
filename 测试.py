import subprocess

def run(cmd):
    # bandit 会标这个为高危
    subprocess.call(cmd, shell=True)
