#include <LiquidCrystal.h>          // https://github.com/arduino-libraries/LiquidCrystal
#include <OneWire.h>                // https://www.pjrc.com/teensy/td_libs_OneWire.html
#include <DallasTemperature.h>      // https://www.milesburton.com/Dallas_Temperature_Control_Library
#include <Pushbutton.h>

// define the default states for the Pushbutton library
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

// push button interrupt pins
int pushbutton_pin2 = 2;
int pushbutton_pin3 = 3;

// determines whether the temperature should be displayed in degrees C or F
char units = 'F';

// holds the temperature value read in from the sensor
float temp;

// instantiate LiquidCrystal object to control the lcd
LiquidCrystal lcd(lcd_rs, lcd_enable, lcd_d4, lcd_d5, lcd_d6, lcd_d7);

// instantiate OneWire object which will act as a data line for the temperature sensor
OneWire data_line(temperature_pin);

// instantiate a DallasTemperature object with the OneWire from above
DallasTemperature temp_sensor(&data_line);

// two Pushbutton objects (one for each interrupt pin)
Pushbutton pushbutton2(pushbutton_pin2);    // rising edge
Pushbutton pushbutton3(pushbutton_pin3);    // falling edge

void setup() {
  // initialize the interrupts for the pushbutton
  attachInterrupt(digitalPinToInterrupt(pushbutton_pin2), buttonPressInterrupt, RISING);
  attachInterrupt(digitalPinToInterrupt(pushbutton_pin3), buttonReleaseInterrupt, FALLING);
  
  // configure the baud rate of the serial moniter (debugging)
  Serial.begin(9600);
  
  // set up the lcd interface, passing in the dimensions
  lcd.begin(16, 2);

  // the lcd shouldn't display anything from the start
  lcd.noDisplay();
  
  // set up the temperature sensor interface
  temp_sensor.begin();
}

void readTemp() {
  // get the temperature from the sensor
  temp_sensor.requestTemperatures();
  temp = temp_sensor.getTempCByIndex(0);

  // convert to degrees F, if needed
  if (units == 'F') {
    temp = (temp * 1.8) + 32;
  }
  
}

void printTemp() {
  // clear any previous writing on the lcd
  lcd.clear();

  // otherwise, if the temperature read is less than -120, notify that the sensor is unplugged
  if (temp < -120) {
    lcd.print("ERROR: unplugged");  
    lcd.setCursor(0,1);
    lcd.print("sensor");  
  }

  // otherwise, there was a valid temperature read, so display the temperature
  else {
    String str = "Temp= " + String(temp) + " " + (char)223 + units;
    lcd.print(str);  
  }
}

void loop() {
  // read the temperature
  readTemp();  

  // print the appropriate message
  printTemp();

  delay(1000);
}

void buttonPressInterrupt() {
  lcd.display();  
}

void buttonReleaseInterrupt() {
  lcd.noDisplay();  
}
