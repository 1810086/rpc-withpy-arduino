#include<Servo.h>
Servo base, thumb, index, mejure, ring, small;
int p;
int x = 2000;  //delay
void setup() {
  base.attach(8);
  thumb.attach(9);
  index.attach(10);
  mejure.attach(11);
  ring.attach(12);
  small.attach(13);
  
  base.write(0);
  thumb.write(0);
  index.write(0);
  mejure.write(0);
  ring.write(0);
  small.write(0);
  
  delay(x);

Serial.begin(9600);
}

void loop() {
  if(Serial.available()>0) {
     p=Serial.read();
    
    if(p=='1') {
rock();
    }
    
    else if(p=='2') {
paper();
    }
    
    else if(p=='3') {
scissor();
    }
  
  }
}


void rock() {
  base.write(180);
  thumb.write(0);
  index.write(0);
  mejure.write(0);
  ring.write(0);
  small.write(0);
  
  delay(x);
  
  base.write(0);
  thumb.write(0);
  index.write(0);
  mejure.write(0);
  ring.write(0);
  small.write(0);
  }

void paper() {
  base.write(180);
  thumb.write(180);
  index.write(180);
  mejure.write(180);
  ring.write(180);
  small.write(180);
  
  delay(x);
  
  base.write(0);
  thumb.write(0);
  index.write(0);
  mejure.write(0);
  ring.write(0);
  small.write(0);
  }

void scissor() {
  base.write(180);
  thumb.write(0);
  index.write(180);
  mejure.write(180);
  ring.write(0);
  small.write(0);
  
  delay(x);
  
  base.write(0);
  thumb.write(0);
  index.write(0);
  mejure.write(0);
  ring.write(0);
  small.write(0); 
  }
