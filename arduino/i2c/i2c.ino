#include <Wire.h>
#include <Servo.h> 
#include <SoftwareSerial.h>
#define SLAVE_ADDRESS 0x04

// Servo
Servo pan_servo;
Servo tilt_servo;
int pan_pin = 10;
int tilt_pin = 11;

// Pan tilt angles
int pan_angle = 90;
int tilt_angle = 60;
int encoded_thetas = 0;
int pan_theta = 0;
int tilt_theta = 0;
int motorControl = 9;
int count = 0;

void setup() {
  // Set up I2C
//  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receive_data);
  Wire.onRequest(send_data);
//  Serial.println("Ready!");
  pinMode(motorControl, OUTPUT);
  pan_servo.attach(pan_pin);
  tilt_servo.attach(tilt_pin);
  pan_servo.write(pan_angle);
  tilt_servo.write(tilt_angle);
  delay(1000);
}

void loop() {
  delay(200);
  if (count > 0) {
    count++;
  }
  if (count > 3) {
    count = 0;
    digitalWrite(motorControl, LOW);
    int pan_angle = 90;
    int tilt_angle = 60;
    pan_servo.attach(pan_pin);
    tilt_servo.attach(tilt_pin);
    pan_servo.write(pan_angle);
    tilt_servo.write(tilt_angle);  
    delay(2000);
  }
  pan_servo.detach();
  tilt_servo.detach();
}

void receive_data(int byte_count) {
//  Serial.print("receive_data");
  while (Wire.available()) {
    // Read encoded pan tilt thetas
    encoded_thetas = Wire.read();
//    Serial.print("Data received: ");
//    Serial.println(encoded_thetas);
    
    // Pan and tilt thetas are encoded such that encoded_thetas = (pan_theta+8)*16+(tilt_theta+8)
    // Pan and tilt thetas are in the range [-7, 7]
    if (encoded_thetas == 0) {
      run_motor();
    } else {
      pan_theta = encoded_thetas/16 - 8;
      tilt_theta = encoded_thetas%16 - 8;
//      Serial.println(pan_theta);
//      Serial.println(tilt_theta);
      pan_angle-=pan_theta;
      tilt_angle+=tilt_theta;
      if (pan_angle > 180) {pan_angle = 180;}
      if (pan_angle < 0) {pan_angle = 0;}
      if (tilt_angle > 180) {tilt_angle = 180;}
      if (tilt_angle < 0) {tilt_angle = 0;}
      
      // Servo
      pan_servo.attach(pan_pin);
      tilt_servo.attach(tilt_pin);
      pan_servo.write(pan_angle);
      tilt_servo.write(tilt_angle);  
    }  
  }
}

void send_data() {
  Wire.write(encoded_thetas);
}

// Run motor to shoot water
void run_motor() {
//  Serial.println("Run motor!");
  digitalWrite(motorControl, HIGH);
  count = 1;
}

