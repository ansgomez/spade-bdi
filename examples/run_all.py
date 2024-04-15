import subprocess

examples = [
    "basic",
    "actions",
    "counter",
    "sender_receiver",
    "master_slave",
    "ask_how",
    "send_achieve",
    "send_achieve_param",
    "tell_belief",
    "tell_how",
    "unachieve_no_recursive",
    "unachieve_while",
    "untell",
    "untell_how",
]
if __name__ == "__main__":

    for example in examples:
        l = 20 + len(example)
        print(l*"*" + "\n" + f"* Running {example} example *" + "\n" + l*"*")
        # Run example using subprocess
        subprocess.call(args=["python", "run_example.py"],
                        cwd=f"./{example}")
        print("Finished {}".format(example))
