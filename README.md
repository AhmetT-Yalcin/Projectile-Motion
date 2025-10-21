# Projectile Motion Calculator
A desktop application for calculating and visualizing projectile trajectories in 3D space. Features user authentication, SQLite database storage for saved projectiles, and interactive matplotlib graphs.

### Features
* Trajectory Calculations: Calculate launch angles, time of flight, and trajectory paths for projectiles in 3D space
* User Authentication: Secure login system with password hashing (SHA-1)
* Database Storage: Save and retrieve projectile configurations using SQLite
* Interactive Visualization: Plot trajectory graphs using matplotlib
* User Management: Admin capabilities for creating users, resetting passwords, and managing accounts
* Multiple Solutions: Calculates both high-angle and low-angle trajectories with time recommendations

### Physics Calculations
The application computes:
* Launch angles (pitch) for hitting targets at different heights
* Horizontal direction (yaw) adjustments
* Time of flight for each trajectory
* Recommended optimal angle based on shortest time
* Full parabolic trajectory visualization

### Installation
Requirements
```
pip install tkinter
pip install customtkinter
pip install matplotlib
pip install numpy
```

### Default Login Credentials
* Admin User:
  Username: admin
  Password: admin
* Regular User:
  Username: ahmet
  Password: ahmet

⚠️ Important: Change these default passwords after first login!

### Usage
Basic Workflow
1. Login with your credentials
2. Enter projectile parameters:
 - Projectile name
 - Initial velocity (m/s)
 - Target coordinates (x, y, z in meters)
3. Calculate to see trajectory options
4. Save your projectile configuration for future use
5. Plot Graph to visualize the trajectory

### Admin Features
- Admins can access additional functions through the User Operations menu:
- Create new users
- Reset user passwords
- Delete users
- Change their own password
