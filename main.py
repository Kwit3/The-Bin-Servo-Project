from machine import Pin, I2C, PWM, ADC
import utime
from ssd1306 import SSD1306_I2C
import sys

# Display resolution
pix_res_x = 128
pix_res_y = 64

# Servo setup
servo_pin = Pin(15, Pin.OUT)
joystick_x = ADC(Pin(28))

pwm = PWM(servo_pin)
pwm.freq(50)

def set_servo_angle(angle):
    # Adjust the pulse width range based on your servo's requirements
    # Typical range is 500 to 2500 microseconds
    min_duty = 1600 # Adjust these values if necessary
    max_duty = 8000  # Adjust these values if necessary
    duty = int((angle / 180 * (max_duty - min_duty)) + min_duty)
    pwm.duty_u16(duty)

def read_joystick_x():
    return joystick_x.read_u16()

def init_i2c(scl_pin, sda_pin):
    # Initialize I2C device
    i2c_dev = I2C(1, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=200000)
    i2c_addr = [hex(ii) for ii in i2c_dev.scan()]
    
    if not i2c_addr:
        print('No I2C Display Found')
        sys.exit()
    else:
        print("I2C Address      : {}".format(i2c_addr[0]))
        print("I2C Configuration: {}".format(i2c_dev))
    
    return i2c_dev

def display_angle(oled, angle):
    # Clear the display
    oled.fill(0)
    # Display the angle of the servo
    oled.text("Servo Angle:", 5, 5)
    oled.text(f"{angle:.2f} degrees", 5, 15)
    oled.show()

def main():
    i2c_dev = init_i2c(scl_pin=27, sda_pin=26)
    oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev)

    # Main loop for joystick and servo control
    while True:
        # Read joystick value
        joystick_value = read_joystick_x()

        # Map joystick value (0-65535) to angle (0-180 degrees)
        angle = (joystick_value / 65535) * 180

        # Set servo angle
        set_servo_angle(angle)

        # Display the angle on the OLED
        display_angle(oled, angle)

        # Small delay to reduce jitter
        utime.sleep(0.1)

if __name__ == '__main__':
    main()
