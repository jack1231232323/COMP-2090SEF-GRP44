# comp-2090SEF-Group-
# Mahjong Table Management System

A desktop application for managing mahjong table bookings and player accounts. Built with “Python” and “Tkinter”, this system provides table session tracking, account balance management, and session control.


## Features

**User Management**
- register new account with username and password
- password using SHA-256 hashing

**Balance Management** 
- Top-up account balance with quick-amount buttons and custom amounts
- Real-time balance updates
- Validation for positive amounts only


**Session Tracking**
- Monitor active sessions and remaining balances


**Table Management**
- Support for up to 4 concurrent mahjong sessions
- Visual indicators for available and in-use tables
- Open and close tables with cost calculation
- Choose from preset durations (3 hours = $30, 6 hours = $60)

**Dashboard**
- Overview of all table (Available / Using)
- User information display (username and balance)
- Value-Added Shortcut

**Owner Authentication** 
- Only table owners can close their sessions

**Cost Transparency** 
- Instant cost calculation with balance validation

**Responsive Updates** 
- Real-time UI refresh after any action

## Installation

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
- 'datetime' (session timing) 

**No external dependencies (uses only standard library)**
- Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mahjong-table-management.gitcd mahjong-table-management
python mahjong_system.py
