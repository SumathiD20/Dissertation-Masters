# Dissertation - Masters in DevOps (30 Credits)
Mitigating Thermal Side-Channel Attacks in Data Centres: A Secure Operational Pipeline Framework for Privacy-Preserving Environmental Sensor Data 

## Description
Data centers are critical for cloud services but face overlooked physical security risks. When someone opens the door to enter, the room’s temperature drops slightly (cold air escapes) and then rises (the cooling system adjusts). Hackers can monitor these tiny temperature changes to guess when someone enters the room, which is a security risk. Attackers could exploit this to infer unauthorized access, bypassing traditional security systems. Current temperature monitoring tools prioritize real-time alerts and efficiency but lack safeguards to hide these subtle patterns. While methods exist to block digital side-channel leaks (e.g., power or sound), thermal data leaks in data centers remain unaddressed. Standards like NIST SP 800-53 and ISO 27001 focus on broad physical security but offer no specific guidance for securing temperature data against inference attacks.

## Problem Statement
This research solves a critical gap: securing temperature data to prevent leaks about human activity without disrupting monitoring. Existing systems fail to mask sensitive thermal fluctuations (e.g., door openings) or encrypt/control access to this data. Using heat probes, the project designs a software-driven pipeline that hides actionable leaks via privacy techniques (e.g., noise injection), enforces encryption/access controls, and detects tampering, all while complying with industry standards. The goal is to stop attackers from exploiting heat data to breach data centers, balancing security and operational needs.


