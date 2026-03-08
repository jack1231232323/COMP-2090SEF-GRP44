# comp-2090SEF-Group-
# Mahjong Table Management System

A desktop application for managing mahjong table bookings and player accounts. Built with “Python” and “Tkinter”, this system provides table session tracking, account balance management, and session control.

---
## Contents
- [Code Analysis](#code-analysis)
- [Features](#features)
- [System Requirement](#system-requirement)
- [Installation](#installation)
- [Architecture mapping](#architecture-mapping)
- [Design system](#design-system)
- [Configuration Documentation](#configuration-documentation)
- [User guide](#user-guide)
- [Admin Guide](#admin-guide)
- [Database schema](#database-schema)
- [Troubleshooting](#troubleshooting)

## Code Analysis
**class** 
(it is an account. It stores the name, secret password, and how much money user have. The check_password() method verifies they entered the correct password.)
-class User:
1. username (name of the player)
2. password_hash (secret password, encrypted)
3. balance (money in account)
4. check_password() (verify if password matches)

**Booking**
(one mahjong table session. It records which table, who is using it, how many hours they booked, when they started, and automatically calculates when they'll finish and how much it costs)
-class Session:
1. table_id ( table being used )
2. username ( who is using )
3. hours (3 hours or 6 hours)
4. start_time ( when started )
5. cost ( total price )
6. end_time_str ( when ended )

**Repository**
(it can store the user and session, creat account , save data when starts and save it to the file)
Repository (The Storage Manager):
1. Load data from file on startup
2. Add user (register)
3. Check user login
4. open table session
5.  Close table session
6.  Save all data to file

## Features

**User Management**
- register new account with username and password
- password using SHA-256 hashing
- track user funds with real-time updates
- secure authentication system

**Balance Management** 
- Top-up account balance with quick-amount buttons and custom amounts
- Real-time balance updates
- Validation for positive amounts only


**Session Tracking**
- Monitor active sessions and remaining balances
- all bookings stored in persistent database


**Table Management**
- Support for up to 4 concurrent mahjong sessions
- Visual indicators for available and in-use tables
- Open and close tables with cost calculation
- Choose from preset durations (3 hours = $30, 6 hours = $60)

**Admin Dashboard**
- Add , edit and deldete users from one interface
- force close table, reset table
- view and manage all bookings
- set pricing rate and manage data
- backup and reset system data

**Owner Authentication** 
- Only table owners can close their sessions

**Cost Transparency** 
- Instant cost calculation with balance validation

**Responsive Updates** 
- Real-time UI refresh after any action

## System Requirement
**Language**
-  Python 3.8+

**GUI Framework**
- Tkinter

**Library**
- 'tkinter' (UI)
- 'ttk' (styled widgets)
- 'hashlib' (password hashing)
- 'dataclasses' (domain models)
- 'json' and 'os' (data persistence)
- 'shutil' (file operation for backup)
- 'datatime'
**No external dependencies (uses only standard library)**

## Installation
- Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mahjong-table-management.git cd mahjong-table-management

## Architecture mapping
1. Data Layer
   DATA_FILE = "mahjong_data.json"
RATE_PER_HOUR = 10
TABLE_IDS = ["0001", "0002", "0003", "0004"]

2. Models Layer (data structure)
- class User
- class Booking

3. Persistence Layer (storage )
- class Repository

4. UI Helper Layer(styling , reusable)
- Colors
- Fonts
- Animations
- Effects

5. UI Window Layer (user interface)
- AuthWindow
- TopUpDialog
- TableCard
- OpenTableDialog
- Dashboard

## Code Structure
main codes/main pro/
- run.py (Application entry point)
- config.py (Configuration & constants)
- models.py (Data models (User, Booking)
- storage.py (Data persistence layer)
- UI.py (UI helper functions & styling)
- verify.py (Authentication window)
- dashboard.py (Main dashboard)
- admin.py (Admin panel)
- tabless.py(Table card component)
- opentable.py (Open table dialog)
- topup.py(Top-up dialog)
- mahjong_data.json(Data storage file)

## Design system
1. color
   <table>
    <tr>
      <th>Element</th>
      <th>Variable</th>
      <th>Color Code</th>
      <th>Usage</th>
    </tr>
    <tr>
      <td>Window Background</td>
      <td>BG_ROOT</td>
      <td>#1e1e1e</td>
      <td>Main app background</td>
    </tr>
    <tr>
      <td>Card Background</td>
      <td>BG_CARD</td>
      <td>#2d2d2d</td>
      <td>Dialogs, frames</td>
    </tr>
    <tr>
      <td>Hover State</td>
      <td>BG_HOVER</td>
      <td>#3d3d3d</td>
      <td>Hover effects</td>
    </tr>
    <tr>
      <td>Active State</td>
      <td>BG_ACTIVE</td>
      <td>#4a4a4a</td>
      <td>Active elements</td>
    </tr>
    <tr>
      <td>Primary Accent</td>
      <td>ACCENT</td>
      <td>#6b8cff</td>
      <td>Main buttons, headers</td>
    </tr>
    <tr>
      <td>Accent Hover</td>
      <td>ACCENT_H</td>
      <td>#5a7ae0</td>
      <td>Accent on hover</td>
    </tr>
    <tr>
      <td>Success</td>
      <td>SUCCESS</td>
      <td>#6fcf97</td>
      <td>Success messages, available</td>
    </tr>
    <tr>
      <td>Error</td>
      <td>ERROR</td>
      <td>#eb5757</td>>
      <td>Error messages, danger</td>
    </tr>
    <tr>
      <td>Warning</td>
      <td>WARNING</td>
      <td>#f2c94c</td>
      <td>Warning messages</td>
    </tr>
    <tr>
      <td>Primary Text</td>
      <td>TEXT</td>
      <td>#f0f0f0</td>
      <td>Main text</td>
    </tr>
    <tr>
      <td>Dim Text</td>
      <td>TEXT_DIM</td>
      <td>#a0a0a0</td>
      <td>Secondary text</td>
    </tr>
    <tr>
      <td>Border</td>
      <td>BORDER</td>
      <td>#404040</td>
      <td>Borders, dividers</td>
    </tr>
  </table>

2. fonts
<table>
    <tr>
      <th>Element</th>
      <th>Font</th>
      <th>Size</th>
      <th>Weight</th>
    </tr>
    <tr>
      <td>Page Title</td>
      <td>Segoe UI</td>
      <td>19px</td>
      <td>Bold</td>
    </tr>
    <tr>
      <td>Heading</td>
      <td>Segoe UI</td>
      <td>14px</td>
      <td>Bold</td>
    </tr>
    <tr>
      <td>Body Text</td>
      <td>Segoe UI</td>
      <td>11px</td>
      <td>Normal</td>
    </tr>
    <tr>
      <td>Button Text</td>
      <td>Segoe UI</td>
      <td>11px</td>
      <td>Bold</td>
    </tr>
    <tr>
      <td>Small Text</td>
      <td>Segoe UI</td>
      <td>9px</td>
      <td>Normal</td>
    </tr>
    <tr>
      <td>Technical</td>
      <td>Courier New</td>
      <td>11px</td>
      <td>Bold</td>
    </tr>
  </table>

## Configuration Documentation

**Configuration 1**
- variable name: DATA_FILE
- type: String
- Default Value:	"mahjong_data.json"
- Format: JSON

**configuration 2**
- Variable Name:	RATE_PER_HOUR
- Type:	Integer
- Default Value:	10
- Currency: Yuan (¥)
- Unit:	Per hour
- Purpose:	Base pricing for table sessions

**configuration 3**
- Variable Name:	TABLE_IDS
- Type:	List of Strings
- Default Value:	["0001", "0002", "0003", "0004"]
- Format:	4-digit strings
- Count:	4 tables
- Purpose:	All available table identifiers

## User guide
**register**
1. user see two pages (login and register) and the management system
2. user click 'register'
3. enter name and password
4. confirm password
5. click register button
6. account requirment:
- Username at least 2 characters
- Password at least 4 characters
- Passwords match
- Username doesn't exist
7. user created successful and save to file
8. switch to the page of the management system
**login**
1. open the "Login" tab
2. Type your username
3. Type your password
4. Click "Login" button
5. successful:
- AuthWindow closes
- Dashboard appears
- You see your username in header
6. error:
- Red error message shows
- Check username and password

**Top-up**
1. User clicks "Top-Up" button in header
- TopUpDialog window opens
- Shows current balance
2. User can choose:
- Click quick amount button (¥30, ¥50, ¥100, ¥200)
- Type custom amount
3. System requirement:
- Amount is a number
- Amount is greater than 0
4. System adds to balance
5. System saves to file
6. Success message shown
**book table**
1. user will see 4 table
2. user can open table with green status
3. OpenTableDialog window opens
4. Shows table ID and current balance
5. User selects duration:
- 1 hour =  ¥10
- 2 hours = ¥20
- 3 hours = ¥30
- 6 hours = ¥60
6. Cost displays and updates
7. User clicks "Confirm"
8. System validates:
- Table not already in use
- not all tables in use
- User has enough balance
9. System deducts cost from balance
10. System creates Session record
11. System saves to file
12. Dialog closes
13. Dashboard refreshes
14. Table now shows "In Use"
**show the table details**
1. User looks at a table card
2. If table is "In Use":
3. table shows:
- Username and the table ID of who booked it
- Duration booked
- Total cost
- Estimated end time
  
**close the table**
You're on Dashboard
1. Look at your table marked with red border if owned by you)
2. See "Close Table" button (red)
3. Click "Close Table" button
4. Confirmation dialog appears:
- Title: "Confirm Close"
- Message: "Close Table 000X?"
- Buttons: Yes/No
5. Click "Yes" to close
If successful:
- Success dialog shows: "Table 0001 closed"
- Dashboard refreshes
- Table card updates:
- Badge: "Available" (green)
- Button: "Open Table" (green)
If you click "No":
- Nothing changes
- Dialog closes

## Admin Guide
**login the admin**
1. Username: admin
2. Password: admin123
3. Dashboard switches to Admin Dashboard
4. 4 Tabs available at the top

**Tab1: User management**
1. View Users:
- showing all the registered users
- double-click to edit
2. Add New User:
- enter new username
- enter new password
- set the balance
- click "CREATE USER"
3.Edit user:
- change balance (number)
- change password
- click "SAVE CHANGE"
4.Delete User:
- cLick "DELETE SELECTED"button
- confirm
- user removed
- cannot remove admin user

**Tab2: Table management**
1. View Tables:
- showing all 4 tables(Table ID, status and username,hours,cost,start time)
2. Force Close Table:
- click "Force Close"
- confirm
- table session ends
- table becomes available
3. Reset Table:
- click "RESET ATBLE" on any table
- clears any pending bookings
- reset table to clean state

**Tad3: Booking Management**
1. View All Bookings:
- Table of all active bookings
- table,user,hours,cost,start time,end time,actions
2. Close Specific Booking:
- click on booking row
- confirm
- click "Yes"
- booking removed from system
3. Clear All Bookings:
- click "CLEAR ALL BOOKINGS"
- WARNING appears
- confirm
- all bookings deleted
- all table become avaialable
4. View Booking Statistic:
- click "VIEW STATISTIC"
- show total user,bookings and revenue

**Tab4: System Settings
1. Rate Configuration:
- edit "Hourly Rate ($)"field
- enter new rate
- click "UPDATE RATE"
2. Backup Data:
- click "BACKUP DATA"
- creates file
- saved in same directory
- success message displays
3. Restore Data:
- click "RESTORE DATA"
- file browser opens
- select backup JSON file
- click "Open"
- Data restored from backup
- system refreshes
4.Reset All Data
- click "RESET ALL DATA"
- first and final warning
- data cleared
- test data recreated
- system reset


## Database Schema
1. data file: mahjong_data.json
```conf
{
  "users": {
    "username1": {
      "username": "username1",
      "password_hash": "sha256_hash_here",
      "balance": 100.50
    },
    "username2": {
      "username": "username2",
      "password_hash": "sha256_hash_here",
      "balance": 75.00
    }
  },
  "bookings": {
    "0001": {
      "table_id": "0001",
      "username": "username1",
      "hours": 3,
      "start_time": "2026-03-08T14:30:00.123456",
      "cost": 30
    }
  }
}
{
  "users": {
    "username1": {
      "username": "username1",
      "password_hash": "sha256_hash_here",
      "balance": 100.50
    },
    "username2": {
      "username": "username2",
      "password_hash": "sha256_hash_here",
      "balance": 75.00
    }
  },
  "bookings": {
    "0001": {
      "table_id": "0001",
      "username": "username1",
      "hours": 3,
      "start_time": "2026-03-08T14:30:00.123456",
      "cost": 30
    }
  }
}
```
2. User Object Structure
- username(string)
- password_hash(string)
- balance(float)

3. Booking Object Strycture
- table_id(string)
- username(string)
- hours(integer)
- start_time(string)
- cost(float)

## Troubleshooting
**No module named'tkinter'**
```conf
# Windows
python -m pip install --upgrade python

# macOS
brew install python-tk@3.10

# Linux (Debian/Ubuntu)
sudo apt-get install python3-tk

# Linux (Fedora/RHEL)
sudo dnf install python3-tkinter
````
**Can't Login**
1. check username spelling
2. verify password is correct
3. register new account if forgotten password

**Balance Not Updating**
1. Close and reopen it
2. CHeck mahjong_data.json file
3. verify file permissions are correct
4. try top-up again

**Table Won't Open**
- add more fund
- check if cost exceeds balance
- verify balance in user account

**Admin Features Not Working**
- ensure looged in as admin
- restart it

**Data Loss**
- restore from backup file
- if not: restart it

## support
for issues or question:
- check the troubleshooting section
- review the user guide

  




