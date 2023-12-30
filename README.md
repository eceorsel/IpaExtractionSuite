# IpaExtractionSuite

IpaExtractionSuite is a user-friendly tool designed for cybersecurity professionals, especially those involved in mobile application pentesting (penetration testing). It simplifies the process of extracting .ipa files (iOS app files) from jailbroken iPhones. This tool is particularly useful for professionals looking to understand the structure of iOS applications, analyze their jailbreak detection mechanisms, and investigate SSL pinning techniques.

Utilizing IpaExtractionSuite, pentesters can efficiently retrieve app files for further analysis using tools like Ghidra or Hopper. This facilitates deeper insights into how applications implement security measures, including jailbreak prevention and SSL pinning, thereby aiding in a more thorough security analysis.

The tool streamlines the initial steps of app extraction, allowing pentesters to focus more on the analytical aspects of their work. Whether for investigating an app's security features or preparing for a detailed security audit, IpaExtractionSuite provides an efficient approach to obtain the necessary .ipa files.

## Usage

1. **SSH Forwarding Over USB:**
Set up usbmuxd/iproxy for SSH forwarding over USB. By default, it forwards local port 2222 to remote port 22.
   
``` iproxy 2222 22 ```


2. **Running IpaExtractionSuite:**
Execute the script with the following command:

``` python3 IpaExtractionSuite.py ```


https://github.com/eceorsel/IpaExtractionSuite/assets/22567896/8dd2bf97-3004-4619-9e0e-d3f7646e587d

