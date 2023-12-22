# Spawncamp

*** As of Fall 2023, this script no longer works :( ***

Spawncamp is everyone's favorite tool to use during **first pass enrollment** at UCSD. It will automatically enroll you in one of the sections you specify when an opening is found and push a desktop notification for Windows and MacOS users.

Most useful for people with bad enrollment times and have to deal with full classes before even getting
a chance to enroll.

This thing actually got me a spot in CSE 151A lmao

## How it works

Spawncamp will use your Chrome cookies to make HTTP requests to Webreg's API to see if there are any openings in the course you specify. When an opening is found in one of the sections you specify, Spawncamp will enroll you in that section, if more than one section is open, Spawncamp will enroll you in whatever section (that you've specified) it wants.

## Setup

### Prerequisites:

Spawncamp assumes you satisfy all prerequisites to enroll in the specified course.

### Installation

1. Clone this repo onto your local machine 
2. Edit the script to monitor the class you're trying to get in.
3. Spawncamp will manage installing dependencies depending on your operating system :)

### Usage

1. Edit the script to monitor the class you're trying to get in.
   1. Section ID's can be found in the leftmost column of the course's Webreg listing.  
   ![rip](./assets/sectionid.png)
2. Sign into Webreg on Google Chrome, you may need to sign in again later when
   the cookies expire.
3. Close Chrome - Spawncamp can't access your cookies if Chrome is open.
You can reopen it after starting Spawncamp.
4. Run `python spawncamp.py` (or `python3 spawncamp.py`)
