#include <ESP8266WiFi.h>



void setup() {
  Serial.begin(115200);

  String ssid = "AndroidAP";
  String password = "Ryno2113!";
  
  WiFi.begin(ssid,password);

  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // put your main code here, to run repeatedly:

}
