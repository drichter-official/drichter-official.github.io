# Advent Calendar - Raspberry Pi Setup

This branch is configured for deployment on a Raspberry Pi.

## Prerequisites

- Raspberry Pi (any model with network connectivity)
- Raspberry Pi OS (or similar Linux distribution)
- Python 3.10 or higher
- Internet connection

## Installation Steps

### 1. Update System
```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install Python and Dependencies
```bash
sudo apt install python3 python3-pip python3-venv git -y
```

### 3. Clone the Repository
```bash
cd ~
git clone https://github.com/drichter-official/calendar.git advent_calendar
cd advent_calendar
git checkout raspberry-pi
```

### 4. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Install Python Packages
```bash
pip install -r requirements.txt
```

### 6. Test the Application
```bash
cd website
python app.py
```

The app should now be running at `http://localhost:5000`

### 7. Setup as System Service (Optional - for auto-start on boot)

Create a systemd service file:
```bash
sudo nano /etc/systemd/system/advent-calendar.service
```

Paste the following (replace `YOUR_USERNAME` with your actual username):
```ini
[Unit]
Description=Advent Calendar Flask App
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/advent_calendar/website
Environment="PATH=/home/YOUR_USERNAME/advent_calendar/venv/bin"
ExecStart=/home/YOUR_USERNAME/advent_calendar/venv/bin/gunicorn --bind 0.0.0.0:8080 --workers 2 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable advent-calendar.service
sudo systemctl start advent-calendar.service
sudo systemctl status advent-calendar.service
```

### 8. Access from Other Devices

Find your Raspberry Pi's IP address:
```bash
hostname -I
```

Access the calendar from any device on your network:
```
http://YOUR_PI_IP:8080
```

## Managing the Service

### Start the service
```bash
sudo systemctl start advent-calendar.service
```

### Stop the service
```bash
sudo systemctl stop advent-calendar.service
```

### Restart the service
```bash
sudo systemctl restart advent-calendar.service
```

### Check status
```bash
sudo systemctl status advent-calendar.service
```

### View logs
```bash
sudo journalctl -u advent-calendar.service -f
```

## Troubleshooting

### Port already in use
If port 8080 is already in use, you can change it in the service file or Procfile.

### Permission issues
Make sure the user in the service file has read access to the application directory.

### Service won't start
Check the logs:
```bash
sudo journalctl -u advent-calendar.service -n 50
```

## Development Mode

For development with auto-reload:
```bash
cd website
python app.py
```

This will run on port 5000 with debug mode enabled.

## Production Deployment

The systemd service uses gunicorn for production deployment with:
- 2 worker processes
- Binding to all network interfaces (0.0.0.0)
- Port 8080
- Automatic restart on failure

## Updating the Application

```bash
cd ~/advent_calendar
source venv/bin/activate
git pull origin raspberry-pi
pip install -r requirements.txt --upgrade
sudo systemctl restart advent-calendar.service
```

## Security Notes

- Consider setting up a firewall (ufw) to restrict access
- Use nginx as a reverse proxy for HTTPS support
- Keep your Raspberry Pi OS and Python packages updated
- Change default passwords if using default Raspberry Pi credentials

