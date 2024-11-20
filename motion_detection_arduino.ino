int ledPin = 12; // Pin for the LED

void setup() {
  pinMode(ledPin, OUTPUT); // Set pin as output
  Serial.begin(9600);      // Start serial communication
}

void loop() {
  if (Serial.available() > 0) {
    char motionDetected = Serial.read(); // Read from serial
    if (motionDetected == '1') {
      digitalWrite(ledPin, HIGH);  // Turn LED on
      delay(100);                  // Keep it on for 100 ms
      digitalWrite(ledPin, LOW);   // Turn LED off
    }
  }
}
