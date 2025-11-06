// Bussystems and Sensors Wintersemester 2025-2026
// Prof. Dr. Rasmus Rettig
// HW Setup: Sensor-Arduino: GND-GND (black), VCC-5V (red), Aout-A0 (yellow)

int DistanceVoltage = 0;

void setup() {
  Serial.begin(19200); // open serial port, set the baud rate to 19200 bps
}
void loop() {
  int counter=0;
  DistanceVoltage=analogRead(A0);
  delay(5);
  Serial.println(DistanceVoltage);
  delay(5);
}
