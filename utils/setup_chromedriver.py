import os
import subprocess

def install_chrome_and_driver():
    if not os.path.exists("/usr/bin/google-chrome"):
        subprocess.run(["apt-get", "update"])
        subprocess.run(["apt-get", "install", "-y", "wget", "curl", "gnupg", "unzip"])
        subprocess.run(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"])
        subprocess.run(["apt", "install", "-y", "./google-chrome-stable_current_amd64.deb"])

    if not os.path.exists("/usr/bin/chromedriver"):
        subprocess.run(["wget", "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip"])
        subprocess.run(["unzip", "chromedriver_linux64.zip"])
        subprocess.run(["mv", "chromedriver", "/usr/bin/chromedriver"])
        subprocess.run(["chmod", "+x", "/usr/bin/chromedriver"])
