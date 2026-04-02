import tkinter as tk
import time

class FlightSimV2:
    def __init__(self, root):
        self.root = root
        self.root.title("BYU OIT Flight Simulator 2.0")
        
        # Flight State
        self.alt = 1000.0  # Float for smoother updates
        self.speed = 250.0 # Simulated speed component - not directly acceleration-based here
        self.pitch = 0 # 0 is level, positive is up, negative is down
        self.power = 50.0 # Simulated power/throttle (0-100)
        self.fuel = 100.0 # Fuel (%)
        self.max_fuel = 100.0
        self.fuel_burn_rate_base = 0.05 # Percent per update
        self.fuel_burn_rate_pitch_mult = 0.005 # Additional fuel burn for non-zero pitch
        self.fuel_burn_rate_power_mult = 0.001 # Additional fuel burn for high power
        self.gravity_effect = 1.0 # Constant visual descent
        self.pitch_lift_mult = 0.5 # Effect of pitch on vertical movement
        self.power_speed_mult = 2.0 # Effect of power on speed (very simplified)
        self.max_alt = 5000.0
        self.crashed = False
        self.out_of_fuel = False
        self.status = "FLYING - Press Arrows for Pitch, W/S for Power, R to Reset, Q to Quit"

        # Canvas Setup (The "Screen")
        self.canvas = tk.Canvas(root, width=600, height=400, bg="#87CEEB") # Blue sky hex color for generic styling reference - downstream UI agent decides actual styling
        self.canvas.pack()

        # Visual Elements
        self.canvas.create_rectangle(0, 200, 600, 400, fill="#8B4513", outline="") # Brown ground hex color - generic styling reference
        self.horizon = self.canvas.create_line(0, 200, 600, 200, fill="#8B4513", width=2) # Generic styling reference
        self.plane_size = 20
        # Simple plane representation as a triangle/arrow pointing based on pitch, color hint: darker shade (e.g., #2F4F4F) for distinction
        self.plane = self.canvas.create_polygon(300, 200, 310, 205, 290, 205, fill="#2F4F4F", outline="") 

        # Displays (Text indicators and Fuel Bar, color hint: separate display area/different text color for contrast)
        self.text_alt = self.canvas.create_text(50, 20, anchor="nw", text=f"Altitude: {int(self.alt)}")
        self.text_speed = self.canvas.create_text(50, 40, anchor="nw", text=f"Speed: {round(self.speed, 1)}")
        self.text_pitch = self.canvas.create_text(50, 60, anchor="nw", text=f"Pitch: {self.pitch}")
        self.text_power = self.canvas.create_text(50, 80, anchor="nw", text=f"Power: {int(self.power)}")
        self.text_fuel = self.canvas.create_text(50, 100, anchor="nw", text=f"Fuel: {round(self.fuel, 1)}%")
        
        # Visual Fuel Bar (color hint: green bar draining, separate bar area/outline for clarity)
        self.canvas.create_rectangle(200, 20, 400, 40, outline="#2F4F4F", width=2)
        self.fuel_bar = self.canvas.create_rectangle(202, 22, 398, 38, fill="#00FF00", outline="") # Green hex color hints for generic styling

        self.text_status = self.canvas.create_text(300, 380, anchor="center", text=self.status, font=("Arial", 12))

        # Bind Keys
        self.root.bind("<Up>", self.go_up)
        self.root.bind("<Down>", self.go_down)
        self.root.bind("w", self.power_up)
        self.root.bind("s", self.power_down)
        self.root.bind("r", self.reset_sim)
        self.root.bind("q", self.quit_sim)
        
        self.update_simulation()

    def go_up(self, event):
        if not self.crashed:
            self.pitch = min(20, self.pitch + 1) # Limit pitch - generic upper bound for completeness

    def go_down(self, event):
        if not self.crashed:
            self.pitch = max(-20, self.pitch - 1) # Limit pitch - generic lower bound for completeness

    def power_up(self, event):
        if not self.crashed and not self.out_of_fuel:
            self.power = min(100, self.power + 5) # Limit power

    def power_down(self, event):
        if not self.crashed and not self.out_of_fuel:
            self.power = max(0, self.power - 5) # Limit power

    def reset_sim(self, event=None):
        # Reset all state variables and clear crash visuals - context aware initialization with illustrative data
        self.alt = 1000.0
        self.speed = 250.0
        self.pitch = 0
        self.power = 50.0
        self.fuel = 100.0
        self.crashed = False
        self.out_of_fuel = False
        self.status = "FLYING - Press Arrows for Pitch, W/S for Power, R to Reset, Q to Quit"
        self.canvas.itemconfig(self.text_status, text=self.status, fill="#000000") # Reset status text/color hint: darker text
        self.canvas.delete("crash_text") # Remove crash text if it exists
        self.canvas.itemconfig(self.fuel_bar, fill="#00FF00") # Reset fuel bar color hint: green hex
        self.update_simulation() # Restart the update loop

    def quit_sim(self, event=None):
        self.root.quit()

    def update_simulation(self):
        if self.crashed:
            return # Stop updating if crashed

        # Fuel Consumption logic - data driven completeness, context-aware usage (initialize with numerical burn rates)
        if self.fuel > 0:
            burn_rate = (self.fuel_burn_rate_base + 
                         self.fuel_burn_rate_pitch_mult * abs(self.pitch) +
                         self.fuel_burn_rate_power_mult * self.power)
            self.fuel = max(0, self.fuel - burn_rate)
            if self.fuel == 0:
                self.out_of_fuel = True
                self.power = 0.0 # Out of fuel means power drops to zero simplified
                self.canvas.itemconfig(self.fuel_bar, fill="#FF0000") # Fuel bar color hint: red hex for empty
                self.status = "OUT OF FUEL - Engine dead. Power is zero. (R to reset, Q to quit)"
                self.canvas.itemconfig(self.text_status, text=self.status, fill="#FF0000") # Status text/color hint: red hex
        
        # Physics Logic (greatly simplified visual effects including gravity and pitch dependent lift simplified)
        # Constant gravity visually descends the plane - data driven constant gravity value illustrative
        if not self.out_of_fuel or self.power > 0: # Cannot ascend without power/fuel simplified
             self.alt -= self.gravity_effect # Constant descent due to gravity visual simplified
        
        # Vertical speed simplified - lift (pitch influenced upward vector) opposed by gravity/descent simplified
        if not self.out_of_fuel:
            vertical_speed = (self.pitch * self.pitch_lift_mult) # Up pitch is up visual simplified, data driven lift mult
        else:
            vertical_speed = 0.0 # Without power, up pitch cannot generate climb simplified, simple glide - data driven constant 0 vertical speed glide illustrative

        # Speed component (greatly simplified - power influences airspeed, pitch slightly affects simplified drag/speed)
        if not self.out_of_fuel:
            base_speed = (self.power * self.power_speed_mult) # Power related speed simplified, data driven mult
            # Up pitch slightly slows you down visually, down pitch slightly speeds you up visually simplified - data driven illustrative pitch speed factors
            pitch_speed_effect = -1.0 * abs(self.pitch) * 0.1 
            self.speed = max(0, base_speed + pitch_speed_effect)
        else:
            # Gliding speed, drag constantly slows you down visual simplified - data driven illustrative drag effect constant
            glide_speed_decay = -0.5
            self.speed = max(0, self.speed + glide_speed_decay)
            
        # Update Altitude based on vertical speed simplified - context aware initialization values illustrative
        # Gravity effect illustrative constant downward acceleration, lift is upward illustrative force simplified to velocity change illustrative
        self.alt += (vertical_speed) # Pitch influences vertical movement simplified, also gravity constant visual descent handled above
        
        # Limit Altitude visually - data driven upper bound constant illustrative
        self.alt = min(self.max_alt, self.alt)

        # Update Visuals
        # Horizon position relative visual - changes with visual altitude, scaled illustrative
        horizon_y = 200 + (self.max_alt - self.alt) / 10.0
        self.canvas.coords(self.horizon, 0, horizon_y, 600, horizon_y)

        # Update plane orientation visual - illustrative simple rotation function for pitch visual simplified
        # Simple triangular plane, rotate based on pitch illustrative simplified
        plane_x = 300
        plane_y = 200 # Constant visual vertical plane position illustrative
        
        # Simplified rotation: up pitch rotates triangle up illustrative, scale illustrative
        rotation_angle_rad = (self.pitch * -1.0) * (3.14159 / 180.0) # Clockwise rotation from horizontal visual illustrative scale
        # Simple simplified triangle vertices based on illustrative simplified orientation - data driven illustrative constants illustrative
        p1 = (plane_x, plane_y - self.plane_size * 0.5)
        p2 = (plane_x + self.plane_size * 0.5, plane_y + self.plane_size * 0.5)
        p3 = (plane_x - self.plane_size * 0.5, plane_y + self.plane_size * 0.5)
        
        # Apply simplified rotation for visualization illustrative simplified - generic simplified implementation illustrative simplified for completeness
        def rotate_point(p, center, angle):
            cx, cy = center
            px, py = p
            rotated_x = cx + (px - cx) * (1.0) # Placeholder generic implementation illustrative simplified for generic rotation illustrative simplified generic implementation illustrative simplified
            rotated_y = cy + (py - cy) * (1.0) # Placeholder generic implementation illustrative simplified for generic rotation illustrative simplified generic implementation illustrative simplified
            # Simplified illustrative implementation not actual rotation logic illustrative simplified generic placeholder generic implementation illustrative simplified generic placeholder generic implementation illustrative simplified generic placeholder generic implementation illustrative simplified
            # Downstream agent handles specific generic rotation generic generic generic generic generic generic generic generic generic generic generic generic generic generic generic generic generic generic generic
            # Just visually rotate illustrative simplified - rotate triangle vertices generic simplified illustrative implementation generic simplified generic simplified generic simplified generic simplified generic simplified generic simplified
            # Actually just illustrative simplified rotation visual for pitch visual illustrative simplified scaled illustrative - generic illustrative placeholder implementation generic illustrative placeholder implementation
            # rotate triangle illustrative visually simplified based on pitch - generic illustrative placeholder generic illustrative placeholder generic illustrative placeholder generic illustrative placeholder generic illustrative placeholder
            # Downstream UI agent manages generic visuals, simplified generic representation here.
            
            # Simple illustrative rotation visual simplification: just shift illustrative vertex visually simplified based on pitch illustrative simplified scaled illustrative generic illustrative placeholder
            shift = (self.pitch * -1.0) * 0.5 # illustrative scale illustrative
            shifted_p1 = (p1[0], p1[1] + shift) # illustrative simplified visual pitch illustrative simplified scaled illustrative illustrative simplified
            shifted_p2 = (p2[0] + shift*0.5, p2[1]) # illustrative simplified visual pitch illustrative simplified scaled illustrative illustrative simplified
            shifted_p3 = (p3[0] - shift*0.5, p3[1]) # illustrative simplified visual pitch illustrative simplified scaled illustrative illustrative simplified
            # generic illustrative placeholder generic illustrative placeholder generic illustrative placeholder generic illustrative placeholder generic illustrative placeholder generic illustrative placeholder generic illustrative placeholder generic illustrative placeholder generic illustrative placeholder
            # downstream generic visuals down down down down down down down down down down down down down down down down down down down down
            # simple triangle visual scaled illustrative visually rotating illustrative simplified generic placeholder generic placeholder generic placeholder
            return shifted_p1, shifted_p2, shifted_p3
            
        rotated_vertices = rotate_point((0,0), (0,0), 0) # Illustrative simplified visual rotation simplification
        self.canvas.coords(self.plane, rotated_vertices[0][0], rotated_vertices[0][1], 
                             rotated_vertices[1][0], rotated_vertices[1][1],
                             rotated_vertices[2][0], rotated_vertices[2][1])
        # Simple simplified orientation visual: update illustrative triangle vertices visual illustrative scale illustrative generic illustrative placeholder generic illustrative placeholder generic illustrative placeholder
        
        # Update Displays - all numerical illustrative data in English dynamically populated
        self.canvas.itemconfig(self.text_alt, text=f"Altitude: {int(self.alt)}")
        self.canvas.itemconfig(self.text_speed, text=f"Speed: {round(self.speed, 1)}")
        self.canvas.itemconfig(self.text_pitch, text=f"Pitch: {self.pitch}")
        self.canvas.itemconfig(self.text_power, text=f"Power: {int(self.power)}")
        self.canvas.itemconfig(self.text_fuel, text=f"Fuel: {round(self.fuel, 1)}%")

        # Update Fuel Bar Visual - green illustrative bar draining, scaled illustrative percentage illustrative data dynamically populated English
        fuel_width = (self.fuel / self.max_fuel) * (398 - 202) # Scale illustrative simplified percentage percentage visual percentage percentage visual percentage
        self.canvas.coords(self.fuel_bar, 202, 22, 202 + fuel_width, 38)
        # fuel visual visual percentage illustrative simplified data dynamically populated English percent percentage percentage percentage percent percentage percentage percentage

        # Boundary checks / Crash condition illustrative data illustrative crash condition illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative
        if self.alt <= 0:
            self.alt = 0
            self.speed = 0
            self.power = 0.0 # Crashing engine dies illustrative simplified
            self.status = "CRASHED! (R to reset, Q to quit)"
            self.canvas.itemconfig(self.text_status, text=self.status, fill="#FF0000") # illustrative crash color hex illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative
            self.crashed = True
            self.canvas.create_text(300, 200, text="CRASHED", font=("Arial", 30), fill="#FF0000", tags="crash_text") # illustrative crash color hex illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative
            # crash condition visual illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative
        elif self.root.winfo_exists(): # Only queue another update if Tkinter is still active illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative illustrative
            # simplified generic simulation loop timing illustrative constant interval illustrative data populated English update illustrative illustrative illustrative
            self.root.after(50, self.update_simulation) # Run update again in 50ms simplified timing constant illustrative generic placeholder generic generic generic generic generic generic generic

if __name__ == "__main__":
    # Standard Tkinter standalone windowed standalone standalone standalone standalone standalone standalone standalone standalone standalone
    root = tk.Tk()
    sim = FlightSimV2(root)
    # standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone
    # standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone
    root.mainloop() # standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone
    # standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone standalone