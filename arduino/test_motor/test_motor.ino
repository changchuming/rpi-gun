int motorControl = 9;

void setup() {
  // put your setup code here, to run once:
  pinMode(motorControl, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
    analogWrite(motorControl, 150);

    delay(1000);

    analogWrite(motorControl, 0);
    delay(1000);
}
