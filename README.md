## COMP2090 GRP 44 PROJECT
## Mahjong Table Manager

A simple desktop app to manage mahjong table bookings.  
Players can top up their balance, open a table for a chosen number of hours, and close it when they’re done.  
The admin has full control over users, tables, rates, and data backups.

---

## Features

- **User accounts** – register / login with username and password
- **Add funds** – top up your balance with preset or custom amounts
- **Book a table** – choose 1–4 hours, see the cost, and pay from your balance
- **Your tables** – only the person who booked a table can close it
- **Admin panel** – manage users, force‑close tables, change hourly rate, backup/restore data
- **Data persistence** – everything is saved in a `mahjong_data.json` file

---

## How to run

1. Make sure you have **Python 3** installed.  
   (Tkinter is included with standard Python installations.)

2. Open a terminal / command prompt in the program’s folder.

3. Run the main script:

   ```bash
   python main.py
   ```

No extra libraries are needed – only the Python standard library.

---

## First time login

When you start the app for the first time, it creates an **admin** account automatically.

- **Username:** `admin`  
- **Password:** `admin123`

You can use this admin account to add other users, change settings, or just explore.

> The data file `mahjong_data.json` is created in the same folder.  
> If you delete it, the app will recreate the admin account on the next run.

---

## Regular user – what you can do

After logging in (or registering a new account), you see the **dashboard** with all 4 tables.

## Top up your balance

Click the **Top Up** button at the top.  
You can pick a quick amount ($30, $50, $100, $200) or type a custom number.  
Your balance updates immediately.

## Open a table

- Find a table marked **🟢 Available**.
- Click **Open Table**.
- Choose how many hours (1–4). The total cost is shown.
- If you have enough balance, confirm – the table becomes yours and the money is deducted.

## Close your own table

When a table is booked by you, it shows **🔴 In Use**.  
You will see a **Close Table** button.  
Click it, confirm, and the table becomes available again.  
No money is returned – you pay for the hours you booked.

> You cannot close a table that was booked by another user.

---

## Admin panel

When you log in as `admin` (or any user with admin rights – currently only `admin`), you get a separate admin window.

## Users tab

- **Add** – create a new user with an initial balance.
- **Edit** – change a user’s balance or password (leave password blank to keep it).
- **Delete** – remove a user. Their active bookings are also deleted.
- You cannot delete the `admin` user.

## Tables tab

Shows every table and its current status (available or in use).  
If a table is occupied, you can **Force Close** it – this removes the booking without refunding the user.  
The **Reset** button does the same for an occupied table (or does nothing if the table is already free).

## Bookings tab

A list of all active bookings. You can **Clear All** to remove every booking at once.

## Settings tab

- **Hourly Rate** – change how much 1 hour costs (default is $10). The new rate applies to future bookings.
- **Backup Data** – saves a copy of `mahjong_data.json` with a timestamp.
- **Restore Data** – load a previously saved backup file.
- **Reset All** – deletes all users (except a fresh admin) and all bookings. Use with care.

At the bottom of the Settings tab you see quick stats: total users, active bookings, and total revenue from current bookings.

---

## Customisation

You can edit the file `config.py` to change:

- `rateperhour` – default hourly price
- `tableids` – list of table IDs (must be 4 items)
- Colours, fonts, window sizes – look for variables like `bgroot`, `accent`, `fonttitle`, etc.

After changing `config.py`, restart the app.

---

## Troubleshooting

- **I forgot my password** – only an admin can change it for you. Ask your admin or, if you are the admin, edit your own password in the admin panel.
- **The app won’t start** – make sure you are in the correct folder and using `python main.py`.  
  If you get “Tkinter not found”, install it (on Linux: `sudo apt install python3-tk`).
- **My balance is not updating** – try clicking **Refresh** in the admin panel, or restart the app.  
  The dashboard updates automatically after every top‑up or table action.

---

