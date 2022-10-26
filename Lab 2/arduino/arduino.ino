void setup() {
  Serial.begin(115200);

}

void loop() {
  int count = 0;
  for (int i = 0; i < 10; i++) {
    delay(1000);
  }
  Serial.print(count);
  count++;
}
