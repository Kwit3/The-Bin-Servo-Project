#include <Servo.h>

// Define the pins
const int joystickXPin = 26; // GP26 (ADC0)
const int joystickYPin = 27; // GP27 (ADC1)
const int joystickSWPin = 15; // GP15 (Button)
const int servoPin = 0; // GP0 for the servo

Servo myservo; // create servo object to control a servo

void setup() {
  // Initialize the servo
  myservo.attach(servoPin);

  // Initialize the joystick button pin as input
  pinMode(joystickSWPin, INPUT_PULLUP);

  // Start serial communication
  Serial.begin(9600);
}

void loop() {
  // Read the joystick values
  int xValue = analogRead(joystickXPin);
  int yValue = analogRead(joystickYPin);
  int buttonState = digitalRead(joystickSWPin);

  // Map the joystick X value to servo position (0 to 180)
  int servoPos = map(xValue, 0, 4095, 0, 180);
  myservo.write(servoPos);

  // Print values to serial monitor for debugging
  Serial.print("X: ");
  Serial.print(xValue);
  Serial.print(" Y: ");
  Serial.print(yValue);
  Serial.print(" Button: ");
  Serial.println(buttonState);

  delay(50);
}
