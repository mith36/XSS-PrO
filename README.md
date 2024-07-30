![](https://img.shields.io/badge/Xss-automation-blue)
![](https://img.shields.io/badge/Bug-Bounty-orange)
![](https://img.shields.io/badge/VAPT-web-pink)
![](https://img.shields.io/badge/Web-Pentesting-green)

    
<h1 align="center"><font face="Arial">XSS_PrO</font></h1>

[@Medium](https://medium.com/@mithun_/how-i-created-my-first-xss-tool-xss-pro-bugbounty-982a16079baf)

XSS_PrO is a powerful tool designed to detect Cross-Site Scripting (XSS) vulnerabilities in web applications. It provides automated scanning capabilities to identify potential XSS vectors and vulnerabilities across web pages and forms.

# Features

- 100% Accurcate Result
- Less number of false possitive

# Requirements
    pip install -r requirements.txt

**Ensure Chrome Browser is installed on your system. if not, download and install.**
- Do wayback on the domain which you want to do xss testing
- Copy all the waybacked url to the urls.txt file
- Add your XSS payloads to payloads.txt

# Run

    python XSS_PRO.py --payloads payload.txt --urls url.txt

![image](https://github.com/user-attachments/assets/2f952022-736a-44a9-9d6f-8ff5ad951e80)


**Note:** The chrome driver attached is for windows. if you want to run on linux machine replace it with linux chrome driver and change the name in the code also.(line 11)

# If you’d like to contribute to its enhancement, you’re welcome to do so.

