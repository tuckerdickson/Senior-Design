int outputPin = 8;
int analogPin = A3;
int reading = 0;
int count;
int numSamples = 300;

void setup() {
  Serial.begin(115200);
  pinMode(outputPin, OUTPUT);           // set pin to input
  digitalWrite(outputPin, LOW);       // turn on pullup resistors
}

void loop() {
  count = 0;
  
  for(int i = 0; i < numSamples; i++){
    reading = analogRead(analogPin);  // read the input pin

    if(reading == 0) {
      count++;  
    }
  }

  if(count >= .98 * numSamples) {
    digitalWrite(outputPin, HIGH);
    Serial.println("Send Text");
  }
  else {
    digitalWrite(outputPin, LOW);
    Serial.println("Clear");
  }
}
