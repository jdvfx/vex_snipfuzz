import subprocess

class YourClass:
    def copy_to_clipboard(self, text: str):
        subprocess.run(['echo', '-n', text], stdout=subprocess.PIPE)
        subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode('utf-8'))

# Example usage:
your_instance = YourClass()
text_to_copy = "OOO"
your_instance.copy_to_clipboard(text_to_copy)
