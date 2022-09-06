#include <LiquidCrystal.h>          // https://github.com/arduino-libraries/LiquidCrystal
#include <OneWire.h>                // https://www.pjrc.com/teensy/td_libs_OneWire.html
#include <DallasTemperature.h>      // https://www.milesburton.com/Dallas_Temperature_Control_Library
#include <Pushbutton.h>

#define DEFAULT_STATE_LOW 1
#define DEFAULT_STATE_HIGH 0

// pin numbers for the lcd
uint8_t lcd_rs = 8;
uint8_t lcd_enable = 9;
uint8_t lcd_d4 = 10;
uint8_t lcd_d5 = 11;
uint8_t lcd_d6 = 12;
uint8_t lcd_d7 = 13;

// data line for the temperature sensor
int temperature_pin = 7;

// push button pin
int pushbutton_pin = 2;

// whether temp should be displayed in C or F
char units = 'C';

//  temperature variable
float temp;

// instantiate LiquidCrystal object to control the lcd
LiquidCrystal lcd(lcd_rs, lcd_enable, lcd_d4, lcd_d5, lcd_d6, lcd_d7);

// instantiate OneWire object which will act as a data line
OneWire data_line(temperature_pin);

// instantiate a DallasTemperature object with the data line from above
DallasTemperature temp_sensor(&data_line);

// object for the push button
Pushbutton pushbutton(pushbutton_pin);

void setup() {
  attachInterrupt(digitalPinToInterrupt(pushbutton_pin), buttonPressInterrupt, RISING);
  attachInterrupt(digitalPinToInterrupt(pushbutton_pin), buttonReleaseInterrupt, FALLING);
  
  // configure the baud rate of the serial moniter (debugging)
  Serial.begin(9600);
  
  // set up the lcd interface, passing in the dimensions
  lcd.begin(16, 2);
  
  // set up the temperature sensor interface
  temp_sensor.begin();

}

void readTemp() {
  temp_sensor.requestTemperatures();
  temp = temp_sensor.getTempCByIndex(0);
  
  if (units == 'F') {
    temp = (temp * 1.8) + 32;
  }
}

void printTemp() {
  lcd.clear();
  String str = "Temp= " + String(temp) + " " + (char)223 + units;
  lcd.print(str);  
}

void loop() {
  readTemp();
  printTemp();
}

void buttonPressInterrupt() {
  Serial.println("push button pressed");
  lcd.display();
}

void buttonReleaseInterrupt() {
  Serial.println("push button released");
  lcd.noDisplay();  
}
