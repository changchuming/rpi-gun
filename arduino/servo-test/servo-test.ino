
#include <Servo.h> 
#include <SoftwareSerial.h>

Servo myservo1;


void setup() 
{ 
  myservo1.attach(10);
//  myservo1.write(180);
  
} 

void loop() 
{
    myservo1.write(0);
    for (int angle = 0; angle <= 180; angle+=1)
    {
      myservo1.attach(10);
      myservo1.write(angle);
      delay(200);
      myservo1.detach();
      delay(2000);
      
    }
//    for (int angle = 180; angle>=150; angle-=1)
//    {
//      myservo1.write(angle);
//      delay(100);
//    }
//    for (int angle = 150; angle>=0; angle-=1)
//    {
//      myservo1.write(angle);
//      delay(20);
//    }
//    myservo1.write(0);
//    delay(2000);
//    myservo1.write(60);
//    delay(2000);
} 

