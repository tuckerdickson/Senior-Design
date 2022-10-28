int outputPin = 8;
int analogPin = A5;
int reading = 0;
int count;

void setup() {
  Serial.begin(115200);
  pinMode(outputPin, INPUT);           // set pin to input
  digitalWrite(outputPin, LOW);       // turn on pullup resistors
}

void loop() {
  count = 0;
  
  for(int i = 0; i < 100; i++){
    reading = analogRead(analogPin);  // read the input pin
    Serial.println(reading);          // debug value

    if(reading < 10) {
      count++;  
    }
  }

  if(count > 90) {
    digitalWrite(outputPin, HIGH);
  }
  else {
    digitalWrite(outputPin, LOW);
  }
//  int count = 0;
//  for (int i = 0; i < 10; i++) {
//    delay(1000);
//  }
//  Serial.print(count);
//  count++;
}
